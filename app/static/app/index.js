document.addEventListener('DOMContentLoaded', function() {
  
  document.querySelectorAll('.remove').forEach(elem => {
	  elem.addEventListener('click', function () {
		  remove_watchlist(elem.parentNode);
		  // alert(elem.parentNode.querySelector('.name').textContent);
	  });
  })
  
});

function remove_watchlist(elem) {
	parent_div = elem.parentNode
	fetch('/remove', {
		method : 'POST',
		body : JSON.stringify({
			name : elem.querySelector('a').textContent,
			type : elem.dataset.num,
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print results
		console.log(result);
		elem.remove();
	})
	
	// fetch response after the following
	if (parent_div.childElementCount == 2) {
		const e = document.createElement('div');
		e.className = 'info';
		e.style = 'margin:0px; padding:15px; text-align:center;';
		
		const p = document.createElement('p');
		p.textContent = "Nothing in watchlist";
		
		e.appendChild(p);
		parent_div.appendChild(e);
	}
}