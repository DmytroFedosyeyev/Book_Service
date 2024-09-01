class Employee:
    def __init__(self, name: str, position: str, phone: str, email: str):
        self.name = name
        self.position = position
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Employee(Name: {self.name}, Position: {self.position}, Phone: {self.phone}, Email: {self.email})"


class EmployeeFactory:
    @staticmethod
    def create_employee(name: str, position: str, phone: str, email: str) -> Employee:
        return Employee(name, position, phone, email)


class Book:
    def __init__(self, title: str, year: int, author: str, genre: str, cost: float, sale_price: float):
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre
        self.cost = cost
        self.sale_price = sale_price

    def __str__(self):
        return (f"Book(Title: {self.title}, Year: {self.year}, Author: {self.author}, "
                f"Genre: {self.genre}, Cost: {self.cost}, Sale Price: {self.sale_price})")


class BookFactory:
    @staticmethod
    def create_book(title: str, year: int, author: str, genre: str, cost: float, sale_price: float) -> Book:
        return Book(title, year, author, genre, cost, sale_price)


class Sale:
    def __init__(self, employee: Employee, book: Book, sale_date: str, actual_sale_price: float):
        self.employee = employee
        self.book = book
        self.sale_date = sale_date
        self.actual_sale_price = actual_sale_price

    def __str__(self):
        return (f"Sale(Employee: {self.employee.name}, Book: {self.book.title}, "
                f"Date: {self.sale_date}, Actual Sale Price: {self.actual_sale_price})")


class SaleFactory:
    @staticmethod
    def create_sale(employee: Employee, book: Book, sale_date: str, actual_sale_price: float) -> Sale:
        return Sale(employee, book, sale_date, actual_sale_price)


class EmployeeService:
    def __init__(self):
        self.employees = []

    def add_employee(self, name: str, position: str, phone: str, email: str):
        for emp in self.employees:
            if emp.name == name or emp.email == email:
                raise ValueError("Employee with this name or email already exists.")
        employee = EmployeeFactory.create_employee(name, position, phone, email)
        self.employees.append(employee)

    def remove_employee(self, name: str):
        updated_employees = []
        removed = False
        found = False
        for emp in self.employees:
            if emp.name == name and not removed:
                removed = True
                found = True
            else:
                updated_employees.append(emp)
        if not found:
            print(f"Employee with name '{name}' not found.")

        self.employees = updated_employees

    def get_all_employees(self):
        return self.employees

    def edit_employee(self, name: str, new_position: str = None, new_phone: str = None, new_email: str = None):
        for emp in self.employees:
            if emp.name == name:
                if new_position:
                    emp.position = new_position
                if new_phone:
                    emp.phone = new_phone
                if new_email:
                    emp.email = new_email
                return emp
        raise ValueError("Employee not found")


class BookService:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, year: int, author: str, genre: str, cost: float, sale_price: float):
        for book in self.books:
            if book.title == title and book.author == author:
                raise ValueError("Book with this title and author already exists.")

        book = BookFactory.create_book(title, year, author, genre, cost, sale_price)
        self.books.append(book)

    def remove_book(self, title: str):
        found = False
        updated_books = []

        for book in self.books:
            if book.title == title and not found:
                found = True
            else:
                updated_books.append(book)

        if not found:
            print(f"Book with title '{title}' not found.")

        self.books = updated_books

    def edit_book(self, title: str, new_year: int = None, new_author: str = None, new_genre: str = None,
                  new_cost: float = None, new_sale_price: float = None):
        for book in self.books:
            if book.title == title:
                if new_year:
                    book.year = new_year
                if new_author:
                    book.author = new_author
                if new_genre:
                    book.genre = new_genre
                if new_cost:
                    book.cost = new_cost
                if new_sale_price:
                    book.sale_price = new_sale_price
                return book
        raise ValueError("Book not found")

    def get_all_books(self):
        return self.books


class SaleService:
    def __init__(self, employee_service: EmployeeService, book_service: BookService):
        self.sales = []
        self.employee_service = employee_service
        self.book_service = book_service

    def add_sale(self, employee_name: str, book_title: str, sale_date: str, actual_sale_price: float):
        employees = self.employee_service.get_all_employees()
        books = self.book_service.get_all_books()

        employee = None
        for e in employees:
            if e.name == employee_name:
                employee = e
                break
        if employee is None:
            raise ValueError(f"Employee '{employee_name}' not found.")

        book = None
        for b in books:
            if b.title == book_title:
                book = b
                break
        if book is None:
            raise ValueError(f"Book '{book_title}' not found.")

        sale = Sale(employee, book, sale_date, actual_sale_price)
        self.sales.append(sale)

    def get_sales_by_date(self, date: str):
        result = []
        for sale in self.sales:
            if sale.sale_date == date:
                result.append(sale)
        return result

    def get_sales_by_period(self, start_date: str, end_date: str):
        result = []
        for sale in self.sales:
            if start_date <= sale.sale_date <= end_date:
                result.append(sale)
        return result

