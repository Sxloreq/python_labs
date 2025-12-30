import sqlite3
import hashlib

base_name = "users.db"

def setup_database():
    db = sqlite3.connect(base_name)
    sql = db.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS users (
            user_login TEXT PRIMARY KEY,
            user_pass TEXT,
            user_fullname TEXT
        )
    """
    sql.execute(query)
    db.commit()
    db.close()

def registration():
    print("\n--- Реєстрація ---")
    name = input("Введіть логін: ")
    pw = input("Введіть пароль: ")
    full = input("Введіть ПІБ: ")

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    db = sqlite3.connect(base_name)
    sql = db.cursor()

    sql.execute("SELECT user_login FROM users WHERE user_login = ?", (name,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO users VALUES (?, ?, ?)", (name, pw_hash, full))
        db.commit()
        print("Користувача успішно додано!")
    else:
        print("Помилка: такий логін вже зайнятий.")
    
    db.close()

def change_password():
    print("\n--- Зміна пароля ---")
    target_login = input("Введіть ваш логін: ")
    new_pw = input("Введіть новий пароль: ")
    
    new_hash = hashlib.sha256(new_pw.encode('utf-8')).hexdigest()
    
    db = sqlite3.connect(base_name)
    sql = db.cursor()
    
    sql.execute("UPDATE users SET user_pass = ? WHERE user_login = ?", (new_hash, target_login))
    db.commit()
    
    if sql.rowcount > 0:
        print("Пароль оновлено.")
    else:
        print("Користувача з таким логіном не знайдено.")
        
    db.close()

def login_system():
    print("\n--- Вхід ---")
    login_input = input("Логін: ")
    pass_input = input("Пароль: ")
    
    db = sqlite3.connect(base_name)
    sql = db.cursor()
    
    sql.execute("SELECT user_pass FROM users WHERE user_login = ?", (login_input,))
    data = sql.fetchone()
    db.close()
    
    if data:
        stored_hash = data[0]
        input_hash = hashlib.sha256(pass_input.encode('utf-8')).hexdigest()
        
        if input_hash == stored_hash:
            print(f"Вітаю, ви увійшли як {login_input}!")
        else:
            print("Невірний пароль.")
    else:
        print("Такого користувача не існує.")

if __name__ == "__main__":
    setup_database()

    while True:
        print("\nГОЛОВНЕ МЕНЮ:")
        print("1 - Додати користувача")
        print("2 - Оновити пароль")
        print("3 - Увійти (Login)")
        print("4 - Вихід")
        
        user_choice = input("Ваш вибір: ")
        
        if user_choice == '1':
            registration()
        elif user_choice == '2':
            change_password()
        elif user_choice == '3':
            login_system()
        elif user_choice == '4':
            print("Робота завершена.")
            break
        else:
            print("Невідома команда, спробуйте ще раз.")
