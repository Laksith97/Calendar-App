import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Modern Calendar App")
        self.geometry("400x400")
        self.configure(bg="#f0f0f0")

        self.current_date = datetime.now()
        self.setup_ui()

    def setup_ui(self):
        header_frame = tk.Frame(self, bg="#4a4a4a")
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        self.month_year_label = tk.Label(
            header_frame,
            font=("Helvetica", 18, "bold"),
            bg="#4a4a4a",
            fg="white"
        )
        self.month_year_label.pack(side=tk.LEFT, padx=10)

        prev_button = ttk.Button(header_frame, text="<", command=self.prev_month)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = ttk.Button(header_frame, text=">", command=self.next_month)
        next_button.pack(side=tk.LEFT)

        self.calendar_frame = tk.Frame(self, bg="#ffffff")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.display_calendar()

    def display_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_year_label.config(
            text=self.current_date.strftime("%B %Y")
        )

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            lbl = tk.Label(
                self.calendar_frame,
                text=day,
                bg="#4a4a4a",
                fg="white",
                font=("Helvetica", 10, "bold"),
                padx=5,
                pady=5
            )
            lbl.grid(row=0, column=i, sticky="nsew")

        month_days = self.get_month_days(self.current_date.year, self.current_date.month)

        for i, day in enumerate(month_days):
            row = i // 7 + 1
            col = i % 7
            if day != 0:
                btn = tk.Button(
                    self.calendar_frame,
                    text=str(day),
                    bg="white",
                    fg="#333333",
                    font=("Helvetica", 12),
                    relief=tk.FLAT,
                    padx=5,
                    pady=5
                )
                btn.grid(row=row, column=col, sticky="nsew")

                if (day == self.current_date.day and
                    self.current_date.month == datetime.now().month and
                    self.current_date.year == datetime.now().year):
                    btn.config(bg="#4a4a4a", fg="white")

        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.calendar_frame.grid_rowconfigure(i, weight=1)

    def get_month_days(self, year, month):
        first_day = datetime(year, month, 1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day
        first_weekday = first_day.weekday()
        
        month_days = [0] * first_weekday + list(range(1, last_day + 1))
        month_days += [0] * (42 - len(month_days))  # Pad to always have 6 weeks
        return month_days

    def prev_month(self):
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month - 1) if self.current_date.month > 1 else self.current_date.replace(year=self.current_date.year - 1, month=12)
        self.display_calendar()

    def next_month(self):
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month + 1) if self.current_date.month < 12 else self.current_date.replace(year=self.current_date.year + 1, month=1)
        self.display_calendar()

if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop() # type: ignore
    