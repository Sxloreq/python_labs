class UserManager:
    def __init__(self):
        self.data = {}

    def add_user(self, username, age):
        if username in self.data:
            raise ValueError("Такий користувач вже існує")
        if age < 0:
            raise ValueError("Вік не може бути меншим за 0")

        self.data[username] = age
        return "Додано"

    def check_status(self, username):
        if username not in self.data:
            return None

        age = self.data[username]
        if age >= 18:
            return "Дорослий"
        else:
            return "Дитина"

    def delete_user(self, username):
        if username in self.data:
            del self.data[username]
            return True
        else:
            return False
