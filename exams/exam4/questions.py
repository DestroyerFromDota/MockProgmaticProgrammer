import random

def generate_question(level_config):
    """Генерирует математический вопрос на основе конфига уровня"""
    operation = random.choice(level_config['operations'])
    max_num = level_config['max_number']
    
    if operation == '+':
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        question = f"{a} + {b}"
        answer = a + b
        
    elif operation == '-':
        a = random.randint(1, max_num)
        b = random.randint(1, a)  # чтобы не было отрицательных
        question = f"{a} - {b}"
        answer = a - b
        
    elif operation == '*':
        # для сложного уровня числа поменьше, чтобы не было слишком сложно
        if max_num > 30:
            a = random.randint(1, 12)
            b = random.randint(1, 12)
        else:
            a = random.randint(1, max_num // 2)
            b = random.randint(1, max_num // 2)
        question = f"{a} * {b}"
        answer = a * b
        
    elif operation == '/':
        # деление без остатка
        b = random.randint(2, 12)
        answer = random.randint(1, max_num // b)
        a = b * answer
        question = f"{a} / {b}"
    
    return question, answer