import openai
import streamlit as st
from decouple import config
from PIL import Image
from components.layout import layout
import copy
import texts

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
    
if 'height' not in st.session_state or 'total_calories' not in st.session_state:
    st.text('홈에서 키와 몸무게 정보, 식단을 입력한 후 사용해 주세요.')
else:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"], avatar=avatar[msg["role"]]).write(msg["content"])


    if prompt := st.chat_input():
        openai.api_key = openai_api_key
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user", avatar=avatar['user']).write(prompt)
        messages = copy.deepcopy(st.session_state.messages)
        messages[-1]['content'] = texts.recipes() + texts.userinfo(int(st.session_state['height']), 
                                                                 int(st.session_state['total_calories'])) + texts.res + messages[-1]['content']
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant", avatar=avatar['assistant']).write(msg['content'])