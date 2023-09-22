import math

# 표준체중(BMI)
def calculate_bmi(height):
    result = height * height * 0.0021
    return math.floor(result)

# 권장칼로리
def calculate_cal(height):
    return calculate_bmi(height) * 30 - 50