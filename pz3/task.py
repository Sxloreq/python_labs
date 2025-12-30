import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

days_list = []
usd_rates = []

print("Завантажую дані...")

for step in range(7):
    current_date = datetime.now() - timedelta(days=7 - step)
    date_query = current_date.strftime("%Y%m%d")
    date_label = current_date.strftime("%d.%m")

    link = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={date_query}&json"

    try:
        r = requests.get(link)
        if r.status_code == 200:
            data = r.json()
            rate = data[0]['rate']
            
            days_list.append(date_label)
            usd_rates.append(rate)
            print(f"{date_label} -> {rate}")
    except:
        print("Помилка з'єднання")

plt.figure(figsize=(12, 6))
plt.plot(days_list, usd_rates, marker='s', linestyle='--', color='blue', label='Долар США')

plt.title('Динаміка курсу USD (тижневий звіт)')
plt.xlabel('Дні')
plt.ylabel('Вартість (UAH)')
plt.legend()
plt.grid(True)

plt.show()
