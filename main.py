from database import DatabaseManager

def main():
    db_file = 'server_logs.db'
    db_manager = DatabaseManager(db_file)
    logs = db_manager.fetch_logs()
    for log in logs:
        print(log)

if __name__ == "__main__":
    main()