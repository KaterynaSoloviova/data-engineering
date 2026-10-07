# Variables, Input & Operators

# 1. Write a Python program that asks the user for their name, age, and city, then displays the information in a meaningful sentence.

name = input("Enter your name: ")
age = int(input("Enter your age: " ))
city = input("Enter the city where you live: ")

print(f"{name} is {age} years old and lives in {city}")


# 2. Write a program that asks the user for two numbers and displays their addition, subtraction, multiplication, and division.

first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))

# variant 1
add = first_number + second_number
sub = first_number - second_number
mult = first_number * second_number
div = first_number / second_number

print(f"Addition: {add:.2f}")
print(f"Subtraction: {sub:.2f}")
print(f"Multiplication: {mult:.2f}")
print(f"Division: {div:.2f}")

# variant 2

def math_operations(first_number, second_number):
    add = first_number + second_number
    sub = first_number - second_number
    mult = first_number * second_number
    div = first_number / second_number

    return add, sub, mult, div

add, sub, mult, div = math_operations(first_number, second_number)

print(f"Addition: {add:.2f}")
print(f"Subtraction: {sub:.2f}")
print(f"Multiplication: {mult:.2f}")
print(f"Division: {div:.2f}")

# 3. Write a program to calculate the area of a rectangle. Ask the user to enter the length and width.

length = float(input("Enter a length of the rectangle: "))
width = float(input("Enter a width of the rectangle: "))

# variant 1
rectangle_area = length * width

print(rectangle_area)

# variant 2

def rectangle_area(length, width):
    return length * width

print(f"The area of rectangle is {rectangle_area(length, width)}")

# 4. Write a program that accepts a temperature in Celsius and converts it to Fahrenheit.

temperature_celsius = float(input("Enter the temperature in Celsius : "))

temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32

print(f"Temperature {temperature_celsius} °C is equal to {temperature_fahrenheit} °F")

# if / elif / else
# 5. Write a program that asks the user for a number and determines whether it is positive, negative, or zero.

number = float(input("Enter the number: "))

if number > 0:
    print(f"Number {number} is positive")
elif number < 0:
    print(f"Number {number} is negative")
else:
    print(f"We have {number} number")    


# 6. Write a program that asks the user for a number and determines whether it is even or odd.

number = float(input("Enter the number: "))

if number % 2 == 0:
    print(f"Number {number} is even")
else:
    print(f"Number {number} is odd")   

# 7. Write a program that asks for a person's age and determines whether they are a child, teenager, or adult.

age = int(input("Enter the age of the person: "))

if age <= 12:
    print(f"The person is a child")
elif age <= 19:
    print(f"The person is a teenager")
else:
    print(f"The person is an adult")      

# 8. Write a program that accepts marks from 0 to 100 and displays the appropriate grade:

mark = float(input(f"Enter your mark from 0 to 100: "))

if mark >= 90:
    print(f"Excellent job! Your grade is A")
elif mark >= 80:
    print(f"Good job! Your grade is B")
elif mark >= 70:
    print(f"You need to practice more.  Your grade is C")
elif mark >= 60:
    print(f"You have to be more concentrated. Your grade is D")
else:
    print(f"Oops, you should start the course again. Your grade is F ")


# 9. Write a program that asks for three numbers and finds the largest number.

num_one = float(input("Enter the first number : "))
num_two = float(input("Enter the second number : "))
num_three = float(input("Enter the third number : "))

if num_one >= num_two and num_one >= num_three:
    max_num = num_one

elif num_two >= num_one and num_two >= num_three:
    max_num = num_two

else:
    max_num = num_three

print(f"The maximum number is {max_num}")


# 10. Write a simple calculator. Ask the user for two numbers and an operator (+, -, *, /) and perform the selected calculation.

num_one = float(input("Enter the first number : "))
num_two = float(input("Enter the second number : "))
operator = input("Choose the operator (+, -, *, /): ")

def calculator(num_one, num_two, operator):
    if operator == "+":
        return num_one + num_two
    elif operator == "-":
        return num_one - num_two
    elif operator == "*":
        return num_one * num_two
    elif operator == "/":
        if num_two == 0:
            return "Cannot divide by zero"
        return num_one / num_two
    else:
        return "Invalid operator"

print(calculator(num_one, num_two, operator))

# for Loops
# 11. Write a program using a for loop to print numbers from 1 to 20.

for number in range(1, 21):
    print (number)

# 12. Write a program to print all even numbers between 1 and 50.

for number in range(2, 51, 2):
     print (number)
     
# 13. Write a program to print all numbers between 1 and 100 that are divisible by both 3 and 5.

