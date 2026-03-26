import customtkinter as ct
from tkinter import ttk, messagebox

class Course:
    def __init__(self, name, duration, description):
        self.name, self.duration, self.description = name, duration, description
    def to_dict(self):
        return {"Course Name": self.name, "Duration": self.duration, "Description": self.description}

class CourseView(ct.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent")
        self.manager, self.selected_index, self.C_Frame = manager, None, None
        self.setup_ui()
        self.show_course_table()

    def setup_ui(self):
        # Course Name Group 
        ct.CTkLabel(self, text="Course Name:", font=("Arial", 25), text_color="black").place(x=50, y=50)
        self.course_name_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white")        
        self.course_name_entry.place(x=50, y=90)

        # Duration Group 
        ct.CTkLabel(self, text="Duration (in months):", font=("Arial", 25), text_color="black").place(x=50, y=150)
        self.duration_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white")
        self.duration_entry.place(x=50, y=190)

        # Description Group 
        ct.CTkLabel(self, text="Description:", font=("Arial", 25), text_color="black").place(x=50, y=250)
        self.txt_description = ct.CTkTextbox(self, font=("Arial", 25), height=150, width=400, text_color="black", fg_color="white")
        self.txt_description.place(x=50, y=290)

        # Buttons Frame
        btn_frame = ct.CTkFrame(self, fg_color="transparent") 
        btn_frame.place(x=50, y=470)
        ct.CTkButton(btn_frame, text="Save", width=100, font=("Arial", 25), command=self.save_course).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Update", width=100, font=("Arial", 25), fg_color="green", hover_color="dark green", command=self.update_course).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Delete", width=100, font=("Arial", 25), fg_color="red", hover_color="dark red", command=self.delete_course).pack(side="left", padx=10)

        # Search Area
        ct.CTkLabel(self, text="Search Course Name:", font=("Arial", 25), text_color="black").place(x=550, y=50)
        self.search_entry = ct.CTkEntry(self, font=("Arial", 25), width=350, text_color="black", fg_color="white")
        self.search_entry.place(x=550, y=90)
        ct.CTkButton(self, text="Search", width=100, font=("Arial", 25), command=self.search_course).place(x=920, y=90)
        ct.CTkButton(self, text="Clear", width=100, font=("Arial", 25), command=self.clear_search_view).place(x=1040, y=90)

    def show_course_table(self, filtered=None):
        if self.C_Frame: self.C_Frame.destroy()
        self.C_Frame = ct.CTkFrame(self, fg_color="white", width=1300, height=450)
        self.C_Frame.place(x=550, y=140)
        
        data = filtered if filtered else self.manager.get_all_courses()
        
        #  REMOVED THE "cid" COLUMN 
        self.Table = ttk.Treeview(self.C_Frame, columns=("name","dur","desc"), show="headings")
        self.Table.heading("name", text="Course Name")
        self.Table.heading("dur", text="Duration")
        self.Table.heading("desc", text="Description", anchor="w")
        
        #  UPDATED COLUMN WIDTHS 
        self.Table.column("name", width=350, minwidth=350, stretch=False, anchor="w")
        self.Table.column("dur", width=150, minwidth=150, stretch=True, anchor="center")
        self.Table.column("desc", width=800, minwidth=800, stretch=True, anchor="w") 

        scroll_y = ttk.Scrollbar(self.C_Frame, orient="vertical", command=self.Table.yview)
        scroll_y.pack(side="right", fill="y")
        self.Table.configure(yscrollcommand=scroll_y.set)

        self.Table.pack(fill="both", expand=True)

        for i, c in enumerate(data): 
            self.Table.insert("", "end", iid=i, values=(c["Course Name"], c["Duration"], c["Description"]))
            
        self.Table.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        sel = self.Table.selection()
        if not sel: return
        self.selected_index = int(sel[0])
        all_courses = self.manager.get_all_courses()
        c = all_courses[self.selected_index]
        
        self.clear_entries()
        self.course_name_entry.insert(0, c["Course Name"])
        self.duration_entry.insert(0, c["Duration"])
        self.txt_description.insert("1.0", c["Description"])

    def clear_entries(self):
        self.course_name_entry.delete(0, "end")
        self.duration_entry.delete(0, "end")
        self.txt_description.delete("1.0", "end")

    def clear_search_view(self):
        self.search_entry.delete(0, 'end')
        self.show_course_table()
        
    def save_course(self):
        n = self.course_name_entry.get().strip()
        d = self.duration_entry.get().strip()
        de = self.txt_description.get("1.0", "end-1c").strip()

        if not n or not d or not de: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        if n.isdigit():
            messagebox.showerror("Format Error", "Course Name can not be a number")
            return

        for c in self.manager.get_all_courses():
            if c["Course Name"].lower() == n.lower():
                messagebox.showerror("Duplicate Error", f"A course named '{n}' already exists!")
                return
        
        if not d.isdigit(): 
            messagebox.showerror("Format Error", "Duration must be an Integer number.") 
            return
            
        elif int(d) > 12:
            messagebox.showerror("Limit Error", "Course duration cannot exceed 12 months.")
            return
        
        if de.isdigit():
            messagebox.showerror("Format Error", "Description can not be a number")
            return        
        
        self.manager.add_course(Course(n, d, de))

        messagebox.showinfo("Success", f"Course '{n}' has been saved successfully.")
        self.clear_entries()      
        self.show_course_table()  

    def update_course(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please click a row in the table to select it first!")
            return

        n = self.course_name_entry.get().strip()
        d = self.duration_entry.get().strip()
        de = self.txt_description.get("1.0", "end-1c").strip()

        if not n or not d or not de: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
        
        if n.isdigit():
            messagebox.showerror("Format Error", "Course Name can not be a number")
            return

        for i, c in enumerate(self.manager.get_all_courses()):
            if i != self.selected_index and c["Course Name"].lower() == n.lower():
                messagebox.showerror("Duplicate Error", f"A course named '{n}' already exists!")
                return
        
        if not d.isdigit(): 
            messagebox.showerror("Format Error", "Duration must be a whole number.\nSymbols and letters are not allowed.") 
            return
            
        elif int(d) > 12:
            messagebox.showerror("Limit Error", "Course duration cannot exceed 12 months.")
            return
        
        if de.isdigit():
            messagebox.showerror("Format Error", "Description can not be a number")
            return        

        self.manager.update_course(self.selected_index, Course(n, d, de))
        messagebox.showinfo("Success", f"Course '{n}' updated successfully!")
        
        self.selected_index = None
        self.clear_entries()
        self.show_course_table()

    def delete_course(self):
        if self.selected_index is None:
            messagebox.showwarning("Selection Error", "Please select a course from the table to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure? This will permanently remove this course."):
            self.manager.delete_course(self.selected_index)
            messagebox.showinfo("Deleted", "Course has been removed from the database.")
            
            self.selected_index = None
            self.clear_entries()
            self.show_course_table()

    def search_course(self):
        query = self.search_entry.get().lower().strip()
        if not query:
            self.show_course_table()
            return
            
        found = self.manager.search_courses(query)
        if found: 
            self.show_course_table(found)
        else: 
            messagebox.showinfo("No Match", "No course found matching your search")