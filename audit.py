import subprocess
def run_audit():
    print("Running audit...")
    subprocess.run(["python","-m","pip-audit"])
if __name__ == "__main__":
    run_audit()