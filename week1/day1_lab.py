# Part 1 — Variables and Python Execution
# Q. 1 — Create an Order Summary

order_id = 1001
city = "London"
amount_gbp = 45.50
is_complete = True

print(order_id)
print(city)
print(amount_gbp)
print(is_complete)

# Q. 2 — Change the Values and Run Again

order_id = 1002
city = "Manchester"
amount_gbp = 18.00
is_complete = False

print(f"Order {order_id} from {city} has value £{amount_gbp:.2f}")

amount_gbp = 23.75

print(f"Order {order_id} from {city} has value £{amount_gbp:.2f}")

# Q. 3 — Fix the Execution Order

store_name = "Bristol"
print(f"Store: {store_name}")

# Q. 4 — MCQ: Variables

# Answer: B. A variable gives a name to a value that can be reused later.

# Part 2 — Data Types, Type Casting, and Arithmetic
# Q. 5 — Check the Data Types

order_count = 12
average_value = 36.75
store_name = "Leeds"
is_open = True

print(type(order_count))
print(type(average_value))
print(type(store_name))
print(type(is_open))

# Q. 6 — Calculate an Order Total

unit_price = 24.50
quantity = 3
delivery_fee = 4.99

subtotal = unit_price * quantity
final_total = subtotal + delivery_fee

print(f"{subtotal:.2f}")
print(f"{final_total:.2f}")

# Q. 7 — Convert Text Before Calculation

quantity_text = "4"
price_text = "12.50"

quantity_int = int("4")
price_float = float("12.50")

total_price = quantity_int * price_float

print(f"Total price is £{total_price}")


# Q. 8 — MCQ: Type Casting

#Answer: D. Convert it with float()

float_number_one = float(input("Please insert first float number: "))
float_number_two = 18.30

print(float_number_one + float_number_two)

# Part 3 — Comparisons, Logical Checks, Input, and Output
# Q. 9 — Check Whether an Order Is High Value

is_high_value = float(input("Please enter the order amount : "))

is_high_value = amount_gbp >= 100

print(f"The entered number is high - {is_high_value}")

# Q. 10 — Combine Two Conditions

# case 1:
status = "complete"
amount_gbp = 45.50

result = status == "complete" and amount_gbp > 0

print(f"The order is accepted: {result}")

# case 2: 
status = "cancelled"
amount_gbp = 45.50

result = status == "complete" and amount_gbp > 0

print(f"The order is accepted: {result}")

# case 3:
status = "complete"
amount_gbp = -5.00

result = status == "complete" and amount_gbp > 0

print(f"The order is accepted: {result}")

# Q. 11 — Build a Small Interactive Check

store_name = input ("Please enter the name of a store: ")
order_amount = float(input("Please enter the order amount in this store: "))

is_order_accepted = order_amount > 0

print(f"{store_name}: order accepted: {is_order_accepted}")

# Q. 12 — MCQ: Comparison Result
# Answer: True

# Part 4 — f-Strings and Basic Debugging
#Q. 13 — Format a Sales Message

city = "London"
orders = 8
revenue_gbp = 356.7

print(f"{city}: {orders} orders | Revenue £{revenue_gbp}")

# Q. 14 — Identify and Fix Four Errors

#case 1: SyntaxError
city = "London"
print(city)

#case 2: NameError
amount = 25
print(amount)

#case 3: TypeError
amount = int("25")
print(amount + 10)

#case 4: ValueError
quantity = int("3")

#Q. 15 — Fix an Indentation Error
amount = 125
print(amount)

# Q. 16 — MCQ: Debugging
price = "12.50"
total = price * 2

# answer: C. Convert price to float before multiplying

# Q. 17 — Build a Small Order Calculator

order_id = int(input("Please enter the order ID: "))
city = input("Please enter the city: ")
unit_price = float(input("Please enter the price per unit: "))
quantity = int(input("Please enter the quantity of units: "))
discount_percent = float(input("Please enter the percent of discount: "))

subtotal = unit_price * quantity
discount_amount = subtotal * discount_percent / 100
final_total = subtotal - discount_amount

print(f"For order {order_id}, {city} city: price for {quantity} units is {subtotal:.2f} Euro. "
      f"The discount amount with discount {discount_percent:.2f}% is {discount_amount:.2f} Euro. "
      f"Then the total price is {final_total:.2f} Euro")

# Q. 18 — Create Validation Flags
quantity = int(input("Please enter the quantity of units: "))
discount_percent = float(input("Please enter the percent of discount: "))

valid_quantity = quantity > 0
valid_discount = (discount_percent >= 0 and discount_percent <= 100)
all_valid = valid_quantity and valid_discount

print(f"Quantity is valid: {valid_quantity }; Discount is valid: {valid_discount}; All values is valid: {all_valid}")

# Q. 19 — Debug an Input and Comparison Script
city = input("City: ")
amount = float(input("Amount: "))
 
is_high_value = amount >= 100
print(f"{city} | £{amount:.2f} |"
      f"High value: {is_high_value}")

#Q. 20 — Test Boundary Values
amount = float(input("Please enter the amount: "))
is_high_value = amount >= 0

print(f"{amount:.2f} is high value: {is_high_value}")

# Because 100.00 is the boundary value. Testing it confirms that we use correctly the the >= condition