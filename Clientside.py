import json
import socket
import random
import ast
import datetime
import requests
import time
import logging

SERVERADDRESS = '3.139.99.41'
SERVERPORT = 12345

#API to get and update dynamoDB

GetPlayerInformationFromDB = requests.get('https://k7hoa04rmc.execute-api.us-east-2.amazonaws.com/default/GetPlayerInfoLambda')
UpdatePlayerInformationToDB = requests.get('https://aq9grh6k25.execute-api.us-east-2.amazonaws.com/default/UpdatePlayerInfoLambda')

#Function to record time Log because it is called many times.
def LogTheTime():
    Logtime = time.strftime("%Y-%m-%d%H:%M:%S", time.gmtime())
    logging.info(Logtime)

# a list to store all players from Table.
ListofIDs = ['Ashley', 'Catt', 'Dave', 'Isaac','Ivan', 'Joss', 'Russell', 'Tanya', 'Tom', 'Trump']
Game = []

def MatchMake():
    #begin logging information for debugging and records.
    logging.basicConfig(filename='Gamelog.log', level=logging.INFO)
    logging.info("Starting Game")
    LogTheTime()

     #get a random player from the list.
    currID = random.choice(ListofIDs)

    #start a connection.
    print("Starting Connection...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVERADDRESS, SERVERPORT))
    print("Connected Successfully to the server. ")
    print("Client ID: " + currID)
    print("Game start time:")


    #variable to hold information to send.
    sock.send(currID.encode())

    response = sock.recv(1024)
    responseDecode = response.decode()

    if responseDecode == 'Unable to find match.':
        print(responseDecode)
        LogTheTime()
        logging.info(responseDecode)
        logging.info('Unable to find match. End of search.')
    else:
        #if the response code isn't 'unable to find match, parse player data.
        player1 = json.loads(responseDecode)['FirstPlayer']
        player2 = json.loads(responseDecode)['SecondPlayer']
        player3 = json.loads(responseDecode)['ThirdPlayer']    
        databaseResponse = GetPlayerInformationFromDB
        PlayersFromDB = databaseResponse.json()['Items']

        for data in PlayersFromDB:
            if data['name'] == player1:
                Game.append(data)
            if data['name'] == player2:
                Game.append(data)
            if data['name'] == player3:
                Game.append(data)
            else:
             print("This player is not part of the game.")
        print("Match Players are: ")   

        for players in Game:
          print(players)
          logging.info(players['name'] + " Connected at " + datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
          logging.info("Their ranking is: " + str(players['ranking']))
          logging.info(players)

    
    # Simulate a game.
     #store losing playre data.
    playersLost = []
    #Randomly choose a player to be a Winner.
    winner = random.choice(Game)

    for data in Game:

        #Update info for the "winner".
        if data['name'] == winner['name']:
            requests.get('https://aq9grh6k25.execute-api.us-east-2.amazonaws.com/default/UpdatePlayerInfoLambda',
             params = {'name': winner['name'], 'wins':'true'})
            print(data['name'] + " Wins!")
            logging.info('Winner is: ')
            logging.info(winner['name'])
        
           
            #Update the info for losers        
        else:
            requests.get('https://aq9grh6k25.execute-api.us-east-2.amazonaws.com/default/UpdatePlayerInfoLambda',
            params={'name': data['name'],'lost':'true'})
            #add the losers to the array.
            playersLost.append(data)
            print(data['name'] + " lost ")
            
    print("Winner is " + winner['name'])
   
    #Store the results.
    afterGame = []

    #Get the player data again from AWS.
    afterGameData = requests.get('https://k7hoa04rmc.execute-api.us-east-2.amazonaws.com/default/GetPlayerInfoLambda')
    afterGameJson = afterGameData.json()['Items']


    for data in afterGameJson:
        if data['name'] == player1:
            afterGame.append(data)
        if data['name'] == player2:
            afterGame.append(data)
        if data['name'] == player3:
            afterGame.append(data)

    logging.info("results")

    for players in afterGame:
        logging.info(players)
        print(players)


    #databaseResponse1 = GetPlayerInformationFromDB
   # PlayersFromDB1 = databaseResponse1.json()['Items']  
    
    #results = [] 

   # for data in PlayersFromDB1:
     #   if data['name'] == player1:
           # results.append(data)
      #  if data['name'] == player2:
          #  results.append(data)
      #  if data['name'] == player3:
      #      results.append(data)
    
    #for players in results: 
    #    print(players)

    #for players in PlayersFromDB1:
    #    print(players['name'])
    #   print("Wins: ")
    #    print(players['wins'])
    #    print("losses")
    #    print(players['losses'])

    # log to log
    LogTheTime()  
    logging.info('Simulation ended')
    
    # end the simulator
    print('Simulation Over')
    sock.close()                    



if __name__ == '__main__':
    GamesToPlay = input("How many matches would you like to simulate?")
    for i in range(int(GamesToPlay)):
        MatchMake()