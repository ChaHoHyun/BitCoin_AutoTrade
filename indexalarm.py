import requests
import datetime as dt
import FinanceDataReader as fdr
import pandas as pd
import sys

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer "+token},
                             data={"channel": channel, "text": text}
                             )
    print(response)

def test_function(myToken):
    data = fdr.DataReader(['T10Y2Y', 'T10Y3M'],
                          data_source="fred", start='2022').reset_index()
    t10y2y = data.iloc[-1]["T10Y2Y"]
    t10y3m = data.iloc[-1]["T10Y3M"]
    date = data.iloc[-1]["DATE"].strftime('%y.%m/%d')
    if (t10y2y < 0) and (t10y3m < 0):
        post_message(myToken, "#flex", "!!!!!!WARNING!!!!!!")
    else:
        pass
    # Slack에 보낼 메세지
    post_message(myToken, "#flex", "Date : " + date + "\n" +
                 " - T10Y2Y : "+str(t10y2y)+"\n"+" - T10Y3M : "+str(t10y3m))

# 실행하기
def execute(myToken):
    post_message(myToken, "#flex", "start!")
    test_function(myToken)
