import numpy as np

#1
def square_value (value):
    print(value ** 2)

square_value(5.5)

def add(a, b):
    return a + b
add(5, 3)
result = add(5,3)
print(result)

square_side = float(input("Please enter the site parameter of the square: "))
def square_area(square_side):
    return square_side ** 2

print(square_area(square_side))

circle_radius = float(input("Please enter the radius  of the circle: "))
def circle_area(circle_radius):
    return 3.14 * (circle_radius ** 2)

print(circle_area(circle_radius))


def circle_area(circle_radius):
    return 3.14 * (circle_radius ** 2)

def square_area(square_side):
    return square_side ** 2


def rectangle_area(a, b):
    return a * b


#2
option = int(input("Enter your option from 1 to 3: "))


if option == 1:
    circle_radius = float(input("Enter the radius of the circle: "))
    print(circle_area(circle_radius))
elif option == 2:
    square_side = float(input("Enter the side of the square: "))
    print(square_area(square_side)) 
else:
    a = float(input("Enter the a side of the rectangle : "))
    b = float(input("Enter the b side of the rectangle : "))
    print(rectangle_area(a, b))

#NumPy
#1

a = np.array([10.5, 30, 40])
b = np.zeros(5)
c = np.ones((2,3))
d = np.arange(0, 10, 2)

print(a)
print(b)
print(c)
print(d)

#2

arr = np.array([[10, 20, 30],
                [40, 50, 60]])
 
print(arr[0, 1])   # row 0, col 1
print(arr[1][2])   # row 1, col 2
print(arr[-1, -1])


 
a = np.array([10.6, 20, 30])
b = np.array([1, 2, 3])
 
print(a + 5)
print(a * 2)
print(a + b)

arr_first = np.array([[10, 20, 30],
               [40, 50, 60]])
arr_second = np.array([[15, 35, 45],
               [25, 35, 55]])


result = arr_first + arr_second 
print(result)

 
data = np.array([[10, 20, 30],
                 [40, 50, 60],
                 [70, 80, 90]])
 
print("Total sum:", data.sum())
print("Column-wise mean:", data.mean(axis=0))
print("Row-wise max:", data.max(axis=1))
print("Overall min:", np.min(data))




    





    







