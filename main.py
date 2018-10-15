import requests
import boto3
from datetime import datetime, timedelta
import calendar

#hook for BAD button
#https://hooks.slack.com/services/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

#hook for GOOD button
#https://hooks.slack.com/services/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


def handler(event, context):

    dynamodb = boto3.client('dynamodb')
    
    #get current PST time
    todaysDayGoop = datetime.now() -  timedelta(hours=7)
    todaysDay = str(todaysDayGoop)
    
    dayOfWeek = calendar.day_name[todaysDayGoop.weekday()]
    
    #strip out all the other stuff and only save the date
    todaysDay = todaysDay[0:10]
    
    #grab the latest info from the table
    response = dynamodb.get_item(TableName='slackFoodBot', Key={'theKeyIGuess':{'S':'dog'}})
    item = response["Item"]
    lastGoodDate =  str(item['goodDate']['S'])
    lastBadDate =  str(item['badDate']['S'])
    goodTotal = int(item['foodGood']['N'])
    badTotal = int(item['foodBad']['N'])
    keyIndex = item['theKeyIGuess']['S']
    
 
    #if todays date doesnt match last known press of both good and bad button, then it's time to archive the yesterday
    if (todaysDay != lastBadDate) and (todaysDay != lastGoodDate):
        dynamodb.put_item(TableName='slackFoodBot', Item={'foodGood':{'N':str(goodTotal)},'foodBad':{'N':str(badTotal)}, 'goodDate':{'S':lastGoodDate}, 'badDate':{'S':lastBadDate}, 'theKeyIGuess':{'S':lastBadDate}})
    
    # #check the date of the last known press of the good button
    # #if the good button hasnt been pressed today, reset it to 1 (since it's just been pressed)
    # #also update the last known date of button press
    # if todaysDay != lastGoodDate:
        # goodTotal = 1
        # lastGoodDate = todaysDay
    # #if good button has already been pressed today, then add one to the count, but dont need to update the date
    # else:
        # goodTotal = 1 + goodTotal
		
		
    #check the date of the last known press of the bad button
    #if the bad button hasnt been pressed today, reset bad button presses to 1 (since it's just been pressed)
    #also update the last known date of button press
    if todaysDay != lastBadDate:
        badTotal = 1
        lastBadDate = todaysDay
        
    #if good button has already been pressed today, then add one to the count, but dont need to update the date
    else:
        badTotal = 1 + badTotal		
		
	
        
   
    
    #now update the table again
    dynamodb.put_item(TableName='slackFoodBot', Item={'foodGood':{'N':str(goodTotal)},'foodBad':{'N':str(badTotal)}, 'goodDate':{'S':lastGoodDate}, 'badDate':{'S':lastBadDate}, 'theKeyIGuess':{'S':'dog'}})

    

    #post to slack for GOOD
  #  requests.post('https://hooks.slack.com/services/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',json={"text" : dayOfWeek + ' ' + todaysDay + ' number of :heart: : ' + str(goodTotal) })
	
	#post to slack for BAD
    requests.post('https://hooks.slack.com/services/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',json={"text" : dayOfWeek + ' ' + todaysDay + ' number of :nauseated_face: : ' + str(badTotal) })