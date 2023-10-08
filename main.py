import tkinter as tk
from tkinter import ttk
import sqlite3
import os


# Класс главного окна
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = db
        self.toplevel = None

        # Настройка гл. окна
        self.title('Список сотрудников компании')
        self.geometry('665x450')
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)

        # TOOLBAR
        self.toolbar = tk.Frame(self, bd=0, background='#c7c7c7')
        self.toolbar.grid(row=0, column=0, sticky='ew')

        # загрузка всех изображений из папки img
        self.images = {path[0:-4]: tk.PhotoImage(file=f'./img/{path}') for path in os.listdir('./img')}

        # Конпки для тулбара
        self.add_button = tk.Button(self.toolbar, bd=0, background='#c7c7c7', image=self.images['add'],
                                    command=self.open_add_dialog)
        self.add_button.grid(row=0, column=0, padx=(120, 0))
        self.edit_button = tk.Button(self.toolbar, bd=0, background='#c7c7c7', image=self.images['update'],
                                     command=self.open_edit_dialog)
        self.edit_button.grid(row=0, column=1)
        self.delete_button = tk.Button(self.toolbar, bd=0, background='#c7c7c7', image=self.images['delete'],
                                       command=self.delete_employees)
        self.delete_button.grid(row=0, column=2)
        self.search_button = tk.Button(self.toolbar, bd=0, background='#c7c7c7', image=self.images['search'],
                                       command=self.open_search_dialog)
        self.search_button.grid(row=0, column=3)
        self.refresh_button = tk.Button(self.toolbar, bd=0, background='#c7c7c7', image=self.images['refresh'],
                                        command=self.update_treeview)
        self.refresh_button.grid(row=0, column=4)

        # TREEVIEW
        self.treeview = ttk.Treeview(self, columns=('ID', 'Name', 'Tel', 'Email', 'Salary'), show='headings', height=16)
        self.treeview.column('ID', width=30, anchor=tk.CENTER)
        self.treeview.column('Name', width=270, anchor=tk.CENTER)
        self.treeview.column('Tel', width=120, anchor=tk.CENTER)
        self.treeview.column('Email', width=120, anchor=tk.CENTER)
        self.treeview.column('Salary', width=90, anchor=tk.CENTER)

        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Name', text='ФИО')
        self.treeview.heading('Tel', text='Телефон')
        self.treeview.heading('Email', text='E-mail')
        self.treeview.heading('Salary', text='Зарплата')

        self.treeview.grid(row=1, column=0, pady=(15, 0), sticky='ns')

        scroll = tk.Scrollbar(self, command=self.treeview.yview)
        scroll.grid(row=1, column=0, pady=(15, 0), sticky='nse')
        self.treeview.configure(yscrollcommand=scroll.set)

        self.update_treeview()

    # Добавление сотрудника
    # Если уже открыто какое - либо окно, оно закрывается
    def open_add_dialog(self):
        if self.toplevel is not None:
            self.toplevel.destroy()
        self.toplevel = DialogFrame(self)
        self.toplevel.init_add_frame()

    # Изменение сотрудника
    def open_edit_dialog(self):
        if self.toplevel is not None:
            self.toplevel.destroy()
        self.toplevel = DialogFrame(self)
        self.toplevel.init_edit_frame(self.treeview.set(self.treeview.selection()[0], '#1'))

    # Поиск сотрудника
    def open_search_dialog(self):
        if self.toplevel is not None:
            self.toplevel.destroy()
        self.toplevel = SearchFrame(self)

    # Работа с БД
    def add_employee(self, name, phone, email, salary):
        self.db.add_employee(name, phone, email, salary)
        self.update_treeview()

    def edit_employee(self, name, phone, email, salary):
        self.db.update_employee(name, phone, email, salary, self.treeview.set(self.treeview.selection()[0], '#1'))
        self.update_treeview()

    def delete_employees(self):
        for selection in self.treeview.selection():
            self.db.delete_employee(self.treeview.set(selection, '#1'))
        self.update_treeview()

    def search_employees(self, name):
        [self.treeview.delete(i) for i in self.treeview.get_children()]
        [self.treeview.insert('', 'end', values=row) for row in self.db.search_employees(f'%{name}%')]
        if len(children := self.treeview.get_children()) != 0:
            self.treeview.selection_set(children[0])

    # Обновление информации в treeview
    def update_treeview(self):
        [self.treeview.delete(i) for i in self.treeview.get_children()]
        [self.treeview.insert('', 'end', values=row) for row in self.db.get_employees()]
        if len(children := self.treeview.get_children()) != 0:
            self.treeview.selection_set(children[0])


