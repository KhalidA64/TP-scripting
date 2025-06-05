import os
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import mysql.connector
from dotenv import load_dotenv
console = Console()
load_dotenv()
def lancer_monitor():
   console.print("[bold cyan]🧪 Lancement de monitor.py...[/bold cyan]")
   subprocess.run(["python", "monitor.py"])
def lancer_audit():
   console.print("[bold cyan]🔒 Audit des paquets Python...[/bold cyan]")
   try:
       subprocess.run(["python", "-m", "pip_audit"])
   except Exception as e:
       console.print(f"[red]Erreur pendant l'audit : {e}[/red]")
def afficher_bdd():
   try:
       conn = mysql.connector.connect(
           host=os.getenv("MYSQL_HOST"),
           user=os.getenv("MYSQL_USER"),
           password=os.getenv("MYSQL_PASSWORD"),
           database=os.getenv("MYSQL_DATABASE")
       )
       cursor = conn.cursor()
       cursor.execute("SELECT id, status, reponse_time, date_checked FROM api_status ORDER BY id DESC LIMIT 5;")
       resultats = cursor.fetchall()
       if resultats:
           console.print(Panel.fit("📊 Derniers appels API", style="bold yellow"))
           for row in resultats:
               console.print(f"[green]#{row[0]}[/green] - {row[1]} - {row[2]}s - {row[3]}")
       else:
           console.print("[italic]Aucun résultat trouvé.[/italic]")
       cursor.close()
       conn.close()
   except Exception as e:
       console.print(f"[bold red]❌ Erreur MySQL : {e}[/bold red]")
def afficher_menu():
   while True:
       console.print("\n[bold blue]=== MENU PRINCIPAL ===[/bold blue]")
       console.print("1️⃣  Vérifier l’API")
       console.print("2️⃣  Audit de sécurité")
       console.print("3️⃣  Afficher les logs BDD")
       console.print("4️⃣  Quitter")
       choix = Prompt.ask("\n[bold]👉 Que veux-tu faire ?[/bold]", choices=["1", "2", "3", "4"], default="1")
       if choix == "1":
           lancer_monitor()
       elif choix == "2":
           lancer_audit()
       elif choix == "3":
           afficher_bdd()
       elif choix == "4":
           console.print("[bold magenta]👋 À bientôt ![/bold magenta]")
           break
if __name__ == "__main__":
   afficher_menu()