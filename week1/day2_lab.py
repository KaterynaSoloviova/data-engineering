# Part 1 — Conditions and for Loops

# Q. 1 — Classify Order Values

amounts = [24.50, 55.00, 120.00, 49.99, 99.50]

for amount in amounts:
	if amount >= 100:
		print(f"The {amount} is a High amount")
	elif amount >= 50:
		print(f"The {amount} is a Medium amount") 
	else:
		print(f"The {amount} is a Low amount") 


# Q. 2 — Apply Two Business Rules

# Case 1: 
amount = 125
is_member = True

if amount >= 100 and is_member:
	print("Discount eligible")
else:
	print("Discount not eligible") 

# Case 2: 
amount = 125
is_member = False

if amount >= 100 and is_member:
	print("Discount eligible")
else:
	print("Discount not eligible") 

# Case 3: 
amount = 65
is_member = True

if amount >= 100 and is_member:
	print("Discount eligible")
else:
	print("Discount not eligible") 


# Q. 3 — Calculate Completed Revenue
statuses = [
	"complete",
	"cancelled",
	"complete",
	"complete",
]

amounts = [
	45.50,
	18.00,
	62.25,
	30.00,
]

completed_revenue = 0
for i in range(len(amounts)):
	if statuses[i] == "complete":
		completed_revenue += amounts[i]

print(f"Completed revenue is {completed_revenue:.2f} ") 

# Q. 4 — MCQ: if, elif, else
# answer: C. It runs that branch and skips the remaining branches.

# Q. 5 — Count Until a Limit

#case 1:
count = 1
while count < 6:
	print(count)
	count += 1

#case 2:
count = 1
while count < 4:
	print(count)
	count += 1


# Q. 6 — Stop When the Order Is Found

order_ids = [301, 302, 303, 304, 305]
target_id = 303

for id in order_ids:
	if id == target_id:
		print(f"We have found the target")
		break


# Q. 7 — Skip Invalid Amounts

amounts = [45.50, -5.00, 18.00, 0, 62.25]

new_amounts_list = []

for amount in amounts:
	if amount <= 0:
		continue

	new_amounts_list.append(amount)

print(new_amounts_list)

# Q. 8 — MCQ: break
# answer: A. When you want to stop the current loop as soon as the required result is found.

# Part 3 — Lists, Tuples, and Sets
# Q. 9 — Update a List of Stores

stores = ["London", "Manchester", "Bristol"]

stores.append("Leeds")
stores[2] = "Birmingham"
stores.remove("Manchester")

print(stores)

# Q. 10 — Remove Duplicate Store IDs

store_ids = ["LDN-01", "MAN-02", "LDN-01", "BRS-03", "MAN-02"]

new_store_ids = set(store_ids)

print(f"The original count: {len(store_ids)}")
print(f"The unique count: {len(new_store_ids)}")
print(f"Unique values: {new_store_ids}")

# Q. 11 — Use a Tuple for Fixed Values

store_location = ("LDN-01", "London", "South")

for index in range(len(store_location)):
	print(store_location[index])

# store_location[1] = "Leeds": TypeError: 'tuple' object does not support item assignment    

# Q. 12 — MCQ: Set
# answer: D. Keep unique values and quickly check membership.

# Part 4 — Dictionaries and Choosing a Data Structure
# Q. 13 — Create a Customer Dictionary

customer_data = {
"customer_id": "C101",
"name": "Amelia Clarke",
"city": "London",
"total_spend": 425.50
}

print(customer_data["name"])
print(customer_data["total_spend"])

# Q. 14 — Create a Nested Dictionary

stores_data = {
	"LDN-01": {
		"city": "London",
		"revenue": 5000
	},
	"MAN-02": {
		"city": "Manchester",
		"revenue": 4200
	},
}

print(stores_data["MAN-02"]["revenue"])

# Q. 15 — Count Orders by City

cities = ["London", "Manchester", "London", "Leeds", "London", "Manchester"]

orders = {}

for city in cities:
	if city in orders:
		orders[city] += 1
	else:
		orders[city] = 1 

print(orders)

# Q. 16 — MCQ: Choosing a Data Structure
# Answer: B. Dictionary

# Optional Practice
# Q. 17 — Build a Small Order Cleaner

orders = [
	{"order_id": 401, "city": "London", "amount_gbp": 45.50},
	{"order_id": 402, "city": "Manchester", "amount_gbp": -5.00},
	{"order_id": 401, "city": "London", "amount_gbp": 45.50},
	{"order_id": 403, "city": "Leeds", "amount_gbp": 30.00},
]

accepted_orders_list = []
rejected_orders_list = []
seen_order_ids = set()

for order in orders:
	order_id = order["order_id"]
	is_rejected = order["amount_gbp"] <= 0 or order_id in seen_order_ids

	if is_rejected:
		rejected_orders_list.append(order)
	else: 
		accepted_orders_list.append(order)

	seen_order_ids.add(order_id)

print(
	f"The accepted orders: {accepted_orders_list} "
	f"The rejected orders: {rejected_orders_list} "
	f"The seen order ids: {seen_order_ids}"
	)

# Q. 18 — Revenue by City

total_revenue = {}

for order in accepted_orders_list:
	city = order["city"]
	if city in total_revenue:
		total_revenue[city] += order["amount_gbp"]
	else:
		total_revenue[city] = order["amount_gbp"]


print(total_revenue)

# Q. 19 — Stop After Three Valid Orders

amounts = [10, -5, 20, 0, 30, 40]

valid_values = []

# variant 1:
for amount in amounts:
	if amount > 0:
		valid_values.append(amount)
		if len(valid_values) < 3:
			continue
		else:
			break

print(valid_values) 

# variant 2:

index = 0
while len(valid_values) < 3:
	if amounts[index] > 0:
		valid_values.append(amounts[index])
	index += 1

print(valid_values)        
		
# Q. 20 — Choose the Structure

"""
Ordered daily file names: list, because we have ordered values, which could be changed
Unique customer IDs: set, because we need unique values without duplicates
Fixed latitude and longitude: tuple, because we need ordered and fixed values
Customer ID mapped to customer details: dictionary, because we have one key related to values
"""




