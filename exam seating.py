import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2
from tkinter import ttk

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname="exam seating",
        user="postgres",  # Change this
        password="postgres",  # Change this
        host="localhost"
    )

def configure_window(window, title, width=900, height=500):
    window.title(title)
    window.geometry(f"{width}x{height}")
    window.resizable(False, False)
    window.configure(bg="white")


# Function to add students (Multiple Entries Without Closing)
def add_students_window():
    student_window = tk.Toplevel(root)
    student_window.title("Add Students")
    student_window.geometry("600x400")  # Adjust width and height
    student_window.resizable(False, False)  # Prevent resizing
    student_window.attributes('-topmost', True)  # Always stay on top
    student_window.focus_force()  # Force focus on the window

    tk.Label(student_window, text="Student Name:").pack()
    student_name_entry = tk.Entry(student_window)
    student_name_entry.pack()

    tk.Label(student_window, text="Roll Number:").pack()
    student_roll_entry = tk.Entry(student_window)
    student_roll_entry.pack()

    # ✅ Function to Add Student with Unique Roll Number Check
    def add_student():
        name = student_name_entry.get()
        roll = student_roll_entry.get()

        if name and roll:
            conn = connect_db()
            cur = conn.cursor()
            try:
                # 🔹 Check if Roll Number Already Exists
                cur.execute("SELECT COUNT(*) FROM students WHERE roll_number = %s", (roll,))
                count = cur.fetchone()[0]

                if count > 0:
                    messagebox.showerror("Error", "Roll number already exists! Enter a unique roll number.")
                else:
                    # ✅ Insert the student only if roll number is unique
                    cur.execute("INSERT INTO students (name, roll_number) VALUES (%s, %s)", (name, roll))
                    conn.commit()
                    messagebox.showinfo("Success", "Student added successfully!")
                
                # ✅ Clear input fields after success
                student_name_entry.delete(0, tk.END)
                student_roll_entry.delete(0, tk.END)

            except Exception as e:
                messagebox.showerror("Database Error", f"Error: {e}")

            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "All fields are required!")

    tk.Button(student_window, text="Add Next Student", command=add_student).pack(pady=5)
    tk.Button(student_window, text="Done", command=student_window.destroy, bg="red", fg="white").pack(pady=5)

# Function to add exams
def add_exams_window():
    exam_window = tk.Toplevel(root)
    exam_window.title("Add Exams")
    exam_window.geometry("600x400")
    exam_window.resizable(False, False)
    exam_window.attributes('-topmost', True)  # Keep window always on top
    exam_window.focus_force()  # Keep focus on the window


    tk.Label(exam_window, text="Exam Name:").pack()
    exam_name_entry = tk.Entry(exam_window)
    exam_name_entry.pack()

    tk.Label(exam_window, text="Exam Date (YYYY-MM-DD):").pack()
    exam_date_entry = tk.Entry(exam_window)
    exam_date_entry.pack()

    def add_exam():
        name = exam_name_entry.get()
        date = exam_date_entry.get()

        if name and date:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO exams (exam_name, exam_date) VALUES (%s, %s)", (name, date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Exam added successfully!")
            exam_name_entry.delete(0, tk.END)
            exam_date_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required!")

    tk.Button(exam_window, text="Add Next Exam", command=add_exam).pack(pady=5)
    tk.Button(exam_window, text="Done", command=exam_window.destroy, bg="red", fg="white").pack(pady=5)

# Function to add rooms
def add_rooms_window():
    room_window = tk.Toplevel(root)
    room_window.title("Add Rooms")
    room_window.geometry("600x400")
    room_window.resizable(False, False)
    room_window.attributes('-topmost', True)  # Keep window always on top
    room_window.focus_force()  # Keep focus on the window

    tk.Label(room_window, text="Room Name:").pack()
    room_name_entry = tk.Entry(room_window)
    room_name_entry.pack()

    tk.Label(room_window, text="Room Capacity:").pack()
    room_capacity_entry = tk.Entry(room_window)
    room_capacity_entry.pack()

    def add_room():
        name = room_name_entry.get()
        capacity = room_capacity_entry.get()

        if name and capacity.isdigit():
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO rooms (room_name, capacity) VALUES (%s, %s)", (name, int(capacity)))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Room added successfully!")
            room_name_entry.delete(0, tk.END)
            room_capacity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "All fields are required and capacity must be a number!")

    tk.Button(room_window, text="Add Next Room", command=add_room).pack(pady=5)
    tk.Button(room_window, text="Done", command=room_window.destroy, bg="red", fg="white").pack(pady=5)

