import customtkinter as ct
from tkinter import messagebox, filedialog
import csv

class ReportView(ct.CTkFrame):
    def __init__(self, parent, c_manager, s_manager, r_manager):
        super().__init__(parent, fg_color="transparent")
        self.c_manager = c_manager
        self.s_manager = s_manager
        self.r_manager = r_manager
        self.setup_ui()

    def setup_ui(self):
        ct.CTkLabel(self, text="Class Statistics & Reports", font=("Arial", 35, "bold"), text_color="black").pack(pady=(30, 20))

        #  Statistics Container 
        stats_frame = ct.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=50, pady=20)

        #  Calculate Live Statistics 
        students = self.s_manager.get_all_students()
        courses = self.c_manager.get_all_courses()
        results = self.r_manager.get_all_results()

        total_students = len(students)
        total_courses = len(courses)
        total_results = len(results)

        # Count passes and fails
        passed = sum(1 for r in results if r["Grade"] != "F")
        failed = total_results - passed
        
        # Calculate Average Marks
        avg_marks = 0
        if total_results > 0:
            avg_marks = sum(int(r["Marks"]) for r in results) / total_results

        #  Display Stat Cards 
        self.create_stat_card(stats_frame, "Total Students", str(total_students), 0)
        self.create_stat_card(stats_frame, "Total Courses", str(total_courses), 1)
        self.create_stat_card(stats_frame, "Total Grades", str(total_results), 2)
        self.create_stat_card(stats_frame, "Passed", str(passed), 3)
        self.create_stat_card(stats_frame, "Failed", str(failed), 4)
        self.create_stat_card(stats_frame, "Avg Marks", f"{avg_marks:.1f}", 5)

    def create_stat_card(self, parent, title, value, col):
        card = ct.CTkFrame(parent, fg_color="#2B2B2B", corner_radius=10)
        card.grid(row=0, column=col, padx=15, pady=10, sticky="nsew")
        ct.CTkLabel(card, text=title, font=("Arial", 20), text_color="white").pack(pady=(20, 5), padx=20)
        ct.CTkLabel(card, text=value, font=("Arial", 40, "bold"), text_color="#1F6AA5").pack(pady=(5, 20), padx=20)

    def export_csv(self):
        results = self.r_manager.get_all_results()
        if not results:
            messagebox.showwarning("Empty Data", "There are no results to export!")
            return

        # Open a "Save As" window
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Final Report"
        )

        if not filepath:
            return # User closed the window without saving

        try:
            with open(filepath, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Roll Number", "Student Name", "Course Name", "Marks", "Grade"])
                
                # Make a dictionary to quickly look up student names by their Roll Number
                students_dict = {s["Roll"]: s["Name"] for s in self.s_manager.get_all_students()}
                
                for r in results:
                    name = students_dict.get(r["Roll"], "Unknown Student")
                    writer.writerow([r["Roll"], name, r["Course"], r["Marks"], r["Grade"]])
            
            messagebox.showinfo("Export Successful", f"Report successfully saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to save file: {e}")