var VisualModule = function(width, height, gridWidth, gridHeight){
	var cellWidth = Math.floor(width / gridWidth);
	var cellHeight = Math.floor(height / gridHeight);

	this.drawRectangle = function(x, y, w, h, color, fill, text, text_color) {
		context.beginPath();
		var dx = w * cellWidth;
		var dy = h * cellHeight;

		// Keep in the center of the cell:
		var x0 = (x + 0.5) * cellWidth - dx/2;
		var y0 = (y + 0.5) * cellHeight - dy/2;

		context.strokeStyle = color;
		context.fillStyle = color;
		if (fill)
			context.fillRect(x0, y0, dx, dy);
		else
			context.strokeRect(x0, y0, dx, dy);

                // This part draws the text inside the Rectangle
                if (text !== undefined) {
                        var cx = (x + 0.5) * cellWidth;
                        var cy = (y + 0.5) * cellHeight;
                        context.fillStyle = text_color;
                        context.textAlign = 'center';
                        context.textBaseline= 'middle';
                        context.fillText(text, cx, cy);
                }
	};

	this.render = function(data) {
		for (var i in data[1]){
			console.log(data[1][i])
			var yDraw = gridHeight - data[1][i]["y"] - 1
			var xDraw = data[1][i]["x"]
			console.log(xDraw, yDraw)
			this.drawRectangle(xDraw, yDraw, 1, 1, 'red', true);
		}
	};

	this.reset = function() {
	};

};