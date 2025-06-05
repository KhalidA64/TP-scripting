import os
import mysql.connector
from dotenv import load_dotenv
from tabulate import tabulate
load_dotenv()
conn = mysql.connector.connect(
   host=os.getenv("MYSQL_HOST"),
   user=os.getenv("MYSQL_USER"),
   password=os.getenv("MYSQL_PASSWORD"),
   database=os.getenv("MYSQL_DATABASE"),
   port=int(os.getenv("MYSQL_PORT", 3306))
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM api_status ORDER BY created_at DESC")
rows = cursor.fetchall()
print(tabulate(rows, headers=["ID", "Status", "Réponse", "Date"], tablefmt="fancy_grid"))
cursor.close()
conn.close()