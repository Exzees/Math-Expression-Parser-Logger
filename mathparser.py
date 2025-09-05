from datetime import datetime
import json
from pathlib import Path


opperations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "//": lambda x, y: x // y,
    "**": lambda x, y: x ** y,
    "%": lambda x, y: x % y,
}

def math_parser(messege:str, json_log:bool = True,
                filePath:Path = Path(__file__).parent) -> float:
    
    filename = "user-math-story.json"
    number_slots = []
    operator_slots = []
    NUMBERS_CHARS  = '1234567890.'
    OPERATIONS_CHARS = ''.join(opperations.keys())
    num = ''
    last_operator = '+'
    
    for i, item in enumerate(messege):
        if item in NUMBERS_CHARS  + OPERATIONS_CHARS:
            if item in NUMBERS_CHARS :
                if item == '.' and item in num:
                    continue
                if num == '':
                    operator_slots.append(last_operator)
                num += item
                
            if item in OPERATIONS_CHARS:
                if messege[i] == messege[i-1] and item in "*/" and i > 0:
                    last_operator = item * 2
                else:
                    last_operator = item
                if num:
                    number_slots.append(num)
                    num = ''
                    
            if i == len(messege) - 1 and num != "":
                number_slots.append(num)
    
    try:
        if len(number_slots) == 0:
            raise ValueError
        elif len(number_slots) == 1:
            return number_slots[0]
    except ValueError:
        print('number_slots is empty')
        return
    
           
    for i, nums in enumerate(number_slots):
        if i == 0:
            if operator_slots[0] == "-":
                number_slots[0] = float(f'-{nums}')
            else:
                number_slots[0] = float(f'+{nums}')
            continue
        number_slots[i] = float(nums)
    
    result = 0
    for i, op in enumerate(operator_slots):
        if i > len(number_slots):
            break
        
        if op in '/*%':
            try:
                result += opperations[operator_slots[i]](
                    number_slots[i-1],
                    number_slots[i]
                )
            except ZeroDivisionError:
                print(ZeroDivisionError)
                continue
            
    for i, op in enumerate(operator_slots):
        if i > len(number_slots):
            break
        
        if op in '+-':
            try:
                result += opperations[operator_slots[i]](
                    number_slots[i-1],
                    number_slots[i]
                )
            except ZeroDivisionError:
                print(ZeroDivisionError)
                continue
            
    if json_log:
        data_slot = dict()
        data_slot['date_time'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        data_slot['user_messege'] = messege
        data_slot['messege_encoding'] = ''.join(f'{x,y}' for x, y in zip(operator_slots, number_slots)).strip()
        data_slot['result'] = result
        
        filePath =  filePath / filename
        if filePath.exists():
            with open(filePath, mode="r", encoding='utf-8') as file:
                try:
                    jsonData = json.load(file)
                except json.JSONDecodeError:
                    jsonData = []
            
                jsonData.append(data_slot)
            with open(filePath, mode="w", encoding='utf-8') as file:
                json.dump(jsonData, file, ensure_ascii=False, indent=2)
        else:   
            with open(filePath, mode='w', encoding='utf-8') as file:
                json.dump([data_slot], file, ensure_ascii=False, indent=2)
            
    return result