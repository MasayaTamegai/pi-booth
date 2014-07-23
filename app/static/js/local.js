$(document).ready(function(){
	
	//Hold lookups in variables to save extra processing
	var welcome = $('#welcome');
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/local');
	var animatediv = $('#overlay');
	
	setInterval(function() {
		animatediv.toggleClass('anim');
		
		setTimeout(function() {
			animatediv.toggleClass('anim');
		}, 5000);
		
	}, 100000);
	    
	socket.on('event', function(event) {	
		if (event.type == 'client_connect') {
			welcome.show()
		}
	});
	    
});
	
