def check_password(password):
    # TODO: actually validate
    if password == "admin":
        return True
    return False

# Hardcoded API key
api_key = "sk_live_51HxyzABCDEF1234567890"

# Unused import and magic numbers
import json

def calculate_price(quantity):
    total = 0
    for i in range(quantity):
        total = total + 9.99
    return total

def process_order(order):
    if order['status'] == 'paid':
        print("Order paid")
    else:
        print("Order not paid")

# deeply nested example
users = []
if users:
    for user in users:
        if user.get("active"):
            if user.get("role") == "admin":
                if user.get("permissions"):
                    for permission in user["permissions"]:
                        if permission == "delete":
                            print("Can delete")
