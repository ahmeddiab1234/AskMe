import os
from .models import User, Question
from .utils import read_file_lines, write_file_lines, input_int

# Base folder = src/askme/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

class QuestionsManager:
    def __init__(self, filepath=None):
        if filepath is None:
            filepath = os.path.join(DATA_DIR, "questions.txt")
        self.filepath = filepath
        self.questions = {} 
        self.thread_map = {} 
        self.last_id = 0

    def load(self):
        self.questions.clear()
        self.thread_map.clear()
        lines = read_file_lines(self.filepath)
        for line in lines:
            q = Question.from_line(line)
            self.questions[q.question_id] = q
            self.last_id = max(self.last_id, q.question_id)
            parent = q.parent_id if q.parent_id != -1 else q.question_id
            self.thread_map.setdefault(parent, []).append(q.question_id)

    def save(self):
        lines = [q.to_line() for q in self.questions.values()]
        write_file_lines(self.filepath, lines, append=False)

    def print_to_questions(self, user: User):
        found = False
        for q in self.questions.values():
            if q.to_user == user.user_id:
                found = True
                print(f"[{q.question_id}] From {q.from_user if not q.is_anonymous else 'Anonymous'}: {q.question_text}")
                if q.answer_text:
                    print(f"    Answer: {q.answer_text}")
        if not found:
            print("No questions found.")

    def print_from_questions(self, user: User):
        """Print all questions FROM this user"""
        found = False
        for q in self.questions.values():
            if q.from_user == user.user_id:
                found = True
                to_user = q.to_user
                print(f"[{q.question_id}] To {to_user}: {q.question_text}")
                if q.answer_text:
                    print(f"    Answer: {q.answer_text}")
        if not found:
            print("No questions found.")

    def ask_question(self, from_user: User, users_manager):
        """Ask a question to another user"""
        users_manager.list_users()
        try:
            to_user_id = int(input("Enter recipient user ID: "))
        except ValueError:
            print("Invalid input")
            return

        # Find user object
        to_user = None
        for u in users_manager.users.values():
            if u.user_id == to_user_id:
                to_user = u
                break
        if not to_user:
            print("User not found")
            return

        anon = 0
        if to_user.allow_anonymous:
            anon = input_int("Anonymous question? (0/1): ", 0, 1)

        text = input("Enter question text: ")

        self.last_id += 1
        q = Question(
            question_id=self.last_id,
            parent_id=-1,
            from_user=from_user.user_id,
            to_user=to_user.user_id,
            is_anonymous=anon,
            question_text=text,
            answer_text=""
        )
        self.questions[self.last_id] = q
        print("Question added!")


    def answer_question(self, user: User):
        try:
            qid = int(input("Enter question ID to answer: "))
        except ValueError:
            print("Invalid input")
            return

        if qid not in self.questions:
            print("Question not found")
            return

        q = self.questions[qid]
        if q.to_user != user.user_id:
            print("You can only answer questions to yourself")
            return

        ans = input("Enter your answer: ")
        q.answer = ans
        print("Answer saved!")

    def delete_question(self, user: User):
        try:
            qid = int(input("Enter question ID to delete: "))
        except ValueError:
            print("Invalid input")
            return

        if qid not in self.questions:
            print("Question not found")
            return

        q = self.questions[qid]
        if q.to_user != user.user_id:
            print("You can only delete questions addressed to you")
            return

        del self.questions[qid]
        print("Question deleted!")

    def list_feed(self):
        """List all answered questions as feed"""
        for q in self.questions.values():
            if q.answer_text:
                print(f"[{q.question_id}] From {q.from_user} to {q.to_user}: {q.question_text}")
                print(f"    Answer: {q.answer_text}")


class UsersManager:
    def __init__(self, filepath=None):
        if filepath is None:
            filepath = os.path.join(DATA_DIR, "users.txt")
        self.filepath = filepath
        self.users = {} 
        self.current_user = None
        self.last_id = 0

    def load(self):
        self.users.clear()
        lines = read_file_lines(self.filepath)
        for line in lines:
            u = User.from_line(line)
            self.users[u.username] = u
            self.last_id = max(self.last_id, u.user_id)

    def save_user(self, user):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        write_file_lines(self.filepath, [user.to_line()])

    def list_users(self):
        if not self.users:
            print("No users in the system.")
            return
        print("System Users:")
        for user in self.users.values():
            print(f"ID: {user.user_id}\tName: {user.name}\tUsername: {user.username}")


