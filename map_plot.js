// var history_images_json_file = require('history_images.json')
// var history_images_json = JSON.parse(history_images_json_file)
// console.log("json", json)

function read(textFile){
    var xhr=new XMLHttpRequest;
    xhr.open('GET',textFile);
    xhr.onload=show;
    xhr.send()
}

function show(){
    var pre=document.createElement('pre');
    pre.textContent=this.response;
    document.body.appendChild(pre)
}

read('history_images.json');

var map;
function initMap() {
	let uluru = {lat: -25.363, lng: 131.044};
	let map = new google.maps.Map(document.getElementById('map'), {
		center: uluru,
		zoom: 7
	});
	let marker = new google.maps.Marker({
		position: uluru,
		map: map
	});
}