for number in range(1, 101):
     if number % 3 == 0 and number % 5 == 0:
          print(number)

# 14. Write a program to display the multiplication table of a number entered by the user.

number = float(input("Enter the number: "))
for value in range (1,11):
     print(f"{number} x {value} = {number * value}")

# 15. Write a program to calculate the sum of all numbers from 1 to 100 using a for loop.

numbers_sum = 0
for number in range(1, 101):
     numbers_sum += number
print(numbers_sum)

# 16. Write a program to count how many even numbers exist between 1 and 100.

count = 0
for number in range(2, 101, 2):
     count += 1

print(count)

# Lists + Loops
#17. Given the following list:
numbers = [12, 45, 7, 89, 23, 56, 34, 91, 10]

even_numbers_array = []
odd_numbers_array = []
more_than_50_array = []

for number in numbers:
    if number % 2 == 0:
        even_numbers_array.append(number)
    if number % 2 != 0:
        odd_numbers_array.append(number)
    if number > 50:
         more_than_50_array.append(number)

print(f"All even numbers: {even_numbers_array}")
print(f"All odd numbers: {odd_numbers_array}")
print(f"All numbers greater than 50 : {more_than_50_array}")       
             

# 18. Given a list of numbers, calculate the total without using the built-in sum() function.

numbers = [12, 45, 7, 89, 23, 56, 34, 91, 10]

total = 0
for number in numbers:
     total += number
print(total)     

# 19. Given a list of numbers, find the largest number without using the built-in max() function.

numbers = [12, 45, 7, 89, 23, 56, 34, 91, 10]

max_num = 0
for number in numbers:
     if number > max_num:
          max_num = number   
print(max_num)  

# 20. Given a list of student marks, use a loop to count how many students passed and how many failed. A mark of 40 or above is considered a pass.

numbers = [12, 45, 7, 89, 23, 56, 34, 91, 10]

count = 0
for number in numbers:
     if number >= 40:
          count += 1

print(f"{count} students passed the test, and the rest {len(numbers) - count} did not pass.")

# Functions
# 21. Write a function greet_user(name) that accepts a person's name and returns a greeting message.

def greet_user(name):
    return f"Hello, {name}!"

print(greet_user("Gurleen"))

# 22. Write a function check_even_odd(number) that accepts a number and returns "Even" or "Odd".

def check_even_odd(number):
     if number % 2 == 0:
          return "Even"
     else:
          return "Odd"
              

print(check_even_odd(31))
print(check_even_odd(12))



# 23. Write a function calculate_sum(n) that uses a loop to calculate and return the sum of numbers from 1 to n.

def calculate_sum(n):
     numbers_sum = 0
     for number in range(1, n+1):
          numbers_sum += number
     return numbers_sum

n = 35
print(f"The sum of numbers from 1 to {n} is {calculate_sum(n)}")     
          
# 24. Write a function count_greater(numbers, value) that accepts a list of numbers and a value, and returns how many numbers in the list are greater than that value.

def count_greater(numbers, value):
     count = 0
     for number in numbers:
          if number > value:
               count += 1
     return count

numbers = [45, 67, 23, 89, 5, 36, 92]   
value = 56

print(f"{count_greater(numbers, value)} numbers in {numbers} are greater than the {value}")

# ⭐ Combined Challenge
# 25. Write a function called analyze_numbers(numbers) that accepts a list of numbers and calculates:

def analyze_numbers(numbers):
    total_values_number = len(numbers)

    values_sum = 0
    total_even_values = 0
    total_odd_values = 0

    largest_value = numbers [0]
    smallest_value = numbers [0]
     

    for number in numbers:
        values_sum += number

        if number % 2 == 0:
             total_even_values += 1
        else:
             total_odd_values += 1

        if number > largest_value:
             largest_value = number

        if number < smallest_value:
            smallest_value = number       
                  
    average = values_sum / len(numbers)

    return total_values_number, values_sum, average, total_even_values, total_odd_values, largest_value, smallest_value  

numbers = [34, 67, 87, 2, 92, 52, 13, 17, 16]

total_values_number, values_sum, average,  total_even_values, total_odd_values, largest_value, smallest_value  = analyze_numbers(numbers)


print(f"Total number of values: {total_values_number}")
print(f"Sum of the values: {values_sum}")
print(f"Average value of values: {average:.2f}")
print(f"Largest value of values: {largest_value}")
print(f"Smallest value of values: {smallest_value}")
print(f"Number of even values: {total_even_values}")
print(f"Number of odd values: {total_odd_values}")

          
     
     


          

     













