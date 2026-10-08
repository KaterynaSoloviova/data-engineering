import pandas as pd

s = pd.Series([10, 20, 30], name="amount")
print(s)

# From a list
ages = pd.Series([21, 19, 22, 20])
#print(ages)
# With custom index
ages = pd.Series([21, 19, 22, 20], index=["Alex", "Maria", "John", "Sara"])
print(ages)

# From a dictionary
data = {
    "name": ["Alex", "Maria", "John", "Sarah"],
    "age": [25, 19, 22, 20],
    "score": [85, 78, 90, 78]
}
#print(data)
df = pd.DataFrame(data)
print(df)

#read the file
df = pd.read_csv("week1/students.csv", sep=";")
print(df)

#inspecting data
print(df.head(2))
print(df.tail(1))
print(df.shape)
print(df.columns)
print(df.info)
print(df.dtypes)

#selecting columns
print(df["name"])
print(df[["name", "age"]])

print(df[df["name"]== "Sara"])
print(df[df["age"] >= 20 & df["score"] > 60])

#loc and iloc

print(df.loc[df["age"] > 20, ["name", "age"]])
print(df.iloc[0:3, 1:3])
print(df[["age"]])
print(df["age"])

#groupby

data = {
    "Name": ["Alex", "Riya", "John", "Tony", "Sam"],
    "Department": ["HR", "IT", "IT", "HR", "IT"],
    "Salary": [30000, 50000, 45000, 32000, 52000]
}
df = pd.DataFrame(data)
print(df)


print(df.groupby("Department")["Salary"].mean())


# sort_values

df.sort_values("Salary", ascending=False)
print(df)

df.groupby("Department")["Salary"].mean().sort_values(ascending=False)

# sum()

print(df.groupby("Department")["Salary"].sum())

print(df.groupby(["Department", "Name"])["Salary"].sum())