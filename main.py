import requests
import boto3
from datetime import datetime, timedelta


def handler(event, context):

    dynamodb = boto3.client('dynamodb')
    
    #get current PST time
    todaysDay = str(datetime.now() -  timedelta(hours=7))
    
    #strip out all the other stuff and only save the day
    todaysDay = todaysDay[8:10]
    
    #grab the latest info from the table
    response = dynamodb.get_item(TableName='slackFoodBot', Key={'theKeyIGuess':{'S':'hello'}})
    item = response["Item"]
    lastGoodDate =  str(item['goodDate']['S'])
    lastBadDate =  str(item['badDate']['S'])
    goodTotal = int(item['foodGood']['N'])
    badTotal = int(item['foodBad']['N'])
    
    
    
     #TESTING ONLY DELETE ME    
   # lastGoodDate = 13
    
    #check the date of the last known press of the good button
    #if the good button hasnt been pressed today, reset it to 1 (since it's just been pressed)
    #also update the last known date of button press
    if todaysDay != lastGoodDate:
        goodTotal = 1
        lastGoodDate = todaysDay
    #if good button has already been pressed today, then add one to the count, but dont need to update the date
    else:
        goodTotal = 1 + goodTotal
        
   
    
    #now update the table again
    dynamodb.put_item(TableName='slackFoodBot', Item={'foodGood':{'N':str(goodTotal)},'foodBad':{'N':str(badTotal)}, 'goodDate':{'S':lastGoodDate}, 'badDate':{'S':lastBadDate}, 'theKeyIGuess':{'S':'hello'}})

    

    
    requests.post('https://hooks.slack.com/services/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',json={"text" : ':heart: : ' + str(goodTotal) })