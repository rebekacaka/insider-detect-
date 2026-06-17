#the library used for this is psycopg2 it creates the connection between the database and the code (Python to PostgresSQL)

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection(): #function that any other function in the prject can call to get a database connection 
    try: 
        return psycopg2.connect( #use the function from psycopg2 which will open the connection to PostgresSQL and returns it 
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )   
    except Exception as e: 
        raise RuntimeError (f"Failed to achieve database connection: {e}")

#the reason why i use os.getenv and the rest and not just give my credentials here directly from the env but rather do this connection with the help of os.getnv to read the values from the environment variables is because i dont want my database connection credentials to be public 
