import hashlib
import datetime


class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.is_active = is_active

    def verify_password(self, password):
        check_hash = hashlib.sha256(password.encode()).hexdigest()
        if check_hash == self.password_hash:
            return True
        else:
            return False


class Administrator(User):
    def __init__(self, username, password, admin_rights=None):
        super().__init__(username, password)
        if admin_rights is None:
            self.admin_rights = []
        else:
            self.admin_rights = admin_rights


class RegularUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.last_entry_date = "Ніколи"


class GuestUser(User):
    def __init__(self, username):
        super().__init__(username, "")
        self.limitations = "Тільки читання"


class AccessControl:
    def __init__(self):
        self.database = {}

    def add_user(self, user_obj):
        name = user_obj.username
        if name in self.database:
            print(f"Увага: Користувач {name} вже є в базі!")
        else:
            self.database[name] = user_obj
            print(f"Додано користувача: {name}")

    def authenticate_user(self, username, password):
        if username in self.database:
            current_user = self.database[username]

            if current_user.verify_password(password):
                if current_user.is_active:
                    print(f"Вхід дозволено! Ласкаво просимо, {username}.")

                    if isinstance(current_user, RegularUser):
                        now = datetime.datetime.now()
                        current_user.last_entry_date = str(now)
                        print(f"Час входу оновлено: {current_user.last_entry_date}")

                    return current_user
                else:
                    print("Помилка: Цей акаунт заблоковано (is_active=False).")
                    return None
            else:
                print("Помилка: Невірний пароль.")
                return None
        else:
            print("Помилка: Такого користувача не знайдено.")
            return None


if __name__ == "__main__":
    my_security = AccessControl()

    admin = Administrator("SuperAdmin", "admin123", admin_rights=["ban", "delete"])
    simple_guy = RegularUser("Matviy", "matviy2005")
    guest = GuestUser("Guest1")

    print("--- Реєстрація ---")
    my_security.add_user(admin)
    my_security.add_user(simple_guy)
    my_security.add_user(guest)

    print("\n--- Спроби входу ---")

    user1 = my_security.authenticate_user("SuperAdmin", "admin123")

    user2 = my_security.authenticate_user("Matviy", "matviy2005")

    my_security.authenticate_user("SuperAdmin", "wrong_pass")

    my_security.authenticate_user("Hacker", "12345")
