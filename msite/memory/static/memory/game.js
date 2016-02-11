function reqListener () {
  console.log(this.responseText);
  response = JSON.parse(this.responseText) 
  console.log(response);
  for (playerID in response.players){
	  player = response.players[playerID]
	  element = document.getElementById(playerID)
	  if (player.is_current_player){
		  element.style.backgroundColor = "red";
	  }
	  else{
		  element.style.backgroundColor = null;
	  }
	  element.textContent = player.name + ": " + player.score 
  }
  for (cardID in response.cards) {
	  card = response.cards[cardID]
	  element = document.getElementById(cardID)
	  element.style.backgroundPosition = card.bgpos
	  if (card.visible){
		  element.style.visibility = "visible";
	  }
	  else{
		  element.style.visibility = "hidden";
	  }
  }
}

function sendRequest() {
	var oReq = new XMLHttpRequest();
	oReq.addEventListener("load", reqListener);
	oReq.open("GET", "#");
	oReq.setRequestHeader("Accept","application/json");
	oReq.send();
}

function clickCard(e) {
	e.preventDefault();/*
	var oReq = new XMLHttpRequest();
	oReq.addEventListener("load", reqListener);
	oReq.open("POST", "#");
	oReq.setRequestHeader("Accept","application/json");
	oReq.send();*/
	console.log(this.value)
	return false;
}

function main(){
	var form = document.getElementById("game-form")
	form.onsubmit = function(e){e.preventDefault(); return false};
	for (name in form.elements) {
		var element = form.elements[name];
		if (element.type == "submit"){
			element.onclick = clickCard;
		}
	} 
	
}