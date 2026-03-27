import customtkinter as ct
from tkinter import messagebox
import csv

class RegistrationWindow(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Register New Account")
        self.geometry("600x550")
        self.configure(fg_color="grey")
        self.setup_ui()

    def setup_ui(self):
        frame = ct.CTkFrame(self, fg_color="white", corner_radius=15, width=500, height=450)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ct.CTkLabel(frame, text="Create Account", font=("Arial", 35, "bold"), text_color="black").place(x=120, y=40)

        ct.CTkLabel(frame, text="Username:", font=("Arial", 20), text_color="black").place(x=50, y=120)
        self.user_entry = ct.CTkEntry(frame, font=("Arial", 20), width=400, fg_color="white", text_color="black")
        self.user_entry.place(x=50, y=160)

        ct.CTkLabel(frame, text="Password:", font=("Arial", 20), text_color="black").place(x=50, y=210)
        self.pass_entry = ct.CTkEntry(frame, font=("Arial", 20), width=400, fg_color="white", text_color="black", show="*")
        self.pass_entry.place(x=50, y=250)

        ct.CTkLabel(frame, text="Confirm Password:", font=("Arial", 20), text_color="black").place(x=50, y=300)
        self.confirm_entry = ct.CTkEntry(frame, font=("Arial", 20), width=400, fg_color="white", text_color="black", show="*")
        self.confirm_entry.place(x=50, y=340)

        ct.CTkButton(frame, text="Register", font=("Arial", 20, "bold"), width=400, height=45, command=self.register_user).place(x=50, y=400)
        ct.CTkButton(frame, text="Back to Home", font=("Arial", 15), fg_color="transparent", text_color="blue", hover_color="#E0E0E0", command=self.go_back).place(x=190, y=460)

    def register_user(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()
        c = self.confirm_entry.get().strip()

        if not u or not p or not c:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if p != c:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        file_exists = True
        try:
            with open("users.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Username"].lower() == u.lower():
                        messagebox.showerror("Error", "Username already exists!")
                        return
        except FileNotFoundError:
            file_exists = False

        # Save new user
        with open("users.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Username", "Password"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"Username": u, "Password": p})

        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        self.go_back()

    def go_back(self):
        self.destroy()
        import main
        main.run_app()

def run():
    app = RegistrationWindow()
    app.mainloop()

if __name__ == "__main__":
    run()