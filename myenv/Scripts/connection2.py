
import mysql.connector
import openai
import io
import csv
import openai
import os
import IPython
from langchain_community.llms import OpenAI
# from pandasai import PandasAI
from langchain.llms import OpenAI
# from pandasai.llm.openai import OpenAI
# from pandasai import SmartDataframe

os.putenv("OPENAI_API_KEY", "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")
os.environ["OPENAI_API_KEY"] = "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"

llm = OpenAI(api_token="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")
# pandas_ai = PandasAI(llm)

# from pandasai import SmartDataframe
# from pandasai.llm import OpenAI

# df = SmartDataframe("actor.csv", config={"llm": llm})




# API configuration
openai.api_key = os.getenv("OPENAI_API_KEY")


# for LangChain
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def set_open_params(
    model="gpt-3.5-turbo",
    temperature=1,
    max_tokens=800,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
):
    """ set openai parameters"""

    openai_params = {}    

    openai_params['model'] = model
    openai_params['temperature'] = temperature
    openai_params['max_tokens'] = max_tokens
    openai_params['top_p'] = top_p
    openai_params['frequency_penalty'] = frequency_penalty
    openai_params['presence_penalty'] = presence_penalty
    return openai_params

def get_completion(params, messages):
    """ GET completion from openai api"""

    response = openai.chat.completions.create(
        model = params['model'],
        messages = messages,
        temperature = params['temperature'],
        max_tokens = params['max_tokens'],
        top_p = params['top_p'],
        frequency_penalty = params['frequency_penalty'],
        presence_penalty = params['presence_penalty'],
    )
    return response

sql_file_path = "myenv\Scripts\sakila-schema.sql"

# Read the contents of the SQL file
with open(sql_file_path, "r") as sql_file:
    sql_contents = sql_file.read()

# print(sql_contents)
# def query_to_csv(sql_query,  cursor, csv_file_path):

#     cursor.execute(sql_query)
#     rows = cursor.fetchall()

#         # Open the CSV file in write mode
#     with open(csv_file_path, 'w', newline='') as csv_file:
#         # Create a CSV writer object
#         csv_writer = csv.writer(csv_file)

#         # Write the column headers to the CSV file
#         csv_writer.writerow([i[0] for i in cursor.description])

#         # Write the rows to the CSV file
#         csv_writer.writerows(rows)

    


def fetch_schema_and_data():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Abn167007@",
        database="datamig"
    )
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Initialize dictionaries to store schema and data
    schema_data = {}
    foreign_keys = {}
    
    # Fetch table names in the database
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Iterate over tables and fetch schema and data
    for table in tables:
        table_name = table[0]
        # print(table)

        # Fetch table schema
        cursor.execute(f"DESCRIBE {table_name}")
        schema = cursor.fetchall()
        # print(schema)       

        cursor.execute(f"SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = 'datamig'")
        keys = cursor.fetchall()
        # print(keys)

        # Store schema and data in dictionary
        schema_data[table_name] = schema
        foreign_keys[table_name] = keys

    # Close cursor and connection
    cursor.close()
    conn.close()

    return schema_data,foreign_keys
   

result = fetch_schema_and_data()
# print(result)

mysql_schema = fetch_schema_and_data()
# print(mysql_schema)

params = set_open_params()

prompt = f"""
1. Identify the MySQL query that you want to convert to PostgreSQL.

2. Make sure that the syntax and functions used in the MySQL query are compatible with PostgreSQL. Some functions and syntax may differ between the two databases.

3.identify foreign key relationships

4. Replace any MySQL-specific keywords or functions with their equivalent in PostgreSQL. For example, if your MySQL query uses `LIMIT` for limiting results, you would replace it with `LIMIT` in PostgreSQL.

5. Check for any data types that may need to be adjusted based on differences between MySQL and PostgreSQL data types.

6. Test your converted query in a PostgreSQL environment to ensure it runs correctly and returns the expected results.

By following these steps, you should be able to successfully convert a MySQL query to a PostgreSQL query. 



\nnow just Convert the MySQL schema to PostgreSQL from {sql_contents}

postgresql:


"""

messages = [
    {"role": "system", "content":"You are a data engineer assistant AI , you need assist in converting Mysql schema to PostgresQL schema  using LLM and openAI model"},
    {
        "role": "user",
        "content": prompt
    }
]



params = set_open_params(temperature=0)
response = get_completion(params, messages)
print(response.choices[0].message.content)






# \nnow just Convert the MySQL schema to PostgreSQL from {mysql_schema} and for identifing foreign key relationships look at the second dictionary 
# which contains information about foreign keys from {mysql_schema} and include it in PostgreSQL schema

# here is the example of sql to postgreSQL

# SQL:
# CREATE TABLE Employees (
#     EmployeeID INT PRIMARY KEY,
#     FirstName VARCHAR(50),
#     LastName VARCHAR(50),
#     DepartmentID INT,
#     Salary DECIMAL(10,2)
# );

# CREATE TABLE Departments (
#     DepartmentID INT PRIMARY KEY,
#     DepartmentName VARCHAR(50)
# );

# postgreSQL:
# CREATE TABLE Employees (
#     EmployeeID SERIAL PRIMARY KEY,
#     FirstName TEXT NOT NULL,
#     LastName TEXT NOT NULL,
#     DepartmentID INT,
#     Salary NUMERIC(10,2)
# );

# CREATE TABLE Departments (
#     DepartmentID SERIAL PRIMARY KEY,
#     DepartmentName TEXT NOT NULL
# );
