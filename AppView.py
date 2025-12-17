import customtkinter as ctk
from controllers.StudentController import StudentController
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppView:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("مدیریت نمرات دانش‌آموزان - MVC")
        self.root.geometry("1500x950")

        self.controller = StudentController(self)
        self.selected_id = None

        self.subjects = [
            ("ریاضی", "math"), ("زبان انگلیسی", "english"), ("برنامه‌نویسی", "programming"),
            ("دینی", "religion"), ("عربی", "arabic"), ("فیزیک", "physics"),
            ("شیمی", "chemistry"), ("زیست‌شناسی", "biology")
        ]

        self.grade_entries = {}
        self.create_ui()
        self.refresh_table()

    def create_ui(self):
        ctk.CTkLabel(self.root, text="سیستم مدیریت نمرات دانش‌آموزان", 
                     font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)

        btn_frame = ctk.CTkFrame(self.root)
        btn_frame.pack(pady=10)

        buttons = [
            ("اضافه کردن", self.controller.add, "#4CAF50"),
            ("ویرایش", self.controller.edit, "#FF9800"),
            ("حذف", self.controller.delete, "#F44336"),
            ("جستجو", self.search_dialog, "#2196F3"),
            ("نمایش همه", lambda: self.refresh_table(), "#9C27B0"),
            ("خروجی اکسل", self.controller.export, "#FF5722"),
            ("کارنامه", self.controller.report, "#E91E63")
        ]

        for text, cmd, color in buttons:
            ctk.CTkButton(btn_frame, text=text, width=180, fg_color=color, command=cmd,
                          font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", padx=5)

        # فرم ورودی
        form = ctk.CTkFrame(self.root)
        form.pack(pady=20, padx=50, fill="x")

        ctk.CTkLabel(form, text="نام:").grid(row=0, column=5, padx=10, pady=10)
        self.first_name = ctk.CTkEntry(form, width=200, justify="right")
        self.first_name.grid(row=0, column=4, padx=10)

        ctk.CTkLabel(form, text="نام خانوادگی:").grid(row=0, column=3, padx=10)
        self.last_name = ctk.CTkEntry(form, width=200, justify="right")
        self.last_name.grid(row=0, column=2, padx=10)

        ctk.CTkLabel(form, text="سن:").grid(row=0, column=1, padx=10)
        self.age = ctk.CTkEntry(form, width=100)
        self.age.grid(row=0, column=0, padx=10)

        # نمرات
        grades_frame = ctk.CTkFrame(self.root)
        grades_frame.pack(pady=10)

        for i, (name, key) in enumerate(self.subjects):
            row = i // 4
            col = (3 - (i % 4)) * 2
            ctk.CTkLabel(grades_frame, text=name + ":").grid(row=row, column=col+1, padx=15, pady=8, sticky="e")
            entry = ctk.CTkEntry(grades_frame, width=100, justify="center")
            entry.grid(row=row, column=col, padx=10)
            self.grade_entries[key] = entry

        # جدول
        self.table_frame = ctk.CTkScrollableFrame(self.root, height=400)
        self.table_frame.pack(pady=20, padx=50, fill="both", expand=True)

    def get_form_data(self):
        try:
            grades = [float(self.grade_entries[k].get() or 0) for k in [k[1] for k in self.subjects]]
            return [
                self.first_name.get().strip(),
                self.last_name.get().strip(),
                int(self.age.get()),
                *grades
            ]
        except:
            return None

    def clear_form(self):
        self.first_name.delete(0, "end")
        self.last_name.delete(0, "end")
        self.age.delete(0, "end")
        for e in self.grade_entries.values():
            e.delete(0, "end")

    def refresh_table(self, data=None):
        for w in self.table_frame.winfo_children():
            w.destroy()

        students = data or self.controller.model.all()
        for row in students:
            frame = ctk.CTkFrame(self.table_frame)
            frame.pack(fill="x", pady=3, padx=10)

            grades = row[4:]
            valid = [g for g in grades if g > 0]
            avg = round(sum(valid)/len(valid), 2) if valid else 0

            ctk.CTkButton(frame, text="انتخاب", width=80, fg_color="#2196f42c1",
                          command=lambda sid=row[0]: self.select_student(sid, row)).pack(side="left", padx=5)

            ctk.CTkLabel(frame, text=f"{avg:.2f}", width=90, fg_color="#198754" if avg>=10 else "#dc3545", text_color="white").pack(side="left", padx=2)

            for g in reversed(grades):
                ctk.CTkLabel(frame, text=f"{g:.1f}", width=85).pack(side="left", padx=1)

            ctk.CTkLabel(frame, text=row[3]).pack(side="left", padx=4)  # سن
            ctk.CTkLabel(frame, text=f"{row[1]} {row[2]}", width=200).pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=row[0], width=60).pack(side="left", padx=5)

    def select_student(self, sid, data):
        self.selected_id = sid
        self.first_name.delete(0, "end"); self.first_name.insert(0, data[1])
        self.last_name.delete(0, "end"); self.last_name.insert(0, data[2])
        self.age.delete(0, "end"); self.age.insert(0, data[3])
        for i, key in enumerate([k[1] for k in self.subjects]):
            self.grade_entries[key].delete(0, "end")
            self.grade_entries[key].insert(0, str(data[4+i]))

    def search_dialog(self):
        keyword = ctk.CTkInputDialog(text="نام یا نام خانوادگی را وارد کنید:", title="جستجو").get_input()
        if keyword:
            result = self.controller.search(keyword)
            self.refresh_table(result)

    def run(self):
        self.root.mainloop()