# API Specifications

If www.example.com is the API you created, then the endpoints are as follows
http://www.example.com/ should contain all the endpoints you created. Sending a simple GET request to
this site should fetch a list of all endpoints you have created. List of expected endpoints (not an exhaustive
list) are:

/addPlayer add a new player

/addGame inserts a game

/searchPlayer allows the user to enter a search key. Return an array of all players who match the search
term (Ex: if the user searches “Ak”, then you should be able to return all players whose name contains the
key “Ak”). This should display details of each player and his/her respective game data

/searchGame similar to searchPlayer

/addGamePrequels for a game gameA, insert an array of game(s) as its prequels

/purchaseGame this endpoint allows the association between a player and a game. A field for player and
a field for the game needs to be provided. Display appropriate error messages

/addFriend personA adds personB as a friend

/multiplayerRequest should send a request from a player playing a game to another player playing
the same game to join him in a game. The multiplayer request is only successful if both players have
finished all the prequels of the game and have at least 1 friend in common

## Additional for Intermediate/Ninja Applicants


1. /recommendedFriends endpoint where a userID is taken as input and a list of recommended friends
is sent as a response

2. /recommendedGames endpoint that looks at games not played by a user and recommends new
games based on features of the games played previously or by his friends. (For the former you can
use tags for each game and recommend games based on tags)

3. /rank a GET request that fetches the player rankings (based on any algorithm of your choice)

4. Implement a new endpoint that adds an interesting feature
