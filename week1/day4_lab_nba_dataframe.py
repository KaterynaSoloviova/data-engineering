import pandas as pd

#1 Data Understanding

#1.1 Load the dataset into a DataFrame called df. 
df = pd.read_csv("week1/nba.csv")
#print(df)

#1.2 Display the first 5 rows.
print(df.head(5))

#1.3 Check the number of rows and columns.
print(df.shape)

#1.4 List all column names.
print(df.columns)
print(df.info)

#2 Data Cleaning 
#2.1 Convert the Salary column to numeric (handle errors).
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce") #coerce - if something cannot be converted to a number, turn it into NaN

print(df["Salary"])

#2.2 Count how many missing (NaN) values are in each column.
print(df.isnull().sum())

#2.3 Drop rows where Salary is missing.
df = df.dropna(subset=["Salary"])
print(df.head())
print(df.isnull().sum())

#2.4 Fill missing College values with "Unknown".
df["College"] = df["College"].fillna("Unknown")
print(df.isnull().sum())
print(df)

#3 Filtering Data
#3.1 Show all players from Boston Celtics.
print(df[df["Team"] == "Boston Celtics"])

#3.2 Show players whose Age is greater than 30
print(df[df["Age"] > 30])

#3.3 Filter players who play as PG (Point Guard).
print(df[df["Position"] == "PG"])

#3.4 Find players with Salary greater than 5,000,000

print(df[df["Salary"] > 5000000])

#4 Sorting
#4.1 Sort players by Salary (highest first). 
print(df.sort_values("Salary", ascending=False))

#4.2 Sort players by Age (youngest first). 
print(df.sort_values("Age", ascending=True))

#5 GroupBy Operations 
#5.1 Find the average salary per team. 
print(df.groupby("Team")["Salary"].mean())

#5.2 Count number of players in each team.
print(df.groupby("Team")["Number"].count())

#5.3 Find the maximum salary in each team.
print(df.groupby("Team")["Salary"].max())

#6 Aggregations
#6.1 What is the average age of players?
print(df["Age"].mean())

#6.2 What is the maximum salary in the dataset?
print(df["Salary"].max())

#6.3 What is the minimum weight?
print(df["Weight"].min())

#7 Column Operations
#7.1 Create a new column Age_in_5_years.
df["Age_in_5_years"] = df["Age"] + 5
print(df)

#7.2 Create a new column Salary_in_Millions (Salary / 1000000). 
df["Salary_in_Millions"] = df["Salary"] / 1000000
print(df)

#8 Bonus 
#8.1 Which team has the highest total salary payout?
print(df.groupby("Team")["Salary"].sum().sort_values(ascending=False))

#8.2 Which position has the highest average salary?
print(df.groupby("Position")["Salary"].mean().sort_values(ascending=False))
 