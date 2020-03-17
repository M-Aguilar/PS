var limit = " / " + document.getElementById("id_text").form.text.maxLength.toString();
wc = document.createElement("P");
wc.setAttribute('id','wc');
cc = document.createElement("P");
cc.setAttribute('id','cc');
wc.classList.add("text-right");
cc.classList.add("text-right");
document.getElementById('counter').appendChild(wc);
document.getElementById('counter').appendChild(cc);

char_count();

function char_count() {
	var text = document.getElementById("id_text").form.text.value.trim();
	if (text == '' || text == ' ') {
		document.getElementById('wc').innerHTML = "Word Count: " + "0".toString();
	} else {
		document.getElementById('wc').innerHTML = "Word Count: " + text.split(' ').length;
	}
	document.getElementById('cc').innerHTML = "Char Count: " + text.length.toString() + limit;
};