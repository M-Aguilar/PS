
const flags = document.getElementsByClassName('flag');
const d = document.createElement('div');
d.setAttribute('class','my-2 d-block start');
let inp = document.createElement('input');
inp.setAttribute('id', 'flag-search')
inp.setAttribute('class','blank p-1')
inp.setAttribute('placeholder', 'Flag Search')
inp.style = "border-radius: 15px;" 
inp.oninput = function() {findFlag()}
d.appendChild(inp)
let row = document.getElementById('gps-row')
row.parentNode.insertBefore(d,row);

const elem = document.getElementById('main-view');

document.onkeydown = function(e) {
	if (e.code.toLowerCase() === 'keyf') {
		openFullscreen()
	}
}

function findFlag(e) {
	let val = inp.value;
	for (let a=0; a < flags.length; a++) {
		if (flags[a].id.toLowerCase().includes(val.toLowerCase()) || val==='') {
			flags[a].hidden = false;
		} else {
			flags[a].hidden = true;
		}
	}
}

function cloneNodes(nodes) {
	new_list = {}
	for (let n = 0; n < nodes.length; n++) {
		let t = nodes[n].cloneNode(true)
		new_list[t.id] = t.childNodes[1].innerHTML
	}
	return new_list
}

document.addEventListener("fullscreenchange", 
	function(){if(!document.fullscreenElement) {
		canvas.full.onclick = function() {openFullscreen()}
		canvas.full.setAttribute('class','bi-arrows-fullscreen')};})

/* View in fullscreen */
function openFullscreen() {
	canvas.full.onclick = function() {closeFullscreen()}
	canvas.full.setAttribute('class','bi-fullscreen-exit')
	if (elem.requestFullscreen) {
	  elem.requestFullscreen();
	} else if (elem.webkitRequestFullscreen) { /* Safari */
	  elem.webkitRequestFullscreen();
	} else if (elem.msRequestFullscreen) { /* IE11 */
	  elem.msRequestFullscreen();
	}
  }
  
  /* Close fullscreen */
  function closeFullscreen() {
	canvas.full.onclick = function() {openFullscreen()}
	canvas.full.setAttribute('class','bi-arrows-fullscreen')
	if (document.exitFullscreen) {
	  document.exitFullscreen();
	} else if (document.webkitExitFullscreen) { /* Safari */
	  document.webkitExitFullscreen();
	} else if (document.msExitFullscreen) { /* IE11 */
	  document.msExitFullscreen();
	}
  }

function new_game(gps) {
	var flag_list = cloneNodes(flags)
	var docs = document.getElementsByClassName('start');
	for(var doc = docs.length-1; doc >= 0; doc--) {
		var e = docs[doc];
		e.parentNode.removeChild(e);
	}
	//var loc = window.location.pathname;
	//alert(pv);
	var c = canvas;
	c.start(gps, flag_list);
};

