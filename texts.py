from utils.calories import calculate_cal, calculate_nut
import csv
import random

def get_header(file_name):
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        return rows[0]

def random_rows_from_csv(file_name, num_rows):
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if len(rows) > 1:
            random_rows = random.sample(rows[1:], num_rows)
            return random_rows
    return None

def random_rows_to_string(file_name):
    headers = get_header(file_name)
    random_rows = random_rows_from_csv(file_name, 3)
    if random_rows:
        res = ''
        for row in random_rows:
            res += '\n'.join([(headers[i] + ": " + field) for i, field in enumerate(row)])
            res += '\n----\n'
        return res
    else:
        return ""

def recipes():
  random_recipes = random_rows_to_string('sample.csv')
  print(random_recipes)
  return random_recipes

def userinfo(height, today):
  return \
'''너는 다이어트 코치 "마요"이다. 유저에게 어린아이같은 귀여운 말투를 사용해야 한다.
내가 입력한 나의 필요 칼로리를 언급하며 그에 맞게 레시피 중 가장 적절한 레시피를 추천하고 레시피를 추천한 이유, 자세한 설명과 함께 조언해야 한다.
나의 키와 체중에 맞는 권장 칼로리는 {cal}kcal이며, 필요한 영양 정보는 {nut} 오늘 섭취한 칼로리는 {today}kcal이다.
'''.format(cal=calculate_cal(height), nut=calculate_nut(height), today=today)

res = '''마크다운 형식으로 답변하되, 각 레시피의 URL과 이미지를 표시하라.'''