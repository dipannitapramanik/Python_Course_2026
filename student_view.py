import customtkinter as ct
from tkinter import ttk, messagebox

class Student:
    def __init__(self, roll, name, phone, gender, address):
        self.roll, self.name, self.phone, self.gender, self.address = roll, name, phone, gender, address
    def to_dict(self):
        return {"Roll": self.roll, "Name": self.name, "Phone": self.phone, "Gender": self.gender, "Address": self.address}

class StudentView(ct.CTkFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, fg_color="transparent")
        self.manager, self.selected_index, self.S_Frame = manager, None, None
        self.setup_ui()
        self.show_student_table()

    def setup_ui(self):
        #  Roll Number 
        ct.CTkLabel(self, text="Roll Number:", font=("Arial", 25), text_color="black").place(x=50, y=50)
        self.roll_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.roll_entry.place(x=50, y=90)
        
        #  Full Name 
        ct.CTkLabel(self, text="Full Name:", font=("Arial", 25), text_color="black").place(x=50, y=140)
        self.name_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.name_entry.place(x=50, y=180)
        
        #  Phone 
        ct.CTkLabel(self, text="Phone Number:", font=("Arial", 25), text_color="black").place(x=50, y=230)
        self.phone_entry = ct.CTkEntry(self, font=("Arial", 25), width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.phone_entry.place(x=50, y=270)
        
        #  Gender (ComboBox) 
        ct.CTkLabel(self, text="Gender:", font=("Arial", 25), text_color="black").place(x=50, y=320)
        self.gender_combo = ct.CTkComboBox(self, values=["Male", "Female"], font=("Arial", 25), width=400,
                                           text_color="black", fg_color="white", border_width=1, border_color="black",
                                           dropdown_fg_color="white", dropdown_text_color="black")
        self.gender_combo.place(x=50, y=360)
        
  
        ct.CTkLabel(self, text="Address:", font=("Arial", 25), text_color="black").place(x=50, y=410)
        self.address_entry = ct.CTkTextbox(self, font=("Arial", 25), height=100, width=400, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.address_entry.place(x=50, y=450)

        #  Button Frame (Moved down slightly to accommodate the textbox height) 
        btn_frame = ct.CTkFrame(self, fg_color="transparent")
        btn_frame.place(x=50, y=570)
        ct.CTkButton(btn_frame, text="Save", width=100, font=("Arial", 25), command=self.save_student).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Update", width=100, font=("Arial", 25), fg_color="green", hover_color="dark green", command=self.update_student).pack(side="left", padx=10)
        ct.CTkButton(btn_frame, text="Delete", width=100, font=("Arial", 25), fg_color="red", hover_color="dark red", command=self.delete_student).pack(side="left", padx=10)

        #  Search Area 
        ct.CTkLabel(self, text="Search Roll:", font=("Arial", 25), text_color="black").place(x=550, y=50)
        self.search_entry = ct.CTkEntry(self, font=("Arial", 25), width=350, text_color="black", fg_color="white", border_width=1, border_color="black")
        self.search_entry.place(x=550, y=90)
        ct.CTkButton(self, text="Search", width=100, font=("Arial", 25), command=self.search_student).place(x=920, y=90)
        ct.CTkButton(self, text="Clear", width=100, font=("Arial", 25), command=self.clear_search_view).place(x=1040, y=90)

    def show_student_table(self, filtered=None):
        if self.S_Frame: self.S_Frame.destroy()
        
        self.S_Frame = ct.CTkFrame(self, fg_color="white", width=1100, height=450)
        self.S_Frame.place(x=550, y=140)
        
        data = filtered if filtered else self.manager.get_all_students()
        
        self.Table = ttk.Treeview(self.S_Frame, columns=("r","n","p","g","a"), show="headings")
        cols = {"r":"Roll", "n":"Name", "p":"Phone", "g":"Gender", "a":"Address"}
        for k, v in cols.items(): 
            self.Table.heading(k, text=v)
        
        self.Table.column("r", width=100, anchor="center")
        self.Table.column("n", width=250, anchor="w")
        self.Table.column("p", width=180, anchor="center")
        self.Table.column("g", width=120, anchor="center")
        self.Table.column("a", width=400, anchor="w")
        
        scroll_y = ttk.Scrollbar(self.S_Frame, orient="vertical", command=self.Table.yview)
        self.Table.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.Table.pack(fill="both", expand=True)
        
        for i, s in enumerate(data): 
            self.Table.insert("", "end", iid=i, values=(s["Roll"], s["Name"], s["Phone"], s["Gender"], s["Address"]))
        self.Table.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        sel = self.Table.selection()
        if not sel: return
        self.selected_index = int(sel[0])
        s = self.manager.get_all_students()[self.selected_index]
        
        self.clear_entries()
        self.roll_entry.insert(0, s["Roll"])
        self.name_entry.insert(0, s["Name"])
        self.phone_entry.insert(0, s["Phone"])
        self.gender_combo.set(s["Gender"])
        self.address_entry.insert("1.0", s["Address"])

    def clear_entries(self):
        self.roll_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.address_entry.delete("1.0", "end")
        self.gender_combo.set("Male")

    def clear_search_view(self):
        self.search_entry.delete(0, 'end')
        self.show_student_table()

    def save_student(self):
        r = self.roll_entry.get().strip()
        n = self.name_entry.get().strip()
        p = self.phone_entry.get().strip()
        g = self.gender_combo.get()
        a = self.address_entry.get("1.0", "end-1c").strip()
        
        if not r or not n or not p or not a: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
            
        if not r.isdigit():
            messagebox.showerror("Format Error", "Roll Number must contain only numbers.")
            return
        if not p.isdigit():
            messagebox.showerror("Format Error", "Phone Number must contain only numbers.")
            return
        
        if len(p)!=11:
            messagebox.showerror("Format Error", "Phone Number can not be more or less than 11 digit")
            return

        if n.isdigit():
            messagebox.showerror("Format Error", "Name cannot be a number.")
            return
            
        self.manager.add_student(Student(r, n, p, g, a))
        messagebox.showinfo("Success", f"Student '{n}' has been saved successfully.")
        self.clear_entries()
        self.show_student_table()

    def update_student(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please click a row in the table to select it first!")
            return
            
        r = self.roll_entry.get().strip()
        n = self.name_entry.get().strip()
        p = self.phone_entry.get().strip()
        g = self.gender_combo.get()
        a = self.address_entry.get("1.0", "end-1c").strip()
        
        if not r or not n or not p or not a: 
            messagebox.showerror("Input Error", "All fields are required!")
            return
            
        if not r.isdigit():
            messagebox.showerror("Format Error", "Roll Number must contain only numbers.")
            return
        if not p.isdigit():
            messagebox.showerror("Format Error", "Phone Number must contain only numbers.")
            return
        
        if len(p)!=11:
            messagebox.showerror("Format Error", "Phone Number can not be more or less than 11 digit")
            return

        if n.isdigit():
            messagebox.showerror("Format Error", "Name cannot be a number.")
            return
            
        self.manager.update_student(self.selected_index, Student(r, n, p, g, a))
        messagebox.showinfo("Success", f"Student '{n}' updated successfully!")
        self.selected_index = None
        self.clear_entries()
        self.show_student_table()

    def delete_student(self):
        if self.selected_index is None: 
            messagebox.showwarning("Selection Error", "Please select a student from the table to delete.")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure? This will permanently remove this student."):
            self.manager.delete_student(self.selected_index)
            messagebox.showinfo("Deleted", "Student has been removed from the database.")
            self.selected_index = None
            self.clear_entries()
            self.show_student_table()

    def search_student(self):
        query = self.search_entry.get().strip()
        if not query:
            self.show_student_table()
            return
            
        found = self.manager.search_students(query)
        if found: 
            self.show_student_table(found)
        else: 
            messagebox.showinfo("No Match", "No student found matching that Roll Number.")