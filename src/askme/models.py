class Question:
    def __init__(self, question_id=-1, parent_id=-1, from_user=-1, to_user=-1,
                 is_anonymous=1, question_text="", answer_text=""):
        self.question_id = question_id
        self.parent_id = parent_id
        self.from_user = from_user
        self.to_user = to_user
        self.is_anonymous = is_anonymous
        self.question_text = question_text
        self.answer_text = answer_text

    @classmethod
    def from_line(cls, line):
        parts = line.strip().split('|')
        return cls(
            question_id=int(parts[0]),
            parent_id=int(parts[1]),
            from_user=int(parts[2]),
            to_user=int(parts[3]),
            is_anonymous=int(parts[4]),
            question_text=parts[5],
            answer_text=parts[6] if len(parts) > 6 else ""
        )

    def to_line(self):
        return f"{self.question_id}|{self.parent_id}|{self.from_user}|{self.to_user}|{self.is_anonymous}|{self.question_text}|{self.answer_text}"


class User:
    def __init__(self, user_id=-1, username="", password="", name="", email="", allow_anonymous=1):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.allow_anonymous = allow_anonymous
        self.questions_from_me = []      
        self.questions_thread_to_me = {} 

    @classmethod
    def from_line(cls, line):
        parts = line.strip().split('|')
        return cls(
            user_id=int(parts[0]),
            username=parts[1],
            password=parts[2],
            name=parts[3],
            email=parts[4],
            allow_anonymous=int(parts[5])
        )

    def to_line(self):
        return f"{self.user_id}|{self.username}|{self.password}|{self.name}|{self.email}|{self.allow_anonymous}"
