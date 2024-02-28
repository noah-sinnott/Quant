from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
load_dotenv()  

from state_manager import state_manager
from old.graphqlHandler import query_database
from newNews import new_news
from alpacaHandler import get_news

state_manager.enable_dev_mode()

def optimisation ():

    end_date = datetime.now()
    start_date = (datetime.now() - timedelta(days=5))

    all_news = []

    current_date = start_date

    while current_date <= end_date:
        current_day = current_date.strftime('%Y-%m-%d')
        news_for_day = get_news(start=current_day, end=(current_date + timedelta(days=1)).strftime('%Y-%m-%d'))
        print(news_for_day)
        all_news.extend(news_for_day)
        current_date += timedelta(days=1)
    
    print(len(all_news))

    return 
    oldest_event = f'''
            query getOldestEvent{{
                events(
                    limit: 1,
                    order_by: {{
                    event_time: asc
                    }}
                ) {{
                    event_time
                }}
            }}
        '''
    
    temp = query_database(oldest_event)

    first_event_date = temp['data']['events'][0]['event_time']


    current_date = datetime.fromisoformat(first_event_date)
    portfolio = {}
    balance = 0
    moneySpent= 0 
    buyingPower = 5

    while current_date <= datetime.now(pytz.utc):  # Use datetime.now with UTC timezone

        current_date_str = current_date.isoformat()

        query = f'''
            query get_days_events {{
            events(
                where: {{
                event_time: {{
                _gte: "{current_date_str}",
                 _lt: "{(current_date + timedelta(days=1)).isoformat()}"
                }}
                }},
                order_by: {{
                event_time: asc
                }}
            ) {{
                event_id
                event_type
                event_time

                symbols
                summary
                id
                T
                url
                source
                author
                updated_at
                created_at
                headline
            }}
        }}
        '''

        response = query_database(query)
        
        for event in response['data']['events']:

            if(event['event_type'] == "alpaca_news"):
                new_news(event)
                
            # if can find a ai evaluation of event use that, otherwise get new one

            # compare event ai score to whatever current evaluation standers are

            # get value of stock at that time

            # if adding then add to portfolio {ticker: stock quantity} and decrease balance and increase money spent

            # if selling then remove from portfolio, and add back to balance

        current_date += timedelta(days=1)

    # (((balance / money spent) - money spent) * 100) gives % profit

    # add to graphql the settings used and the result




optimisation()