const ws = new WebSocket("ws://localhost:5678/");
const middle = {
  x: $(window).width() / 2,
  y: $(window).height() / 2,
};

const cmInPixels = 10 * 1.133333;
//const cmInPixels = 11;
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
    case "waitingForGift":
      showInstructions("Bitte Geschenk in die obere linke Ecke zum Vermessen schieben");
      break;
    case "sizeCalculated":
      showInstructions("Bitte Abrissvorrichtung nach oben klappen und Papier abrollen");
      break;
    case "paperPrepared":
      showInstructions("Bitte Abrissvorrichtung herunter klappen und Papier mit Messer abschneiden");
      break;
    case "paperCutOff":
      showInstructions("Bitte Messer zurück schieben");
      break;
    case "knifeMovedBack":
      renderGiftOnPaperFrame(paper_width * cmInPixels, paper_height * cmInPixels, gift_width * cmInPixels, gift_height * cmInPixels);
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
    default:
      hideAll();
      break;
  }
};

function showInstructions(text){
  $("#instructions").text(text).css({visibility: "visible"});
}

function renderPaperFrame(width, height){

  //get middle point of table which is middle point of screen/projection
  hideAll();
  const top_left_x = middle.x - width/2 - border_width;
  const top_left_y = middle.y - height/2 - border_width;
  $("#paperFrame").css({top: top_left_y, left: top_left_x, width: width, height: height, visibility: "visible"});

}

function renderGiftOnPaperFrame(paper_width, paper_height, gift_width, gift_height){
  hideAll();
  const top_left_x = middle.x - gift_width/2;
  const top_left_y = middle.y - gift_height/2;
  const top_left_x_paper = middle.x - paper_width/2 - border_width;
  const top_left_y_paper = middle.y - paper_height/2 - border_width;
  $("#paperFrame").css({top: top_left_y_paper, left: top_left_x_paper, width: paper_width, height: paper_height, visibility: "visible"});
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
  setTimeout(()=> {
    hideAll();
    renderFalt(1, paper_width, paper_height, gift_width, gift_height);
  }, 5000);
  /*if (isGiftLandscape){
    hideAll();
    /*$("#innerRightVertical").css({left: middle.x + gift_width/2, borderColor: second_color, height: gift_height, top: middle.y - gift_height/2, visibility: "visible"});
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
  }*/


}

function renderThirdFold(paper_width, paper_height, gift_width, gift_height, gift_depth) {
  /*if (isGiftLandscape){
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
  }*/
  setTimeout(()=> {
    hideAll();
    renderFalt(2, paper_width, paper_height, gift_width, gift_height);
  }, 5000);
}

function renderFalt(faltID, paper_width, paper_height, gift_width, gift_height){

  let tapeWidth = 60;
  let tapeHeight = 30;
  let tapeX, tapeY = -1;

  let rotationAngle = 0;
  let height, width, x, y = -1;
  if (isGiftLandscape) {
    width = (paper_width - gift_width) / 2;
    height = gift_height;
    if (faltID===1) {
      x = middle.x + gift_width / 2;
      tapeX = x - tapeWidth/2;
    } else {
      x = middle.x - paper_width / 2;
      tapeX = middle.x - gift_width/2 - tapeWidth/2;
      rotationAngle = 180;
    }
    tapeY = middle.y - tapeHeight/2;
    y = middle.y - gift_height / 2;
  } else {
    width = gift_width;
    height = (paper_height - gift_height) / 2;

    x = middle.x - gift_width/2;
    tapeX = middle.x - tapeHeight/2;
    if (faltID===1) {
      y = middle.y - paper_height / 2;

      tapeY = middle.y - gift_height/2 - tapeWidth/2;
    } else {
      y = middle.y + gift_height / 2;
      tapeY = middle.y + gift_height/2 - tapeWidth/2;
      rotationAngle = 180;
    }
    let tmp = tapeHeight;
    tapeHeight = tapeWidth;
    tapeWidth = tmp;
  }
  const css = {visibility: "visible", transform: "rotate("+rotationAngle+"deg)", height, width, left: x, top: y, position: "absolute"};
  const tapecss = {visibility: "visible", transform: "rotate("+rotationAngle+"deg)", height: tapeHeight, width: tapeWidth, left: tapeX, top: tapeY, position: "absolute"}
  if (isGiftLandscape){
    $("#faltung_vert").css(css);
    $("#tape_hor").css(tapecss);
  } else {
    $("#faltung_hor").css(css);
    $("#tape_vert").css(tapecss);
  }
}


function hideAll(){
  $(".verticalIndicator").css({visibility: "hidden"});
  $(".horizontalIndicator").css({visibility: "hidden"});
  $(".diagonalIndicator").css({visibility: "hidden"});
  $("#paperFrame").css({visibility: "hidden"});
  $("#giftOnPaper").css({visibility: "hidden"});
  $("#instructions").css({visibility: "hidden"});
  $("#faltung_hor").css({visibility: "hidden"});
  $("#faltung_vert").css({visibility: "hidden"});
  $("#tape_hor").css({visibility: "hidden"});
  $("#tape_vert").css({visibility: "hidden"});
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
