sales_data = [
    {"продукт": "телефон", "кількість": 2, "ціна": 15000},
    {"продукт": "чохол", "кількість": 5, "ціна": 200},
    {"продукт": "ноутбук", "кількість": 1, "ціна": 30000},
    {"продукт": "чохол", "кількість": 2, "ціна": 200}
]

def calculate_revenue(sales_list):
    revenue_dict = {}
    
    for sale in sales_list:
        name = sale["продукт"]
        qty = sale["кількість"]
        price = sale["ціна"]
        
        total_price = qty * price
        
        if name in revenue_dict:
            revenue_dict[name] = revenue_dict[name] + total_price
        else:
            revenue_dict[name] = total_price
            
    return revenue_dict

total_revenue = calculate_revenue(sales_data)
print("Загальний дохід по продуктах:", total_revenue)

high_revenue_products = []
for product in total_revenue:
    money = total_revenue[product]
    if money > 1000:
        high_revenue_products.append(product)

print("Продукти з доходом більше 1000:", high_revenue_products)
