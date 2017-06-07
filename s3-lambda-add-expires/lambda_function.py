from datetime import datetime, timedelta
import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')

def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])


        expires = datetime.now() + timedelta(days=365)
        print('Expires: ' + str(expires))
        contentType = response['ContentType'] if 'ContentType' in response else 'application/octet-stream'
        cacheControl = response['CacheControl'] if 'CacheControl' in response else ''
        copySource = bucket + '/' + key

        print('replace object.')
        print('bucket : ' + bucket)
        print('CopySource : ' + copySource)

        response = s3.copy_object(
            Bucket=bucket,
            CopySource=copySource,
            Key=key,
            ContentType=contentType,
            Expires=expires,
            CacheControl=cacheControl,
            MetadataDirective='REPLACE'
        )
        print('replace done! Expires : ' + json.dumps(response['CopyObjectResult'], indent=2, default=datetime_handler))
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
