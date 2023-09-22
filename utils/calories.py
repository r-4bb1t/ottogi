import math

# 표준체중(BMI)
def calculate_bmi(height):
    result = height * height * 0.0021
    return result

# 권장칼로리
def calculate_cal(height):
    return math.floor(calculate_bmi(height) * 30 - 50)

def calculate_nut(height):
    return '탄수화물 {car}g, 지방 {fat}g, 단백질 {protein}g'.format(car=calculate_cal(height)*(5/13)/4, fat=calculate_cal(height)*(2/13)/4, protein=calculate_cal(height)*(5/13)/9)