import time
import pyupbit
import datetime
import requests
import math

access = "access_key"
secret = "secret_key"
# myToken = "myToken"

# def post_message(token, channel, text):
#     """슬랙 메시지 전송"""
#     response = requests.post("https://slack.com/api/chat.postMessage",
#                              headers={"Authorization": "Bearer "+token},
#                              data={"channel": channel, "text": text}
#                              )
#     print(response)


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 시작 메세지 슬랙 전송
# post_message(myToken, "#coin", "autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BSV")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_buy_price = 100700
            target_sell_price = 104500
            current_price = get_current_price("KRW-BSV")
            if target_buy_price > current_price:
                krw = upbit.get_balance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-BSV", math.floor(krw*0.9995/target_buy_price)*target_buy_price)
                    # post_message(myToken, "#coin", "BSV Buy : "+str(buy_result))
            elif target_sell_price < current_price:
                BSV = upbit.get_balance("KRW-BSV")
                if BSV > 0:
                    sell_result = upbit.sell_market_order("KRW-BSV", 1)
                    # post_message(myToken, "#coin", "BSV Sell : " + str(sell_result))
                else:
                    pass
            else:
                pass
        time.sleep(1)
    except Exception as e:
        print(e)
        # post_message(myToken, "#crypto", e)
        time.sleep(1)