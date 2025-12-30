import sqlite3
import datetime

DB_FILE = "security_logs.db"

def create_database():
    db = sqlite3.connect(DB_FILE)
    db.execute("PRAGMA foreign_keys = 1")
    sql = db.cursor()

    sql.execute("""
        CREATE TABLE IF NOT EXISTS EventSources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            location TEXT,
            type TEXT
        )
    """)

    sql.execute("""
        CREATE TABLE IF NOT EXISTS EventTypes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT UNIQUE,
            severity TEXT
        )
    """)

    sql.execute("""
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            source_id INTEGER,
            event_type_id INTEGER,
            message TEXT,
            ip_address TEXT,
            username TEXT,
            FOREIGN KEY (source_id) REFERENCES EventSources(id),
            FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
        )
    """)

    db.commit()
    db.close()
    print("Базу даних створено.")

def add_source(name, location, s_type):
    db = sqlite3.connect(DB_FILE)
    sql = db.cursor()
    try:
        sql.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)", 
                    (name, location, s_type))
        db.commit()
        print(f"Джерело {name} додано.")
    except:
        print(f"Джерело {name} вже є в базі.")
    db.close()

def add_event_type(t_name, severity):
    db = sqlite3.connect(DB_FILE)
    sql = db.cursor()
    try:
        sql.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", 
                    (t_name, severity))
        db.commit()
    except:
        pass
    db.close()

def new_security_event(source, event_type, msg, ip=None, user=None):
    db = sqlite3.connect(DB_FILE)
    sql = db.cursor()

    sql.execute("SELECT id FROM EventSources WHERE name = ?", (source,))
    source_data = sql.fetchone()

    sql.execute("SELECT id FROM EventTypes WHERE type_name = ?", (event_type,))
    type_data = sql.fetchone()

    if source_data and type_data:
        now = datetime.datetime.now()
        
        sql.execute("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (now, source_data[0], type_data[0], msg, ip, user))
        db.commit()
    else:
        print("Помилка: Неправильна назва джерела або типу події")
    
    db.close()

def check_failed_logins():
    db = sqlite3.connect(DB_FILE)
    sql = db.cursor()
    
    query = """
        SELECT se.timestamp, se.username, se.ip_address 
        FROM SecurityEvents se
        JOIN EventTypes et ON se.event_type_id = et.id
        WHERE et.type_name = 'Login Failed' 
        AND se.timestamp > datetime('now', '-1 day')
    """
    sql.execute(query)
    results = sql.fetchall()
    
    print(f"\n--- Невдалі входи за добу ({len(results)}) ---")
    for row in results:
        print(f"Час: {row[0]} | Юзер: {row[1]} | IP: {row[2]}")
    db.close()

def find_brute_force():
    db = sqlite3.connect(DB_FILE)
    sql = db.cursor()
    
    query = """
        SELECT se.ip_address, COUNT(*) 
        FROM SecurityEvents se
        JOIN EventTypes et ON se.event_type_id = et.id
        WHERE et.type_name = 'Login Failed' 
        AND se.timestamp > datetime('now', '-1 hour')
        GROUP BY se.ip_address
        HAVING COUNT(*) > 5
    """
    sql.execute(query)
    results = sql.fetchall()
    
    print("\n--- Перевірка на Brute Force ---")
    if len(results) == 0:
        print("Атак не виявлено.")
    else:
        for row in results:
            print(f"УВАГА! IP {row[0]} зробив {row[1]} спроб входу!")
    db.close()

def critical_events_report():
    db = sqlite3.connect(DB_FILE)
    sql = db.cursor()
    
    query = """
        SELECT es.name, COUNT(*) 
        FROM SecurityEvents se
        JOIN EventTypes et ON se.event_type_id = et.id
        JOIN EventSources es ON se.source_id = es.id
        WHERE et.severity = 'Critical' 
        AND se.timestamp > datetime('now', '-7 days')
        GROUP BY es.name
    """
    sql.execute(query)
    results = sql.fetchall()
    
    print("\n--- Критичні події за тиждень ---")
    for row in results:
        print(f"Джерело: {row[0]} | Кількість критичних помилок: {row[1]}")
    db.close()

def search_in_logs(word):
    db = sqlite3.connect(DB_FILE)
    sql = db.cursor()
    
    query = "SELECT timestamp, message FROM SecurityEvents WHERE message LIKE ?"
    sql.execute(query, ('%' + word + '%',))
    results = sql.fetchall()
    
    print(f"\n--- Пошук слова '{word}' ---")
    for row in results:
        print(f"{row[0]} -> {row[1]}")
    db.close()

if __name__ == "__main__":
    create_database()

    add_event_type("Login Success", "Informational")
    add_event_type("Login Failed", "Warning")
    add_event_type("Port Scan Detected", "Warning")
    add_event_type("Malware Alert", "Critical")

    add_source("Firewall_1", "Server Room", "Firewall")
    add_source("Main_Server", "Cloud", "Server")
    add_source("User_PC_22", "Office", "Endpoint")

    print("\nГенеруємо тестові дані...")
    
    new_security_event("Main_Server", "Login Success", "Admin увійшов", "192.168.0.1", "admin")
    new_security_event("Firewall_1", "Port Scan Detected", "Сканування порту 80", "10.10.10.5")
    new_security_event("User_PC_22", "Malware Alert", "Вірус Trojan.Win32", "192.168.0.105", "manager")

    hacker_ip = "66.55.44.33"
    for i in range(7):
        new_security_event("Main_Server", "Login Failed", f"Невірний пароль спроба {i}", hacker_ip, "root")

    check_failed_logins()
    find_brute_force()
    critical_events_report()
    search_in_logs("Вірус")
