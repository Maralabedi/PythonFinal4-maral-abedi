from models.Student import Student
from utils.helpers import export_to_csv, generate_report
from tkinter import messagebox

class StudentController:
    def __init__(self, view):
        self.view = view
        self.model = Student()

    def add(self):
        data = self.view.get_form_data()
        if not data[0] or not data[1]:
            messagebox.showerror("خطا", "نام و نام خانوادگی الزامی است")
            return
        self.model.create(data)
        messagebox.showinfo("موفقیت", "دانش‌آموز اضافه شد")
        self.view.clear_form()
        self.view.refresh_table()

    def edit(self):
        if not self.view.selected_id:
            messagebox.showwarning("هشدار", "ابتدا یک ردیف انتخاب کنید")
            return
        data = self.view.get_form_data()
        self.model.update(self.view.selected_id, data)
        messagebox.showinfo("موفقیت", "ویرایش انجام شد")
        self.view.clear_form()
        self.view.refresh_table()

    def delete(self):
        if not self.view.selected_id:
            return
        if messagebox.askyesno("تأیید حذف", "آیا مطمئن هستید؟"):
            self.model.delete(self.view.selected_id)
            self.view.selected_id = None
            self.view.refresh_table()

    def export(self):
        export_to_csv(self.model.all())

    def report(self):
        if not self.view.selected_id:
            messagebox.showwarning("هشدار", "یک دانش‌آموز انتخاب کنید")
            return
        student = self.model.find(self.view.selected_id)
        generate_report(student)

    def search(self, keyword):
        result = self.model.search(keyword)
        self.view.refresh_table(result)