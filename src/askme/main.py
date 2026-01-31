from .managers import UsersManager, QuestionsManager
from .models import User
from .utils import show_menu, input_int
import getpass  

def main():
    users_manager = UsersManager()
    questions_manager = QuestionsManager()

    users_manager.load()
    questions_manager.load()

    choice = show_menu(["Login", "Sign Up"])
    if choice == 1:
        username = input("Username: ")
        password = getpass.getpass("Password: ") 
        if username in users_manager.users and users_manager.users[username].password == password:
            users_manager.current_user = users_manager.users[username]
        else:
            print("Invalid credentials")
            return 
    else:
        username = input("New Username: ")
        while username in users_manager.users:
            print("Username already exists. Try again.")
            username = input("New Username: ")

        password = getpass.getpass("Password: ")  
        name = input("Name: ")
        email = input("Email: ")
        allow_anon = input_int("Allow anonymous questions? (0/1): ", 0, 1)

        users_manager.last_id += 1
        user_id = users_manager.last_id

        user = User(user_id, username, password, name, email, allow_anon)

        users_manager.users[username] = user
        users_manager.current_user = user

        users_manager.save_user(user)

    print(f"Welcome {users_manager.current_user.name}!")

    while True:
        menu = [
            "Print Questions To Me",
            "Print Questions From Me",
            "Answer Question",
            "Delete Question",
            "Ask Question",
            "List System Users",
            "Feed",
            "Logout"
        ]
        choice = show_menu(menu)

        users_manager.load()
        questions_manager.load()

        current_user = users_manager.current_user

        if choice == 1:
            questions_manager.print_to_questions(current_user)
        elif choice == 2:
            questions_manager.print_from_questions(current_user)
        elif choice == 3:
            questions_manager.answer_question(current_user)
        elif choice == 4:
            questions_manager.delete_question(current_user)
        elif choice == 5:
            questions_manager.ask_question(current_user, users_manager)
        elif choice == 6:
            users_manager.list_users()
        elif choice == 7:
            questions_manager.list_feed()
        else:
            print("Logging out...")
            break
        
        users_manager.save_user(current_user)
        questions_manager.save()

if __name__ == "__main__":
    main()


