var start_time,
	prompt,
	stop=false,
	timer;

function timer() {
	timer = document.createElement('p');
	start_time = new Date();
	prompt = document.getElementById('prompt');
	timer.innerHTML = start_time.getTime();
	prompt.insertBefore(timer, prompt.firstChild);
	updateTimer();
}

function updateTimer() {
	var cur_time = new Date();
	cur_time = minutes(((cur_time - start_time)/1000).toFixed(0));
	timer.innerHTML = cur_time;
	if (!stop){
		setTimeout(updateTimer, 500);
	}
}

function minutes(time) {
	if (time < 10) {
		return "0:0"+time;
	} else if (time < 60) {
		return "0:" + time;
	} else {
		if ((time % 60) < 10) {
			return (time/60).toFixed(0).toString() + ':0' + (time%60).toString();			
		} else {
			return (time/60).toFixed(0).toString() + ':' + (time%60).toString();
		}
	}
}