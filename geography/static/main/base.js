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
	var text = document.getElementById("id_text").form.text.value;
	if (text == '' || text == ' ') {
		document.getElementById('wc').innerHTML = "Word Count: " + "0".toString();
	} else {
		document.getElementById('wc').innerHTML = "Word Count: " + text.split(/\r\n|\r|\n/).length;
	}
	document.getElementById('cc').innerHTML = "Char Count: " + true_text_length(text.trim()) + limit;
}

function true_text_length(t) {
	var te = t.search(/\r\n|\r|\n/);
	var num = t.split('').length;
	//num += t;
	return num.toString();
}

$(document).ready(function(){
	$("#id_banner_path").on({
		change: function() {
			$('#preview').attr('src',$("#id_banner_path").val().substring(13));
		}
	});
	$("#id_image_path").on({
		change: function() {
			console.log($("#id_image_path").val().substring(13));
			$('#preview').attr('src',$("#id_image_path").val().substring(13));
		}
	});
});
	
		//$.ajax({url: $("#id_banner_path option [selected='']").value, success: function(result) {
			//console.log("does this work");
			//console.log($("#id_banner_path"));
			//$('#preview').html(result);

/*document.getElementById("id_banner_path").onclick = image_update();

function image_update() {
	var banner = ''
	try {
		var banner = document.getElementById("id_banner_path").value.slice(13);
		document.getElementById("preview").src = banner;
		console.log(banner);
	}
	catch(err) {
		console.log('There was an Error');
	}
}*/