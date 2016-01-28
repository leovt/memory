# Memory
A Memory Game with Django

# Project Plan

  1. Define model 
  
     - https://www.lucidchart.com/documents/view/81a6d95b-3cf0-40b8-97bc-6317804c47b2
     - actions on the entities
     
  2. Define states and transitions
  
     - in a game
     - in the app
  
  3. Backend prototype
  
  4. Frontend using basic forms 
  
  5. Frontend with js / ajax / svg
  
Model Entities and Actions
--------------------------

*  GET /game
 
   Show a page for starting a new game (newgame.html)

*  POST /game (name=string)

   start a game, create first player and send user to /game/[id] with an identifying cookie


*  GET /game/[id]

   show the current state of game [id]
   - if the second player has not joined yet, show a link to /game/[id]/join for the second player to join (wait.html)
   - if the game is started use main game page (game.html)
   - if the user has no player cookie and the game has not started, offer him to join the game
   - if the user has no player cookie but the game has started, refuse with 404 or redirect


*  POST /game/[id]/join (name=string)

   create second player and send user to /game/[id] with an identifying cookie


*  GET /game/[id]/actions

   a list of events that happend since the start of the game
   - json or html
   - range request


*  POST /game/[id]  (card=id)

   verify that the player is allowed to turn the card card[id]
   if so perform the corresponding move
   - send a message to clients for updating their game state




   