import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3

class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Enhanced Calendar App")
        self.geometry("600x700")
        self.configure(bg="#f0f0f0")

        # Initialize date variables
        self.current_date = datetime.now()
        self.today = datetime.now().date()
        
        # Define color codes for different event categories
        self.categories = {
            "Work": "#FF6B6B",
            "Personal": "#4ECDC4",
            "Holiday": "#45B7D1",
            "Other": "#FFA07A"
        }
        
        # Set up the database and UI
        self.create_database()
        self.setup_ui()

    def setup_ui(self):
        # Set up the main components of the UI
        self.setup_header()
        self.setup_calendar()
        self.setup_time_display()
        self.setup_event_section()

    def setup_header(self):
        # Create the header section with navigation buttons
        header_frame = tk.Frame(self, bg="#4a4a4a")
        header_frame.pack(fill=tk.X, padx=20, pady=10)

        # Label to display current month and year
        self.month_year_label = tk.Label(
            header_frame,
            font=("Helvetica", 16, "bold"),
            bg="#4a4a4a",
            fg="white",
            anchor="w"
        )
        self.month_year_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Navigation buttons for previous and next month
        nav_frame = tk.Frame(header_frame, bg="#4a4a4a")
        nav_frame.pack(side=tk.RIGHT)

        prev_button = ttk.Button(nav_frame, text="<", command=self.prev_month, width=3)
        prev_button.pack(side=tk.LEFT, padx=(0, 5))

        next_button = ttk.Button(nav_frame, text=">", command=self.next_month, width=3)
        next_button.pack(side=tk.LEFT)

    def setup_calendar(self):
        # Create the main calendar display area
        self.calendar_frame = tk.Frame(self, bg="#ffffff")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    def setup_time_display(self):
        # Set up the current time display
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
        # Create the section for displaying and managing events
        event_frame = tk.Frame(self, bg="#ffffff")
        event_frame.pack(fill=tk.X, padx=20, pady=10)

        # Label to show the selected date
        self.event_date_label = tk.Label(event_frame, text="Selected Date: ", bg="#ffffff", font=("Helvetica", 12, "bold"))
        self.event_date_label.pack(anchor="w")

        # Listbox to display events
        self.event_listbox = tk.Listbox(event_frame, width=70, height=6)
        self.event_listbox.pack(pady=10)

        # Buttons for adding and deleting events
        button_frame = tk.Frame(event_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X)

        add_button = ttk.Button(button_frame, text="Add Event", command=self.show_add_event_dialog)
        add_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(button_frame, text="Delete Event", command=self.delete_event)
        delete_button.pack(side=tk.LEFT, padx=5)

    def create_database(self):
        # Set up the SQLite database for storing events
        self.conn = sqlite3.connect('calendar_events.db')
        self.cursor = self.conn.cursor()
        
        # Check if the events table exists
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='events'
        ''')
        table_exists = self.cursor.fetchone()
        
        if not table_exists:
            # If the table doesn't exist, create it with all columns
            self.cursor.execute('''
                CREATE TABLE events
                (id INTEGER PRIMARY KEY, date TEXT, event TEXT, category TEXT)
            ''')
        else:
            # If the table exists, check if the category column exists
            self.cursor.execute('PRAGMA table_info(events)')
            columns = [column[1] for column in self.cursor.fetchall()]
            
            if 'category' not in columns:
                # If the category column doesn't exist, add it
                self.cursor.execute('ALTER TABLE events ADD COLUMN category TEXT')
        
        self.conn.commit()

    def display_calendar(self):
        # Clear existing calendar display
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Update the month and year display
        self.month_year_label.config(text=self.current_date.strftime("%B %Y"))

        # Display day labels (Mon, Tue, etc.)
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

        # Get the days for the current month
        month_days = self.get_month_days(self.current_date.year, self.current_date.month)

        # Display the days and highlight days with events
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

                # Check for events on this day and color-code accordingly
                date = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                self.cursor.execute("SELECT category FROM events WHERE date = ?", (date,))
                events = self.cursor.fetchall()
                if events:
                    categories = set(event[0] for event in events)
                    if len(categories) == 1:
                        btn.config(fg=self.categories[list(categories)[0]])
                    else:
                        btn.config(fg="red")

        # Configure grid layout
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.calendar_frame.grid_rowconfigure(i, weight=1)

    def get_month_days(self, year, month):
        # Calculate the days to display for the given month
        first_day = datetime(year, month, 1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day
        first_weekday = first_day.weekday()
        
        # Create a list of days, including padding for the start and end of the month
        month_days = [0] * first_weekday + list(range(1, last_day + 1))
        month_days += [0] * (42 - len(month_days))
        return month_days

    def prev_month(self):
        # Navigate to the previous month
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month - 1) if self.current_date.month > 1 else self.current_date.replace(year=self.current_date.year - 1, month=12)
        self.display_calendar()

    def next_month(self):
        # Navigate to the next month
        self.current_date = self.current_date.replace(day=1)
        self.current_date = self.current_date.replace(month=self.current_date.month + 1) if self.current_date.month < 12 else self.current_date.replace(year=self.current_date.year + 1, month=1)
        self.display_calendar()

    def update_time(self):
        # Update the current time display
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Schedule the next update in 1 second

    def show_add_event_dialog(self):
        # Display a dialog for adding a new event
        dialog = tk.Toplevel(self)
        dialog.title("Add Event")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Event:").pack()
        event_entry = tk.Entry(dialog, width=30)
        event_entry.pack()
        
        tk.Label(dialog, text="Category:").pack()
        category_var = tk.StringVar(dialog)
        category_var.set(list(self.categories.keys())[0])  # default value
        category_menu = ttk.Combobox(dialog, textvariable=category_var, values=list(self.categories.keys()))
        category_menu.pack()
        
        def add_event():
            # Add the new event to the database
            event = event_entry.get()
            category = category_var.get()
            if event:
                date = f"{self.current_date.year}-{self.current_date.month:02d}-{self.current_date.day:02d}"
                self.cursor.execute("INSERT INTO events (date, event, category) VALUES (?, ?, ?)", (date, event, category))
                self.conn.commit()
                self.show_events(self.current_date.day)
                self.display_calendar()
                dialog.destroy()
            else:
                messagebox.showwarning("Invalid Input", "Please enter an event.")
        
        tk.Button(dialog, text="Add", command=add_event).pack()

    def show_events(self, day):
        # Display events for the selected day
        self.current_date = self.current_date.replace(day=day)
        date = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
        self.event_date_label.config(text=f"Selected Date: {date}")
        
        # Fetch events from the database
        self.cursor.execute("SELECT * FROM events WHERE date = ?", (date,))
        events = self.cursor.fetchall()
        
        # Display events in the listbox
        self.event_listbox.delete(0, tk.END)
        for event in events:
            category = event[3]
            color = self.categories.get(category, self.categories["Other"])
            self.event_listbox.insert(tk.END, f"{event[2]} ({category})")
            self.event_listbox.itemconfig(tk.END, {'bg': color})

    def delete_event(self):
        # Delete the selected event
        selection = self.event_listbox.curselection()
        if selection:
            event = self.event_listbox.get(selection[0])
            date = f"{self.current_date.year}-{self.current_date.month:02d}-{self.current_date.day:02d}"
            
            # Create a confirmation dialog
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the event:\n\n{event}\n\non {date}?")
            
            if confirm:
                event_name = event.split(" (")[0]  # Extract event name without category
                self.cursor.execute("DELETE FROM events WHERE date = ? AND event = ?", (date, event_name))
                self.conn.commit()
                self.show_events(self.current_date.day)
                self.display_calendar()
                messagebox.showinfo("Event Deleted", "The event has been successfully deleted.")
            else:
                messagebox.showinfo("Deletion Cancelled", "The event was not deleted.")
        else:
            messagebox.showwarning("No Selection", "Please select an event to delete.")

if __name__ == "__main__":
    app = CalendarApp()
    app.update_time()
    app.display_calendar()
    app.mainloop() # type: ignore
    