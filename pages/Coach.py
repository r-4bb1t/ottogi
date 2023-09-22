import openai
import streamlit as st
from decouple import config
from PIL import Image

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
    st.session_state["messages"] = [{"role": "assistant", "content": "다이어트 조언을 해드릴게요!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=avatar[msg["role"]]).write(msg["content"])

if prompt := st.chat_input():
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=avatar['user']).write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant", avatar=avatar['assistant']).write(msg.content)