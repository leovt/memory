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
}

function sendRequest() {
	var oReq = new XMLHttpRequest();
	oReq.addEventListener("load", reqListener);
	oReq.open("GET", "#");
	oReq.setRequestHeader("Accept","application/json");
	oReq.send();
}