import streamlit as st
import pandas as pd
from components.layout import layout 

layout()

food_data = {
    "칠햄 돈부리": {
        "칼로리(kcal)": 699.4,
        "총 지방(g)": 22.2,
        "포화지방(g)": 6.0,
        "콜레스테롤(mg)": 312.6,
        "나트륨(mg)": 1613.0,
        "탄수화물(g)": 94.1,
        "식이섬유(g)": 4.5,
        "단백질(g)": 33.0,
        "비타민A(ug)": 78.1,
        "비타민C(mg)": 17.9,
        "칼슘(mg)": 89.8,
        "필수 재료": "칠햄 오리지널 1캔(200g), 간장 4T(40g), 양파 1개, 설탕 2T(20g), 계란 2개, 물 100ml, 대파 1대(80g), 오뚜기밥 2개, 청양고추 1개(10g), 고소한 참기름 1T, 옛날 볶음참깨 약간"
    },
    "닭고기크림스튜": {
        "칼로리(kcal)": 573.24,
        "총 지방(g)": 29.02,
        "포화지방(g)": 4.97,
        "콜레스테롤(mg)": 161.55,
        "나트륨(mg)": 770.57,
        "탄수화물(g)": 37.61,
        "식이섬유(g)": 3.94,
        "단백질(g)": 41.08,
        "비타민A(ug)": 229.73,
        "비타민C(mg)": 55.42,
        "칼슘(mg)": 171.25,
        "필수 재료": "닭다리살 350g, 프레스코 카놀라유 2T(30g),마늘 2개(8g), 크림스프 40g, 양파 1개(200g), 우유 200ml, 당근 1/5개(30g), 물 200ml, 브로콜리 6조각(90g), 소금 약간, 양송이버섯 4개(80g), 순후추 약간"
    },
    "카레 치즈라면": {
        "칼로리(kcal)": 337.2,
        "총 지방(g)": 24.84,
        "포화지방(g)": 7.1,
        "콜레스테롤(mg)": 15,
        "나트륨(mg)": 2848.4,
        "탄수화물(g)": 102.96,
        "식이섬유(g)": 0,
        "단백질(g)": 20.54,
        "비타민A(ug RAE)": 56.73,
        "비타민C(mg)": 0,
        "칼슘(mg)": 236.8,
        "필수 재료": "진라면 매운맛 1개(분말스프 1T), 3분카레(순한맛) 1봉, 슬라이스치즈 1장(20g), 물 550ml, 파슬리가루 약간"
    }
}

# 표준체중 계산 함수
def calculate_weightav(height):
    result = height * height * 0.0021
    return result


# 예시 데이터
data = {
    "음식 이름": ["칰햄 돈부리", "닭고기크림스튜", "카레 치즈라면", "참치두부유부초밥"],
    "칼로리(kcal)": [699.4, 573.24, 337.2, 338.3],
    "탄수화물(g)": [94.1, 37.61, 102.96, 10.7],
    "단백질(g)": [33.0, 41.08, 20.54, 28.5],
    "지방(g)": [22.2, 29.02, 24.84, 20.1]
}
df = pd.DataFrame(data)


col1, col2 = st.columns([1, 6]) 
col1.image("ch2.png", width=110)  # width를 조정하여 아이콘 크기를 변경할 수 있습니다.

# 두 번째 컬럼에 제목 추가
col2.title("적정 칼로리 및 식단 관리")

# 키와 몸무게 입력
height = st.text_input("키를 입력해주세요 (cm):")
if height:
    st.session_state['height'] = height
weight = st.text_input("몸무게를 입력해주세요 (kg):")
if weight:
    st.session_state['weight'] = weight


reccal = 0
total_calories = 0

if height and weight:
    height = float(height)
    weight = float(weight)
    
    weightav = calculate_weightav(height)
    
    with st.expander("결과 보기"):  # beta_expander를 expander로 변경
        st.markdown(f"**평균체중**: 키가 {height}cm인 경우 평균체중은: {weightav:.2f}kg 입니다.")
        
        # 권장칼로리 계산
        reccal = weightav * 30
        st.markdown(f"**권장칼로리**: {reccal:.2f}Kcal")
        
        # 체중감량 권장 칼로리 계산
        dietcal = reccal - 500
        st.markdown(f"**체중감량칼로리**: {dietcal:.2f}")



def search_food(session_state, meal_type):
    food_name = st.text_input(f"{meal_type}에 먹은 음식:", key=f"{meal_type}_input_key")
    if food_name in food_data:
        st.write(f"음식 이름: {food_name}")
        for nutrient, value in food_data[food_name].items():
            st.write(f"{nutrient}: {value}")
        session_state.total_calories += food_data[food_name]["칼로리(kcal)"]
        session_state.food_list[meal_type].append(food_name)
        # 검색창 초기화를 위해 새로운 세션 상태 변수를 사용
        session_state[f"{meal_type}_reset"] = True

# 세션 상태 초기화
if not hasattr(st.session_state, 'food_list'):
    st.session_state.food_list = {"아침": [], "점심": [], "저녁": []}
if not hasattr(st.session_state, 'total_calories'):
    st.session_state.total_calories = 0

# 아침, 점심, 저녁 음식 검색 및 추가
for meal_type in ["아침", "점심", "저녁"]:
    clicked = st.button(f"+ {meal_type} 음식 검색 및 추가")
    if clicked or st.session_state.get(meal_type + "_expanded", False):
        with st.expander(f"{meal_type} 음식 검색 및 추가", expanded=True):
            search_food(st.session_state, meal_type)
            st.write(f"{meal_type} 음식 리스트: {', '.join(st.session_state.food_list[meal_type])}")
            
            # 음식 삭제 기능
            food_to_remove = st.selectbox(f"{meal_type}에서 삭제할 음식 선택:", st.session_state.food_list[meal_type], key=f"{meal_type}_remove")
            if st.button(f"{meal_type}에서 {food_to_remove} 삭제"):
                st.session_state.food_list[meal_type].remove(food_to_remove)
                st.session_state.total_calories -= food_data[food_to_remove]["칼로리(kcal)"]
        st.session_state[meal_type + "_expanded"] = True

st.write(f"오늘 섭취한 총 칼로리: {st.session_state.total_calories}Kcal")


# 추천 시스템
remaining_calories = reccal - st.session_state.total_calories  # 수정된 부분
recommended_foods = df[df["칼로리(kcal)"] <= remaining_calories]
st.write("추천 음식:")
st.write(recommended_foods)