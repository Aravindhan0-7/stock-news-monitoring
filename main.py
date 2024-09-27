import requests
from twilio.rest import Client
STOCK = "STOCK_NAME"
COMPANY_NAME = "COMPANY_NAME"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY="API_KEY"
NEWS_API_KEY="API_KEY"

news_params={
    'apikey': NEWS_API_KEY,
    'qInTitle':COMPANY_NAME
}

stock_params={
    "function": "TIME_SERIES_DAILY",
    "apikey": STOCK_API_KEY,
    "symbol": STOCK
}
response=requests.get(STOCK_ENDPOINT,params=stock_params)
response.raise_for_status()
closing_price_of_yesterday=response.json()["Time Series (Daily)"]["2024-07-30"]["4. close"]
closing_price_of_day_before_yesterday=response.json()["Time Series (Daily)"]["2024-07-29"]["4. close"]
positive_difference=abs(float(closing_price_of_yesterday) - float(closing_price_of_day_before_yesterday))
percentage=(positive_difference/float(closing_price_of_yesterday))*100

if percentage>4:
    news_response=requests.get(NEWS_ENDPOINT,params=news_params)
    news_response.raise_for_status()
    articles=news_response.json()["articles"]
    three_articles=articles[:3]

    formatted_article=[f"Headlines:{article['title']}. \nBrief:{article['description']}" for article in three_articles]


    account_sid = 'ACCOUNT_SID'
    auth_token = 'AUTH_TOKEN'
    client = Client(account_sid, auth_token)
    for article in formatted_article:
        message = client.messages.create(
            from_='whatsapp:TWILLIO_NO.',
            body=article,
            to='whatsapp:RECEIVER_NO.' )
        print(message.status)
