import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


face = Image.open("face.png")
st.set_page_config(page_title='다이오뚜', page_icon=face, layout="centered", initial_sidebar_state="auto", menu_items=None)

# 그래프 생성
def display_graph():
    global carbs, fats, proteins  # 이 부분 추가

    # 데이터 수집
    calories = sum(st.session_state.get(meal + "_calories", 0) for meal in ["아침", "점심", "저녁"])
    carbs = sum(food_data[food]["탄수화물(g)"] for meal in ["아침", "점심", "저녁"] for food in st.session_state.get(meal + "_foods", []))
    fats = sum(food_data[food]["총 지방(g)"] for meal in ["아침", "점심", "저녁"] for food in st.session_state.get(meal + "_foods", []))
    proteins = sum(food_data[food]["단백질(g)"] for meal in ["아침", "점심", "저녁"] for food in st.session_state.get(meal + "_foods", []))
    
    nutrients = ["탄수화물(g)", "단백질(g)", "총 지방(g)"]
    intake = {nutrient: 0 for nutrient in nutrients}
    
    for meal_type in ["아침", "점심", "저녁"]:
        for food in st.session_state.food_list[meal_type]:
            for nutrient in nutrients:
                intake[nutrient] += food_data[food][nutrient]
    
    df = pd.DataFrame(intake, index=["Intake"])
    st.bar_chart(df.T)  # Transpose the dataframe for better visualization


# 섭취한 음식 리스트 나열
def display_food_list():
    all_foods = []
    for meal_type in ["아침", "점심", "저녁"]:
        all_foods.extend(st.session_state.food_list[meal_type])
    
    st.write("### 오늘 섭취한 음식:")
    for food in all_foods:
        st.write(f"* {food}  {food_data[food]['에너지(kcal)']}kcal")

# 표준체중 계산 함수
def calculate_weightav(height):
    result = height * height * 0.0021
    return result

# 음식 검색 및 추가
def search_food(session_state, meal_type):
    food_name = st.text_input(f"{meal_type}에 먹은 음식:", key=f"{meal_type}_input")
    if food_name in food_data and food_name not in session_state.food_list[meal_type]:
        st.write(f"음식 이름: {food_name}")
        for nutrient, value in food_data[food_name].items():
            st.write(f"{nutrient}: {value}")
        session_state.total_calories += food_data[food_name]["에너지(kcal)"]
        session_state.food_list[meal_type].append(food_name)
        
def recommend_foods():
    ottogi_data_df['distance'] = np.sqrt(
        (ottogi_data_df['칼로리(kcal)'] - remaining_calories)**2 +
        (ottogi_data_df['탄수화물(g)'] - remaining_carbs)**2 +
        (ottogi_data_df['단백질(g)'] - remaining_proteins)**2 +
        (ottogi_data_df['총 지방(g)'] - remaining_fats)**2
    )
    recommended = ottogi_data_df.nsmallest(5, 'distance')
    st.write("추천 음식:")
    
    for _, row in recommended.iterrows():
        # 이미지와 음식 이름을 링크로 표시
        st.markdown(f"""
        <div style="display: flex; align-items: center;">
            <img src="{row['이미지_링크']}" width="50" height="50" style="margin-right: 10px;">
            <a href="{row['음식_링크']}" target="_blank">{row['음식_이름']}</a>
        </div>
        """, unsafe_allow_html=True)


################################################

st.image("logo.png", width=100) 

dietcal = 0
carbo = 0
pro = 0
fat = 0
# CSV 파일에서 음식 데이터 읽어오기
food_data_df = pd.read_csv('전국통합식품영양성분정보(음식).csv', encoding='cp949')
food_data = food_data_df.set_index('음식_이름').T.to_dict()


col1, col2 = st.columns([1, 6]) 
col1.image("ch2.png", width=110)  # width를 조정하여 아이콘 크기를 변경할 수 있습니다.

# 두 번째 컬럼에 제목 추가
col2.title("적정 칼로리 및 식단 관리")

# 키와 몸무게 입력
height = st.text_input("키를 입력해주세요 (cm):")
weight = st.text_input("몸무게를 입력해주세요 (kg):")

reccal = 0
if height and weight:
    height = float(height)
    weight = float(weight)
    
    weightav = calculate_weightav(height)
    
    # 내용을 펼쳐진 상태로 보여주는 박스 생성
    with st.expander("결과 보기", expanded=True):  # expanded=True 추가
        st.markdown(f"**평균체중**: {weightav:.2f}kg")
        
        # 권장칼로리 계산
        reccal = weightav * 30
        st.markdown(f"**권장칼로리**: {reccal:.2f}Kcal")
        
        # 체중감량 권장 칼로리 계산
        dietcal = reccal - 500
        st.markdown(f"**체중감량칼로리**: {dietcal:.2f}Kcal")

        # 권장 탄단지 계산
        carbo = reccal * 0.5 / 4
        st.markdown(f"**권장 탄수화물**: {carbo:.2f}g")
        
        pro = reccal * 0.3 / 4
        st.markdown(f"**권장 단백질**: {pro:.2f}g")
        
        fat = reccal * 0.2 / 9
        st.markdown(f"**권장 지방**: {fat:.2f}g")




# 세션 상태 초기화
if not hasattr(st.session_state, 'food_list'):
    st.session_state.food_list = {"아침": [], "점심": [], "저녁": []}
if not hasattr(st.session_state, 'total_calories'):
    st.session_state.total_calories = 0


# 아침, 점심, 저녁 음식 검색 및 추가
for meal_type in ["아침", "점심", "저녁"]:
    with st.expander(f"{meal_type} 음식 검색 및 추가"):
        search_food(st.session_state, meal_type)
        st.write(f"{meal_type} 음식 리스트: {', '.join(st.session_state.food_list[meal_type])}")

st.write(f"오늘 섭취한 총 칼로리: {st.session_state.total_calories}Kcal")

#리스트
display_food_list()
#그래프
display_graph()


# 추천 시스템
remaining_calories = dietcal - st.session_state.total_calories
remaining_carbs = carbo - carbs
remaining_proteins = pro - proteins
remaining_fats = fat - fats

# CSV 파일에서 오뚜기 음식 데이터 읽어오기
ottogi_data_df = pd.read_csv('오뚜기.csv', encoding='utf-8')
ottogi_data = ottogi_data_df.set_index('음식_이름').T.to_dict()

# 섭취 가능한 칼로리와 가장 가까운 제품 5개 추천
recommend_foods()
