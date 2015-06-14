$(document).ready(function(){

var map;
	function init(){
		// initiate leaflet map
		map = new L.Map('cartodb-map', { 
			center: [47.609907473000,-122.342577078000],
			zoom: 11
		})//end new L.Map

		var layerUrl = 'https://dvass1994.cartodb.com/api/v2_1/viz/a54110f8-12b7-11e5-aae5-0e0c41326911/viz.json';
		
		L.tileLayer('https://dnv9my2eseobd.cloudfront.net/v3/cartodb.map-4xtxp73f/{z}/{x}/{y}.png', {
			attribution: 'Mapbox <a href="http://mapbox.com/about/maps" target="_blank">Terms &amp; Feedback</a>'
		}).addTo(map);

		cartodb.createLayer(map, layerUrl)
			.addTo(map)
			.on('done', function(layer) {
	


			}).on('error', function() {
		  		//log the error



			});//end cartodb.createLayer

		cartodb.createSubLayer({

		})

		var url = 'http://documentation.cartodb.com/api/v2/viz/2b13c956-e7c1-11e2-806b-5404a6a683d5/viz.json';

		cartodb.createVis('map', url)
			.done(function(vis, layers) {
			});





	}// end function init

}//end dom ready