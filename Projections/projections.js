const ws = new WebSocket("ws://localhost:5678/");
const middle = {
  x: $(window).width() / 2,
  y: $(window).height() / 2,
};

const cmInPixels = 10 * 1.133333;
const border_width = 4;

//let isGiftLandscape = true;
const first_color = "#00FF00";
const second_color = "#00FF00";
let tapeWidth = 60;
let tapeHeight = 30;

const tape_text = 'Bitte an den gestrichelten Linien falten und dann Klebeband auf die rote Stelle kleben.';

ws.onmessage = function (event) {
  // convert the string we get into a JSON object
  const json = JSON.parse(event.data);
  console.log("Message", json);
  let { paper_width, paper_height, gift_width, gift_height, gift_depth } = json;
  if (paper_width < paper_height){
    //swap variables
    [gift_width,gift_height] = [gift_height,gift_width];
    [paper_width,paper_height] = [paper_height,paper_width];
  }
  switch (json.state) {
    case "start":
      hideAll();
      showInstructions("Bitte Geschenk in die obere linke Ecke zum Vermessen schieben");
      break;
    case "sizeCalculated":
      showInstructions("Bitte Abrissvorrichtung nach oben klappen und Papier abrollen");
      break;
    case "paperPrepared":
      showInstructions("Bitte Abrissvorrichtung herunter klappen und Papier mit Messer abschneiden");
      break;
    case "paperCutOff":
      showInstructions('Bitte Messer zur\u00FCck schieben');
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

function showInstructionsWithPos(text, x, y){
  $("#falt_instructions").text(text).css({visibility: "visible", top:y, left:x});
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

  const left_horizontals = middle.x - paper_width/2;
  $("#topHorizontal").css({top: middle.y - gift_height/2 - gift_depth, borderColor: second_color});
  $("#innerTopHorizontal").css({top: middle.y - gift_height/2, borderColor: first_color});
  $("#innerBottomHorizontal").css({top: middle.y + gift_height/2, borderColor: first_color});
  $("#bottomHorizontal").css({top: middle.y + gift_height/2 + gift_depth, borderColor: second_color});

  $(".horizontalIndicator").css({visibility: "visible", width: paper_width, left: left_horizontals});
  $("#tape_vert").css({visibility: "visible", width: tapeHeight, height: tapeWidth, left: middle.x - tapeHeight/2, top: middle.y - tapeWidth/2, position: "absolute"});
  showInstructionsWithPos(tape_text, middle.x + paper_width/2 + 10, middle.y - gift_height/2);
}

function renderSecondFold(paper_width, paper_height, gift_width, gift_height, gift_depth) {
  setTimeout(()=> {
    hideAll();
    renderFalt(1, paper_width, paper_height, gift_width, gift_height);
    showInstructionsWithPos(tape_text, middle.x + paper_width/2 + 10, middle.y - gift_height/2);
  }, 5000);


}

function renderThirdFold(paper_width, paper_height, gift_width, gift_height, gift_depth) {
  setTimeout(()=> {
    hideAll();
    renderFalt(2, paper_width, paper_height, gift_width, gift_height);
    showInstructionsWithPos(tape_text, middle.x + paper_width/2 + 10, middle.y - gift_height/2);
  }, 5000);
}

function renderFalt(faltID, paper_width, paper_height, gift_width, gift_height){

  let tapeX = -1;

  let rotationAngle = 0;
  let x = -1;

  const width = (paper_width - gift_width) / 2;
  const height = gift_height;
  if (faltID===1) {
    x = middle.x + gift_width / 2;
    tapeX = x - tapeWidth/2;
  } else {
    x = middle.x - paper_width / 2;
    tapeX = middle.x - gift_width/2 - tapeWidth/2;
    rotationAngle = 180;
  }
  tapeY = middle.y - tapeHeight/2;
  const y = middle.y - gift_height / 2;

  const css = {visibility: "visible", transform: "rotate("+rotationAngle+"deg)", height, width, left: x, top: y, position: "absolute"};
  const tapecss = {visibility: "visible", transform: "rotate("+rotationAngle+"deg)", height: tapeHeight, width: tapeWidth, left: tapeX, top: tapeY, position: "absolute"}

  $("#faltung_vert").css(css);
  $("#tape_hor").css(tapecss);

}


function hideAll(){
  $(".verticalIndicator").css({visibility: "hidden"});
  $(".horizontalIndicator").css({visibility: "hidden"});
  $(".diagonalIndicator").css({visibility: "hidden"});
  $("#paperFrame").css({visibility: "hidden"});
  $("#giftOnPaper").css({visibility: "hidden"});
  $("#instructions").css({visibility: "hidden"});
  $("#falt_instructions").css({visibility: "hidden"});
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
