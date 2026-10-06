
import numpy as np

# Part 1 — Functions, Parameters, and Return Values
# Q. 1 — Create a Reusable Revenue Function

def calculate_revenue(price, quantity):
    return(price * quantity)

revenue1 = calculate_revenue(24.50, 3)
revenue2 = calculate_revenue(12.00, 5)

print(revenue1)
print(revenue2)

# Q. 2 — Return More Than One Result

def calculate_purchase(unit_price, quantity):
    subtotal = unit_price * quantity
    vat_amount = subtotal * 0.20
    final_total = subtotal + vat_amount

    return subtotal, vat_amount, final_total

result = calculate_purchase(45, 2)

print(result)

# Q. 3 — Reuse the Same Function for Three Orders

def calculate_order (price, quantity):
    return price * quantity

order_one = calculate_order(10.00 , 4)
order_two = calculate_order(35.50 , 2)
order_three = calculate_order(7.25 , 10)

print(f"final total for Order 1 is {order_one}, for Order 2 is {order_two}, and for Order 3 - {order_three}")

# Q. 4 — MCQ: Return Value
# Answer: D. It sends a result back to the code that called the function.

# Part 2 — Default Arguments and Reusable Functions
# Q. 5 — Add a Default Discount

def apply_discount(amount, discount_percent=5):
    return (amount - amount * discount_percent / 100)

print(apply_discount(100)) 
print(apply_discount(100, 10)) 

# Q. 6 — Build a Validation Function

def is_valid_amount(amount):
    if amount > 0:
        return True
    return False

print(is_valid_amount(45.50))
print(is_valid_amount(0))
print(is_valid_amount(-5))

# Q. 7 — Combine Two Functions

def is_valid_amount(amount):
    if amount > 0:
        return True
    return False

def apply_discount(amount, discount_percent=5):
    return (amount - amount * discount_percent / 100)

amounts = [100, -10, 50]

for amount in amounts:
    if is_valid_amount(amount):
        print(apply_discount(amount, 10))
    else:
        print("Amount is invalid")    


# Q. 8 — MCQ: Default Argument

"""def add_fee(amount, fee=2):
    return amount + fee
 
add_fee(10)"""
# Answer: B. It returns 12

# Part 3 — NumPy Arrays, Indexing, Slicing, and Filtering
# Q. 9 — Create Three Sales Arrays


array_batch_1 = np.array([45.50, 18.00, 62.25])
array_batch_2 = np.array([30.00, 55.50, 12.00])
array_batch_3 = np.array([80.00, 20.00, 100.00])


print(array_batch_1, array_batch_1.dtype)
print(array_batch_2, array_batch_2.dtype)
print(array_batch_3, array_batch_3.dtype)


# Q. 10 — Practice Indexing and Slicing

amounts = np.array([10, 20, 30, 40, 50, 60])

print(amounts[0])
print(amounts[-1])
print(amounts[1:4])
print(amounts[:3])

# Q. 11 — Filter High-Value Orders

amounts = np.array([45.50, 18.00, 120.00, 62.25, 150.00])

print(amounts[amounts >= 100])

# Q. 12 — MCQ: Boolean Indexing

# amounts[amounts > 50]
# Answer: A. A new array containing values greater than 50

# Part 4 — Array Operations and Aggregations
# Q. 13 — Apply a Percentage Increase

prices = np.array([10.00, 20.00, 50.00])

print(prices * 1.10)

# Q. 14 — Calculate Sales Metrics

sales = np.array([45.50, 18.00, 62.25, 30.00, 55.50])

print(sales.sum())
print(sales.min())
print(sales.max())
print(sales.mean())

# Q. 15 — Work with a Two-Dimensional Array

sales = np.array([
    [100, 120, 90],
    [80, 110, 105],
    [95, 100, 130],
])

print(
    f"Total sales for each store: {np.sum(sales, axis = 1)}. "
    f"Total sales for each day: {np.sum(sales, axis = 0)}"
    )

# Q. 16 — MCQ: NumPy Aggregation

# Which expression calculates the average of all values in a NumPy array named sales?
#  Answer: C. sales.mean() 

# Optional Practice
# Q. 17 — Create a Reusable NumPy Summary Function


def summarise_sales(sales):
    return (sales.sum(), sales.min(), sales.max(), sales.mean())

result = np.array([45.50, 18.00, 62.25, 30.00, 55.50])

print(summarise_sales(result))

# Q. 18 — Reject Invalid Values Before Aggregation

sales = np.array([45.50, -5.00, 18.00, 0, 62.25])

valid_values = sales[sales > 0]

print(f"Valid values: {valid_values}")
print(f"Total amount: {valid_values.sum():.2f}")
print(f"Mean value: {valid_values.mean():.2f}")

# Q. 19 — Compare Loop and NumPy Results

# case 1: with a normal Python loop
sales = [10, 20, 30, 40, 50]

new_array = []
for value in sales:
    new_array.append(round(value * 1.10, 2))
print(new_array)

# case 2: with a NumPy array
sales_np_array = np.array([10, 20, 30, 40, 50])
print(sales_np_array * 1.10)

# Q. 20 — Analyse Three Store Batches

batch_1 = np.array([45.50, 18.00, 62.25])
batch_2 = np.array([30.00, 55.50, 12.00])
batch_3 = np.array([80.00, 20.00, 100.00])

total_sales = np.concatenate([
    batch_1,
    batch_2,
    batch_3,
])

average = total_sales.mean()
above_average = total_sales[total_sales > average]
above_average_size = above_average.size


print(f"Total sales: {total_sales}")
print(f"Average value of sales: {average:.2f}")
print(f"Values above the average: {above_average}")
print(f"Number of values above the average: {above_average_size}")