# Диалоговое окно создания / изменения сотрудника
class DialogFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('400x220')
        self.resizable(False, False)

        # Общие элементы окон
        # Заголовки
        self.name_label = tk.Label(self, text='ФИО')
        self.name_label.grid(row=0, column=0, padx=(40, 0), pady=(30, 0))
        self.phone_label = tk.Label(self, text='Телефон')
        self.phone_label.grid(row=1, column=0, padx=(40, 0), pady=(10, 0))
        self.email_label = tk.Label(self, text='E-mail')
        self.email_label.grid(row=2, column=0, padx=(40, 0), pady=(10, 0))
        self.salary_label = tk.Label(self, text='Зарплата')
        self.salary_label.grid(row=3, column=0, padx=(40, 0), pady=(10, 0))

        # Поля для ввода
        self.name_entry = tk.Entry(self, width=40)
        self.name_entry.grid(row=0, column=1, padx=(15, 0), pady=(30, 0))
        self.phone_entry = tk.Entry(self, width=40)
        self.phone_entry.grid(row=1, column=1, padx=(15, 0), pady=(10, 0))
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.grid(row=2, column=1, padx=(15, 0), pady=(10, 0))
        self.salary_entry = tk.Entry(self, width=40)
        self.salary_entry.grid(row=3, column=1, padx=(15, 0), pady=(10, 0))

        # Кнопки
        self.confirm_button = ttk.Button(self)
        self.confirm_button.grid(row=4, column=0, columnspan=2, padx=(0, 80), pady=20)
        self.cansel_button = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.cansel_button.grid(row=4, column=0, columnspan=2, padx=(140, 0), pady=20)

    # Инициализация элементов для окна добавления сотрудника
    def init_add_frame(self):
        self.title('Добавление сотрудника')
        self.confirm_button.configure(text='Добавить',
                                      command=lambda: app.add_employee(self.name_entry.get(), self.phone_entry.get(),
                                                                       self.email_entry.get(), self.salary_entry.get())
                                      or self.destroy())

    # Инициализация элементов для окна изменения сотрудника
    def init_edit_frame(self, employee_id: int):
        self.title('Изменение сотрудника')

        employee = app.db.get_employee(employee_id)
        self.name_entry.insert(0, employee[0])
        self.phone_entry.insert(0, employee[1])
        self.email_entry.insert(0, employee[2])
        self.salary_entry.insert(0, employee[3])

        self.confirm_button.configure(text='Изменить',
                                      command=lambda: app.edit_employee(self.name_entry.get(), self.phone_entry.get(),
                                                                        self.email_entry.get(), self.salary_entry.get())
                                      or self.destroy())


# Диалоговое окно поиска сотрудника (-ов)
class SearchFrame(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)

        self.search_label = tk.Label(self, text='ФИО')
        self.search_label.grid(row=0, column=0, padx=(40, 0), pady=(5, 0))

        self.search_entry = tk.Entry(self, width=30)
        self.search_entry.grid(row=0, column=1, padx=(15, 0), pady=(20, 15))

        self.search_button = ttk.Button(self, text='Поиск',
                                        command=lambda: app.search_employees(self.search_entry.get()) or self.destroy())
        self.search_button.grid(row=1, column=0, columnspan=2, padx=0)
        self.cansel_button = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.cansel_button.grid(row=1, column=0, columnspan=2, padx=(160, 0))


# Класс БД (наследуется от Connection)
class DB(sqlite3.Connection):
    def __init__(self):
        super().__init__('data.db')
        self.c = self.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary TEXT
            )
        """)
        self.commit()

    def add_employee(self, name: str, phone: str, email: str, salary: str):
        self.c.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
                       (name, phone, email, salary))
        self.commit()

    def update_employee(self, name: str, phone: str, email: str, salary: str, employee_id: int):
        self.c.execute("UPDATE employees SET name = ?, phone = ?, email = ?, salary = ? WHERE id = ?",
                       (name, phone, email, salary, employee_id))
        self.commit()

    def delete_employee(self, employee_id: int):
        self.c.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        self.commit()

    def search_employees(self, template) -> list[tuple]:
        self.c.execute("SELECT * FROM employees WHERE name LIKE ?", (template,))
        return self.c.fetchall()

    def get_employees(self) -> list[tuple]:
        self.c.execute("SELECT * FROM employees")
        return self.c.fetchall()

    def get_employee(self, employee_id: int) -> tuple:
        self.c.execute("SELECT name, phone, email, salary FROM employees WHERE id = ?", (employee_id,))
        return self.c.fetchone()


# Начало работы программы
if __name__ == '__main__':
    db = DB()
    app = App()
    app.mainloop()
