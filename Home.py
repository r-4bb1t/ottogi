import streamlit as st
from PIL import Image

st.markdown(
    """
    <style>
        .reportview-container {
            background-color: white;
            width: 437px;
            height: 883px;
            position: relative;
            top: -423px;
            left: -807px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

logo = Image.open("logo.png")
st.image(logo, width=96)

character = Image.open("ch2.png")
st.image(character, width=153)

st.markdown(
    """
    <div style="border: 1px solid black; padding: 16px 27px; margin: 10px; background-color: #f9f9f9; width: 345px; height: 250px; border-radius: 10px; gap: 15px;">
        <h2 style="font-family: Pretendard; font-size: 20px; font-weight: 400; line-height: 24px; letter-spacing: 0em; text-align: center;">안녕하세요, 가은님!</h2>
        <p style="font-family: Pretendard; font-size: 20px; font-weight: 700; line-height: 24px; letter-spacing: 0em; text-align: center;">오늘 섭취한 칼로리는</p>
        <p style="font-family: Binggrae; font-size: 20px; font-weight: 400; line-height: 27px; letter-spacing: 0em; text-align: center;color: red;"><strong>1480Kcal</strong>이에요.</p>
        <div style="display: flex; justify-content: space-between;">
            <div style="background: linear-gradient(0deg, #000000, #000000), linear-gradient(0deg, #DF2D32, #DF2D32); width: 68px; height: 25px; border-radius: 100px; border: 1px solid black; color: white;">탄</div>
            <div style="background: linear-gradient(0deg, #000000, #000000), linear-gradient(0deg, #FFA484, #FFA484); width: 68px; height: 25px; border-radius: 100px; border: 1px solid black;">단</div>
            <div style="background: linear-gradient(0deg, #000000, #000000), linear-gradient(0deg, #FFF100, #FFF100); width: 68px; height: 25px; border-radius: 100px; border: 1px solid black;">지</div>
            <div style="background: linear-gradient(0deg, #000000, #000000), linear-gradient(0deg, #A8C5D5, #A8C5D5); width: 68px; height: 25px; border-radius: 100px; border: 1px solid black;"></div>
        </div>
        <button style="background: rgba(223, 45, 50, 1); padding: 12px 24px; border: none; color: white; border-radius: 1000px; box-shadow: 2px 2px 0px 0px rgba(0, 0, 0, 1); margin-top: 10px;">식단 등록하기</button>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<h4 style='font-weight: bold;'>오늘 저녁은 간편하게 어때요?</h4>", unsafe_allow_html=True)
st.markdown("<p style='color: #888;'>맞춤 간편식 추천</p>", unsafe_allow_html=True)

foods = ["recipe_image1.png", "recipe_image2.png", "recipe_image3.png"]
st.image(foods, width=153)

st.markdown("<h4 style='font-weight: bold;'>요리를 해볼 까요?</h4>", unsafe_allow_html=True)
st.markdown("<p style='color: #888;'>맞춤 레시피 추천</p>", unsafe_allow_html=True)


recipe = ["recipe_image1.png", "recipe_image2.png", "recipe_image3.png"]
st.image(recipe, width=153)

st.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; background-color: #f1f1f1; padding: 10px; text-align: center;">
        <strong>홈</strong> | 코치 | 식단
    </div>
    """,
    unsafe_allow_html=True,
)
