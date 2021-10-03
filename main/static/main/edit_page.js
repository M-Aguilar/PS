var frnt_brak = 'BracketLeft',
bck_brak = 'BracketRight',
ctrl_down = false,
cmd_left = 'OSLeft',
cmd_right = 'OSRight',
ctrl_right = 'ControlRight',
ctrl_left = 'ControlLeft',
os = navigator.platform;

document.getElementById("id_html").addEventListener('keydown', function(e) {
    if (e.key == 'Tab') {
        e.preventDefault();
        var start = this.selectionStart;
        var end = this.selectionEnd;
        this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 1;
    }

    if (os == 'MacIntel') {
        if (e.code == cmd_left || e.code == cmd_right) {
            ctrl_down = true;
        }
    } else {
        if (e.code == ctrl_left || e.code == ctrl_right) {
            ctrl_down = true;
        }
    }

    if (ctrl_down && (e.code == frnt_brak)) {
        e.preventDefault();
        start = this.selectionStart;
        end = this.selectionEnd;
        val = this.value.substring(start, end).split('\n');
        for (var i = 0; i < val.length; i++) {
            if (val[i].startsWith("\t")) {
                val[i] = val[i].substring(1);
            }
        }
        new_val = val.join('\n');
        this.value = this.value.substring(0, start) + new_val;
        this.setSelectionRange(start, start + new_val.length);
    }

    if (ctrl_down && (e.code == bck_brak)) {
        e.preventDefault();
        start = this.selectionStart;
        end = this.selectionEnd;
        val = this.value.substring(start, end).split('\n');
        for (var i = 0; i < val.length; i++) {
            val[i] = '\t' + val[i];
        }
        new_val = val.join('\n');
        this.value = this.value.substring(0, start) + new_val;
        this.setSelectionRange(start, start + new_val.length);
    }
  });

  document.getElementById("id_html").addEventListener('keyup', function(e) {
    if (os == 'MacIntel') {
        if (e.code == cmd_left || e.code == cmd_right) {
            ctrl_down = false;
        }
    } else {
        if (e.code == ctrl_left || e.code == ctrl_right) {
            ctrl_down = false;
        }
    }
  });