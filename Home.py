import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd

# CSV 파일에서 음식 데이터 읽어오기
food_data_df = pd.read_csv('전국통합식품영양성분정보(음식).csv', encoding='cp949')
food_data = food_data_df.set_index('식품명').T.to_dict()


# 표준체중 계산 함수
def calculate_weightav(height):
    result = height * height * 0.0021
    return result

st.image("logo.png", width=100) 


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
    st.session_state.height = height
weight = st.text_input("몸무게를 입력해주세요 (kg):")


reccal = 0
if height and weight:
    height = float(height)
    weight = float(weight)
    
    weightav = calculate_weightav(height)
    
    # 내용을 숨기거나 표시하는 박스 생성
    with st.expander("결과 보기"):
        st.markdown(f"**평균체중**: 키가 {height}cm인 경우 평균체중은: {weightav:.2f}kg 입니다.")
        
        # 권장칼로리 계산
        reccal = weightav * 30
        st.markdown(f"**권장칼로리**: {reccal:.2f}Kcal")
        
        # 체중감량 권장 칼로리 계산
        dietcal = reccal - 500
        st.markdown(f"**체중감량칼로리**: {dietcal:.2f}")




# 음식 검색 및 추가
def search_food(session_state, meal_type):
    food_name = st.text_input(f"{meal_type}에 먹은 음식:", key=f"{meal_type}_input")
    if food_name in food_data:
        st.write(f"음식 이름: {food_name}")
        for nutrient, value in food_data[food_name].items():
            st.write(f"{nutrient}: {value}")
        session_state.total_calories += food_data[food_name]["에너지(kcal)"]  # 수정된 부분
        session_state.food_list[meal_type].append(food_name)

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


# 추천 시스템
remaining_calories = reccal - st.session_state.total_calories  # 수정된 부분
recommended_foods = df[df["칼로리(kcal)"] <= remaining_calories]
st.write("추천 음식:")
st.write(recommended_foods)