//Starts a game for new visitor
const canvas = {
	start : function (csv_input,flag_list) {
		this.flags = flag_list;
		this.ref = csv_input;
		this.correct = [];
		this.incorrect = [];
		this.m = document.getElementById('main-view');
		
		this.buttons = [];
		this.cur = [];

		//MANIPULATED ELEMENTS
		
		//CANVAS P
		this.a = document.createElement('div');
		//SCORE
		this.s = document.createElement('P');
		//PROMPT
		this.p = document.createElement('DIV');

		//Prompt center text
		this.pp = document.createElement('P');
		//BUTTONS
		this.n = document.createElement('DIV');

		//CANVAS
		this.c = document.createElement('DIV');

		this.setup();
		this.update();
	},

	//Creates all the elements necessary for the game
	setup : function() {
		//Create score nodes <p>Total: x out of t</p>
		let t = document.createElement('p');
		t.innerHTML = 'Total: '.concat(Object.keys(this.ref).length);
		
		//set canvas node id & attributes
		this.c.setAttribute('id','canvas');
		this.c.setAttribute('class','text-center');

		//Append canvas to game.html
		this.m.appendChild(this.c);

		//set choices node id & attributes
		this.n.setAttribute('id','choices');
		this.n.setAttribute('class','w-100 pb-0 mx-auto row justify-content-around');

		//create fullscreen button
		let full = document.createElement('i')
		full.setAttribute('class', 'bi-arrows-fullscreen')
		full.setAttribute('id', 'full')
		//append canvas to game.html
		this.m.appendChild(this.n);

		//set prompt node id & attributes
		this.p.setAttribute('id', 'prompt');
		this.p.setAttribute('class', 'jumbotron c-1 d-flex justify-content-between');

		//Create node that contains game elements (flags)
		this.a.setAttribute('id', 'a');

		//Creates 4 option buttons
		for(let i = 0; i < 4; i++) {
			var button = document.createElement('BUTTON');
			button.setAttribute('class','btn btn-1 my-2 col-auto');
			this.n.appendChild(button);
			this.buttons.push(button);
		}
		//Insert prompt before canvas
		this.m.insertBefore(this.p, this.c);

		//append center text to prompt
		this.p.appendChild(this.pp);
		//append score to prompt
		this.p.appendChild(this.s);
		//append time to prompt
		this.p.appendChild(t);
		this.p.appendChild(full)
		//append main game element to canvas
		this.c.appendChild(this.a);
		this.full = document.getElementById('full');
		openFullscreen()
	},

	//updates the choices
	choices : function () {
		const cs = 4;
		let a = [];
		var i;
		var temp = Object.keys(this.ref);
		var index = Math.floor(Math.random() * 4);
		for(var i = 0; i < cs; i++) {
			if (i == index) {
				a.push(this.cur);
				this.buttons[i].innerHTML = this.cur;
			} else {
			//IM RIGHT HERE
				var acceptable = true;
				while (acceptable) {
					var wrong = temp[Math.floor(Math.random() * temp.length)];
					if (!a.includes(wrong) && wrong != this.cur) {
						acceptable = false;
						a.push(wrong);
						this.buttons[i].innerHTML = wrong;
					}
				}
			}
			this.buttons[i].setAttribute('onclick','canvas.submit('.concat(i,')'));
			//document.getElementById('choices').appendChild(b);
		}
		this.ch = a;
	},

	submit : function (answer) {
		var user_answer = this.ch[answer];
		this.toggle_buttons(this.ch.indexOf(this.cur));
		if (this.cur == user_answer) {
			this.pp.innerHTML = "CORRECT!!";
			this.correct.push(this.cur);
		} else {
			this.pp.innerHTML = "WRONG! The correct answer was ".concat(this.cur);
			this.incorrect.push(this.cur);
		}
		setTimeout(function() {canvas.toggle_buttons(-1);canvas.update();}, 2000);
	},

	toggle_buttons : function (answer) {
		var i;
		for(i = 0; i < this.buttons.length; i++) {
			if (this.buttons[i].getAttribute('class').search('disabled') > -1) {
				this.buttons[i].setAttribute("class", "btn btn-1 my-2");
				this.buttons[i].setAttribute('onclick','canvas.submit('.concat(i,')'));
				this.buttons[i].removeAttribute('selected')
			} else {
				if (answer == i) {
					this.buttons[i].setAttribute("class", this.buttons[i].getAttribute('class').concat(" text-light bg-success disabled"));
					this.buttons[i].setAttribute('onclick','');
				} else {
					this.buttons[i].setAttribute("class", this.buttons[i].getAttribute('class').concat(" text-light bg-danger disabled"));
					this.buttons[i].setAttribute('onclick','');
				}
			}
		}
	},

	//returns formated score
	score : function() {
		var score = ''.concat(this.correct.length,' out of ',''.concat(this.incorrect.length));
		return score;
	},

	//Returns a new question country and makes sure its not in the answered pile
	next_question : function() {
		//This may be an area for study as some appraches may reduce cpu cycles not that theyr're expensive
		var acceptable = false;
		var temp = Object.keys(this.ref);
		while (!acceptable) {
			var num = Math.floor(Math.random() * temp.length);
			var r = temp[num];
			if (!this.correct.includes(r) && !this.incorrect.includes(r)) {
				acceptable = true;
				this.cur = r;
				//return r;
			}
		}
	},

	//updates the question
	update : function () {
		if ((this.correct.length + this.incorrect.length) == Object.keys(this.ref).length) {
			this.endgame();
		} else {
			this.next_question();
			this.s.innerHTML = this.score();
			this.pp.innerHTML = "What does this flag represent?";
			this.choices();
			this.a.innerHTML = this.flags[this.cur]
		}
	},

	endgame :function () {
		stop=true;
		this.s.innerHTML = this.score();
		this.pp.innerHTML = "Congratulations on completing the quiz!"
		this.a.style = "font-size:15vw;";
		this.a.innerHTML = (((this.correct.length/(this.correct.length+this.incorrect.length))*100).toString() + "% ").concat("Your score is ", this.score(), "!");
		for (let i = 0; i < this.buttons.length; i++) {
			this.buttons[i].setAttribute('class', 'd-none');
		}
	},
};