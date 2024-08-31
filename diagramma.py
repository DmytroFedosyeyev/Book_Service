from graphviz import Digraph

dot = Digraph()


dot.node('Employee', 'Employee\n- name : str\n- position : str\n- phone : str\n- email : str\n+ __init__(name : str, position : str, phone : str, email : str)\n+ __str__() : str')
dot.node('Book', 'Book\n- title : str\n- year : int\n- author : str\n- genre : str\n- cost : float\n- sale_price : float\n+ __init__(title : str, year : int, author : str, genre : str, cost : float, sale_price : float)\n+ __str__() : str')
dot.node('Sale', 'Sale\n- employee : Employee\n- book : Book\n- sale_date : str\n- actual_sale_price : float\n+ __init__(employee : Employee, book : Book, sale_date : str, actual_sale_price : float)\n+ __str__() : str')


dot.node('EmployeeService', 'EmployeeService\n+ add_employee(name : str, position : str, phone : str, email : str)\n+ remove_employee(name : str)\n+ get_all_employees() : List[Employee]')
dot.node('BookService', 'BookService\n+ add_book(title : str, year : int, author : str, genre : str, cost : float, sale_price : float)\n+ remove_book(title : str)\n+ get_all_books() : List[Book]')
dot.node('SaleService', 'SaleService\n+ add_sale(employee_name : str, book_title : str, sale_date : str, actual_sale_price : float)\n+ get_sales_by_date(date : str) : List[Sale]\n+ get_sales_by_period(start_date : str, end_date : str) : List[Sale]')


dot.node('DataManager', 'DataManager\n+ save_data(filename : str, data : object)\n+ load_data(filename : str) : object')
dot.node('Report', 'Report\n+ generate_full_employee_report() : str\n+ generate_full_book_report() : str\n+ generate_sales_report() : str\n+ generate_sales_by_date(date : str) : str')


dot.edge('EmployeeService', 'Employee', label='manages')
dot.edge('BookService', 'Book', label='manages')
dot.edge('SaleService', 'Sale', label='manages')

dot.edge('SaleService', 'Employee', label='uses')
dot.edge('SaleService', 'Book', label='uses')

dot.edge('DataManager', 'EmployeeService', label='uses')
dot.edge('DataManager', 'BookService', label='uses')
dot.edge('DataManager', 'SaleService', label='uses')

dot.edge('Report', 'EmployeeService', label='queries')
dot.edge('Report', 'BookService', label='queries')
dot.edge('Report', 'SaleService', label='queries')


dot.render('bookstore_uml_diagram', format='pdf', cleanup=True)

print("UML диаграмма создана и сохранена как 'bookstore_uml_diagram.pdf'")