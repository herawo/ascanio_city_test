from django.core.management.base import BaseCommand, CommandError
import requests
from city_app.models import Region
from city_app.models import Department
from city_app.models import City
from city_app.models import ZipCode
from city_app.exceptions import SourceException
from django.db import transaction


class Command(BaseCommand):
    help = 'Get the cities from trusted source'

    def handle(self, *args, **options):

        def request_endpoint(url, arg_dict=None):
            full_url = url
            if arg_dict:
                full_url = url.format(**arg_dict)
            source_request = requests.get(full_url)
            if source_request.status_code is not 200:
                raise SourceException("request failed %s" % source_request.reason)
            return source_request.json()
        
        with transaction.atomic():
            data = request_endpoint('https://geo.api.gouv.fr/communes')
            for source_city in data:
                try:
                    assert source_city.get('nom'), "missing key `nom`"
                    assert source_city.get('code'), "missing key `code`"
                    assert source_city.get('codeDepartement'), "missing key `codeDepartement`"
                    assert source_city.get('codeRegion'), "missing key `codeRegion`"
                except AssertionError as e:
                    self.stdout.write(self.style.WARNING('Ignored city %s because %s' % (source_city.get('nom', '<unnamed>'), e)))
                    continue

                region, region_created = Region.objects.get_or_create(
                    code=source_city.get('codeRegion'),
                )
                if region_created:
                    reg_data = request_endpoint(
                        'https://geo.api.gouv.fr/regions/{code}',
                        {'code': region.code}
                    )
                    region.name = reg_data.get('nom')
                    region.save()
                    self.stdout.write(self.style.SUCCESS("created region : " + region.code))

                department, department_created = Department.objects.get_or_create(
                    code=source_city.get('codeDepartement'),
                    region_id=region.id
                )
                if department_created:
                    dpt_data = request_endpoint(
                        'https://geo.api.gouv.fr/departements/{code}',
                        {'code': department.code}
                    )
                    department.name = dpt_data.get('nom')
                    department.save()
                    self.stdout.write(self.style.SUCCESS("created dpt : " + department.code))

                city, city_created = City.objects.get_or_create(
                    name=source_city.get('nom'),
                    population=source_city.get('population', 0),
                    department_id=department.id,
                )
                if city_created:
                    self.stdout.write(self.style.SUCCESS("created city : " + city.name))
                    # TODO Bulk create
                    city.save()

                for source_city_code in source_city.get('codesPostaux', []):
                    city_code, city_code_created = ZipCode.objects.get_or_create(
                        value=source_city_code
                    )
                    if city_code_created:
                        city_code.save()
                    city.zip_codes.add(city_code)
        self.stdout.write(self.style.SUCCESS("Retrieve command ended without major error"))

        