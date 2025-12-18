import json
import uuid
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Student-Details')

def lambda_handler(event, context):
    try:
        # Parse request body from API Gateway
        body = json.loads(event.get('body', '{}'))

        roll_number = str(body['roll_number'])
        student_name = body['student_name']
        student_class = str(body['student_class'])

        # Generate ID
        unique_id = str(uuid.uuid4())

        # Get AEST time
        utc_now = datetime.utcnow()
        aest_now = utc_now + timedelta(hours=10, minutes=30)
        aest_now_str = aest_now.strftime("%a, %d %b %Y %H:%M:%S +1030 AEST")

        # Store in DynamoDB
        table.put_item(
            Item={
                'ID': unique_id,
                'roll_number': roll_number,
                'student_name': student_name,
                'student_class': student_class,
                'created_at': aest_now_str
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({
                'message': 'Student added successfully',
                'id': unique_id
            })
        }

    except KeyError as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Missing field: {str(e)}'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
