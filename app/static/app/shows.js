document.addEventListener('DOMContentLoaded', function() {
  
  document.querySelectorAll('.test').forEach(elem => {
	  elem.addEventListener('click', function () {
		  add_watchlist(elem.parentNode.parentNode);
		  // alert(elem.parentNode.querySelector('.name').textContent);
	  });
  })
  
});

function add_watchlist(elem) {
	fetch('/addShow', {
		method : 'POST',
		body : JSON.stringify({
			name : elem.querySelector('.name').textContent,
			genre : document.querySelector('h2.genre').querySelector('strong').textContent,
			url : elem.querySelector('.url').href,
			img : elem.querySelector('.img').src,
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print results
		console.log(result);
		
		// Add message
		const td = elem.querySelectorAll('td')[1];
		const msg = document.createElement('p');
		msg.className = 'msg';
		msg.addEventListener('animationend', () => {
			msg.remove();
		});
		
		if ('message' in result) {
			msg.style = "display:inline; margin:0px; color: red";
			msg.textContent = result['message'];
		}
		else {
			msg.style = "display:inline; margin:0px; color: green";
			msg.textContent = 'Added to watchlist';
		}
		
		prev = elem.querySelector('.msg');
		if (prev) {
			prev.remove();
		}
		td.appendChild(msg);
	})
}