function curTime() {
	var today = new Date();
	var h = today.getHours();
	var m = today.getMinutes();
	var s = today.getSeconds();
	m = checkTime(m);
	s = checkTime(s);
	document.getElementById('time').innerHTML = h + ':' + m + ':' + s + ' ' + today.toString().substring(today.toString().indexOf('('));
	//today.toUTCString().substring(today.toUTCString().length-3)
	var t = setTimeout(curTime, 500);
}

function checkTime(i) {
	if (i < 10) {i = "0" + i};
	return i;
}
