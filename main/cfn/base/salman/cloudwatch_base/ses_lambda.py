import json
import boto3
def lambda_handler(event, context):
  sns = boto3.client('sns')
  message=(event['Records'][0]['Sns']['Message'])
  message_dict=json.loads(message)
  alarm_name=message_dict['AlarmName']
  alarm_description=message_dict['AlarmDescription']
  alarm_account=message_dict['AWSAccountId']
  region=message_dict['Region']
  metrics_name=message_dict['Trigger']['MetricName']
  service=message_dict['Trigger']['Namespace']
  instance_Id=message_dict['Trigger']['Dimensions'][0]['value']
  # Publish a simple message to the specified SNS topic
  # Create SES client
  # Create a new SES resource and specify a region.
  client = boto3.client('ses',region_name='us-east-1')
  SENDER = "xalman.ilyas@gmail.com"
  RECIPIENT = "xalman.ilyas@gmail.com"
  AWS_REGION = 'us-east-1'
  SUBJECT = str("EC2_Id::") + str(instance_Id) + " | " + str("AWS_ACCOUNT::" +str(alarm_account)) + " | " + str(metrics_name) + " >20"
  # The email body for recipients with non-HTML email clients.
  BODY_TEXT = (str(alarm_description) + "\n Metric name is  " + 
                str(metrics_name) + " \n In region " + 
               str(region)  + "\n Account Id is " + 
               str(alarm_account)
               
              )

  # The character encoding for the email.
  CHARSET = "UTF-8"
  response = client.send_email(
    Destination={
        'ToAddresses': [
            RECIPIENT,
        ],
    },
    Message={
        'Body': {
            'Text': {
                'Charset': CHARSET,
                'Data': BODY_TEXT,
            },
        },
        'Subject': {
            'Charset': CHARSET,
            'Data': SUBJECT,
        },
    },
    Source=SENDER
  )
  
