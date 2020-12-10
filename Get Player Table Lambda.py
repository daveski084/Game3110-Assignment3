import json
import datetime
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    
    table = dynamodb.Table('A3Players')
    
    TableScan = table.scan()
    
    return {
        'statusCode': 200,
        'body': json.dumps(TableScan, cls = JsonDecimal)
    }


class JsonDecimal(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(JsonDecimal, self).default(obj)