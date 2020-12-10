import json
import sys
import random
import time
import socket
import threading
from operator import itemgetter
import json
import requests
import logging



#Function to record time Log.
def LogTheTime():
    Logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    logging.info(Logtime)


HOST = ''
SERVERPORT = 12345
lost = []

GetPlayerInformationFromDB = requests.get('https://k7hoa04rmc.execute-api.us-east-2.amazonaws.com/default/GetPlayerInfoLambda')
UpdatePlayerInformationToDB = requests.get('https://aq9grh6k25.execute-api.us-east-2.amazonaws.com/default/UpdatePlayerInfoLambda')

gameServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gameServer.bind((HOST, SERVERPORT))

def Run():
    print("Server has started... Waiting..")

    while True:
        gameServer.listen(1)
        conn, addr = gameServer.accept()
        PlayerIDClient = conn.recv(1024).decode("ascii")
        databaseResponse = GetPlayerInformationFromDB
        PlayersFromDB = databaseResponse.json()['Items']

        #empty array to be the game room.
        gameRoom = []

        #get player data from the DB
        for data in PlayersFromDB:
            if data['name'] == PlayerIDClient:
                newPlayerRequest = data
                gameRoom.append(newPlayerRequest)

        if newPlayerRequest['wins'] <= 10:
            newPlayersRanking = 50
        else:
            #take the value of wins divided by lossed to make a "ranking"
            newPlayersRanking = newPlayerRequest["wins"] / newPlayerRequest['losses']   

        newPlayerID = newPlayerRequest['name']
        print("This player would like to start a new room:")
        LogTheTime()
        print(newPlayerRequest['name'])   
        seachCount = 0
        patience = 25

        # Keep searching for players until the game room has 3 appropriate players.
        while len(gameRoom) < 3:
            randomPerson = random.choice(PlayersFromDB)

            #calculate ranking 
            if  randomPerson['wins'] <= 10:
                randomPersonRanking = 50
            else:
                randomPersonRanking = randomPerson['wins'] / randomPerson['losses']
                
            if abs(newPlayersRanking - randomPersonRanking) <= 50 and randomPerson not in gameRoom:
                gameRoom.append(randomPerson)
            else:
                    sendError = "Unable to find match."
                    conn.sendall(sendError.encode())
                    print("Failed to find match")
                    break;

        print(len(gameRoom))
        if len(gameRoom) == 3:
            print("three people here")
            playerRoomData = { "FirstPlayer": gameRoom[0]['name'], "SecondPlayer": gameRoom[1]["name"], "ThirdPlayer": gameRoom[2]['name']}
            gameData = json.dumps(playerRoomData)
            conn.sendall(gameData.encode())
            print("end of server code")
           


if __name__ == '__main__':
    Run(); 