var GameBoard = {
	start : function() {
	},
};

function start_game() {
	var game = GameBoard();
};

function new_game(){
	var docs = document.getElementsByClassName('start');
	for(var doc = docs.length-1; doc >= 0; doc--) {
		var e = docs[doc];
		e.parentNode.removeChild(e);
	}

	var loc = window.location.pathname;
	alert(loc);
	startgame();
};