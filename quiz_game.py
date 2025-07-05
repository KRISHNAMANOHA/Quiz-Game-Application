import json
import os

class QuizGame:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.current_question = 0
        self.load_questions()
    
    def load_questions(self):
        """Load questions from a JSON file or use default questions"""
        try:
            if os.path.exists('questions.json'):
                with open('questions.json', 'r') as f:
                    self.questions = json.load(f)
            else:
                self.questions = self.get_default_questions()
                with open('questions.json', 'w') as f:
                    json.dump(self.questions, f, indent=4)
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.questions = self.get_default_questions()
    
    def get_default_questions(self):
        """Return a list of default questions"""
        return [
            {
                "type": "multiple_choice",
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "answer": "Paris",
                "points": 1
            },
            {
                "type": "true_false",
                "question": "The Earth is flat.",
                "answer": False,
                "points": 1
            },
            {
                "type": "multi_select",
                "question": "Which of these are programming languages?",
                "options": ["Python", "HTML", "Java", "CSS"],
                "answer": ["Python", "Java"],
                "points": 2
            },
            {
                "type": "fill_blank",
                "question": "The process of finding and fixing errors in code is called ______.",
                "answer": "debugging",
                "points": 1
            },
            {
                "type": "short_answer",
                "question": "What does 'HTTP' stand for?",
                "answer": "HyperText Transfer Protocol",
                "accept": ["hypertext transfer protocol"],
                "points": 2
            }
        ]
    
    def display_question(self):
        """Display the current question"""
        if self.current_question >= len(self.questions):
            return False
        
        question = self.questions[self.current_question]
        print(f"\nQuestion {self.current_question + 1}/{len(self.questions)}")
        print(f"Points: {question['points']}")
        print(question['question'])
        
        if question['type'] == 'multiple_choice':
            for i, option in enumerate(question['options'], 1):
                print(f"{i}. {option}")
            print("Enter the number of your answer (1-4):")
        
        elif question['type'] == 'true_false':
            print("1. True")
            print("2. False")
            print("Enter 1 or 2:")
        
        elif question['type'] == 'multi_select':
            for i, option in enumerate(question['options'], 1):
                print(f"{i}. {option}")
            print("Enter the numbers of all correct answers separated by commas (e.g., 1,3):")
        
        elif question['type'] == 'fill_blank':
            print("Fill in the blank. Enter your answer:")
        
        elif question['type'] == 'short_answer':
            print("Enter your answer:")
        
        return True
    
    def get_user_answer(self):
        """Get and validate user's answer"""
        question = self.questions[self.current_question]
        
        if question['type'] in ['multiple_choice', 'true_false']:
            while True:
                try:
                    choice = int(input("> ").strip())
                    if question['type'] == 'multiple_choice':
                        if 1 <= choice <= len(question['options']):
                            user_answer = question['options'][choice - 1]
                            break
                    else:  # true_false
                        if choice in [1, 2]:
                            user_answer = (choice == 1)
                            break
                    print(f"Please enter a number between 1 and {len(question['options']) if question['type'] == 'multiple_choice' else 2}")
                except ValueError:
                    print("Please enter a valid number.")
        
        elif question['type'] == 'multi_select':
            while True:
                try:
                    choices = input("> ").strip().split(',')
                    choices = [int(c.strip()) for c in choices if c.strip()]
                    if all(1 <= c <= len(question['options']) for c in choices):
                        user_answer = [question['options'][c - 1] for c in choices]
                        break
                    print(f"Please enter numbers between 1 and {len(question['options'])} separated by commas")
                except ValueError:
                    print("Please enter valid numbers separated by commas.")
        
        else:  # fill_blank or short_answer
            user_answer = input("> ").strip().lower()
            if question['type'] == 'short_answer' and 'accept' in question:
                # Check if answer matches any acceptable variation
                user_answer = user_answer if user_answer in question['accept'] else user_answer
        
        return user_answer
    
    def check_answer(self, user_answer):
        """Check if the user's answer is correct"""
        question = self.questions[self.current_question]
        correct = False
        
        if question['type'] in ['multiple_choice', 'true_false', 'fill_blank']:
            correct = (str(user_answer).lower() == str(question['answer']).lower())
        
        elif question['type'] == 'multi_select':
            correct = (set(user_answer) == set(question['answer']))
        
        elif question['type'] == 'short_answer':
            correct = (user_answer.lower() == question['answer'].lower()) or \
                     ('accept' in question and user_answer in question['accept'])
        
        if correct:
            self.score += question['points']
            print("✅ Correct!")
        else:
            print("❌ Incorrect!")
            if question['type'] in ['multiple_choice', 'true_false', 'multi_select']:
                print(f"The correct answer is: {question['answer']}")
        
        self.current_question += 1
    
    def show_results(self):
        """Display the final score and performance"""
        max_score = sum(q['points'] for q in self.questions)
        percentage = (self.score / max_score) * 100
        
        print("\nQuiz Complete!")
        print(f"Your score: {self.score}/{max_score}")
        print(f"Percentage: {percentage:.1f}%")
        
        if percentage >= 80:
            print("Excellent performance! 🎉")
        elif percentage >= 60:
            print("Good job! 👍")
        elif percentage >= 40:
            print("Not bad! Keep practicing.")
        else:
            print("Keep learning! You'll do better next time.")
    
    def run(self):
        """Run the quiz game"""
        print("Welcome to the Interactive Quiz Game!")
        print("Answer the following questions. Good luck!\n")
        
        while self.current_question < len(self.questions):
            if self.display_question():
                user_answer = self.get_user_answer()
                self.check_answer(user_answer)
        
        self.show_results()
        
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again in ['yes', 'y']:
            self.score = 0
            self.current_question = 0
            self.run()
        else:
            print("Thanks for playing!")

if __name__ == "__main__":
    quiz = QuizGame()
    quiz.run()