const ws = new WebSocket("ws://localhost:5678/");
const middle = {
  x: $(window).width() / 2,
  y: $(window).height() / 2,
};

const cmInPixels = 10;
const border_width = 4;

ws.onmessage = function (event) {
  // convert the string we get into a JSON object
  const json = JSON.parse(event.data);
  console.log("Message", json);
  const { paper_width, paper_height, gift_width, gift_height, gift_depth } = json;
  switch (json.state) {
    case "paperPrepared":
      renderPaperFrame(paper_width * cmInPixels, paper_height * cmInPixels);
      break;
    case "paperLaidOut":
      renderGiftOnPaperFrame(gift_width * cmInPixels, gift_height * cmInPixels);
      break;
    case "giftPlaced":
      renderFoldIndicators(paper_width * cmInPixels, paper_height * cmInPixels, gift_width * cmInPixels, gift_height * cmInPixels, gift_depth * cmInPixels);
      break;
  }
};

function renderPaperFrame(width, height){
  //get middle point of table which is middle point of screen/projection
  const top_left_x = middle.x - width/2 - border_width;
  const top_left_y = middle.y - height/2 - border_width;
  $("#giftOnPaper").css({visibility: "hidden"});
  $("#paperFrame").css({top: top_left_y, left: top_left_x, width: width, height: height, visibility: "visible"});

}

function renderGiftOnPaperFrame(gift_width, gift_height){

  const top_left_x = middle.x - gift_width/2 - border_width/2;
  const top_left_y = middle.y - gift_height/2 - border_width/2;
  $("#paperFrame").css({visibility: "hidden"});
  $(".verticalIndicator").css({visibility: "hidden"});
  $(".horizontalIndicator").css({visibility: "hidden"});
  $("#giftOnPaper").css({top: top_left_y, left: top_left_x, width: gift_width, height: gift_height, visibility: "visible"});
}

function renderFoldIndicators(paper_width, paper_height, gift_width, gift_height, gift_depth){

  $("#paperFrame").css({visibility: "hidden"});
  $("#giftOnPaper").css({visibility: "hidden"});
  
  const top_verticals = middle.y - paper_height/2;
  $("#leftVertical").css({left: middle.x - gift_width/2 - gift_depth});
  $("#innerLeftVertical").css({left: middle.x - gift_width/2});
  $("#innerRightVertical").css({left: middle.x + gift_width/2});
  $("#rightVertical").css({left: middle.x + gift_width/2 + gift_depth});

  $(".verticalIndicator").css({visibility: "visible", height: paper_height, top: top_verticals});

  const left_horizontals = middle.x - paper_width/2;
  $("#topHorizontal").css({top: middle.y - gift_height/2 - gift_depth});
  $("#innerTopHorizontal").css({top: middle.y - gift_height/2});
  $("#innerBottomHorizontal").css({top: middle.y + gift_height/2});
  $("#bottomHorizontal").css({top: middle.y + gift_height/2 + gift_depth});

  $(".horizontalIndicator").css({visibility: "visible", width: paper_width, left: left_horizontals});
}
/*
setTimeout(()=>renderPaperFrame(350,400),200);
setTimeout(()=>renderGiftOnPaperFrame(200,130),500);
setTimeout(()=>renderFoldIndicators(350,400,200,130,50),1000);
*/
