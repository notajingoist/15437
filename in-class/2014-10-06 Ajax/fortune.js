var btn = document.getElementById('btn');
btn.addEventListener('click', sendRequest)

function sendRequest() {
	var req;
	if (window.XMLHttpRequest) {
		req = new XMLHttpRequest();
	} else {
		req = new ActiveXObject('Microsoft.XMLHTTP');
	}
	req.onreadystatechange = function() {
		if (req.readyState !== 4 || req.status !== 200) {
			return;
		}

		var content = document.getElementById('content');

		var fortune = JSON.parse(req.responseText);
		content.innerHTML = fortune['fortune'];
		console.log(fortune);
	}

	req.open('GET', 'http://garrod.isri.cmu.edu/webapps/fortune', true);
	req.send();
}

