//IMPORTANT INFORMATION:
//The JavaScript component is the main component of the code.
//The variable data is the dataset containing the information to build the map and is already defined based on the Python code.
//This is based on HTML and SVG. It only runs with the right HTML and SVG already existing.

//A choropleth map is a map where shapes are filled in, such as countries in the map in this program.


loadMap();
function loadMap(){

	//Opens where the map should go in the SVG
	var svg = document.getElementById("polygroup");
	var svgMetadata = data["map"]["metadata"];
	var entireSVG = document.getElementById("svgmap");

	//Adjust height and width
	entireSVG.setAttribute("height",svgMetadata["height"]);
	entireSVG.setAttribute("width",svgMetadata["width"]);

	//Map points
	var svgPoints = data["map"]["data"];

	//Choropleth map data
	var choropleth = data["data"]["data"][data["choropleth"]["source"]];
	var choropleth_min = Math.min.apply(null,choropleth);
	var choropleth_max = Math.max.apply(null,choropleth);
	var choropleth_range = choropleth_max - choropleth_min;

	//Choropleth map colors
	var choropleth_colors = data["choropleth"]["colors"];
	var choropleth_red_min = choropleth_colors["r"][0];
	var choropleth_red_max = choropleth_colors["r"][1];
	var choropleth_green_min = choropleth_colors["g"][0];
	var choropleth_green_max = choropleth_colors["g"][1];
	var choropleth_blue_min = choropleth_colors["b"][0];
	var choropleth_blue_max = choropleth_colors["b"][1];
	var choropleth_red_range = choropleth_red_max - choropleth_red_min;
	var choropleth_green_range = choropleth_green_max - choropleth_green_min;
	var choropleth_blue_range = choropleth_blue_max - choropleth_blue_min;

	//Ordered list of territories
	var territory_list = data["data"]["territory_list"];

	//Infobox
	var infobox_styles = data["infobox"]["style"];
	var infobox_styles_text = infobox_styles["text"];
	var infobox_text = data["infobox"]["text"];

	//Draw map
	var polyPoints;
	var jsonPoint;
	var country;
	var poly;

	var rescaleY = svgMetadata["height"] / 180;
	var rescaleX = svgMetadata["width"] / 360;
	var translateY = svgMetadata["translate"][1];
	var translateX = svgMetadata["translate"][0];
	var zoom = svgMetadata["scale"];
	var pointX;
	var pointY;

	for (var countryData in svgPoints){
		polyPoints = ""
		for (jsonPoint in svgPoints[countryData]["Points"]){
			pointX = (svgPoints[countryData]["Points"][jsonPoint][0] - translateX) * rescaleX * zoom;
			pointY = (180 / zoom - svgPoints[countryData]["Points"][jsonPoint][1] + translateY) * rescaleY * zoom;
			polyPoints = polyPoints + pointX + "," + pointY + " ";
		}
		polyPoints = polyPoints.substring(0,polyPoints.length-1);
		poly = document.createElementNS("http://www.w3.org/2000/svg","polygon");
		poly.setAttributeNS(null,"points",polyPoints);
		poly.setAttributeNS(null,"class",svgPoints[countryData]["Country"]);
		poly.setAttributeNS(null,"style","fill:lime;stroke:purple;stroke-width:0.5");
		svg.appendChild(poly);

	}
	colorMap();
}
function colorMap(){

	//Choropleth map data
	var choropleth = data["data"]["data"][data["choropleth"]["source"]];
	var choropleth_min = Math.min.apply(null,choropleth);
	var choropleth_max = Math.max.apply(null,choropleth);
	var choropleth_range = choropleth_max - choropleth_min;

	//Choropleth map colors
	var choropleth_colors = data["choropleth"]["colors"];
	var choropleth_red_min = choropleth_colors["r"][0];
	var choropleth_red_max = choropleth_colors["r"][1];
	var choropleth_green_min = choropleth_colors["g"][0];
	var choropleth_green_max = choropleth_colors["g"][1];
	var choropleth_blue_min = choropleth_colors["b"][0];
	var choropleth_blue_max = choropleth_colors["b"][1];
	var choropleth_red_range = choropleth_red_max - choropleth_red_min;
	var choropleth_green_range = choropleth_green_max - choropleth_green_min;
	var choropleth_blue_range = choropleth_blue_max - choropleth_blue_min;

	//Ordered list of territories
	var territory_list = data["data"]["territory_list"];

	//Color map
	for (var j in territory_list){
	
		//Get country on map
		country = document.getElementsByClassName(territory_list[j]);
	
		//Scale data
		var data_proportional = (choropleth[j] - choropleth_min) / choropleth_range;
	
		//Calculate colors
		var red = data_proportional * choropleth_red_range + choropleth_red_min;
		var green = data_proportional * choropleth_green_range + choropleth_green_min;
		var blue = data_proportional * choropleth_blue_range + choropleth_blue_min;

		var color = "rgb(" + red + "," + green + "," + blue + ")";

		for (var i = 0; i < country.length; i++){
			country[i].style.fill = color;
			country[i].setAttribute("onmousemove",data["inputs"]["onHover"].replaceAll("[COUNTRY]",j));
			country[i].setAttribute("onmouseout",data["inputs"]["onMouseOut"].replaceAll("[COUNTRY]",j));
			country[i].setAttribute("onclick",data["inputs"]["onClick"].replaceAll("[COUNTRY]",j));
		}
	}
}

