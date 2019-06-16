var Line = function(x, y){
	this.x0 = this.x = x;
	this.y0 = this.y = y;
	this.update = function() {
		var dx = mouse.x - this.x0,
				dy = mouse.y - this.y0;
		var dist = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
		var angle = Math.atan2(dx, dy);
		var near = (dist / maxDist).toFixed(2);
		this.radio = near * maxRadio;
		this.x = (Math.sin(angle) * this.radio) + this.x0;
		this.y = (Math.cos(angle) * this.radio) + this.y0;
		this.alpha = 1 - (near*0.5);
		this.lineWidth = this.alpha * 5;
		this.color = "rgba(140, 137, 115, "+this.alpha+")";
	}
	this.draw = function(){
		this.update();
		context.beginPath();
		context.moveTo(this.x0, this.y0);
		context.lineTo(this.x, this.y);
		context.lineWidth = this.lineWidth;
		context.strokeStyle = this.color;
		context.stroke();
	}
	return this;
}

var canvas, context;
var mouse = { x: 0, y: 0 };
var cursor = {
	x: window.innerWidth,
	y: window.innerHeight
};
var lines = [];
var separation = 50;
var maxDist = 50, maxRadio = separation/2, minRadio = 1;

function init(){
	canvas = document.getElementById("canvas");
	context = canvas.getContext("2d");
	onResizeWindow();
	document.addEventListener("mousemove", onPointerMove, false);
	document.addEventListener("touchmove", onPointerMove, false);
	window.addEventListener("resize", onResizeWindow, false);
}

function onResizeWindow() {
	canvas.style.width = window.innerWidth + "px";
	canvas.style.height = window.innerHeight + "px";
	canvas.width = window.innerWidth * window.devicePixelRatio;
	canvas.height = window.innerHeight * window.devicePixelRatio;
	maxDist = canvas.width > canvas.height ? canvas.width : canvas.height;
	maxDist = 300;
	setLines();
}

function onPointerMove(event) {
	event.preventDefault();
	var point = event.touches ? event.touches[0] : event;
	cursor = {
		x: point.clientX,
		y: point.clientY
	}
}

function setLines(){
	lines = [];
	for (var x = 0; x <= canvas.width; x+= separation) {
		for (var y = 0; y <= canvas.height; y+= separation) {
			lines.push(new Line(x, y));
		}
	}
}

function render(){
	mouse.x += (cursor.x - mouse.x) / 10;
	mouse.y += (cursor.y - mouse.y) / 10;
	context.clearRect(0,0, canvas.width, canvas.height);
	context.lineCap = "round";
	context.strokeStyle = "white";
	for (var i = 0; i < lines.length; i++) lines[i].draw();
}

function animate(){
	requestAnimationFrame(animate);
	render();
}

init();
animate();