var MapVisualization = function(width, height, gridWidth, gridHeight, context) {
	var width = width;
	var height = height;
	var context = context;
	var cellWidth = Math.floor(width / gridWidth);
	var cellHeight = Math.floor(height / gridHeight);
	var maxR = Math.min(cellHeight, cellWidth)/2 - 1;

	// Draws walls
	this.drawRooms = function(array_rooms){
		context.font = "15px Arial"
		rooms = array_rooms;
		for (var i in rooms){
			var room = rooms[i];
			room.y = gridHeight - room.y - 1;
			if(room.type != 'out'){
				for(var i=0; i < 4; i++){
					this.drawRectangle(room.x, room.y, 1, 1,"Brown", false);
				}
				this.drawRectangle(room.x, room.y, 1, 1,"Brown", false , room.text, "black");
			}
			else{
				var cx = (room.x + 0.5) * cellWidth;
                var cy = (room.y + 0.5) * cellHeight;
                context.fillStyle = 'black';
                context.textAlign = 'center';
                context.textBaseline= 'middle';
                context.fillText(room.text, cx, cy);
			}
			context.font = "20px Arial"
			var cx = (room.x + 0.25) * cellWidth;
			var cy = (room.y + 0.35) * cellHeight;
			color = 'blue'

            context.fillStyle = color;
            context.textAlign = 'right';
            context.textBaseline = 'bottom';
            context.fillText(room.nAgents, cx, cy);
            context.font = "15px Arial"
		}
		for (var o in rooms){
			for (var p in rooms){
				var room1 = rooms[o]
				var room2 = rooms[p]
				adj = this.areAdj(room1, room2)
				if (adj){
					if (room1.name == room2.name){
						if(room1.y == room2.y){
							x = (room1.x + room2.x + 1)/2
							y1 = room1.y 
							y2 = room1.y + 1
							for(var i=0; i < 6; i++){
								this.drawLine(x, y1, x, y2, '#eee');
							}
						}
						if(room1.x == room2.x){
							y = (room1.y + room2.y + 1)/2
							x1 = room1.x
							x2 = room1.x + 1
							for(var i=0; i < 6; i++){
								this.drawLine(x1, y, x2, y, '#eee');
							}
						}
					}
				}
			}
		}
	}
	
	this.areAdj = function(room1, room2){
		x1 = room1.x
		y1 = room1.y
		adj = false
		if (room2.x == room1.x){
			if (room2.y == (room1.y+1) || room2.y == (room1.y-1))
				adj = true
		}
		if (room2.y == room1.y){
			if (room2.x == (room1.x+1) || room2.x == (room1.x-1))
				adj = true
		}
		return adj

	}

	// Draws doors
	this.drawDoorsRooms = function(array_doors){
		doors = array_doors;
		for (var i in doors){
			var door = doors[i];
			var yDraw = 0
			var xDraw = 0
			if(door.x1 == door.x2){
				xDraw = door.x1;
				yDraw = (door.y1 + door.y2)/2;
				yDraw = gridHeight - yDraw - 1;
				var color = "red";
				if (door.state == true){
					color = "Green";
				}
				this.drawRectangle(xDraw, yDraw, 0.25, 0.05, color, true);
			}
			if(door.y1 == door.y2){
				yDraw = door.y1;
				xDraw = (door.x1 + door.x2)/2;
				yDraw = gridHeight - yDraw - 1;
				var color = "red";
				if (door.state == true){
					color = "Green";
				}
				this.drawRectangle(xDraw, yDraw, 0.05, 0.25, color, true);
			}
		}	
	}

// Draws walls
	this.drawWalls = function(array_walls){
		walls = array_walls;
		
		for (var i in walls){
			var wall = walls[i];
			var y1Draw = gridHeight - wall["y1"] - 1
			var x1Draw = wall["x1"]
			var y2Draw = gridHeight - wall["y2"] - 1
			var x2Draw = wall["x2"]
			if (y1Draw == y2Draw){
				this.drawLine((x1Draw + x2Draw)/2+ 0.5, y1Draw, (x1Draw + x2Draw)/2 + 0.5, y1Draw -1, 'brown');
		}
			else{
				this.drawLine(x1Draw ,(y1Draw  + y2Draw)/2 - 0.5, x1Draw +1, (y1Draw + y2Draw)/2 - 0.5, 'brown');
	}
			
		}	
	}

// Draws walls
	this.drawDoors = function(array_doors){
		doors = array_doors;
		
		for (var i in doors){
			var door = doors[i];
			var yDraw = gridHeight - door["y"] - 1
			var xDraw = door["x"]
			color = 'red'
			if (door["state"] == 'True'){
				color = 'green'
			}
			if (door["rot"] == 'y'){
				this.drawLine(xDraw+1, yDraw, xDraw+1, yDraw +1, color);
		}
			else{
				this.drawLine(xDraw, yDraw, xDraw +1 , yDraw, color);
	}
}		
	}

// Draws walls
	this.drawPoi = function(array_doors){
		doors = array_doors;
		
		for (var i in doors){
			var door = doors[i];
			var yDraw =gridHeight - door["y"] - 1
			var xDraw = door["x"]
			this.drawRectangle(xDraw, yDraw, 1, 1, 'green', true);
		}	
	}

// Draws walls
	this.drawGeneralItem = function(array_doors){
		doors = array_doors;
		
		for (var i in doors){
			var door = doors[i];
			var yDraw = gridHeight - door["y"] - 1
			var xDraw = door["x"]
			this.drawRectangle(xDraw, yDraw, 1, 1, 'grey', true);
		}
	}


	// Calls the appropriate shape(agent)
    this.drawLayer = function(portrayalLayer) {
		for (var i in portrayalLayer) {
			var p = portrayalLayer[i];

	            p.y = gridHeight - p.y - 1;
				if (p.Shape == "rect"){
					w = 1
					h = 1
					this.drawRectangle(p.x, p.y, w, h, p.Color, p.Filled, p.text, p.text_color);
				}
				else if (p.Shape == "circle"){
					this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled, p.text, p.text_color);
				}
	            else if (p.Shape == "arrowHead"){
					this.drawArrowHead(p.x, p.y, p.heading_x, p.heading_y, p.scale, p.Color, p.Filled, p.text, p.text_color);
	            }
			
		}
	};




	this.drawLine = function(x1,y1,x2,y2,color) {
		var dx1 = x1 * cellWidth;
		var dy1 = y1 * cellHeight;
		var dx2 = x2 * cellWidth;
		var dy2 = y2 * cellHeight;

		context.beginPath();
		context.moveTo(dx1, dy1);
		context.lineTo(dx2, dy2);
		context.lineWidth = 1;
		context.strokeStyle = color;
		context.stroke();

	};



	this.drawCircle = function(x, y, radius, color, fill, text, text_color) {
		var cx = (x + 0.5) * cellWidth;
		var cy = (y + 0.5) * cellHeight;
		var r = radius * maxR

		context.beginPath();
		context.arc(cx, cy, r, 0, Math.PI * 2, false);
		context.closePath();

		context.strokeStyle = color;
		context.stroke();

		if (fill) {
			context.fillStyle = color;
			context.fill();
		}
                if (text !== undefined) {
                        context.fillStyle = text_color;
                        context.textAlign = 'center';
                        context.textBaseline= 'middle';
                        context.fillText(text, cx, cy);
                }

	};

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


    this.drawGridLines = function() {
    	context.beginPath();
		context.strokeStyle = "#eee";
		maxX = cellWidth * gridWidth;
		maxY = cellHeight * gridHeight;

		// Draw horizontal grid lines:
		for(var y=0; y<=maxY; y+=cellHeight) {
			context.moveTo(0, y+0.5);
			context.lineTo(maxX, y+0.5);
		}

		for(var x=0; x<=maxX; x+= cellWidth) {
			context.moveTo(x+0.5, 0);
			context.lineTo(x+0.5, maxY);
		}
		context.stroke();
	};

	this.resetCanvas = function() {
		context.clearRect(0, 0, width, height);
		context.beginPath();
	};

};
var context = undefined;
var CanvasModule = function(canvas_width, canvas_height, grid_width, grid_height) {
	// Create the element
	// ------------------

	// Create the tag:
	var canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:1px dotted'></canvas>";
	// Append it to body:
	var canvas = $(canvas_tag)[0];
	$("body").append(canvas);

	// Create the context and the drawing controller:
	context = canvas.getContext("2d");
	var canvasDraw = new MapVisualization(canvas_width, canvas_height, grid_width, grid_height, context);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.drawGridLines();
		if(data[100] == 'rooms'){
			canvasDraw.drawRooms(data[10]);
			canvasDraw.drawDoorsRooms(data[20]);}
		else{
			canvasDraw.drawGeneralItem(data[40]);
			canvasDraw.drawPoi(data[30]);
			canvasDraw.drawWalls(data[10]);
			canvasDraw.drawDoors(data[20]);
			
		for (var layer in data)
			canvasDraw.drawLayer(data[layer]);
		};
	};
	this.reset = function() {
		canvasDraw.resetCanvas();
	};

}