function showInfobox(c){

	//Infobox
	var infobox_styles = data["infobox"]["style"];
	var infobox_styles_text = infobox_styles["text"];
	var infobox_text = data["infobox"]["text"];


	//Text
	var textPopUpParent = document.getElementById("dataInfo");
	var textPopUpList = [];
	var textPopUpText;

	//Sort text containers into lines
	for(var i in infobox_text){
		while(textPopUpList.length <= infobox_text[i]["line"]){
			textPopUpList.push([]);
		}
		textPopUpText = {};
		textPopUpText["text"] = infobox_text[i]["text"];
		textPopUpText["type"] = infobox_text[i]["type"];
		textPopUpText["style"] = infobox_styles_text[i];
		textPopUpList[infobox_text[i]["line"]].push(textPopUpText);
	}

	//Create text
	var textX;
	var textY;
	var numberLines = textPopUpList.length;
	var lineWidth;
	var ttlHeight = 0;
	var maxWidth = 0;
	var maxHeight;
	var bbox;
	var textColorHTML;
	var textColorDict;
	var font_size;
	var font;
	var iReverse;
	var textPopUpGroup = document.getElementById("dataInfo");
	var textPopUpDelete = document.getElementsByClassName("infoboxText")

	//Delete old text
	while(textPopUpDelete.length > 0){
		textPopUpDelete[0].parentNode.removeChild(textPopUpDelete[0]);
	}
	for(i in textPopUpList){
		lineWidth = 0;
		maxHeight = 0;
		iReverse = numberLines - 1 - i;
		for(var j in textPopUpList[iReverse]){
			textPopUp = document.createElementNS("http://www.w3.org/2000/svg","text");
			if(textPopUpList[iReverse][j]["type"] == "text"){
				textPopUp.innerHTML = textPopUpList[iReverse][j]["text"].replaceAll(" ","&nbsp;");
			} else {
				textPopUp.innerHTML = eval(textPopUpList[iReverse][j]["text"]);
			}

			//Calculate x and y of text
			textX = event.pageX - 72 + lineWidth;
			textY = event.pageY - 65 - ttlHeight;

			//Style
			textColorDict = textPopUpList[iReverse][j]["style"];
			textColorHTML = "rgb(" + textColorDict["r"] + "," + textColorDict["g"] + "," + textColorDict["b"] + ");"
			font_size = textColorDict["size"];
			font_family = textColorDict["font"];

			//Set property and style
			textPopUp.setAttributeNS(null,"x",textX);
			textPopUp.setAttributeNS(null,"y",textY);
			textPopUp.setAttributeNS(null,"font-family",font_family);
			textPopUp.setAttributeNS(null,"font-size",font_size);
			textPopUp.setAttributeNS(null,"fill",textColorHTML);
			textPopUp.setAttributeNS(null,"class","infoboxText");
			textPopUpGroup.appendChild(textPopUp);
			
			//Adjust future elements by accounting for element width
			bbox = textPopUp.getBBox();
			lineWidth = lineWidth + bbox.width;
			if(bbox.height > maxHeight){
				maxHeight = bbox.height;
			}
		}
		if(lineWidth > maxWidth){
			maxWidth = lineWidth;
		}
		ttlHeight = ttlHeight + maxHeight;
	}

	//Box
	var boxPopUp = document.getElementById("dataInfoBox");
	boxPopUp.setAttribute("x",event.pageX-82);
	boxPopUp.setAttribute("y",event.pageY-65-ttlHeight);
	boxPopUp.setAttribute("height",ttlHeight+10);
	boxPopUp.setAttribute("width",maxWidth+20);

	//Set stroke width
	boxPopUp["style"]["stroke-width"] = infobox_styles["border"]["stroke-width"];

	//Fill colors
	var red = infobox_styles["color"]["r"];
	var green = infobox_styles["color"]["g"];
	var blue = infobox_styles["color"]["b"];

	var color = "rgb(" + red + "," + green + "," + blue + ")";
	boxPopUp.setAttribute("fill",color);

	//Border colors

	red = infobox_styles["border"]["color"]["r"];
	green = infobox_styles["border"]["color"]["g"];
	blue = infobox_styles["border"]["color"]["b"];

	color = "rgb(" + red + "," + green + "," + blue + ")";
	boxPopUp.style.stroke = color;

	//Make visible
	boxPopUp.style.visibility = "visible";
}

function hideInfobox(c){
	var textPopUp = document.getElementsByClassName("infoboxText");
	while(textPopUp.length > 0){
		textPopUp[0].parentNode.removeChild(textPopUp[0]);
	}
	var boxPopUp = document.getElementById("dataInfoBox");
	boxPopUp.style.visibility = "hidden";
}