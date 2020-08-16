var api_url = "http://127.0.0.1:8000/city_app/";

var app = new Vue({
    el: '#app',
    data: {
        cities: [],
        status: "retrieving",
        search: "",
        selected_city: null
    },
    created: function(){
        this.update_cities();
    },
    watch:{
        search: function (new_value, old_value){
            this.update_cities()
        }
    },
    methods:{
        update_cities: function(){
            
            var app = this;
            app.status = "retrieving";
            
            // Bof, trop de requetes lancées
            url = api_url + "city/";
            if(app.search !== ""){
                url = url + "?search=" + app.search;
            }
            axios.get(url)
            .then((response) => {
                app.status = "retrieved";
                app.cities = response.data.results;
            }, (error) => {
                console.log(error);
            });
        },
        select_city: function(city){
            console.log(city);
            this.selected_city = city;
        },
        send_new_info: function(){
            var app = this;            
            // Bof, trop de requetes lancées
            url = api_url + "city/" + app.selected_city.id + "/";
            params = {
                "population": app.selected_city.population,
                "name": app.selected_city.name,
                "department": app.selected_city.department,
                "zip_codes": app.selected_city.zip_codes,
            }
            axios.put(url, params)
            .then((response) => {
                console.log(response);
            }, (error) => {
                console.log(error);
            });
        }

    }
});