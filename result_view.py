import customtkinter as ct
from tkinter import ttk, messagebox

class Result:
    def __init__(self, roll, course, marks, grade):
        self.roll, self.course, self.marks, self.grade = roll, course, marks, grade
    def to_dict(self):
        return {"Roll": self.roll, "Course": self.course, "Marks": self.marks, "Grade": self.grade}

class ResultView(ct.CTkFrame):
    def __init__(self, parent, r_manager, s_manager, c_manager):
        super().__init__(parent, fg_color="transparent")
        self.r_manager = r_manager
        self.s_manager = s_manager
        self.c_manager = c_manager
        self.selected_index = None
        self.R_Frame = None
        
        self.setup_ui()
        self.show_result_table()

    def setup_ui(self):
        # Dynamically load student rolls and courses for the dropdowns
        student_rolls = [s["Roll"] for s in self.s_manager.get_all_students()]
        course_names = [c["Course Name"] for c in self.c_manager.get_all_courses()]
        
        if not student_rolls: student_rolls = ["No Students Found"]
        if not course_names: course_names = ["No Courses Found"]

        #  Roll Number Selection 
        ct.CTkLabel(self, text="Select Student Roll:", font=("Arial", 25), text_color="black").place(x=50, y=50)
        self.roll_combo = ct.CTkComboBox(self, values=student_rolls, font=("Arial", 25), width=400,
                                         text_color="black", fg_color="white", border_width=1, border_color="black",
                                         dropdown_fg_color="white", dropdown_text_color="black")
        self.roll_combo.place(x=50, y=90)
        
        #  Course Selection 
        ct.CTkLabel(self, text="Select Course:", font=("Arial", 25), text_color="black").place(x=50, y=140)
        self.course_combo = ct.CTkComboBox(self, values=course_names, font=("Arial", 25), width=400,
                                           text_color="black", fg_color="white", border_width=1, border_color="black",
                                           dropdown_fg_color="white", dropdown_text_color="black")
        self.course_combo.place(x=50, y=180)
        
        #  Marks Input 
        ct.CTkLabel(self, text="Marks (0-100):", font=("Arial", 25), text_color="black").place(x=50, y=230)
        self.marks_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.marks_entry.place(x=50, y=270)
        
        #  Grade Display (Read-Only) 
        ct.CTkLabel(self, text="Auto-Calculated Grade:", font=("Arial", 25), text_color="black").place(x=50, y=320)
        self.grade_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="gray", fg_color="#F0F0F0", border_width=1, border_color="black")
        self.grade_entry.place(x=50, y=360)
        self.grade_entry.insert(0, "Will calculate on save...")
        self.grade_entry.configure(state="disabled") # Prevent manual typing

        #  Button Frame 
        btn_frame = ct.CTkFrame(self, fg_color="transparent")
        btn_frame.place(x=50, y=440)
        ct.CTkButton(btn_frame, text="Save", width=100, font=("Arial", 25), command=self.save_result).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Update", width=100, font=("Arial", 25), fg_color="green", hover_color="dark green", command=self.update_result).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Delete", width=100, font=("Arial", 25), fg_color="red", hover_color="dark red", command=self.delete_result).pack(side="left", padx=10)

        #  Search Area 
        ct.CTkLabel(self, text="Search Roll:", font=("Arial", 25), text_color="black").place(x=550, y=50)
        self.search_entry = ct.CTkEntry(self, font=("Arial", 25), width=350, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.search_entry.place(x=550, y=90)
        ct.CTkButton(self, text="Search", width=100, font=("Arial", 25), command=self.search_result).place(x=920, y=90)
        ct.CTkButton(self, text="Clear", width=100, font=("Arial", 25), command=self.clear_search_view).place(x=1040, y=90)

    def show_result_table(self, filtered=None):
        if self.R_Frame: self.R_Frame.destroy()
        
        self.R_Frame = ct.CTkFrame(self, fg_color="white", width=1100, height=450)
        self.R_Frame.place(x=550, y=140)
        
        data = filtered if filtered else self.r_manager.get_all_results()
        
        self.Table = ttk.Treeview(self.R_Frame, columns=("r","c","m","g"), show="headings")
        cols = {"r":"Roll Number", "c":"Course", "m":"Marks", "g":"Grade"}
        for k, v in cols.items(): 
            self.Table.heading(k, text=v)
        
        self.Table.column("r", width=150, anchor="center")
        self.Table.column("c", width=350, anchor="w")
        self.Table.column("m", width=150, anchor="center")
        self.Table.column("g", width=150, anchor="center")
        
        scroll_y = ttk.Scrollbar(self.R_Frame, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.Table.pack(fill="both", expand=True)
        
        for i, r in enumerate(data): 
            self.Table.insert("", "end", iid=i, values=(r["Roll"], r["Course"], r["Marks"], r["Grade"]))
        self.Table.bind("<<TreeviewSelect>>", self.on_select)

    def calculate_grade(self, marks):
        m = int(marks)
        if m >= 90: return "A+"
        elif m >= 85: return "A"
        elif m >= 80: return "B+"
        elif m >= 75: return "B"
        elif m >= 70: return "C+"
        elif m >= 65: return "C"
        elif m >= 60: return "D"
        else: return "F"

    def on_select(self, event):
        sel = self.Table.selection()
        if not sel: return
        self.selected_index = int(sel[0])
        r = self.r_manager.get_all_results()[self.selected_index]
        
        self.marks_entry.delete(0, "end")
        self.roll_combo.set(r["Roll"])
        self.course_combo.set(r["Course"])
        self.marks_entry.insert(0, r["Marks"])
        
        # Update the read-only grade field
        self.grade_entry.configure(state="normal")
        self.grade_entry.delete(0, "end")
        self.grade_entry.insert(0, r["Grade"])
        self.grade_entry.configure(state="disabled")

    def clear_entries(self):
        self.marks_entry.delete(0, "end")
        self.grade_entry.configure(state="normal")
        self.grade_entry.delete(0, "end")
        self.grade_entry.insert(0, "Will calculate on save...")
        self.grade_entry.configure(state="disabled")

    def clear_search_view(self):
        self.search_entry.delete(0, 'end')
        self.show_result_table()

    def save_result(self):
        r = self.roll_combo.get().strip()
        c = self.course_combo.get().strip()
        m = self.marks_entry.get().strip()
        
        if not r or not c or not m or r == "No Students Found" or c == "No Courses Found": 
            messagebox.showerror("Input Error", "Valid Roll, Course, and Marks are required!")
            return
            
        if not m.isdigit():
            messagebox.showerror("Format Error", "Marks must be a whole number.")
            return
            
        if not (0 <= int(m) <= 100):
            messagebox.showerror("Limit Error", "Marks must be between 0 and 100.")
            return

        grade = self.calculate_grade(m)
        
        success, msg = self.r_manager.add_result(Result(r, c, m, grade))
        if success:
            messagebox.showinfo("Success", f"Grade {grade} saved for Roll {r}!")
            self.clear_entries()
            self.show_result_table()
        else:
            messagebox.showerror("Duplicate Error", msg)

    def update_result(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please click a row in the table to select it first!")
            return
            
        r = self.roll_combo.get().strip()
        c = self.course_combo.get().strip()
        m = self.marks_entry.get().strip()
        
        if not r or not c or not m: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
            
        if not m.isdigit():
            messagebox.showerror("Format Error", "Marks must be a whole number.")
            return
            
        if not (0 <= int(m) <= 100):
            messagebox.showerror("Limit Error", "Marks must be between 0 and 100.")
            return

        grade = self.calculate_grade(m)
        
        self.r_manager.update_result(self.selected_index, Result(r, c, m, grade))
        messagebox.showinfo("Success", "Result updated successfully!")
        self.selected_index = None
        self.clear_entries()
        self.show_result_table()

    def delete_result(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please select a result from the table to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure? This will permanently remove this result."):
            self.r_manager.delete_result(self.selected_index)
            messagebox.showinfo("Deleted", "Result has been removed.")
            self.selected_index = None
            self.clear_entries()
            self.show_result_table()

    def search_result(self):
        query = self.search_entry.get().strip()
        if not query:
            self.show_result_table()
            return
            
        found = self.r_manager.search_results(query)
        if found: 
            self.show_result_table(found)
        else: 
            messagebox.showinfo("No Match", "No results found for that Roll Number.")