//country_list keeps track of layers
var country_list,
	//name of all countries
	names = [],
	//map object
	mymap,
	//number of multiple choice.
	option_num = 4,
	//tracker for submitted answer
	submitted,
	//used for tracking selected country layer in pregame map
	cur;

function print(message) {
	format = ''
	for (var i = 0; i < message.length; i++) {
		format = format .concat(message[i],': [',i.toString(),']\n');
	}
	return format
}

function new_game(gps) {
	//REMOVE START COMPONENTS
	var docs = document.getElementsByClassName('start');
	for(var doc = docs.length-1; doc >= 0; doc--) {
		var e = docs[doc];
		e.parentNode.removeChild(e);
	}

	for (var i = 0; i < country_list.getLayers().length; i++) {
		mymap.removeLayer(country_list.getLayers()[i]);
	}
	mymap.off('click', latlng_marker);

	GameManager.start();
}

var GameManager = {
	init: function() {
		this.name_pool;
		this.correct;
		this.cur_layer;
		this.incorrect;
		this.current;
		this.buttons;
		this.toggle;
	},

	start: function(self) {
		this.toggle=null;
		this.correct= [];
		this.incorrect = [];
		this.name_pool = names.slice();
		this.current;
		this.prompt();
		this.select();
	},

	//
	select: function(self) {
		this.q.innerHTML = "Which country is this?";
		this.current = this.name_pool[Math.floor(Math.random() * this.name_pool.length)];
		this.cur_layer = country_list.getLayers()[names.indexOf(this.current)].setStyle({color:'#000000'}).addTo(mymap);
		this.cur_layer.off('click', popu);
		this.cur_layer.unbindPopup();
		mymap.flyToBounds(this.cur_layer.getBounds(), {padding:[10,10]});
		this.button_populate();
		if (this.toggle==null) {
			this.toggle = true;
		} else {
			this.toggle_buttons();
		}
		//DEBUG <P> TAG
		//console.log("Country selected: " + this.current);
		//p.innerHTML = "countries_quiz.js line 46 current: ".concat(this.current);
	},

	toggle_buttons: function() {
		for (var i = 0; i < this.buttons.length;i++) {
			if (this.toggle) {
				this.buttons[i].disabled = true;
			} else{
				this.buttons[i].disabled = false;
			}
		}
		this.toggle = !this.toggle;
	},

	submit: function(self) {
		this.toggle_buttons();
		var s = this.name_pool.splice(this.name_pool.indexOf(this.current),1);
		if (submitted == this.current) {
			this.correct.push(s);
			this.q.innerHTML = 'CORRECT! The answer is '.concat(this.current);
			this.cur_layer.setStyle({color:'green'});
		} else {
			this.incorrect.push(s);
			this.q.innerHTML = "INCORRECT! The correct answer is ".concat(this.current);
			this.cur_layer.setStyle({color:'red'});
		}
		if (this.name_pool.length > 1) {
			var timer = setTimeout(() => {
				GameManager.select();
			},3000);
		} else {
			this.endgame();
		}
	},

	button_populate: function(self) {
		var mix = Math.floor(Math.random() * (option_num-1));
		var acceptable;
		var r;
		var temp;
		var index = 0;
		for (var i = 0; i < option_num; i++) {
			acceptable = false;
			if (i == mix) {
				this.buttons[i].innerHTML = this.current;
			} else {
				while(!acceptable) {
					index += 1;
					console.log('Attempt # ' + index.toString());
					r = Math.floor(Math.random() * names.length);	
					temp = names[r];
					if (!this.buttons.slice(0,i+1).includes(temp) && (this.current != temp)) {
						this.buttons[i].innerHTML = temp;
						acceptable = true;
					}
				}
			}
			this.buttons[i].setAttribute('onclick', "submitted='"+ this.buttons[i].innerHTML + "';GameManager.submit();");
		}
	},

	prompt: function(self) {
		//CREATE TOP PROMPT
		var prompt = document.createElement('div');
		prompt.setAttribute('class', 'blank text-color jumbotron p-1 m-auto text-center');
		prompt.setAttribute('id','prompt')
		this.q = document.createElement('p');
		this.q.innerHTML = "Which country is this?";
		prompt.appendChild(this.q);
		document.getElementById('main-view').insertBefore(prompt, document.getElementById('game'));
		this.buttons = [];
		var buttons = document.createElement('DIV');
		buttons.setAttribute('class','mx-auto d-md-flex justify-content-md-between');
		buttons.setAttribute('id','choices');
		for (var i = 0; i < option_num; i++) {
			var q = document.createElement('button');
			q.setAttribute('class', 'btn btn-theme my-1');
			this.buttons[i]=q;
			buttons.appendChild(q);
		}
		document.getElementById('game').appendChild(buttons);
	},

	score: function(self) {
		var score = ((this.correct.length/(this.correct.length+this.incorrect.length)) * 100).toFixed(1).toString() + '%';
		score = score.concat('\n', this.correct.length.toString(), ' out of ', (this.correct.length+this.incorrect.length).toString());
		return score;
	},

	endgame: function(self) {
		message = 'Congratulations on completing the country map quiz.\nYour score is ';
		this.q.innerHTML = message+this.score();
	}
}

	//RETURN WINDOW TO TOP.
	//window.scrollTo(0,0)
function setup() { 	//ADD MAP
	//ADD CLEAN GAME SLATE
	var g = document.createElement('div');
	g.setAttribute('id','mapid');
	//g.setAttribute('class','start');
	document.getElementById('game').appendChild(g);
	
	var southWest = L.latLng(-85.03, -180.45),
    northEast = L.latLng(84.55, 193.71),
    bounds = L.latLngBounds(southWest, northEast);

	//ADD BASE MAP
	mymap = L.map('mapid').setView([21, 0],2).setMaxBounds(bounds);
	L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}{r}.{ext}', {
		attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
		subdomains: 'abcd',
		ext: 'png',
		minZoom: 1
	}).addTo(mymap);
	pregame();
}

function pregame() {
	//LATLONG POPUP WHEN CLICKING ON MAP OUTSIDE OF COUNTRY BOUNDS
	//mymap.on('click',latlng_marker);
	const xhr = new XMLHttpRequest();
	xhr.open('GET', '/static/games/countries.geo.json');
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.responseType = 'json';
	xhr.onload = function() {
	    if (xhr.status !== 200) return
	   	country_list = new L.geoJSON(xhr.response,{
		style: function(feature) {
			return {color: '#F0F8FF'};
		},
		onEachFeature:onEachFeature
	}).addTo(mymap);
	};
	xhr.send();
	//COUNTRY NAME POPUP


	//BOTTOM P TAG DEBUG	
	p = document.createElement('p');
	p.setAttribute('class', 'text-theme pb-0');
	document.getElementById('main-view').appendChild(p);

}

function onEachFeature(feature, layer) {
	if (feature.properties && feature.properties.name) {
		layer.bindPopup(feature.properties.name);
		names.push(feature.properties.name);
	}
	layer.on('click', popu);
}

//LATLNG MARKER
function latlng_marker(e) {
	var popuploc = e.latlng;
	var mes = e.latlng.lat.toFixed(2).toString() + ', ' + e.latlng.lng.toFixed(2).toString();
	var popup = L.popup()
	.setLatLng(popuploc)
	.setContent(mes)
	.openOn(mymap);
}

function popu(e) {
	if (cur != null) {
		cur.setStyle({color: '#F0F8FF'});
	}
	this.setStyle({color:'#DC143C'});
	this.openPopup(e.latlng);
	cur = this;
}
