import json

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


class DataManager:
    def __init__(self, employee_service: EmployeeService, book_service: BookService, sale_service: SaleService):
        self.employee_service = employee_service
        self.book_service = book_service
        self.sale_service = sale_service

    def load_data(self, employee_file: str, book_file: str, sale_file: str):

        with open(employee_file, 'r') as f:
            employee_data = json.load(f)
            for emp in employee_data:
                self.employee_service.add_employee(emp['name'], emp['position'], emp['phone'], emp['email'])

        with open(book_file, 'r') as f:
            book_data = json.load(f)
            for book in book_data:
                self.book_service.add_book(book['title'], book['year'], book['author'], book['genre'], book['cost'], book['sale_price'])

        with open(sale_file, 'r') as f:
            sale_data = json.load(f)
            for sale in sale_data:
                self.sale_service.add_sale(sale['employee_name'], sale['book_title'], sale['sale_date'], sale['actual_sale_price'])

    def save_data(self, employee_file: str, book_file: str, sale_file: str):

        employees = self.employee_service.get_all_employees()
        employee_dicts = []
        for emp in employees:
            employee_dicts.append({
                'name': emp.name,
                'position': emp.position,
                'phone': emp.phone,
                'email': emp.email
            })
        with open(employee_file, 'w') as f:
            json.dump(employee_dicts, f)

        books = self.book_service.get_all_books()
        book_dicts = []
        for book in books:
            book_dicts.append({
                'title': book.title,
                'year': book.year,
                'author': book.author,
                'genre': book.genre,
                'cost': book.cost,
                'sale_price': book.sale_price
            })
        with open(book_file, 'w') as f:
            json.dump(book_dicts, f)

        sales = self.sale_service.sales
        sale_dicts = []
        for sale in sales:
            sale_dicts.append({
                'employee_name': sale.employee.name,
                'book_title': sale.book.title,
                'sale_date': sale.sale_date,
                'actual_sale_price': sale.actual_sale_price
            })
        with open(sale_file, 'w') as f:
            json.dump(sale_dicts, f)


class Report:
    def __init__(self, employee_service: EmployeeService, book_service: BookService, sale_service: SaleService):
        self.employee_service = employee_service
        self.book_service = book_service
        self.sale_service = sale_service

    def generate_sales_report(self, start_date: str, end_date: str):
        sales = self.sale_service.get_sales_by_period(start_date, end_date)
        report = []
        for sale in sales:
            report.append(f"{sale.sale_date}: {sale.employee.name} sold '{sale.book.title}' for {sale.actual_sale_price}")
        return "\n".join(report)

    def generate_employee_sales_report(self, employee_name: str):
        report = []
        for sale in self.sale_service.sales:
            if sale.employee.name == employee_name:
                report.append(f"{sale.sale_date}: '{sale.book.title}' sold for {sale.actual_sale_price}")
        if not report:
            return f"No sales found for employee '{employee_name}'"

        return "\n".join([f"Sales report for {employee_name}:"] + report)

    def generate_top_books_report(self, top_n: int):
        book_sales = {}
        for sale in self.sale_service.sales:
            if sale.book.title not in book_sales:
                book_sales[sale.book.title] = 0
            book_sales[sale.book.title] += 1

        sorted_books = []
        for book, count in book_sales.items():
            sorted_books.append((book, count))
        sorted_books.sort(key=lambda item: item[1], reverse=True)

        report = [f"Top {top_n} selling books:"]

        for book, count in sorted_books[:top_n]:
            report.append(f"{book}: {count} sales")
        return "\n".join(report)


employee_service = EmployeeService()
book_service = BookService()
sale_service = SaleService(employee_service, book_service)

data_manager = DataManager(employee_service, book_service, sale_service)

employee_data = [
    {"name": "John", "position": "Manager", "phone": "111-111", "email": "john@gmail.com"},
    {"name": "Bruce", "position": "Sales", "phone": "222-222", "email": "bruce@gmail.com"},
    {"name": "Marta", "position": "Sales", "phone": "333-333", "email": "marta@gmail.com"}
]

book_data = [
    {"title": "Taras Bulba", "year": 1835, "author": "N.V. Gogol", "genre": "Novel", "cost": 10.0, "sale_price": 15.0},
    {"title": "War and Peace", "year": 1867, "author": "L.N. Tolstoy", "genre": "Novel", "cost": 20.0, "sale_price": 25.0},
    {"title": "1984", "year": 1949, "author": "G. Orwell", "genre": "Fantasy", "cost": 18.5, "sale_price": 19.5}
]

sale_data = [
    {"employee_name": "John", "book_title": "1984", "sale_date": "2024-08-30", "actual_sale_price": 19.0},
    {"employee_name": "John", "book_title": "1984", "sale_date": "2024-08-31", "actual_sale_price": 19.5},
    {"employee_name": "Bruce", "book_title": "Taras Bulba", "sale_date": "2024-08-29", "actual_sale_price": 14.0},
    {"employee_name": "Marta", "book_title": "War and Peace", "sale_date": "2024-08-29", "actual_sale_price": 23.4}
]

with open('employees.json', 'w') as f:
    json.dump(employee_data, f)

with open('books.json', 'w') as f:
    json.dump(book_data, f)

with open('sales.json', 'w') as f:
    json.dump(sale_data, f)

data_manager.load_data('employees.json', 'books.json', 'sales.json')

report = Report(employee_service, book_service, sale_service)

print("Sales Report from 2024-08-30 to 2024-08-31:")
print(report.generate_sales_report("2024-08-30", "2024-08-31"))

print("\nEmployee Sales Report for John:")
print(report.generate_employee_sales_report("John"))

print("\nTop 1 Selling Books Report:")
print(report.generate_top_books_report(1))

data_manager.save_data('employees.json', 'books.json', 'sales.json')
