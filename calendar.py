import tkinter as tk
from tkinter import ttk
import calendar as cal
from datetime import datetime

class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Modern Calendar App")
        self.geometry("400x400")
        self.configure(bg="#f0f0f0")

        # Initialize variables
        self.current_date = datetime.now()
        
        # Create and set up widgets
        self.setup_ui()

    def setup_ui(self):
        # Create a frame for the header
        header_frame = tk.Frame(self, bg="#4a4a4a")
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        # Add month and year label
        self.month_year_label = tk.Label(
            header_frame,
            font=("Helvetica", 18, "bold"),
            bg="#4a4a4a",
            fg="white"
        )
        self.month_year_label.pack(side=tk.LEFT, padx=10)

        # Add navigation buttons
        prev_button = ttk.Button(header_frame, text="<", command=self.prev_month)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = ttk.Button(header_frame, text=">", command=self.next_month)
        next_button.pack(side=tk.LEFT)

        # Create a frame for the calendar
        self.calendar_frame = tk.Frame(self, bg="#ffffff")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Display the calendar
        self.display_calendar()

    def display_calendar(self):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Update month and year label
        self.month_year_label.config(
            text=self.current_date.strftime("%B %Y")
        )

        # Get calendar for current month
        month_cal = cal.monthcalendar(self.current_date.year, self.current_date.month)

        # Create day labels
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

        # Create date buttons
        for week_num, week in enumerate(month_cal, start=1):
            for day_num, day in enumerate(week):
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
                    btn.grid(row=week_num, column=day_num, sticky="nsew")

                    # Highlight current day
                    if (day == self.current_date.day and
                        self.current_date.month == datetime.now().month and
                        self.current_date.year == datetime.now().year):
                        btn.config(bg="#4a4a4a", fg="white")

        # Make the grid expandable
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.calendar_frame.grid_rowconfigure(i, weight=1)

    def prev_month(self):
        # Go to previous month
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month - 1) if self.current_date.month > 1 else self.current_date.replace(year=self.current_date.year - 1, month=12)
        self.display_calendar()

    def next_month(self):
        # Go to next month
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month + 1) if self.current_date.month < 12 else self.current_date.replace(year=self.current_date.year + 1, month=1)
        self.display_calendar()

if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop()