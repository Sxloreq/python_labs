warehouse = {
    "молоко": 10,
    "хліб": 2,
    "масло": 20
}

def update_inventory(product_name, quantity):
    if product_name in warehouse:
        warehouse[product_name] = warehouse[product_name] + quantity
    else:
        if quantity > 0:
            warehouse[product_name] = quantity

update_inventory("молоко", -3)
update_inventory("хліб", 10)
update_inventory("цукор", 4)

print("Оновлений склад:", warehouse)

low_stock = []
for product in warehouse:
    qty = warehouse[product]
    if qty < 5:
        low_stock.append(product)

print("Продукти, яких менше 5 шт:", low_stock)
print("-" * 30)
