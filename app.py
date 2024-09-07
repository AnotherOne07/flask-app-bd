import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_TABLES = (
    "CREATE TABLE IF NOT EXISTS users(cpf TEXT PRIMARY KEY, name TEXT, born_date TEXT);"
)

INSERT_USER = (
    "INSERT INTO users(cpf, name, born_date) VALUES (%s, %s, %s);"
)

INSERT_USER_RETURN_ID = (
    "INSERT INTO users(cpf, name, born_date) VALUES (%s, %s, %s) RETURNING cpf;"
)

SELECT_USER = (
    "SELECT * FROM users WHERE cpf = (%s)"
)

load_dotenv()
app = Flask(__name__)
url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(
    database="postgres",
    user="postgresadmin",
    password="202200014060admin",
    host=url,
    port='5432')

@app.post("/api/user")
def create_user():
    data = request.get_json()
    cpf, name, born_date = data["cpf"], data["name"], data["born_date"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLES)
            # cursor.execute(INSERT_USER, (cpf, name, born_date,))
            cursor.execute(INSERT_USER_RETURN_ID, (cpf, name, born_date,))
            user_cpf = cursor.fetchone()[0]
        return {"cpf": user_cpf, "message": f"User {cpf} created."}, 201
    

@app.get("/api/getUser/<cpf>")
def get_users(cpf):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_USER, (cpf,))
            user = cursor.fetchone()
        return {"user": user[0], "name": user[1], "birth_date": user[2]}
