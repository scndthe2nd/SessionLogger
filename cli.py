from database import fetch_logs

def run_cli():
    logs = fetch_logs()
    for log in logs:
        print(log)

if __name__ == '__main__':
    run_cli()