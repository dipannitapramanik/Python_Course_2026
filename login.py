import customtkinter as ct
from tkinter import messagebox
import csv

class LoginWindow(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("System Login")
        self.geometry("600x500")
        self.configure(fg_color="grey")
        self.setup_ui()

    def setup_ui(self):
        frame = ct.CTkFrame(self, fg_color="white", corner_radius=15, width=500, height=400)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ct.CTkLabel(frame, text="Admin Login", font=("Arial", 35, "bold"), text_color="black").place(x=140, y=40)

        ct.CTkLabel(frame, text="Username:", font=("Arial", 20), text_color="black").place(x=50, y=120)
        self.user_entry = ct.CTkEntry(frame, font=("Arial", 20), width=400, fg_color="#F0F0F0", text_color="black")
        self.user_entry.place(x=50, y=160)

        ct.CTkLabel(frame, text="Password:", font=("Arial", 20), text_color="black").place(x=50, y=210)
        self.pass_entry = ct.CTkEntry(frame, font=("Arial", 20), width=400, fg_color="#F0F0F0", text_color="black", show="*")
        self.pass_entry.place(x=50, y=250)

        ct.CTkButton(frame, text="Login", font=("Arial", 20, "bold"), width=400, height=45, command=self.verify_login).place(x=50, y=320)
        ct.CTkButton(frame, text="Back to Home", font=("Arial", 15), fg_color="transparent", text_color="blue", hover_color="#E0E0E0", command=self.go_back).place(x=190, y=370)

    def verify_login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Please enter username and password.")
            return
        success = False
        

        try:
            with open("users.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Username"] == u and row["Password"] == p:
                        success = True
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "No accounts found. Please register first.")
            return

        if success:
            messagebox.showinfo("Welcome", f"Login successful! Welcome, {u}.")
            self.destroy() 
            self.launch_dashboard() 
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def launch_dashboard(self):

        from dashboard import StudentResultApp, CourseManager, StudentManager, ResultManager, CSVStorage
        
        c_man = CourseManager(CSVStorage("courses.csv", ["Course Name", "Duration", "Description"]))
        s_man = StudentManager(CSVStorage("students.csv", ["Roll", "Name", "Phone", "Gender", "Address"]))
        r_man = ResultManager(CSVStorage("results.csv", ["Roll", "Course", "Marks", "Grade"])) 
        
        dashboard_app = StudentResultApp(c_man, s_man, r_man)
        dashboard_app.mainloop()

    def go_back(self):
        self.destroy()
        import main
        main.run_app()

def run():
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    run()