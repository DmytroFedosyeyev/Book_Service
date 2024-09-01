import unittest

from exam_book import (
    EmployeeService,
    BookService,
    SaleService,
    DataManager,
    Report
)


class TestEmployeeService(unittest.TestCase):
    def setUp(self):
        self.service = EmployeeService()

    def test_add_employee(self):
        self.service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        employees = self.service.get_all_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].name, "Alice")

    def test_add_employee_duplicate(self):
        self.service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        with self.assertRaises(ValueError):
            self.service.add_employee("Alice", "Manager", "555-555", "alice@example.com")

    def test_remove_employee(self):
        self.service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.service.remove_employee("Alice")
        self.assertEqual(len(self.service.get_all_employees()), 0)

    def test_edit_employee(self):
        self.service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.service.edit_employee("Alice", new_position="Senior Manager", new_phone="555-555")
        employee = self.service.get_all_employees()[0]
        self.assertEqual(employee.position, "Senior Manager")
        self.assertEqual(employee.phone, "555-555")


class TestBookService(unittest.TestCase):
    def setUp(self):
        self.service = BookService()

    def test_add_book(self):
        self.service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        books = self.service.get_all_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Test Book")

    def test_add_book_duplicate(self):
        self.service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        with self.assertRaises(ValueError):
            self.service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)

    def test_remove_book(self):
        self.service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.service.remove_book("Test Book")
        self.assertEqual(len(self.service.get_all_books()), 0)

    def test_edit_book(self):
        self.service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.service.edit_book("Test Book", new_cost=12.0, new_sale_price=18.0)
        book = self.service.get_all_books()[0]
        self.assertEqual(book.cost, 12.0)
        self.assertEqual(book.sale_price, 18.0)


class TestSaleService(unittest.TestCase):
    def setUp(self):
        self.employee_service = EmployeeService()
        self.book_service = BookService()
        self.sale_service = SaleService(self.employee_service, self.book_service)

    def test_add_sale(self):
        self.employee_service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.book_service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-30", 14.0)
        sales = self.sale_service.get_sales_by_date("2024-08-30")
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].employee.name, "Alice")
        self.assertEqual(sales[0].book.title, "Test Book")

    def test_get_sales_by_date(self):
        self.employee_service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.book_service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-30", 14.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-31", 14.0)
        sales = self.sale_service.get_sales_by_date("2024-08-30")
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].sale_date, "2024-08-30")

    def test_get_sales_by_period(self):
        self.employee_service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.book_service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-30", 14.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-31", 14.0)
        sales = self.sale_service.get_sales_by_period("2024-08-29", "2024-08-30")
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].sale_date, "2024-08-30")


class TestReport(unittest.TestCase):
    def setUp(self):
        self.employee_service = EmployeeService()
        self.book_service = BookService()
        self.sale_service = SaleService(self.employee_service, self.book_service)
        self.report = Report(self.employee_service, self.book_service, self.sale_service)

    def test_generate_sales_report(self):
        self.employee_service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.book_service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-30", 14.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-31", 14.0)
        expected_report = "2024-08-30: Alice sold 'Test Book' for 14.0\n2024-08-31: Alice sold 'Test Book' for 14.0"
        self.assertEqual(self.report.generate_sales_report("2024-08-30", "2024-08-31"), expected_report)

    def test_generate_employee_sales_report(self):
        self.employee_service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.book_service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-30", 14.0)
        expected_report = "Sales report for Alice:\n2024-08-30: 'Test Book' sold for 14.0"
        self.assertEqual(self.report.generate_employee_sales_report("Alice"), expected_report)

    def test_generate_top_books_report(self):
        self.employee_service.add_employee("Alice", "Manager", "444-444", "alice@example.com")
        self.book_service.add_book("Test Book", 2024, "Author", "Genre", 10.0, 15.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-30", 14.0)
        self.sale_service.add_sale("Alice", "Test Book", "2024-08-31", 14.0)
        expected_report = "Top 1 selling books:\nTest Book: 2 sales"
        self.assertEqual(self.report.generate_top_books_report(1), expected_report)


if __name__ == "__main__":
    unittest.main()
