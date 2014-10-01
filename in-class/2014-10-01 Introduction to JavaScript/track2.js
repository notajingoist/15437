var startBtn = document.getElementById('startBtn');
var stopBtn = document.getElementById('stopBtn');
var resetBtm = document.getElementById('resetBtn');
var timeElapsed = document.getElementById('timeElapsed');

startBtn.addEventListener('click', start);
stopBtn.addEventListener('click', stop);
resetBtn.addEventListener('click', reset);

var intervalId;

function start() {
	console.log('starting');
	intervalId = window.setInterval(countUp, 1000);
}

function countUp() {
	console.log('counting up');
	var currentTime = timeElapsed.innerHTML;
	var newTime = parseInt(currentTime) + 1;
	timeElapsed.innerHTML = newTime;
}

function stop() {
	window.clearInterval(intervalId);
}

function reset() {
	window.clearInterval(intervalId);
	timeElapsed.innerHTML = 0;
}