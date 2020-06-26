function new_game(gps) {
	var docs = document.getElementsByClassName('start');
	for(var doc = docs.length-1; doc >= 0; doc--) {
		var e = docs[doc];
		e.parentNode.removeChild(e);
	}
	//var loc = window.location.pathname;
	//alert(pv);
	var c = canvas;
	c.start(gps);
};
//Starts a game for new visitor

var canvas = {
	start : function (csv_input) {
		this.ref = csv_input;
		this.correct = [];
		this.incorrect = [];
		this.c = document.getElementById('main-view');
		
		this.buttons = [];
		this.cur = [];

		//MANIPULATED ELEMENTS
		
		//CANVAS P
		this.a = document.createElement('P');
		//SCORE
		this.s = document.createElement('P');
		//PROMPT
		this.p = document.createElement('DIV');

		this.pp = document.createElement('P');
		//BUTTONS
		this.n = document.createElement('DIV');

		//CANVAS
		this.c = document.createElement('DIV');

		this.setup();
		this.update();
	},

	setup : function() {
		this.c.setAttribute('id','canvas');
		this.c.setAttribute('class','w-100 text-center');
		document.getElementById('main-view').appendChild(this.c);
		this.n.setAttribute('id','choices');
		this.n.setAttribute('class','d-block pb-5 w-100 d-md-flex justify-content-md-between');
		document.getElementById('main-view').appendChild(this.n);
		this.p.setAttribute('id', 'prompt');
		this.p.setAttribute('class', 'jumbotron theme py-2');
		this.s.setAttribute('class', 'float-right');
		this.a.setAttribute('id', 'a');
		this.a.setAttribute('style', 'font-family: Segoe UI Emoji');
		var i;
		for(i = 0; i < 4; i++) {
			var button = document.createElement('BUTTON');
			button.setAttribute('class','btn btn-theme my-2');
			this.n.appendChild(button);
			this.buttons.push(button);
		}
		this.c.appendChild(this.p);
		this.p.appendChild(this.pp);
		this.p.appendChild(this.s);
		this.c.appendChild(this.a);
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
		var i;
		var user_answer = this.ch[answer];
		this.toggle_buttons(this.ch.indexOf(this.cur));
		if (this.cur == user_answer) {
			this.pp.innerHTML = "CORRECT!!";
			this.correct.push(user_answer);
		} else {
			this.pp.innerHTML = "WRONG! The correct answer was ".concat(this.cur);
			this.incorrect.push(answer);
		}
		setTimeout(function() {canvas.toggle_buttons(-1);canvas.update();}, 2000);
	},

	toggle_buttons : function (answer) {
		var i;
		for(i = 0; i < this.buttons.length; i++) {
			if (this.buttons[i].getAttribute('class').search('disabled') > -1) {
				this.buttons[i].setAttribute("class", "btn btn-theme my-2");
				this.buttons[i].setAttribute('onclick','canvas.submit('.concat(i,')'));
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
		var score = ''.concat(this.correct.length, ' out of ' ,''.concat((this.correct.length + this.incorrect.length)));
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
			this.pp.innerHTML = "Which country does this correspond to?";
			this.choices();
			this.a.innerHTML = this.ref[this.cur][0];
			this.a.setAttribute('alt',this.ref[this.cur][1]);
		}
	},

	endgame :function () {
		this.p.innerHTML = "Congratulations on completing the quiz!"
		this.a.style = "font-size:15vw;";
		this.a.innerHTML = (((this.correct.length/(this.correct.length+this.incorrect.length))*100).toString() + "% ").concat("Your score is ", this.score(), "!");
		var i;
		for (i = 0; i < this.buttons.length; i++) {
			this.buttons[i].setAttribute('class', 'd-none');
		}
	},
};