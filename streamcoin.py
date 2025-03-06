import streamlit as st
import datetime
import requests
import pandas as pd

# 날짜 입력 받기
d = st.date_input("날짜를 선택 : ", datetime.date.today())

# 비트코인 1일 차트
st.write('비트코인 1일 차트')

ticker = 'KRW-BTC'
interval = 'minute60'  # 1시간 간격
to = datetime.datetime.combine(d + datetime.timedelta(days=1), datetime.time(0, 0))
to_str = to.strftime('%Y-%m-%d %H:%M:%S')  # API의 `to` 파라미터에 맞는 문자열로 변환
count = 24

# Upbit API에서 비트코인 가격 데이터 가져오기
url = "https://api.upbit.com/v1/candles/minutes/60"
params = {
    "market": ticker,
    "to": to_str,
    "count": count
}

# API 호출
response = requests.get(url, params=params)
data = response.json()

# 데이터 가공: 필요한 데이터만 추출
prices = []
for item in data:
    prices.append([item['timestamp'], item['opening_price'], item['high_price'], item['low_price'], item['trade_price']])

# Pandas DataFrame으로 변환
df = pd.DataFrame(prices, columns=["timestamp", "open", "high", "low", "close"])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # 타임스탬프를 datetime으로 변환

# 결과 차트 표시
st.line_chart(df.set_index("timestamp")["close"])  # 종가(close) 차트
