import requests
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import mysql.connector
from rich.console import Console
from rich.panel import Panel
# Charger les variables d'environnement
load_dotenv()
console = Console()
# Variables d'environnement
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")
# Configuration des logs
logging.basicConfig(
   filename="logs/monitor.log",
   level=logging.INFO,
   format="%(asctime)s - %(levelname)s - %(message)s"
)
def save_to_db(status, reponse_time):
   try:
       conn = mysql.connector.connect(
           host=DB_HOST,
           user=DB_USER,
           password=DB_PASSWORD,
           database=DB_NAME
       )
       cursor = conn.cursor()
       cursor.execute(
           "INSERT INTO api_status (status, reponse_time) VALUES (%s, %s)",
           (status, reponse_time)
       )
       conn.commit()
       cursor.close()
       conn.close()
   except Exception as e:
       logging.error(f"Erreur MySQL : {e}")
       console.print(f"[bold red]❌ Erreur MySQL : {e}[/bold red]")
def check_api():
   headers = {"Authorization": f"Bearer {API_TOKEN}"}
   try:
       response = requests.get(API_URL, headers=headers, timeout=5)
       response.raise_for_status()
       data = response.json()
       reponse_time = data.get("response_time", 0)
       logging.info(f"✅ API OK - {reponse_time}s")
       save_to_db("OK", reponse_time)
       console.print(Panel.fit(f"✅ API OK - Temps de réponse : {reponse_time}s", style="bold green"))
   except Exception as e:
       logging.error(f"❌ API Down : {e}")
       save_to_db("Down", 0)
       console.print(Panel.fit(f"❌ API Down : {e}", style="bold red"))
if __name__ == "__main__":
   check_api()