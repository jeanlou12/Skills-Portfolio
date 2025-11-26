import tkinter as tk
from tkinter import ttk, messagebox
import os

DATA_FILE = "studentmarks.text.txt"
MAX_CW = 20
MAX_EXAM = 100

def load_students():
    """Loads student data from the file, handling potential bad data."""
    if not os.path.exists(DATA_FILE):
        return []

    students = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 6:
                continue
            code, name, c1, c2, c3, exam = parts
            try:
                # Robustly attempt to convert marks to integers
                students.append({
                    "code": code,
                    "name": name,
                    "cw1": int(c1),
                    "cw2": int(c2),
                    "cw3": int(c3),
                    "exam": int(exam),
                })
            except ValueError:
                # Skip corrupted records and inform the user (optional, but good practice)
                print(f"Skipping corrupted record: {line.strip()}")
                continue
    return students

def save_students(students):
    """Saves student data back to the file."""
    with open(DATA_FILE, "w") as f:
        for s in students:
            # Ensure data being saved is correctly formatted
            f.write(f"{s['code']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n")

def validate_marks(cw1_str, cw2_str, cw3_str, exam_str):
    """Validates mark inputs are integers and within defined limits."""
    try:
        cw1 = int(cw1_str)
        cw2 = int(cw2_str)
        cw3 = int(cw3_str)
        exam = int(exam_str)
    except ValueError:
        return False, "All coursework and exam marks must be integers."

    if not (0 <= cw1 <= MAX_CW and 0 <= cw2 <= MAX_CW and 0 <= cw3 <= MAX_CW):
        return False, f"CW marks must be between 0 and {MAX_CW}."
    if not (0 <= exam <= MAX_EXAM):
        return False, f"Exam mark must be between 0 and {MAX_EXAM}."

    return True, (cw1, cw2, cw3, exam)



#   MAIN APP CONTROLLER

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager System")
        self.geometry("900x650")
        self.resizable(True, True) 
        # Styling
        style = ttk.Style()
        style.theme_use("clam") 
        style.configure("Title.TLabel", font=("Helvetica", 28, "bold"), foreground="#1313CB")
        style.configure("Primary.TButton", font=("Helvetica", 14), padding=10, background="#3498DB", foreground="black")
        style.map("Primary.TButton", background=[('active', "#D6892C")])
        style.configure("Section.TLabel", font=("Helvetica", 18, "bold"), foreground="#54E5C8")
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Consolas", 11), rowheight=25)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        
        for F in (CoverPage, MenuPage, ViewAllFrame, IndividualViewFrame, DataModificationFrame):
            name = F.__name__
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.attributes("-alpha", 0.0)
        self.fade_in()
        self.show_frame("CoverPage")

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1:
            alpha += 0.04
            self.attributes("-alpha", alpha)
            self.after(25, self.fade_in)

    def show_frame(self, name, **kwargs):
        """Switches to the specified frame and refreshes it if needed."""
        frame = self.frames[name]
        if hasattr(frame, "refresh"):
            # Pass  to refresh
            frame.refresh(**kwargs)
        frame.tkraise()

    def show_top_bottom_record(self, mode):
        """Finds and displays the student with the highest or lowest total score."""
        students = load_students()
        if not students:
            messagebox.showwarning("Warning", "No student data available!")
            return

        for s in students:
            s["total"] = s["cw1"] + s["cw2"] + s["cw3"] + s["exam"]

       
        if not students:
             messagebox.showwarning("Warning", "No valid student data to analyze!")
             return

        
        student = max(students, key=lambda x: x["total"]) if mode == "highest" else min(students, key=lambda x: x["total"])

        messagebox.showinfo(
            f"{mode.capitalize()} Score Result",
            f"STUDENT WITH {mode.upper()} TOTAL SCORE:\n\n"
            f"Code: {student['code']}\n"
            f"Name: {student['name']}\n"
            f"CW1: {student['cw1']}, CW2: {student['cw2']}, CW3: {student['cw3']}, Exam: {student['exam']}\n"
            f"TOTAL: {student['total']}"
        )


