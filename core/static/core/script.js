function roundRect(ctx, x, y, width, height, radius) {
	radius = {tl: radius, tr: radius, br: radius, bl: radius};
	ctx.beginPath();
	ctx.moveTo(x + radius.tl, y);
	ctx.lineTo(x + width - radius.tr, y);
	ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
	ctx.lineTo(x + width, y + height - radius.br);
	ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
	ctx.lineTo(x + radius.bl, y + height);
	ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
	ctx.lineTo(x, y + radius.tl);
	ctx.quadraticCurveTo(x, y, x + radius.tl, y);
	ctx.closePath();
	ctx.fill();
	ctx.lineWidth = 3;
	ctx.stroke();
}
function drawName(name, x, y, mandatory, done){
	var ctx = document.getElementById("class").getContext("2d");
	if (done) {
		ctx.strokeStyle="#d3d3d3";
		ctx.fillStyle="#d3d3d3";
	} else {
		ctx.strokeStyle="#d3d3d3";
		ctx.fillStyle="#f0e68c";
	}
	var w = ctx.measureText(name).width + 10;
	roundRect(ctx, x, y, w, 40, 10);
	ctx.textAlign="center";
	ctx.font="bold 12px Arial";
	if (mandatory) {
		ctx.strokeStyle="#b22222";
		ctx.fillStyle="#b22222";
	} else {
		ctx.strokeStyle="#000000";
		ctx.fillStyle="#000000";
	}
	ctx.fillText(name, x+w/2, y+25);
}
