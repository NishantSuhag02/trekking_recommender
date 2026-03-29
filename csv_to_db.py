import sqlite3
import pandas as pd

df = pd.read_csv("data/trek_dataset.csv")

conn = sqlite3.connect("treks.db")

# create table
df.to_sql("treks", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully!")