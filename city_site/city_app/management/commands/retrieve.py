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
        # requetes vers https://geo.api.gouv.fr/communes
        r = requests.get('https://geo.api.gouv.fr/communes')
        if r.status_code is not 200:
            raise SourceException("request failed %s" % r.reason)
        with transaction.atomic():
            for source_city in r.json():
                # source_city_codes = []
                try:
                    assert source_city.get('nom'), "missing key `nom`"
                    assert source_city.get('code'), "missing key `code`"
                    assert source_city.get('codeDepartement'), "missing key `codeDepartement`"
                    assert source_city.get('codeRegion'), "missing key `codeRegion`"
                except AssertionError as e:
                    self.stdout.write(self.style.WARNING('Ignored city %s because %s' % (source_city.get('nom', '<unnamed>'), e)))
                    continue

                # source_city_codes.append(source_city.get('code'))
                if source_city.get('codesPostaux'):
                    source_city_codes.extend(source_city.get('codesPostaux'))

                region, region_created = Region.objects.get_or_create(
                    code=source_city.get('codeRegion'),
                )
                if region_created:
                    self.stdout.write(self.style.SUCCESS("created region : " + region.code))
                    region.save()

                department, department_created = Department.objects.get_or_create(
                    code=source_city.get('codeDepartement'),
                    region_id=region.id
                )
                if department_created:
                    self.stdout.write(self.style.SUCCESS("created dpt : " + department.code))
                    department.save()

                city, city_created = City.objects.get_or_create(
                    name=source_city.get('nom'),
                    population=source_city.get('population', 0),
                    department_id=department.id,
                    zip_code=source_city.get('code')
                )
                if city_created:
                    self.stdout.write(self.style.SUCCESS("created city : " + city.name))
                    # TODO Bulk create
                    city.save()

                # for source_city_code in source_city_codes:
                #     city_code, city_code_created = ZipCode.objects.get_or_create(
                #         value=source_city_code
                #     )
                #     if city_code_created:
                #         city_code.save()
                #     city.zip_code.add(city_code)
        self.stdout.write(self.style.SUCCESS("Retrieve command ended without error"))

        