# Task 1
number = int(input("Please enter your number: "))


for i in range(1, 11):
    result = number * i
    print(f"{number} * {i} =", number * i )
    print(number, "*", i, "=", number * i)

#Task 2
"""number = int(input("Please enter your number: "))

if number % 2 == 0:
    print("The number {number} is even")
else:
    print("The number {number} is odd")"""

#Task 3
"""num1 = float(input("Please enter first number: "))
num2 = float(input("Please enter second number: ")) 
option = int(input("Please choose the option from 1 to 4: "))  

if option == 1:
    print(num1, "+", num2, "=", num1 + num2)
elif option == 2:
    print(num1, "-", num2, "=", num1 - num2)
elif option == 3:
    print(num1, "*", num2, "=", num1 * num2)
elif option == 4:
    print(num1, "/", num2, "=", num1 / num2)   

orders = [120, 450, 999, 300, 1500, 345, 678, 1200]
for amount in orders:
    if amount >= 1000:
        print("High-value order found:", amount)
        continue   """      

#Task4:
"""sum = 0

for i in range(2, 21, 2):
    sum += 1
print(sum) """   


#Task5:
"""list_cel = [23.4, 34.5, 45.5]

list_far = []

for item in list_cel:
    list_far.append(int((item*9/5) + 32))
print(list_far)

or 

list_cel= [23.4 , 34.5, 45.5, 56.5]
list_fah= [temp * 9/5 + 32 for temp in list_cel]
print(f"Temperature in Fahrenheit: {list_fah}")"""

#Task6:
"""salary = int(input("Please enter your salary: "))
if salary > 50000:
    tax = salary * 0.2
    final_salary = salary - tax
elif salary >= 35000 and salary <= 50000:
    tax = salary * 0.15
    final_salary = salary - tax
else:
    tax = salary * 0.12
    final_salary = salary - tax

print(f"The final salary including tax is: {final_salary}")"""

#Task7 List
order_ids = [101, 102.4, "hello", True]
print(order_ids)









