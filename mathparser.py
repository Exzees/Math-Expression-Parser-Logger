from datetime import datetime
import json
from pathlib import Path


operations  = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "//": lambda x, y: x // y,
    "pow": lambda x, y: x ** y,
    "%": lambda x, y: x % y,
}

def math_parser(message:str, precision: int = 4,
                json_log:bool = True,
                return_encoding:bool = False,
                file_path:Path = Path(__file__).parent) -> float:
    
    filename = "user-math-story.json"
    number_slots = []
    operator_slots = []
    NUMBERS_CHARS = '1234567890.'
    OPERATIONS_CHARS = ''.join(operations .keys())
    OPERATIONS_PRIORITY = {
        1 : 'pow',
        2 : '*//%',
        3 : '+-'
    }
        
    num = ''
    last_operator = '+'
    
    for i, item in enumerate(message):
        if item in NUMBERS_CHARS  + OPERATIONS_CHARS:
            if item in NUMBERS_CHARS :
                if item == '.' and item in num:
                    continue
                if num == '':
                    operator_slots.append(last_operator)
                num += item
                
            if item in OPERATIONS_CHARS:
                if message[i] == message[i-1] and item in "*/" and i > 0:
                    last_operator = item * 2
                else:
                    last_operator = item
                if num:
                    number_slots.append(num)
                    num = ''
                    
            if i == len(message) - 1 and num != "":
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
                operator_slots[0] = '+'
            continue
        number_slots[i] = float(nums)
    
    __empty = ['' for x in range(len(number_slots))]
    __form = ''.join(f'{x,y,z}' for x, y, z in zip(__empty, operator_slots, number_slots))
    encoding = ''.join([x for x in __form if x not in "('),"]).strip()
    if return_encoding:
        return encoding
    del operator_slots[0]
      
    for i, item in enumerate(operator_slots):
        if item == '**':
            operator_slots[i] = 'pow'
      
    debug = []
    for priority in OPERATIONS_PRIORITY.keys():
        for i, op in enumerate(operator_slots.copy()):            
            if op in OPERATIONS_PRIORITY[priority]:
                try:
                    number_slots[i + 1] = operations [operator_slots[i]](
                        number_slots[i],
                        number_slots[i + 1]
                    )
                    debug.append(i)
                    
                except IndexError:
                    result += number_slots[0]   
                except ZeroDivisionError:
                    print(ZeroDivisionError) 
                                    
        debug.reverse()
        if debug:
            for idx in debug:
                del number_slots[idx]
                del operator_slots[idx]
            debug.clear()
    result = number_slots[len(number_slots) - 1] 
                    
    if json_log:
        data_slot = dict()
        data_slot['date_time'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        data_slot['user_message'] = message
        data_slot['message_encoding'] = encoding
        data_slot['result'] = result
        
        file_path =  file_path / filename
        if file_path.exists():
            with open(file_path, mode="r", encoding='utf-8') as file:
                try:
                    jsonData = json.load(file)
                except json.JSONDecodeError:
                    jsonData = []
            
                jsonData.append(data_slot)
            with open(file_path, mode="w", encoding='utf-8') as file:
                json.dump(jsonData, file, ensure_ascii=False, indent=2)
        else:   
            with open(file_path, mode='w', encoding='utf-8') as file:
                json.dump([data_slot], file, ensure_ascii=False, indent=2)
            
    if precision:
        return round(result,precision )
    
    return result
