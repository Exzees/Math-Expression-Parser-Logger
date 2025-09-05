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

def math_parser(messege:str) -> float:
    
    filename = "user-math-story.json"
    numslots = []
    opslots = []
    numbers = '1234567890.'
    num = ''
    lastop = '+'
    
    for i, item in enumerate(messege):
        if item in numbers + ''.join(opperations.keys()):
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
            return numslots[0]
    except ValueError:
        print('numslots is empty')
        return
    
           
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
            print(ZeroDivisionError)
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
            
    return result
    

