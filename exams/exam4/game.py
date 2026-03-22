import random
from config import LEVELS
from questions import generate_question

class MathGame:
    def __init__(self):
        self.score = 0
        self.current_level = None
        self.questions_count = 0
        self.questions_answered = 0
    
    def show_welcome(self):
        """Показывает приветствие и правила"""
        print("\n" + "="*50)
        print(" " * 15 + "MATHEMATICAL GAME")
        print("="*50)
        print("\nWelcome!")
        print("You will be asked mathematical questions.")
        print("Enter answers as numbers.")
        print("To exit, enter 'q' at any time.\n")
    
    def select_level(self):
        """Выбор уровня сложности"""
        print("\nAvailable difficulty levels:")
        print("-" * 40)
        
        levels_list = list(LEVELS.keys())
        for i, level_key in enumerate(levels_list, 1):
            level = LEVELS[level_key]
            print(f"{i}. {level['name']} - {level['description']}")
            print(f"   Questions: {level['questions_count']}\n")
        
        while True:
            try:
                choice = input("\nSelect level (1-{}): ".format(len(levels_list)))
                if choice.lower() == 'q':
                    return None
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(levels_list):
                    level_key = levels_list[choice_idx]
                    self.current_level = LEVELS[level_key]
                    self.questions_count = self.current_level['questions_count']
                    print(f"\nLevel selected: {self.current_level['name']}")
                    print(f"You will be asked {self.questions_count} questions.\n")
                    return True
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")
    
    def ask_question(self):
        """Задает один вопрос"""
        question, correct_answer = generate_question(self.current_level)
        
        while True:
            user_input = input(f"\nQuestion {self.questions_answered + 1}: {question} = ")
            
            if user_input.lower() == 'q':
                return 'quit'
            
            try:
                user_answer = float(user_input)
                if user_answer.is_integer():
                    user_answer = int(user_answer)
                
                if user_answer == correct_answer:
                    print("[CORRECT]")
                    self.score += 1
                    return 'correct'
                else:
                    print(f"[INCORRECT] Correct answer: {correct_answer}")
                    return 'incorrect'
            except ValueError:
                print("Please enter a number.")
    
    def play(self):
        """Основной игровой цикл"""
        self.show_welcome()
        
        while True:
            if not self.select_level():
                print("\nGame terminated. Goodbye!")
                break
            
            self.score = 0
            self.questions_answered = 0
            
            print("Starting game!")
            print("="*40)
            
            while self.questions_answered < self.questions_count:
                result = self.ask_question()
                
                if result == 'quit':
                    print("\nGame interrupted by user.")
                    return
                
                self.questions_answered += 1
                print(f"Progress: {self.questions_answered}/{self.questions_count}")
            
            self.show_result()
            
            if not self.play_again():
                break
    
    def show_result(self):
        """Показывает результат игры"""
        percentage = (self.score / self.questions_count) * 100
        
        print("\n" + "="*40)
        print(" " * 12 + "GAME RESULTS")
        print("="*40)
        print(f"Level: {self.current_level['name']}")
        print(f"Correct answers: {self.score} out of {self.questions_count}")
        print(f"Result: {percentage:.1f}%")
        
        if percentage == 100:
            print("Evaluation: Excellent - All answers correct!")
        elif percentage >= 80:
            print("Evaluation: Good - Well done!")
        elif percentage >= 60:
            print("Evaluation: Satisfactory - Good result")
        elif percentage >= 40:
            print("Evaluation: Below average - More practice needed")
        else:
            print("Evaluation: Poor - Significant improvement needed")
    
    def play_again(self):
        """Спрашивает, хочет ли игрок сыграть еще"""
        while True:
            choice = input("\nPlay again? (yes/no): ").lower()
            if choice in ['yes', 'y']:
                return True
            elif choice in ['no', 'n']:
                print("\nThank you for playing! Goodbye!")
                return False
            else:
                print("Please answer 'yes' or 'no'.")

def main():
    """Главная функция"""
    game = MathGame()
    game.play()

if __name__ == "__main__":
    main()