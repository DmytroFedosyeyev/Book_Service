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