# Function to generate seating arrangement
# Function to generate seating arrangement
def generate_seating():
    seating_window = tk.Toplevel(root)
    seating_window.title("Generate Seating Arrangement")
    seating_window.geometry("500x350")  # Increased window size
    seating_window.configure(bg="white")  # Consistent background

    tk.Label(seating_window, text="Select Exam:", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, exam_name FROM exams")
    exams = cur.fetchall()
    conn.close()

    if not exams:
        messagebox.showerror("Error", "No exams found! Please add an exam first.")
        seating_window.destroy()
        return

    exam_var = tk.StringVar(seating_window)
    exam_dropdown = ttk.Combobox(seating_window, textvariable=exam_var, values=[exam[1] for exam in exams])
    exam_dropdown.pack(pady=10)

    # ✅ Single "Generate Seating" Button
    generate_button = tk.Button(seating_window, text="Generate Seating", command=lambda: generate(exam_var.get()), width=25, bg="#5DC1B9", fg="black")
    generate_button.pack(pady=20)

def generate(selected_exam):
    if not selected_exam:
        messagebox.showerror("Error", "Please select an exam!")
        return

    conn = connect_db()
    cur = conn.cursor()

    # Get exam ID
    cur.execute("SELECT id FROM exams WHERE exam_name = %s", (selected_exam,))
    exam = cur.fetchone()
    if not exam:
        messagebox.showerror("Error", "Exam not found!")
        conn.close()
        return
    exam_id = exam[0]
    print(f"✅ Exam Selected: {selected_exam} (ID: {exam_id})")  

    # Get students sorted by roll number
    cur.execute("SELECT id, roll_number, name FROM students ORDER BY CAST(roll_number AS INTEGER) ASC")
    students = cur.fetchall()
    print(f"✅ Found {len(students)} students.")  

    # Get available rooms sorted by capacity
    cur.execute("SELECT id, room_name, capacity FROM rooms ORDER BY room_name ASC")
    rooms = cur.fetchall()
    # Ensure correct sorting if room names have numbers (e.g., A1, A2, ..., A10)
    rooms = sorted(rooms, key=lambda x: int(x[1][1:]))  # Sort numerically
    print("\n🔹 Rooms fetched from DB:")
    for room in rooms:
        print(f"➡ Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")

    # Delete old seating arrangement for the exam
    cur.execute("DELETE FROM seating_arrangement WHERE exam_id = %s", (exam_id,))
    conn.commit()
    print("✅ Deleted old seating arrangement for this exam.")  

    if not students or not rooms:
        messagebox.showerror("Error", "Please ensure students and rooms are added!")
        return

    room_index = 0
    seat_no = 1
    current_capacity = rooms[room_index][2]

    for student in students:
        if seat_no > current_capacity:
            room_index += 1
            if room_index >= len(rooms):
                messagebox.showerror("Error", "Not enough rooms for all students!")
                return
            seat_no = 1
            current_capacity = rooms[room_index][2]
        print(f"✅ Assigning Student {student[1]} (Roll {student[0]}) → Room: {rooms[room_index][1]}, Seat: {seat_no}")

        # Save seating arrangement in the database
        cur.execute("""
            INSERT INTO seating_arrangement (student_id, exam_id, room_id, seat_number) 
            VALUES (%s, %s, %s, %s)
        """, (student[0], exam_id, rooms[room_index][0], seat_no))
        
        print(f"✅ Inserted: Student {student[1]} (ID {student[0]}) → Exam {exam_id}, Room {rooms[room_index][0]}, Seat {seat_no}")
        
        conn.commit()

        seat_no += 1

    conn.close()
    messagebox.showinfo("Success", "Seating arrangement generated successfully!")

def search_data():
    search_window = tk.Toplevel(root)
    configure_window(search_window, "Search Data")

    tk.Label(search_window, text="Select Category:").pack()
    search_type_var = tk.StringVar()
    search_type_dropdown = ttk.Combobox(search_window, textvariable=search_type_var, values=["Student", "Exam", "Room"])
    search_type_dropdown.pack()

    tk.Label(search_window, text="Enter Search Keyword:").pack()
    search_entry = tk.Entry(search_window)
    search_entry.pack()

    result_label = tk.Label(search_window, text="", font=("Arial", 12, "bold"))
    result_label.pack(pady=10)

    def perform_search():
        search_text = search_entry.get().strip().lower()
        search_type = search_type_var.get()

        if not search_text or not search_type:
            result_label.config(text="Please select a category and enter a search keyword.")
            return

        conn = connect_db()
        cur = conn.cursor()

        if search_type == "Student":
            cur.execute("""
                SELECT students.roll_number, students.name, rooms.room_name, 
                       seating_arrangement.seat_number, exams.exam_name, exams.exam_date
                FROM students
                LEFT JOIN seating_arrangement ON students.id = seating_arrangement.student_id
                LEFT JOIN rooms ON seating_arrangement.room_id = rooms.id
                LEFT JOIN exams ON seating_arrangement.exam_id = exams.id
                WHERE LOWER(students.name) LIKE %s OR students.roll_number LIKE %s
            """, (f"%{search_text}%", f"%{search_text}%"))

            data = cur.fetchall()
            if not data:
                result_label.config(text="No student found.")
            else:
                result_text = "\n".join([
                     f"Roll No: {row[0]}, Name: {row[1]}, Room: {row[2]}, Seat No: {row[3]}, Exam: {row[4]}, Date: {row[5]}"
                     for row in data
                ])
                result_label.config(text=result_text)


        elif search_type == "Exam":
            cur.execute("""
                SELECT exam_name, exam_date FROM exams
                WHERE LOWER(exam_name) LIKE %s OR exam_date::TEXT LIKE %s
            """, (f"%{search_text}%", f"%{search_text}%"))

            data = cur.fetchall()
            if not data:
                result_label.config(text="No exam found.")
            else:
                result_text = "\n".join([f"Exam: {row[0]}, Date: {row[1]}" for row in data])
                result_label.config(text=result_text)

        elif search_type == "Room":
            cur.execute("""
                SELECT room_name, capacity FROM rooms
                WHERE LOWER(room_name) LIKE %s
            """, (f"%{search_text}%",))

            data = cur.fetchall()
            if not data:
                result_label.config(text="No room found.")
            else:
                result_text = "\n".join([f"Room: {row[0]}, Capacity: {row[1]}" for row in data])
                result_label.config(text=result_text)

        conn.close()

    tk.Button(search_window, text="Search", command=perform_search).pack(pady=5)

# Function to open Admin Panel
def open_admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")
    admin_window.geometry("500x450")  # Adjusted to fit all buttons
    admin_window.configure(bg="white")

    # Dashboard Title
    tk.Label(admin_window, text="Admin Dashboard", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    # Button Styling
    button_style = {"width": 22, "height": 1, "font": ("Arial", 10, "bold")}

    # Buttons List
    buttons = [
        ("Add Students", add_students_window, "#A5D6A7"),  # Light Green
        ("Add Exams", add_exams_window, "#90CAF9"),  # Light Blue
        ("Add Rooms", add_rooms_window, "#FFE082"),  # Light Yellow
        ("Generate Seating", generate_seating, "#4DD0E1"),  # Teal
        ("Search Data", search_data, "white"),  # White
        ("Update", open_update_window, "#FFAB91"),  # ✅ Corrected function
        ("Delete", open_delete_window, "#EF9A9A"),  # ✅ Corrected function
        ("Exit", lambda: close_admin_panel(admin_window), "#E57373")  # Red
     ]


    # Frame for Buttons
    frame = tk.Frame(admin_window, bg="white")
    frame.pack()

    # Generate Buttons
    for text, command, color in buttons:
        btn = tk.Button(frame, text=text, command=command, bg=color, **button_style)
        btn.pack(pady=5)  # Reduced padding for better spacing

    admin_window.protocol("WM_DELETE_WINDOW", lambda: close_admin_panel(admin_window))
def close_admin_panel(admin_window):
    admin_window.destroy()  # Close only the Admin Panel
    root.deiconify()  # Show Main Window Again


def open_update_window():
    update_window = tk.Toplevel(root)
    configure_window(update_window, "Update Records")

    tk.Label(update_window, text="Select an Option to Update", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(update_window, text="Update Student", command=lambda: open_update_details("Student"), width=30).pack(pady=5)
    tk.Button(update_window, text="Update Exam", command=lambda: open_update_details("Exam"), width=30).pack(pady=5)
    tk.Button(update_window, text="Update Room", command=lambda: open_update_details("Room"), width=30).pack(pady=5)

    tk.Button(update_window, text="Close", command=update_window.destroy, width=30, bg="red", fg="white").pack(pady=5)

# ✅ Open Update Details (Single Function for Student, Exam, Room)
def open_update_details(category):
    update_window = tk.Toplevel(root)
    configure_window(update_window, f"Update {category} Details")

    tk.Label(update_window, text=f"Search {category}:", font=("Arial", 12)).pack()
    search_entry = tk.Entry(update_window)
    search_entry.pack()

    record_listbox = tk.Listbox(update_window, height=10)
    record_listbox.pack(fill=tk.BOTH, expand=True)

    tk.Label(update_window, text="New Name (if applicable):").pack()
    new_name_entry = tk.Entry(update_window)
    new_name_entry.pack()

    tk.Label(update_window, text="New Number/Capacity/Date:").pack()
    new_value_entry = tk.Entry(update_window)
    new_value_entry.pack()

    # ✅ Fetch Records Based on Category
    def fetch_records(event=None):
        search_text = search_entry.get().lower()
        record_listbox.delete(0, tk.END)

        conn = connect_db()
        cur = conn.cursor()

        if category == "Student":
            cur.execute("SELECT id, roll_number, name FROM students ORDER BY CAST(roll_number AS INTEGER) ASC")
        elif category == "Exam":
            cur.execute("SELECT id, exam_name, exam_date FROM exams ORDER BY exam_date ASC")
        elif category == "Room":
            cur.execute("SELECT id, room_name, capacity FROM rooms ORDER BY room_name ASC")

        records = cur.fetchall()
        conn.close()

        for record in records:
            if search_text in str(record[1]).lower() or search_text in str(record[2]).lower():
                record_listbox.insert(tk.END, f"{record[1]} - {record[2]}")

    search_entry.bind("<KeyRelease>", fetch_records)
    fetch_records()

    # ✅ Save Updated Record
    def save_update():
        selected_index = record_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", f"Please select a {category.lower()}!")
            return

        selected_text = record_listbox.get(selected_index[0])
        old_value = selected_text.split(" - ")[0]
        new_name = new_name_entry.get().strip()
        new_value = new_value_entry.get().strip()

        if not new_name and not new_value:
            messagebox.showerror("Error", "Enter a value to update!")
            return

        conn = connect_db()
        cur = conn.cursor()

        if category == "Student":
            if new_name and new_value:
                cur.execute("UPDATE students SET name = %s, roll_number = %s WHERE roll_number = %s", (new_name, new_value, old_value))
            elif new_name:
                cur.execute("UPDATE students SET name = %s WHERE roll_number = %s", (new_name, old_value))
            elif new_value:
                cur.execute("UPDATE students SET roll_number = %s WHERE roll_number = %s", (new_value, old_value))

        elif category == "Exam":
            if new_name and new_value:
                cur.execute("UPDATE exams SET exam_name = %s, exam_date = %s WHERE exam_name = %s", (new_name, new_value, old_value))
            elif new_name:
                cur.execute("UPDATE exams SET exam_name = %s WHERE exam_name = %s", (new_name, old_value))
            elif new_value:
                cur.execute("UPDATE exams SET exam_date = %s WHERE exam_name = %s", (new_value, old_value))

        elif category == "Room":
            if new_name and new_value:
                cur.execute("UPDATE rooms SET room_name = %s, capacity = %s WHERE room_name = %s", (new_name, new_value, old_value))
            elif new_name:
                cur.execute("UPDATE rooms SET room_name = %s WHERE room_name = %s", (new_name, old_value))
            elif new_value:
                cur.execute("UPDATE rooms SET capacity = %s WHERE room_name = %s", (new_value, old_value))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"{category} updated successfully!")
        update_window.destroy()

    # ✅ Save Button
    tk.Button(update_window, text="Save Update", command=save_update, width=20, bg="green", fg="white").pack(pady=5)
def open_delete_window():
    delete_window = tk.Toplevel(root)
    configure_window(delete_window, "Delete Records")

    tk.Label(delete_window, text="Select a Category to Delete", font=("Arial", 12, "bold")).pack(pady=10)

    category_var = tk.StringVar(delete_window)
    category_dropdown = ttk.Combobox(delete_window, textvariable=category_var, values=["Student", "Exam", "Room"], state="readonly", width=30)
    category_dropdown.pack(pady=5)
    category_dropdown.set("Student")  # Default selection

    search_label = tk.Label(delete_window, text="Search:")
    search_label.pack(pady=5)
    search_entry = tk.Entry(delete_window)
    search_entry.pack()

    listbox = tk.Listbox(delete_window, height=10)
    listbox.pack(fill=tk.BOTH, expand=True)

    def fetch_data(event=None):
        """Fetch data dynamically based on category selection."""
        search_text = search_entry.get().lower()
        listbox.delete(0, tk.END)

        conn = connect_db()
        cur = conn.cursor()

        category = category_var.get()
        if category == "Student":
            cur.execute("SELECT id, name, roll_number FROM students ORDER BY roll_number ASC")
            data = cur.fetchall()
            for item in data:
                if search_text in item[1].lower() or search_text in str(item[2]):
                    listbox.insert(tk.END, f"{item[2]} - {item[1]}")  # Roll No - Name
        elif category == "Exam":
            cur.execute("SELECT id, exam_name, exam_date FROM exams ORDER BY exam_date ASC")
            data = cur.fetchall()
            for item in data:
                if search_text in item[1].lower() or search_text in item[2]:
                    listbox.insert(tk.END, f"{item[1]} ({item[2]})")  # Exam Name (Date)
        elif category == "Room":
            cur.execute("SELECT id, room_name FROM rooms ORDER BY room_name ASC")
            data = cur.fetchall()
            for item in data:
                if search_text in item[1].lower():
                    listbox.insert(tk.END, item[1])  # Room Name
        
        conn.close()

    search_entry.bind("<KeyRelease>", fetch_data)
    category_dropdown.bind("<<ComboboxSelected>>", fetch_data)

    fetch_data()  # Fetch initial data

    def delete_record():
        """Delete the selected record based on the category."""
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an item to delete!")
            return
        
        selected_item = listbox.get(selected_index[0])
        category = category_var.get()

        conn = connect_db()
        cur = conn.cursor()

        if category == "Student":
            roll_number = selected_item.split(" - ")[0]
            cur.execute("DELETE FROM students WHERE roll_number = %s", (roll_number,))
        elif category == "Exam":
            exam_name = selected_item.split(" (")[0]
            cur.execute("DELETE FROM exams WHERE exam_name = %s", (exam_name,))
        elif category == "Room":
            room_name = selected_item
            cur.execute("DELETE FROM rooms WHERE room_name = %s", (room_name,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"{category} deleted successfully!")
        fetch_data()  # Refresh the listbox after deletion

    delete_button = tk.Button(delete_window, text="Delete", command=delete_record, width=20, bg="red", fg="white")
    delete_button.pack(pady=5)

def open_admin_login():
    root.withdraw()  # Hide main window when opening login
    login_window = tk.Toplevel(root)
    configure_window(login_window, "Admin Login")
    login_window.lift()  # Moves the window to the top
    login_window.focus_force()  # Forces focus to the window
    login_window.attributes("-topmost", True)  # Ensures it stays on top
    login_window.after(100, lambda: login_window.attributes("-topmost", False))  # Reset after 100ms
    tk.Label(login_window, text="Admin Login", font=("Arial", 14, "bold"), bg="#0056b3", fg="white", pady=10).pack(fill="x")
    
    frame = tk.Frame(login_window, bg="white", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Username:", font=("Arial", 12)).pack()
    entry_username = tk.Entry(frame, font=("Arial", 12), width=25)
    entry_username.pack(pady=5)

    tk.Label(frame, text="Password:", font=("Arial", 12)).pack()
    entry_password = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
    entry_password.pack(pady=5)

    def admin_login():
        if entry_username.get() == "admin" and entry_password.get() == "admin123":
            login_window.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(frame, text="Login", command=admin_login, width=15, height=2, bg="#28a745", fg="white").pack(pady=10)

    login_window.grab_set()  # Prevents root from interfering
    login_window.protocol("WM_DELETE_WINDOW", lambda: root.deiconify())  # Show root when closed

# Function to open Student Login Window
def open_student_login():
    root.withdraw()
    student_login_window = tk.Toplevel(root)
    configure_window(student_login_window, "Student Login")

    tk.Label(student_login_window, text="Student Login", font=("Arial", 14, "bold"), 
             bg="#0056b3", fg="white", pady=10).pack(fill="x")

    frame = tk.Frame(student_login_window, bg="white", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Username:", font=("Arial", 12), bg="white").pack(anchor="w")
    entry_username = tk.Entry(frame, font=("Arial", 12), width=25)
    entry_username.pack(pady=5)

    tk.Label(frame, text="Password:", font=("Arial", 12), bg="white").pack(anchor="w")
    entry_password = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
    entry_password.pack(pady=5)

    def student_login():
        if entry_username.get() == "student" and entry_password.get() == "123":
            student_login_window.destroy()
            open_student_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(frame, text="Login", command=student_login, width=15, height=2, 
              bg="#28a745", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    student_login_window.grab_set()
    student_login_window.protocol("WM_DELETE_WINDOW", lambda: root.deiconify())
def view_seating_arrangement(selected_date):
    if not selected_date:
        messagebox.showerror("Error", "Please select an exam date first!")
        return

    seating_window = tk.Toplevel(root)
    seating_window.title(f"Seating Arrangement for {selected_date}")
    seating_window.geometry("700x450")  # Increased size for better visibility

    tk.Label(seating_window, text=f"Seating Arrangement for {selected_date}", 
             font=("Arial", 12, "bold")).pack(pady=5)

    # 🔹 **Search Bar**
    tk.Label(seating_window, text="Search Student (by Roll No. or Name):").pack()
    search_entry = tk.Entry(seating_window)
    search_entry.pack(pady=5)

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT students.roll_number, students.name, rooms.room_name, seating_arrangement.seat_number, exams.exam_name
        FROM students
        JOIN seating_arrangement ON students.id = seating_arrangement.student_id
        JOIN rooms ON seating_arrangement.room_id = rooms.id
        JOIN exams ON seating_arrangement.exam_id = exams.id
        WHERE exams.exam_date = %s
        ORDER BY CAST(students.roll_number AS INTEGER) ASC
    """, (selected_date,))
    seating_data = cur.fetchall()
    conn.close()

    if not seating_data:
        messagebox.showerror("Error", "No seating arrangement found for this date!")
        return

    # 🔹 **Create Table to Show Seating Data**
    columns = ("Roll No", "Name", "Room", "Seat No", "Exam Name")
    tree = ttk.Treeview(seating_window, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for row in seating_data:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")

    # 🔹 **Real-time Search Function**
    def filter_students(event=None):
        search_text = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)  # Clear existing entries

        for row in seating_data:
            if search_text in row[1].lower() or search_text in str(row[0]):  # Search by name or roll number
                tree.insert("", "end", values=row)

    search_entry.bind("<KeyRelease>", filter_students)  # Trigger search when typing

def open_student_dashboard():
    student_window = tk.Toplevel(root)
    student_window.title("Student Dashboard")
    student_window.geometry("600x400")  # Same size as Add Student/Room/Exam windows
    student_window.resizable(False, False)
    student_window.configure(bg="white")

    tk.Label(student_window, text="Student Dashboard", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    # Fetch available exam dates from the database
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT exam_date FROM exams ORDER BY exam_date ASC")
    dates = cur.fetchall()
    conn.close()

    if not dates:
        messagebox.showerror("Error", "No exams found! Please ask the admin to add an exam.")
        student_window.destroy()
        return

    # Convert dates to string format
    date_options = [str(date[0]) for date in dates]

    tk.Label(student_window, text="Select Exam Date:", font=("Arial", 12), bg="white").pack()

    # ✅ Use Combobox instead of OptionMenu
    exam_date_var = tk.StringVar(student_window)
    exam_date_dropdown = ttk.Combobox(student_window, textvariable=exam_date_var, values=date_options, width=30)
    exam_date_dropdown.pack(pady=10)
    exam_date_dropdown.set(date_options[0])  # Set default value

    # View Seating Button
    view_button = tk.Button(student_window, text="View Seating Arrangement",
                            command=lambda: view_seating_arrangement(exam_date_var.get()), 
                            width=25, height=2, bg="#5DC1B9", fg="black", font=("Arial", 10, "bold"))
    view_button.pack(pady=10)

    # Logout Button
    logout_button = tk.Button(student_window, text="Logout", command=student_window.destroy,
                              width=25, height=2, bg="red", fg="white", font=("Arial", 10, "bold"))
    logout_button.pack(pady=10)




# Function to show Student Seating Arrangement
def show_student_seating():
    student_window = tk.Toplevel()
    student_window.title("Student Dashboard")

    tk.Label(student_window, text="Student Dashboard", font=("Arial", 14, "bold")).pack(pady=10)

    # Fetch available exam dates
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT exam_date FROM exams ORDER BY exam_date ASC")
    dates = cur.fetchall()
    conn.close()

    if not dates:
        messagebox.showerror("Error", "No exams found! Please ask the admin to add an exam.")
        student_window.destroy()
        return

    tk.Label(student_window, text="Select Exam Date:").pack()
    
    exam_date_var = tk.StringVar(student_window)
    date_dropdown = tk.OptionMenu(student_window, exam_date_var, *[str(date[0]) for date in dates])
    date_dropdown.pack()

def fetch_seating(selected_date):
    if not selected_date:
        messagebox.showerror("Error", "Please select an exam date first!")
        return

    conn = connect_db()
    cur = conn.cursor()

    # Fetch the exam ID and name based on the selected date
    cur.execute("SELECT id, exam_name FROM exams WHERE exam_date = %s", (selected_date,))
    exam = cur.fetchone()

    if not exam:
        messagebox.showerror("Error", "No exam found for this date!")
        conn.close()
        return

    exam_id, exam_name = exam

    # Fetch seating arrangement for this exam
    cur.execute("""
        SELECT students.roll_number, students.name, rooms.room_name, seating_arrangement.seat_number, exams.exam_name
        FROM students
        JOIN seating_arrangement ON students.id = seating_arrangement.student_id
        JOIN rooms ON seating_arrangement.room_id = rooms.id
        JOIN exams ON seating_arrangement.exam_id = exams.id
        WHERE seating_arrangement.exam_id = %s
        ORDER BY CAST(students.roll_number AS INTEGER) ASC
    """, (exam_id,))

    seating_data = cur.fetchall()
    conn.close()

    if not seating_data:
        messagebox.showerror("Error", "No seating arrangement found for this exam!")
        return

    # ✅ Show seating arrangement in a bigger window
    seating_window = tk.Toplevel(root)
    seating_window.title(f"Seating Arrangement for {exam_name} on {selected_date}")
    seating_window.geometry("700x450")  # Bigger window size

    tk.Label(seating_window, text=f"Seating Arrangement for {exam_name} on {selected_date}", 
             font=("Arial", 12, "bold")).pack(pady=5)

    # Search Bar
    tk.Label(seating_window, text="Search Student:").pack()
    search_entry = tk.Entry(seating_window)
    search_entry.pack()

    # Table to show seating data
    columns = ("Roll No", "Name", "Room", "Seat No", "Exam Name")
    tree = ttk.Treeview(seating_window, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for row in seating_data:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")

    # ✅ Real-time search function
    def filter_students(event=None):
        search_text = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)  # Clear current entries

        for row in seating_data:
            if search_text in row[1].lower() or search_text in row[0]:  
                tree.insert("", "end", values=row)

    search_entry.bind("<KeyRelease>", filter_students)  # Trigger search when typing

# Main Window
root = tk.Tk()
configure_window(root, "Exam Seating Management")

# Load and place image
image = Image.open("exam.jpg").resize((400, 500), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(root, image=photo)
image_label.place(x=0, y=0, width=400, height=500)

frame = tk.Frame(root, bg="white")
frame.place(relx=0.65, rely=0.35, anchor="center")

tk.Label(frame, text="Exam Seating Management", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

admin_button = tk.Button(frame, text="Admin Login", width=20, height=2,
                         font=("Arial", 12, "bold"), bg="#5A89E6", fg="white", command=open_admin_login)
admin_button.pack(pady=10)

student_button = tk.Button(frame, text="Student Login", width=20, height=2,
                           font=("Arial", 12, "bold"), bg="#5A89E6", fg="white", command=open_student_login)
student_button.pack(pady=10)

root.mainloop()