from DatabaseConnection import DatabaseConnection
from MainApplication import MainApplication

def main():
    # Connect to DB with hardcoded credentials
    db = DatabaseConnection()
    connected = db.connect(
        host="localhost",
        database="db5785_2068_9606",
        user="postgres",
        password="dbdocker12",
        port="5432"
    )

    if connected:
        app = MainApplication(db)
        app.run()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
