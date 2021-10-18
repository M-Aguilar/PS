
//country_list keeps track of layers
var country_list, 
	names = [], //name of all countries
	mymap, 	//map object
	option_num = 4, //number of multiple choice.
	m, //capital popup marker
	cur; //Current country 

//Place initial map
setup();

function new_game() {
	//REMOVE START COMPONENTS
	var docs = document.getElementsByClassName('start');
	for (let doc = docs.length-1; doc >= 0; doc--) {
		var e = docs[doc];
		e.parentNode.removeChild(e);
	}
	for (let i = 0; i < country_list.getLayers().length; i++) {
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

	//updates prompt and selects a new territory not yet decided
	select: function(self) {
		this.q.innerHTML = "Which country is this?";
		this.current = this.name_pool[Math.floor(Math.random() * this.name_pool.length)];
		this.cur_layer = country_list.getLayers()[names.indexOf(this.current)].setStyle({color:'#000000'}).addTo(mymap);
		this.cur_layer.off('click', popu);
		this.cur_layer.unbindPopup();
		this.reset();
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
		for (let i = 0; i < this.buttons.length;i++) {
			if (this.toggle) {
				if (this.buttons[i].innerHTML===this.current) {
					this.buttons[i].setAttribute('class', 'btn btn-1 my-1 bg-success')
				} else {
					this.buttons[i].setAttribute('class','btn btn-1 my-1 bg-danger')
				}
				this.buttons[i].disabled = true;
			} else{
				this.buttons[i].setAttribute('class', 'btn btn-1 my-1');
				this.buttons[i].disabled = false;
			}
		}
		this.toggle = !this.toggle;
	},

	submit: (country) => {
		GameManager.toggle_buttons();
		var s = GameManager.name_pool.splice(GameManager.name_pool.indexOf(GameManager.current),1);
		if (country == GameManager.current) {
			GameManager.correct.push(s);
			GameManager.q.innerHTML = 'CORRECT! The answer is '.concat(GameManager.current);
			GameManager.cur_layer.setStyle({color:'green'});
		} else {
			GameManager.incorrect.push(s);
			GameManager.q.innerHTML = "INCORRECT! The correct answer is ".concat(GameManager.current);
			GameManager.cur_layer.setStyle({color:'red'});
		}
		GameManager.sc.innerHTML = GameManager.score();
		if (GameManager.name_pool.length > 1) {
			var timer = setTimeout(() => {
				GameManager.select();
			},3000);
		} else {
			GameManager.endgame();
		}
	},

	//updates the buttons with the correct answer and 3 random territory names. Does not repeat answers.
	button_populate: function(self) {
		let mix = Math.floor(Math.random() * (option_num-1))
		for (let i = 0; i < option_num; i++) {
			let acceptable = false,
				index = 0;
			if (i == mix) {
				this.buttons[i].innerHTML = this.current;
			} else {
				while(!acceptable) {
					index += 1;
					let r = Math.floor(Math.random() * names.length);	
					let temp = names[r];
					if (!this.buttons.slice(0,i+1).includes(temp) && (this.current != temp) && !this.check_buttons(index).includes(this.current)) {
						this.buttons[i].innerHTML = temp;
						acceptable = true;
					}
				}
			}
			this.buttons[i].setAttribute('onclick', `GameManager.submit('${this.buttons[i].innerHTML}')`);
		}
	},
	
	//Checks to see if the provided potential button name is not present in the current pool of buttons up to the current index being added
	check_buttons: (index) => {
		btns = []
		for (let i = 0; i < index; i++) {
			btns.push(GameManager.buttons[i])
		}
		return btns
	},

	//Create the prompt element at the top of the map. Includes score, time, text and reset button
	prompt: function(self) {
		//CREATE TOP PROMPT
		var prompt = document.createElement('div');
		prompt.setAttribute('class', 'c-1 text-color jumbotron p-1 m-auto text-center d-flex justify-content-between');
		prompt.setAttribute('id','prompt')

		//Center text Element		
		this.q = document.createElement('p');
		this.q.innerHTML = "Which country is this?";
		prompt.appendChild(this.q);

		//Score Element
		this.sc = document.createElement('p');
		this.sc.innerHTML = this.score();
		prompt.appendChild(this.sc);

		//Reset button. Reset view to current area of interest
		var reset = document.createElement('button');
		reset.setAttribute('class', 'btn alt-btn');
		reset.innerHTML = 'Reset';
		reset.setAttribute('onclick', 'GameManager.reset()');
		prompt.appendChild(reset);

		//Append prompt to game element
		document.getElementById('main-view').insertBefore(prompt, document.getElementById('game'));
		
		//Create option buttons
		this.buttons = [];
		var buttons = document.createElement('DIV');
		buttons.setAttribute('class','mx-auto d-md-flex justify-content-md-between');
		buttons.setAttribute('id','choices');
		for (let i = 0; i < option_num; i++) {
			var q = document.createElement('button');
			q.setAttribute('class', 'btn btn-1 my-1');
			this.buttons[i]=q;
			buttons.appendChild(q);
		}
		document.getElementById('game').appendChild(buttons);
	},

	//Returns current score
	score: function(self) {
		var score = "";
		if (this.correct.length > 0 || this.incorrect.length > 0){
			score = ((this.correct.length/(this.correct.length+this.incorrect.length)) * 100).toFixed(1).toString() + '%';
		}
		score = score.concat('\n', this.correct.length.toString(), ' out of ', (this.correct.length+this.incorrect.length).toString());
		return score;
	},

	//stops time and provides score
	endgame: function(self) {
		stop_timer=true
		message = 'Congratulations on completing the country map quiz.\nYour score is ';
		this.q.innerHTML = message+this.score();
	},
	
	reset: function(self) {
		mymap.flyToBounds(this.cur_layer.getBounds(), {maxZoom:5,padding:[10,10]});
	}
}

	//RETURN WINDOW TO TOP.
	//window.scrollTo(0,0)

//Populates game.html with map.
function setup() {
	var g = document.createElement('div');
	g.setAttribute('id','mapid');
	document.getElementById('game').appendChild(g);
	
	//Set bounds
	const southWest = L.latLng(-85.03, -180.45),
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

//Initial function that grabs json and populates the map with elements
function pregame() {
	//LATLONG POPUP WHEN CLICKING ON MAP OUTSIDE OF COUNTRY BOUNDS
	//mymap.on('click',latlng_marker);

	//Pulls the geo.json file containing countries
	const xhr = new XMLHttpRequest();
	xhr.open('GET', '/static/games/countries2.geo.json');
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.responseType = 'json';
	xhr.onload = function() {
	    if (xhr.status !== 200) return
	   	country_list = new L.geoJSON(xhr.response,{
		style: function() {
			return {color: '#f0f8ff'};
		},
		onEachFeature:onEachFeature,
	}).addTo(mymap);
	};
	xhr.send();
	/*BOTTOM P TAG DEBUG	
	let p = document.createElement('p');
	p.setAttribute('class', 'text-theme pb-0');
	p.innerHTML = "where am i?"
	document.getElementById('main-view').appendChild(p);
	*/
}

//Applies popups to each feature and adds country names to name list
function onEachFeature(feature, layer) {
	if (feature.properties && feature.properties.name) {
		country_label = `<b><a href="https://en.wikipedia.org/wiki/${feature.properties.name}">${feature.properties.name}</a>`;
		if (feature.properties.capital != "N/A") {
			country_label = country_label + `</b><br>Capital: <a href="https://en.wikipedia.org/wiki/${feature.properties.capital}">${feature.properties.capital}</a>`
		}
		layer.bindPopup(country_label);
		names.push(feature.properties.name);
	}
	layer.on('click', popu);
}

//LATLNG MARKER Not implemented by default. see line #229
function latlng_marker(e) {
	L.popup()
	.setLatLng(e.latlng)
	.setContent(e.latlng.lat.toFixed(2).toString() + ', ' + e.latlng.lng.toFixed(2).toString())
	.openOn(mymap);
}

//Capitals icon
var myIcon = L.icon({
    iconUrl: '/static/games/star.png',
    iconSize: [20, 20],
});

//Popup function. Resets other popups and capital markers when a different area is selected
function popu(e) {
	if (m) {
		m.removeFrom(mymap);
	}
	if (cur != null) {
		reset()
	}
	cur = this;
	this.setStyle({color:'#DC143C'});
	this.openPopup(e.latlng);
	if (cur.feature.properties.capital != "N/A") {
		m = L.marker(cur.feature.properties.capital_coordinate, {icon: myIcon}).addTo(mymap);
	}
}

//Reset color of selected area
function reset() {
	cur.setStyle({color: '#F0F8FF'});
}

console.log(names)