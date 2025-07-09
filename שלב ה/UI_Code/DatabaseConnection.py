import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font
import psycopg2
from datetime import datetime, date
import re

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, host, database, user, password, port=5432):
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {str(e)}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

