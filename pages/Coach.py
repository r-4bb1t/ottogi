import openai
import streamlit as st
from decouple import config
from PIL import Image
from components.layout import layout
from utils.calories import calculate_cal
import copy

layout()

openai_api_key = config('OPENAI_KEY')

mayo = Image.open('ch1.png')
ttogi = Image.open('ch2.png')

avatar={"assistant": mayo, "user": ttogi}

col1, mid, col2 = st.columns([1,2,20])
with col1:
    st.image(mayo, width=100)
with col2:
    st.title("다이어트 코치 마요")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "레시피 추천은 마요에게 맡겨주세요!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=avatar[msg["role"]]).write(msg["content"])

recipes =\
'''url: https://ottogi.okitchen.co.kr/category/detail.asp?idx=1379
음식 이름: 칰햄 돈부리
레시피 영양성분:
칼로리(kcal)   699.4
총 지방(g)   22.2
포화지방(g)   6.0
콜레스테롤(mg)   312.6
나트륨(mg)   1613.0
탄수화물(g)   94.1
식이섬유(g)   4.5
단백질(g)   33.0
비타민A(ug)   78.1
비타민C(mg)   17.9
칼슘(mg)   89.8
필수 재료
: 칰햄 오리지널 1캔(200g), 간장 4T(40g), 양파 1개, 설탕 2T(20g), 계란 2개, 물 100ml, 대파 1대(80g), 오뚜기밥 2개, 청양고추 1개(10g), 고소한 참기름 1T, 옛날 볶음참깨 약간
---------------------------------------
url: https://ottogi.okitchen.co.kr/category/detail.asp?idx=1377
음식 이름: 닭고기크림스튜
레시피 영양성분:
칼로리(kcal)   573.24
총 지방(g)   29.02
포화지방(g)   4.97
콜레스테롤(mg)   161.55
나트륨(mg)   770.57
탄수화물(g)   37.61
식이섬유(g)   3.94
단백질(g)   41.08
비타민A(ug)   229.73
비타민C(mg)   55.42
칼슘(mg)   171.25
필수 재료
: 닭다리살 350g, 프레스코 카놀라유 2T(30g),마늘 2개(8g), 크림스프 40g, 양파 1개(200g), 우유 200ml, 당근 1/5개(30g), 물 200ml, 브로콜리 6조각(90g), 소금 약간, 양송이버섯 4개(80g), 순후추 약간
---------------------------------------
url: https://ottogi.okitchen.co.kr/category/detail.asp?idx=1376
음식 이름: 카레 치즈라면
레시피 영양성분:
칼로리(kcal)   337.2
총 지방(g)   24.84
포화지방(g)   7.1
콜레스테롤(mg)   15
나트륨(mg)   2848.4
탄수화물(g)   102.96
식이섬유(g)   0
단백질(g)   20.54
비타민A(ug RAE)   56.73
비타민C(mg)   0
칼슘(mg)   236.8
필수 재료
: 진라면 매운맛 1개(분말스프 1T), 3분카레(순한맛) 1봉, 슬라이스치즈 1장(20g), 물 550ml, 파슬리가루 약간
---------------------------------------
url: https://ottogi.okitchen.co.kr/category/detail.asp?idx=1355
음식 이름: 참치두부유부초밥
레시피 영양성분:
칼로리(kcal)   338.3
총 지방(g)   20.1
포화지방(g)   4.1
콜레스테롤(mg)   41.3
나트륨(mg)   636.7
탄수화물(g)   10.7
식이섬유(g)   5.6
단백질(g)   28.5
비타민A(ug RAE)   0.1
비타민C(mg)   0
칼슘(mg)   129.4
필수 재료
: 초밥용 유부 6장, 두부 1/3모 100g, 파프리카 1/3개, 브로콜리 1/8개, 오뚜기 참치 ½캔(75g), 오뚜기 고소한 소이마요 1T
'''

userinfo = \
'''너는 다이어트 코치 "마요"이다. 유저에게 어린아이같은 귀여운 말투를 사용해야 한다.
내가 입력한 나의 정보에 맞게, 위 레시피 중 적절한 레시피를 추천하고 조언해야 한다.
나의 키와 체중에 맞는 권장 칼로리는 {cal}kcal이며, 오늘 섭취한 칼로리는 {today}kcal이다.
'''.format(cal=calculate_cal(155), today=1000)

res = '''JSON 답변 형식
{
  "answer": "너의 답변",
  "url": ["레시피의 url 1", "레시피의 url 2"],
}
'''


if prompt := st.chat_input():
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=avatar['user']).write(prompt)
    messages = copy.deepcopy(st.session_state.messages)
    messages[-1]['content'] = recipes + userinfo + res + messages[-1]['content']
    print(messages)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant", avatar=avatar['assistant']).write(msg.content)