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
		this.update(this.next_question());
	},

	setup : function() {
		this.c.setAttribute('id','canvas');
		this.c.setAttribute('class','w-100 text-center');
		document.getElementById('main-view').appendChild(this.c);
		this.n.setAttribute('id','choices');
		this.n.setAttribute('class','d-block pb-5 w-100 d-md-flex justify-content-md-between');
		document.getElementById('main-view').appendChild(this.n);
		this.p.setAttribute('id', 'prompt');
		this.p.setAttribute('class', 'jumbotron py-2');
		this.s.setAttribute('class', 'float-right');
		this.a.setAttribute('id', 'a');
		var i;
		for(i = 0; i < 4; i++) {
			var button = document.createElement('BUTTON');
			button.setAttribute('class','btn btn-dark my-2');
			this.n.appendChild(button);
			this.buttons.push(button);
		}
		this.c.appendChild(this.p);
		this.p.appendChild(this.pp);
		this.p.appendChild(this.s);
		this.c.appendChild(this.a);
	},

	//updates the choices
	choices : function (answer) {
		const cs = 4;
		let a = [];
		var i;
		let index = Math.floor(Math.random() * 4);
		for(var i = 0; i < cs; i++) {
			if (i == index) {
				a.push(answer);
				this.buttons[i].innerHTML = answer;
			} else {
				var temp = Object.keys(this.ref);
				var wrong = temp[Math.floor(Math.random() * temp.length)];
				a.push(wrong);
				this.buttons[i].innerHTML = wrong;
			}
			this.buttons[i].setAttribute('onclick','canvas.submit('.concat(i,')'));
			//document.getElementById('choices').appendChild(b);
		}
		this.choices = a;
	},

	submit : function (answer) {
		var user_answer = this.buttons[answer];
		if (this.ref[this.cur] == user_answer) {
			this.pp.innerHTML = "CONGRATS!";
			this.correct.push(this.pool.splice(this.cur,1));
		} else {
			this.pp.innerHTML = "WRONG!!";
			this.incorrect.push(this.pool.splice(this.cur,1));
		}
		this.update(this.next_question);
	},
	//returns formated score
	score : function() {
		var score = ''.concat((this.correct.length + this.incorrect.length).toString(), ' out of ' ,''.concat((this.correct.length)));
		return score;
	},

	//Returns a new question country and makes sure its not in the answered pile
	next_question : function() {
		//This may be an area for study as some appraches may reduce cpu cycles not that theyr're expensive
		var acceptable = false;
		var temp = Object.keys(this.ref); 
		while (!acceptable) {
			var num = Math.floor(Math.random * this.ref.length);
			var r = temp[num];
			if (!(r in this.correct) && !(r in this.incorrect)) {
				acceptable = true;
				this.cur = this.ref[r];
				return temp[num];
			}
		}
	},

	//updates the question
	update : function (new_name) {
		this.s.innerHTML = this.score();
		this.pp.innerHTML = "Which country does this correspond to?";
		this.a.innerHTML = this.cur;
		this.choices(new_name);
	},
};