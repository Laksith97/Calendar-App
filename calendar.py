import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3

class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Enhanced Calendar App")
        self.geometry("500x600")
        self.configure(bg="#f0f0f0")

        # Initialize date variables
        self.current_date = datetime.now()
        self.today = datetime.now().date()
        
        # Set up the user interface and database
        self.setup_ui()
        self.create_database()

    def setup_ui(self):
        """Set up the main components of the user interface"""
        self.setup_header()
        self.setup_calendar()
        self.setup_time_display()
        self.setup_event_section()

    def setup_header(self):
        """Create the header with month/year display and navigation buttons"""
        header_frame = tk.Frame(self, bg="#4a4a4a")
        header_frame.pack(fill=tk.X, padx=20, pady=10)

        # Month and Year label
        self.month_year_label = tk.Label(
            header_frame,
            font=("Helvetica", 18, "bold"),
            bg="#4a4a4a",
            fg="white",
            anchor="w"
        )
        self.month_year_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg="#4a4a4a")
        nav_frame.pack(side=tk.RIGHT)

        prev_button = ttk.Button(nav_frame, text="<", command=self.prev_month, width=3)
        prev_button.pack(side=tk.LEFT, padx=(0, 5))

        next_button = ttk.Button(nav_frame, text=">", command=self.next_month, width=3)
        next_button.pack(side=tk.LEFT)

    def setup_calendar(self):
        """Create the main calendar frame"""
        self.calendar_frame = tk.Frame(self, bg="#ffffff")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    def setup_time_display(self):
        """Create the current time display"""
        time_frame = tk.Frame(self, bg="#4a4a4a")
        time_frame.pack(fill=tk.X, padx=20, pady=10)

        self.time_label = tk.Label(
            time_frame,
            font=("Helvetica", 14),
            bg="#4a4a4a",
            fg="white",
            anchor="center"
        )
        self.time_label.pack(fill=tk.X, expand=True)

    def setup_event_section(self):
        """Create the event management section"""
        event_frame = tk.Frame(self, bg="#ffffff")
        event_frame.pack(fill=tk.X, padx=20, pady=10)

        # Event entry field
        tk.Label(event_frame, text="Event:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.event_entry = tk.Entry(event_frame, width=30)
        self.event_entry.grid(row=0, column=1, padx=5)

        # Add event button
        add_button = ttk.Button(event_frame, text="Add Event", command=self.add_event)
        add_button.grid(row=0, column=2, padx=5)

        # Event list
        self.event_listbox = tk.Listbox(event_frame, width=50, height=5)
        self.event_listbox.grid(row=1, column=0, columnspan=3, pady=10)

        # Delete event button
        delete_button = ttk.Button(event_frame, text="Delete Event", command=self.delete_event)
        delete_button.grid(row=2, column=0, columnspan=3)

    def create_database(self):
        """Create or connect to the SQLite database"""
        self.conn = sqlite3.connect('calendar_events.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events
            (id INTEGER PRIMARY KEY, date TEXT, event TEXT)
        ''')
        self.conn.commit()

    def display_calendar(self):
        """Display the calendar for the current month"""
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Update month/year label
        self.month_year_label.config(text=self.current_date.strftime("%B %Y"))

        # Create weekday labels
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

        # Get days for the current month
        month_days = self.get_month_days(self.current_date.year, self.current_date.month)

        # Create day buttons
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
                    pady=5,
                    command=lambda d=day: self.show_events(d)
                )
                btn.grid(row=row, column=col, sticky="nsew")

                # Highlight today's date
                if (day == self.today.day and
                    self.current_date.month == self.today.month and
                    self.current_date.year == self.today.year):
                    btn.config(bg="#4a4a4a", fg="white")

                # Check for events on this day
                date = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                self.cursor.execute("SELECT * FROM events WHERE date = ?", (date,))
                if self.cursor.fetchone():
                    btn.config(fg="red")  # Highlight days with events

        # Make the grid expandable
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.calendar_frame.grid_rowconfigure(i, weight=1)

    def get_month_days(self, year, month):
        """Calculate the days to be displayed for the given month"""
        first_day = datetime(year, month, 1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day
        first_weekday = first_day.weekday()
        
        # Create a list of days, padding with zeros for days before the 1st
        month_days = [0] * first_weekday + list(range(1, last_day + 1))
        # Pad the end to always have 6 weeks displayed
        month_days += [0] * (42 - len(month_days))
        return month_days

    def prev_month(self):
        """Go to the previous month"""
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month - 1) if self.current_date.month > 1 else self.current_date.replace(year=self.current_date.year - 1, month=12)
        self.display_calendar()

    def next_month(self):
        """Go to the next month"""
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month + 1) if self.current_date.month < 12 else self.current_date.replace(year=self.current_date.year + 1, month=1)
        self.display_calendar()

    def update_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Schedule the next update in 1 second

    def add_event(self):
        """Add a new event to the database"""
        event = self.event_entry.get()
        if event:
            date = f"{self.current_date.year}-{self.current_date.month:02d}-{self.current_date.day:02d}"
            self.cursor.execute("INSERT INTO events (date, event) VALUES (?, ?)", (date, event))
            self.conn.commit()
            self.event_entry.delete(0, tk.END)
            self.show_events(self.current_date.day)
            self.display_calendar()  # Refresh the calendar to show the new event
        else:
            messagebox.showwarning("Invalid Input", "Please enter an event.")

    def show_events(self, day):
        """Display events for the selected day"""
        self.current_date = self.current_date.replace(day=day)
        date = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
        self.cursor.execute("SELECT * FROM events WHERE date = ?", (date,))
        events = self.cursor.fetchall()
        
        self.event_listbox.delete(0, tk.END)
        for event in events:
            self.event_listbox.insert(tk.END, event[2])

    def delete_event(self):
        """Delete the selected event from the database"""
        selection = self.event_listbox.curselection()
        if selection:
            event = self.event_listbox.get(selection[0])
            date = f"{self.current_date.year}-{self.current_date.month:02d}-{self.current_date.day:02d}"
            self.cursor.execute("DELETE FROM events WHERE date = ? AND event = ?", (date, event))
            self.conn.commit()
            self.show_events(self.current_date.day)
            self.display_calendar()  # Refresh the calendar to reflect the deletion
        else:
            messagebox.showwarning("No Selection", "Please select an event to delete.")

if __name__ == "__main__":
    app = CalendarApp()
    app.update_time()
    app.display_calendar()
    app.mainloop() 
    # type: ignore
