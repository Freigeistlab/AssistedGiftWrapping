const ws = new WebSocket("ws://localhost:5678/");
const middle = {
  x: $(window).width() / 2,
  y: $(window).height() / 2,
};

const cmInPixels = 10;
const border_width = 4;

let isGiftLandscape = true;
const first_color = "#00FF00";
const second_color = "#0000FF";


ws.onmessage = function (event) {
  // convert the string we get into a JSON object
  const json = JSON.parse(event.data);
  console.log("Message", json);
  const { paper_width, paper_height, gift_width, gift_height, gift_depth } = json;
  checkIfLandscape(gift_width, gift_height);
  switch (json.state) {
    case "sizeCalculated":
      showInstructions("Bitte Papier heraus ziehen")
      break;
    case "paperPrepared":
      renderPaperFrame(paper_width * cmInPixels, paper_height * cmInPixels);
      break;
    case "paperLaidOut":
      renderGiftOnPaperFrame(gift_width * cmInPixels, gift_height * cmInPixels);
      break;
    case "giftPlaced":
      renderFirstFold(paper_width * cmInPixels, paper_height * cmInPixels, gift_width * cmInPixels, gift_height * cmInPixels, gift_depth * cmInPixels);
      break;
    case "firstFold":
      renderSecondFold(paper_width * cmInPixels, paper_height * cmInPixels, gift_width * cmInPixels, gift_height * cmInPixels, gift_depth * cmInPixels);
      break;
    case "secondFold":
      renderThirdFold(paper_width * cmInPixels, paper_height * cmInPixels, gift_width * cmInPixels, gift_height * cmInPixels, gift_depth * cmInPixels);
      break;
  }
};

function showInstructions(text){
  $("#instructions").text(text).css({visibility: "visible"});
}

function renderPaperFrame(width, height){

  //get middle point of table which is middle point of screen/projection
  const top_left_x = middle.x - width/2 - border_width;
  const top_left_y = middle.y - height/2 - border_width;
  hideAll();
  $("#paperFrame").css({top: top_left_y, left: top_left_x, width: width, height: height, visibility: "visible"});

}

function renderGiftOnPaperFrame(gift_width, gift_height){
  const top_left_x = middle.x - gift_width/2 - border_width/2;
  const top_left_y = middle.y - gift_height/2 - border_width/2;
  hideAll();
  $("#giftOnPaper").css({top: top_left_y, left: top_left_x, width: gift_width, height: gift_height, visibility: "visible"});
}

function renderFirstFold(paper_width, paper_height, gift_width, gift_height, gift_depth){

  hideAll();

  // the default case

  if (isGiftLandscape){
    const left_horizontals = middle.x - paper_width/2;
    $("#topHorizontal").css({top: middle.y - gift_height/2 - gift_depth, borderColor: second_color});
    $("#innerTopHorizontal").css({top: middle.y - gift_height/2, borderColor: first_color});
    $("#innerBottomHorizontal").css({top: middle.y + gift_height/2, borderColor: first_color});
    $("#bottomHorizontal").css({top: middle.y + gift_height/2 + gift_depth, borderColor: second_color});

    $(".horizontalIndicator").css({visibility: "visible", width: paper_width, left: left_horizontals});
  } else {
    const top_verticals = middle.y - paper_height/2;
    $("#leftVertical").css({left: middle.x - gift_width/2 - gift_depth, borderColor: second_color});
    $("#innerLeftVertical").css({left: middle.x - gift_width/2, borderColor: first_color});
    $("#innerRightVertical").css({left: middle.x + gift_width/2, borderColor: first_color});
    $("#rightVertical").css({left: middle.x + gift_width/2 + gift_depth, borderColor: second_color});

    $(".verticalIndicator").css({visibility: "visible", height: paper_height, top: top_verticals});
  }
}

function renderSecondFold(paper_width, paper_height, gift_width, gift_height, gift_depth) {
  if (isGiftLandscape){
    hideAll();
    $("#innerRightVertical").css({left: middle.x + gift_width/2, borderColor: second_color, height: gift_height, top: middle.y - gift_height/2, visibility: "visible"});
    $("#topRightDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x + gift_width/2,
      "y1": middle.y - gift_height/2,
      "x2": middle.x + paper_width/2,
      "y2": middle.y - gift_height/4,
    });
    $("#bottomRightDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x + gift_width/2,
      "y1": middle.y + gift_height/2,
      "x2": middle.x + paper_width/2,
      "y2": middle.y + gift_height/4,
    });
  } else {
    hideAll();
    $("#innerTopHorizontal").css({top: middle.y - gift_height/2, borderColor: second_color, width: gift_width, left: middle.x - gift_width/2, visibility: "visible"});
    $("#topRightDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x + gift_width/2,
      "y1": middle.y - gift_height/2,
      "x2": middle.x + gift_width/4,
      "y2": middle.y - paper_height/2,
    });
    $("#topLeftDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x - gift_width/2,
      "y1": middle.y - gift_height/2,
      "x2": middle.x - gift_width/4,
      "y2": middle.y - paper_height/2,
    });
  }
}

function renderThirdFold(paper_width, paper_height, gift_width, gift_height, gift_depth) {
  if (isGiftLandscape){
    hideAll();
    $("#innerLeftVertical").css({left: middle.x - gift_width/2, borderColor: second_color, height: gift_height, top: middle.y - gift_height/2, visibility: "visible"});
    $("#topLeftDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x - gift_width/2,
      "y1": middle.y - gift_height/2,
      "x2": middle.x - paper_width/2,
      "y2": middle.y - gift_height/4,
    });
    $("#bottomLeftDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x - gift_width/2,
      "y1": middle.y + gift_height/2,
      "x2": middle.x - paper_width/2,
      "y2": middle.y + gift_height/4,
    });
  } else {
    hideAll();
    $("#innerBottomHorizontal").css({top: middle.y + gift_height/2, borderColor: second_color, width: gift_width, left: middle.x - gift_width/2, visibility: "visible"});
    $("#bottomRightDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x + gift_width/2,
      "y1": middle.y + gift_height/2,
      "x2": middle.x + gift_width/4,
      "y2": middle.y + paper_height/2,
    });
    $("#bottomLeftDiagonal").css({visibility: "visible", stroke: first_color}).attr({
      "x1": middle.x - gift_width/2,
      "y1": middle.y + gift_height/2,
      "x2": middle.x - gift_width/4,
      "y2": middle.y + paper_height/2,
    });
  }
}


function hideAll(){
  $(".verticalIndicator").css({visibility: "hidden"});
  $(".horizontalIndicator").css({visibility: "hidden"});
  $(".diagonalIndicator").css({visibility: "hidden"});
  $("#paperFrame").css({visibility: "hidden"});
  $("#giftOnPaper").css({visibility: "hidden"});
  $("#instructions").css({visibility: "hidden"});
}


function checkIfLandscape(giftWidth, giftHeight){
  if (giftWidth < giftHeight){
    isGiftLandscape = false
  } else {
    isGiftLandscape = true
  }
}


/*
setTimeout(()=>renderPaperFrame(350,400),200);
setTimeout(()=>renderGiftOnPaperFrame(200,130),500);
setTimeout(()=>renderFoldIndicators(350,400,200,130,50),1000);
*/
