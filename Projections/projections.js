const ws = new WebSocket("ws://localhost:5678/");

ws.onmessage = function (event) {
  // convert the string we get into a JSON object
  const json = JSON.parse(event.data);
  console.log("Message", json)
  const { paper_width, paper_height, gift_width, gift_height } = json;
  switch (json.state) {
    case "paperPrepared":
      renderPaperFrame(paper_width, paper_height);
      break;
    case "paperLaidOut":
      renderGiftOnPaperFrame(paper_width, paper_height, gift_width, gift_height);
      break;
  }
};

function renderPaperFrame(width, height){
  //TODO
  $("#paperFrame").toggle();
  console.log("render paper frame")
}

function renderGiftOnPaperFrame(paper_width, paper_height, gift_width, gift_height){
  //TODO
  $("#giftOnPaperFrame").toggle();
  console.log("render gift on paper frame")
}