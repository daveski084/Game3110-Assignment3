import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')



# main
def lambda_handler(event, context):
    
    params = event['queryStringParameters']
    #params = {'name': 'Dave', 'win': 'true'}
    
    print(params)
    # get player ID
    UserID = params['name']
    
    if not VarifyUser(UserID):
      return {
        'statusCode': 200,
        'body': json.dumps('This player does not exist')
      }
      
    if 'wins' in params:
        UpdateWinScore(UserID)
        return {
        'statusCode': 200,
        'body': json.dumps('Player won')
        }
        
    if 'lost' in params:
        UpdateLostScore(UserID)
        return {
        'statusCode': 200,
        'body': json.dumps('Player lost')
    }  


def VarifyUser(UserName):
    table = dynamodb.Table('A3Players')
    
    desiredUser = table.get_item(
        Key = {
            'name': UserName
        }
    )
    
    return 'Item' in desiredUser

def UpdateWinScore(UserName):
    table = dynamodb.Table('A3Players')
    
    #Get desired information from DB
    desiredUser = table.get_item(
        Key = {
            'name': UserName
        }
    )
    
    #Get player info from DB
    playerInfo = desiredUser['Item']
    rankingScore = playerInfo['ranking']
    loss = playerInfo['losses']
    wins = playerInfo['wins']
    wins += 1
    rankingScore += 1

    #Update DB with new info
    table.put_item(
        Item = {
            'name': UserName,
            'ranking': rankingScore,
            'losses': loss,
            'wins': wins
        }
    )


def UpdateLostScore(UserName):
    table = dynamodb.Table('A3Players')
    
    #Get desired information from DB
    desiredUser = table.get_item(
        Key = {
            'name': UserName
        }
    )
    
    #Get player info from DB
    playerInfo = desiredUser['Item']
    rankingScore = playerInfo['ranking']
    loss = playerInfo['losses']
    wins = playerInfo['wins']
 
    loss += 1
    rankingScore -= 1
    
    #Update DB with new info
    table.put_item(
        Item = {
            'name': UserName,
            'ranking': rankingScore,
            'losses': loss,
            'wins': wins
        }
    )

