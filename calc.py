from sys import exit
from datetime import datetime
import json
from pathlib import Path


opperations = {
    "+": lambda x, y : x + y,
    "-": lambda x, y : x - y,
    "*": lambda x, y : x * y,
    "/": lambda x, y : x / y,
    "//": lambda x, y : x // y,
    "**": lambda x, y : x ** y,
    "%": lambda x, y : x % y,
}

while True:
    messege = input().lower()
    
    if messege == "exit":
        exit()

    filename = "user-math-story.json"
    numslots = []
    opslots = []
    numbers = '1234567890.'
    validation = f'{numbers}+-/*%'
    num = ''
    lastop = '+'
    
    for i, item in enumerate(messege):
        if item in validation:
            if item in numbers:
                if item == '.' and item in num:
                    continue
                if num == '':
                    opslots.append(lastop)
                num += item
                
            if item in opperations.keys():
                if messege[i] == messege[i-1] and item in "*/" and i > 0:
                    lastop = item * 2
                else:
                    lastop = item
                if num:
                    numslots.append(num)
                    num = ''
                    
            if i == len(messege) - 1 and num != "":
                numslots.append(num)
    
    try:
        if len(numslots) == 0:
            raise ValueError
        elif len(numslots) == 1:
            print(f'Ваше число: {float(numslots[0])}')
            continue
    except ValueError:
        print('Чисел не найдено')
        continue
    
           
    for i, nums in enumerate(numslots):
        if i == 0:
            if opslots[0] == "-":
                numslots[0] = float(f'-{nums}')
            else:
                numslots[0] = float(f'+{nums}')
            continue
        numslots[i] = float(nums)
    
    result = 0
    for op in enumerate(opslots):
        if i >= len(numslots):
            break

        try:
            result += opperations[opslots[i]](
                numslots[i-1],
                numslots[i]
            )
        except ZeroDivisionError:
            print('На ноль делить нельзя')
            continue
    
    dataSlot = dict()
    dataSlot['date_time'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    dataSlot['user_messege'] = messege
    dataSlot['messege_encoding'] = ''.join(f'{x,y}' for x, y in zip(opslots, numslots)).strip()
    dataSlot['result'] = result
    
    filePath = Path(__file__).parent / filename
    if filePath.exists():
        with open(filePath, mode="r", encoding='utf-8') as file:
            try:
                jsonData = json.load(file)
            except json.JSONDecodeError:
                jsonData = []
        
            jsonData.append(dataSlot)
        with open(filePath, mode="w", encoding='utf-8') as file:
            json.dump(jsonData, file, ensure_ascii=False, indent=2)
    else:   
        with open(filePath, mode='w', encoding='utf-8') as file:
            json.dump([dataSlot], file, ensure_ascii=False, indent=2)
            
    print(f'Результат выполнения: {result}')
    

