# Employee_management_system-CURD-_flask_MySQL
# Employee Management System (CRUD API)

## Overview
This is a Flask-based REST API for managing employees in a MySQL database. The API supports creating, reading, updating, and deleting employee records with proper validation and error handling.

## Features
- Add new employees with validation
- Retrieve all employees or a specific employee by ID
- Update employee details
- Delete an employee record
- Secure MySQL database integration

## Technologies Used
- Python
- Flask
- MySQL
- Flask-CORS
- PyMySQL

## Detailed Explanation of the Code

### Database Configuration
The `DATABASE_CONFIG` dictionary stores the MySQL database connection details. These credentials must be updated to match your MySQL setup.
```python
DATABASE_CONFIG = {
    "MYSQL_HOST": "localhost",
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "your-password",
    "MYSQL_DB": "employees_db"
}
```

### Initializing MySQL Connection
The `init_db()` function establishes a connection with the MySQL database. If the connection fails, an error message is printed.
```python
def init_db():
    global db
    try:
        db = MySQLdb.connect(...)
        print("✅ Database connected successfully")
    except MySQLdb.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        db = None
```

### CRUD Operations
The application includes functions to interact with the database, such as:
- `get_all_employees()`: Fetch all employees.
- `get_employee_by_id(emp_id)`: Retrieve a specific employee by ID.
- `create_employee(name, email, age, position, salary)`: Insert a new employee.
- `update_employee(emp_id, name, email, age, position, salary)`: Modify employee details.
- `delete_employee(emp_id)`: Remove an employee from the database.

Example function:
```python
def create_employee(name, email, age, position, salary):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, email, age, position, salary) VALUES (%s, %s, %s, %s, %s)",
        (name, email, age, position, salary)
    )
    conn.commit()
    cursor.close()
    return True
```

### API Routes
The application exposes multiple API routes using Flask:
- `@app.route('/')`: Home route displaying a welcome message.
- `@app.route('/employees', methods=['POST'])`: Adds a new employee.
- `@app.route('/employees', methods=['GET'])`: Fetches all employees.
- `@app.route('/employees/<int:id>', methods=['GET'])`: Fetches a single employee by ID.
- `@app.route('/employees/<int:id>', methods=['PUT'])`: Updates an employee record.
- `@app.route('/employees/<int:id>', methods=['DELETE'])`: Deletes an employee record.

Example route:
```python
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    create_employee(data['name'], data['email'], data['age'], data['position'], data['salary'])
    return jsonify({"message": "Employee added successfully"}), 201
```

## Installation

### Prerequisites
- Python 3.x
- MySQL Server
- pip (Python package manager)

### Steps
1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure MySQL:
   - Create a database named `employees_db`.
   - Update `DATABASE_CONFIG` in `Employee_Management_system.py` with your credentials.
   - Run this SQL command to create the employees table:
   ```sql
   CREATE TABLE employees (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL UNIQUE,
       age INT NOT NULL CHECK (age BETWEEN 18 AND 65),
       position VARCHAR(255) NOT NULL,
       salary FLOAT NOT NULL CHECK (salary >= 5000)
   );
   ```
4. Run the application:
   ```bash
   python Employee_Management_system.py
   ```

## API Endpoints

| Method | Endpoint | Description |
|--------|-------------|-------------|
| `GET`  | `/` | Welcome message |
| `POST` | `/employees` | Add a new employee |
| `GET`  | `/employees` | Get all employees |
| `GET`  | `/employees/<id>` | Get an employee by ID |
| `PUT`  | `/employees/<id>` | Update an employee by ID |
| `DELETE` | `/employees/<id>` | Delete an employee by ID |

## Usage

### Adding an Employee
```bash
curl -X POST "http://127.0.0.1:5000/employees" -H "Content-Type: application/json" -d '{"name":"John Doe","email":"john@example.com","age":30,"position":"Software Engineer","salary":75000}'
```

### Fetching All Employees
```bash
curl -X GET "http://127.0.0.1:5000/employees"
```

### Updating an Employee
```bash
curl -X PUT "http://127.0.0.1:5000/employees/1" -H "Content-Type: application/json" -d '{"name":"John Doe","email":"john@example.com","age":32,"position":"Senior Engineer","salary":85000}'
```

### Deleting an Employee
```bash
curl -X DELETE "http://127.0.0.1:5000/employees/1"
```

