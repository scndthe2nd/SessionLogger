import tkinter as tk
from database import fetch_logs

def run_gui():
    root = tk.Tk()
    root.title("Log Viewer")

    logs = fetch_logs()
    for log in logs:
        label = tk.Label(root, text=str(log))
        label.pack()

    root.mainloop()

if __name__ == '__main__':
    run_gui()