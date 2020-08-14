var app = new Vue({
    el: '#app',
    data: {
        cities: [],
        status: "retrieving",
        search: "",
        search_chrono: null
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
            app.status = "retrieved";
            var url = "http://127.0.0.1:8000/city_app/city/";
            // Bof, trop de requetes lancées
            
            if(app.search !== ""){
                url = url + "?search=" + app.search;
            }
            axios.get(url)
            .then((response) => {
                app.search_chrono = Date.now();
                app.status = "retrieved";
                app.cities = response.data.results;
            }, (error) => {
                console.log(error);
            });
        }
    }
});