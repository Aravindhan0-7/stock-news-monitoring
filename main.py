import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY="JRHJS4OXPIN47BWP"
NEWS_API_KEY="97c0717b81ca49f48868ca0a88891dcf"

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


    account_sid = 'AC72496d0c0dd0e7cba918dc70a572053f'
    auth_token = '5a31def6c358aee222b45c90133f06f7'
    client = Client(account_sid, auth_token)
    for article in formatted_article:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=article,
            to='whatsapp:+918124174607' )
        print(message.status)