# Cover Page
class CoverPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="150 150 150 150")
        # Content
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        content_frame = ttk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew")

        ttk.Label(content_frame, text="STUDENT MANAGER SYSTEM", style="Title.TLabel").pack(pady=40)
        ttk.Label(content_frame, text="Analyse Marks • Manage Data • View Records",
                  font=("Helvetica", 16), foreground="#555").pack(pady=15)
        ttk.Button(content_frame, text="ENTER →", style="Primary.TButton",
                   command=lambda: controller.show_frame("MenuPage")).pack(fill="x", pady=50)


# MENU PAGE
class MenuPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=40)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        ttk.Label(self, text="MAIN MENU", style="Title.TLabel").grid(row=0, columnspan=2, pady=30)

        # VIEW & ANALYSE
        view_frame = ttk.LabelFrame(self, text="VIEW & ANALYSE", padding=15)
        view_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # DATA MANAGEMENT
        data_frame = ttk.LabelFrame(self, text="🗂 DATA MANAGEMENT", padding=15)
        data_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Configure frames to expand equally
        self.grid_rowconfigure(1, weight=1)

        # Buttons for VIEW & ANALYSE
        for idx, (text, func) in enumerate([
            ("View All Student Records (Table)", lambda: controller.show_frame("ViewAllFrame")),
            ("View Individual Student", lambda: controller.show_frame("IndividualViewFrame")),
            ("Student With Highest Total Score", lambda: controller.show_top_bottom_record("highest")),
            ("Student With Lowest Total Score", lambda: controller.show_top_bottom_record("lowest")),
        ]):
            view_frame.columnconfigure(0, weight=1)
            ttk.Button(view_frame, text=text, style="Primary.TButton", command=func).pack(fill="x", pady=8, ipady=5)

        # Buttons for DATA MANAGEMENT
        for idx, (text, action) in enumerate([
            
            ("Sort Student Records (by Name)", lambda: controller.show_frame("ViewAllFrame", sort_by_name=True)),
            ("Add New Student Record", "add"),
            ("Delete Student Record", "delete"),
            ("Update Existing Student Record", "update"),
        ]):
            data_frame.columnconfigure(0, weight=1)
            if isinstance(action, str):
                # Data modification buttons
                ttk.Button(data_frame, text=text, style="Primary.TButton",
                           command=lambda a=action: controller.show_frame("DataModificationFrame", action=a)
                           ).pack(fill="x", pady=8, ipady=5)
            else:
                # Sort button 
                 ttk.Button(data_frame, text=text, style="Primary.TButton", command=action).pack(fill="x", pady=8, ipady=5)


        # BACK button
        ttk.Button(self, text="← BACK TO COVER", style="Primary.TButton",
                   command=lambda: controller.show_frame("CoverPage")).grid(row=2, columnspan=2, sticky="ew", pady=20)



#   VIEW ALL STUDENTS 

class ViewAllFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ttk.Label(self, text="ALL STUDENT RECORDS", style="Title.TLabel").grid(row=0, column=0, pady=10)

        # Treeview Setup
        columns = ("code", "name", "cw1", "cw2", "cw3", "exam", "total")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # Define Headings and Widths
        self.tree.heading("code", text="Code")
        self.tree.heading("name", text="Name")
        self.tree.heading("cw1", text=f"CW1 (/{MAX_CW})")
        self.tree.heading("cw2", text=f"CW2 (/{MAX_CW})")
        self.tree.heading("cw3", text=f"CW3 (/{MAX_CW})")
        self.tree.heading("exam", text=f"EXAM (/{MAX_EXAM})")
        self.tree.heading("total", text="Total")

        self.tree.column("code", width=80, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("cw1", width=70, anchor="center")
        self.tree.column("cw2", width=70, anchor="center")
        self.tree.column("cw3", width=70, anchor="center")
        self.tree.column("exam", width=80, anchor="center")
        self.tree.column("total", width=80, anchor="center")

        self.tree.grid(row=1, column=0, sticky="nsew", pady=10)

        # Add scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=hsb.set)

        ttk.Button(self, text="← BACK TO MENU", style="Primary.TButton",
                   command=lambda: controller.show_frame("MenuPage")).grid(row=3, column=0, sticky="ew", pady=10)

    def refresh(self, sort_by_name=False):
        """Loads and displays student data in the Treeview, with optional sorting."""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        students = load_students()
        
        # Calculate total and prepare data
        for s in students:
            s["total"] = s["cw1"] + s["cw2"] + s["cw3"] + s["exam"]

        if sort_by_name:
            students.sort(key=lambda s: s["name"].lower())

        # Insert new data
        for s in students:
            self.tree.insert("", tk.END, values=(
                s["code"], s["name"], s["cw1"], s["cw2"], s["cw3"], s["exam"], s["total"]
            ))



#   INDIVIDUAL VIEW

class IndividualViewFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=40)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1) #  result frame to expand

        ttk.Label(self, text="VIEW INDIVIDUAL STUDENT", style="Title.TLabel").grid(row=0, column=0, pady=20)

        input_frame = ttk.Frame(self)
        input_frame.grid(row=1, column=0, sticky="ew", pady=10)
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Student Code:").grid(row=0, column=0, padx=5)
        self.code_entry = ttk.Entry(input_frame)
        self.code_entry.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Button(input_frame, text="SEARCH", style="Primary.TButton",
                   command=self.search_student).grid(row=0, column=2, padx=5)

        result_frame = ttk.Frame(self)
        result_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        
        self.result = tk.Text(result_frame, height=12, font=("Consolas", 13), wrap="word", relief="groove", borderwidth=2)
        self.result.pack(side="left", fill="both", expand=True)
        self.result.config(state=tk.DISABLED) 

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result.yview)
        scrollbar.pack(side="right", fill="y")
        self.result.config(yscrollcommand=scrollbar.set)

        ttk.Button(self, text="← BACK", style="Primary.TButton",
                   command=lambda: controller.show_frame("MenuPage")).grid(row=4, column=0, sticky="ew", pady=10)

    def refresh(self):
        """Clears the fields when returning to this page."""
        self.code_entry.delete(0, tk.END)
        self.result.config(state=tk.NORMAL)
        self.result.delete("1.0", tk.END)
        self.result.config(state=tk.DISABLED)

    def search_student(self):
        code = self.code_entry.get().strip()
        self.result.config(state=tk.NORMAL)
        self.result.delete("1.0", tk.END)

        if not code:
            self.result.insert(tk.END, "Please enter a student code to search.")
            self.result.config(state=tk.DISABLED)
            return

        students = load_students()
        
        found_student = None
        for s in students:
            if s["code"].lower() == code.lower(): 
                found_student = s
                break
        
        if found_student:
            s = found_student
            total = s["cw1"] + s["cw2"] + s["cw3"] + s["exam"]
            
            output = (
                f"--- Student Record ---\n\n"
                f"Code: {s['code']}\n"
                f"Name: {s['name']}\n\n"
                f"CW1 ({MAX_CW}): {s['cw1']}\n"
                f"CW2 ({MAX_CW}): {s['cw2']}\n"
                f"CW3 ({MAX_CW}): {s['cw3']}\n"
                f"Exam ({MAX_EXAM}): {s['exam']}\n\n"
                f"Total Score: {total} / {3 * MAX_CW + MAX_EXAM}"
            )
            self.result.insert(tk.END, output)
        else:
            messagebox.showwarning("Not found", f"Student code '{code}' not found in records.")
            self.result.insert(tk.END, f"Student code '{code}' not found.")

        self.result.config(state=tk.DISABLED)



#   ADD / DELETE / UPDATE

class DataModificationFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=40)
        self.controller = controller
        self.action = None

        self.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self, text="", style="Title.TLabel")
        self.title_label.grid(row=0, column=0, pady=20)

       
        input_frame = ttk.Frame(self)
        input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        input_frame.columnconfigure(1, weight=1)

        self.entries = {}
        fields = [
            ("code", "Student Code:"),
            ("name", "Name:"),
            ("cw1", f"CW1 (0-{MAX_CW}):"),
            ("cw2", f"CW2 (0-{MAX_CW}):"),
            ("cw3", f"CW3 (0-{MAX_CW}):"),
            ("exam", f"Exam (0-{MAX_EXAM}):")
        ]
        
        for i, (field, label_text) in enumerate(fields):
            ttk.Label(input_frame, text=label_text).grid(row=i, column=0, sticky="w", pady=5, padx=5)
            entry = ttk.Entry(input_frame)
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=5)
            self.entries[field] = entry

        ttk.Button(self, text="CONFIRM ACTION", style="Primary.TButton",
                   command=self.perform_action).grid(row=2, column=0, sticky="ew", pady=10)
        ttk.Button(self, text="← BACK TO MENU", style="Primary.TButton",
                   command=lambda: controller.show_frame("MenuPage")).grid(row=3, column=0, sticky="ew", pady=5)

    def refresh(self, action):
        """Sets up the frame for the specific action (add, delete, update)."""
        self.action = action
        self.title_label.config(text=f"{action.upper()} STUDENT RECORD")
        
        # Clear all 
        for e in self.entries.values():
            e.delete(0, tk.END)
        
        # Configure which fields are required/disabled based on action
        is_add_or_update = action in ("add", "update")
        
        self.entries["name"].config(state=tk.NORMAL if is_add_or_update else tk.DISABLED)
        self.entries["cw1"].config(state=tk.NORMAL if is_add_or_update else tk.DISABLED)
        self.entries["cw2"].config(state=tk.NORMAL if is_add_or_update else tk.DISABLED)
        self.entries["cw3"].config(state=tk.NORMAL if is_add_or_update else tk.DISABLED)
        self.entries["exam"].config(state=tk.NORMAL if is_add_or_update else tk.DISABLED)
        
        self.entries["code"].config(state=tk.NORMAL) 
    def perform_action(self):
        code = self.entries["code"].get().strip()
        students = load_students()

        if not code:
            messagebox.showwarning("Input Error", "Student code cannot be empty.")
            return

       
        if self.action == "add":
            if any(s["code"].lower() == code.lower() for s in students):
                messagebox.showerror("Error", f"Student code '{code}' already exists. Use 'Update' instead.")
                return

            # Validate marks
            valid, result = validate_marks(
                self.entries["cw1"].get(), self.entries["cw2"].get(), self.entries["cw3"].get(), self.entries["exam"].get()
            )
            if not valid:
                messagebox.showerror("Input Error", result)
                return
            
            cw1, cw2, cw3, exam = result
            
            new_s = {
                "code": code,
                "name": self.entries["name"].get().strip(),
                "cw1": cw1,
                "cw2": cw2,
                "cw3": cw3,
                "exam": exam,
            }
            students.append(new_s)
            save_students(students)
            messagebox.showinfo("Success", f"Student '{code}' added successfully!")
            self.controller.show_frame("MenuPage")


        #  DELETE ACTION 
        elif self.action == "delete":
            initial_count = len(students)
            students = [s for s in students if s["code"].lower() != code.lower()]
            
            if len(students) < initial_count:
                save_students(students)
                messagebox.showinfo("Success", f"Student '{code}' deleted successfully!")
                self.controller.show_frame("MenuPage")
            else:
                messagebox.showwarning("Error", f"Student code '{code}' not found.")


        #  UPDATE 
        elif self.action == "update":
            # 1. Validate marks
            valid, result = validate_marks(
                self.entries["cw1"].get(), self.entries["cw2"].get(), self.entries["cw3"].get(), self.entries["exam"].get()
            )
            if not valid:
                messagebox.showerror("Input Error", result)
                return
            
            cw1, cw2, cw3, exam = result

            # 2.  update the record
            found = False
            for s in students:
                if s["code"].lower() == code.lower():
                    s["name"] = self.entries["name"].get().strip()
                    s["cw1"] = cw1
                    s["cw2"] = cw2
                    s["cw3"] = cw3
                    s["exam"] = exam
                    found = True
                    break
            
            if found:
                save_students(students)
                messagebox.showinfo("Success", f"Record for '{code}' updated successfully!")
                self.controller.show_frame("MenuPage")
            else:
                messagebox.showwarning("Error", f"Student code '{code}' not found for update.")

        #  UNKNOWN ACTION 
        else:
            messagebox.showerror("System Error", "Unknown action requested.")




if __name__ == "__main__":
    App().mainloop()