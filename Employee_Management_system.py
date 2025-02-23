#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install pymysql')


# In[ ]:


from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


# ---------------------- Database Configuration ----------------------
DATABASE_CONFIG = {
    "MYSQL_HOST": "localhost",
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "Asish@2002",  
    "MYSQL_DB": "employees_db"
}

# ---------------------- Initialize MySQL Connection ----------------------
db = None  # Global database variable

def init_db():
    """Initialize the MySQL database connection."""
    global db
    try:
        db = MySQLdb.connect(
            host=DATABASE_CONFIG["MYSQL_HOST"],
            user=DATABASE_CONFIG["MYSQL_USER"],
            passwd=DATABASE_CONFIG["MYSQL_PASSWORD"],
            db=DATABASE_CONFIG["MYSQL_DB"],
            cursorclass=MySQLdb.cursors.DictCursor
        )
        print(" Database connected successfully")
    except MySQLdb.Error as e:
        print(f" Error connecting to MySQL: {e}")
        db = None  # Ensure db is None if connection fails

def get_db():
    """Returns the database connection or initializes it if not already connected."""
    global db
    if db is None:
        print(" Database connection is not initialized. Attempting to reconnect...")
        init_db()
    
    if db is None:
        print(" Database connection failed. Check MySQL server and credentials.")
        return None
    return db

# ---------------------- Flask App Setup ----------------------
app = Flask(__name__)
CORS(app)

# Initialize Database
init_db()

#  Email validation function
def is_valid_email(email):
    """Validate email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ---------------------- CRUD Operations ----------------------
def get_all_employees():
    """Fetch all employees from the database."""
    try:
        conn = get_db()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()
        return employees
    except MySQLdb.Error as e:
        print(f" Error fetching employees: {e}")
        return []

def get_employee_by_id(emp_id):
    """Fetch an employee by ID."""
    try:
        conn = get_db()
        if conn is None:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
        employee = cursor.fetchone()
        cursor.close()
        return employee
    except MySQLdb.Error as e:
        print(f" Error fetching employee by ID: {e}")
        return None

def get_employee_by_email(email):
    """Fetch an employee by email."""
    try:
        conn = get_db()
        if conn is None:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE email = %s", (email,))
        employee = cursor.fetchone()
        cursor.close()
        return employee
    except MySQLdb.Error as e:
        print(f" Error fetching employee by email: {e}")
        return None

def create_employee(name, email, age, position, salary):
    """Insert a new employee into the database."""
    try:
        conn = get_db()
        if conn is None:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, email, age, position, salary) VALUES (%s, %s, %s, %s, %s)",
            (name, email, age, position, salary)
        )
        conn.commit()
        cursor.close()
        return True
    except MySQLdb.Error as e:
        print(f" Error creating employee: {e}")
        return False

def update_employee(emp_id, name, email, age, position, salary):
    """Update an existing employee."""
    try:
        conn = get_db()
        if conn is None:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employees SET name = %s, email = %s, age = %s, position = %s, salary = %s WHERE id = %s",
            (name, email, age, position, salary, emp_id)
        )
        conn.commit()
        cursor.close()
        return True
    except MySQLdb.Error as e:
        print(f" Error updating employee: {e}")
        return False

def delete_employee(emp_id):
    """Delete an employee by ID."""
    try:
        conn = get_db()
        if conn is None:
            return False
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        conn.commit()
        cursor.close()
        return True
    except MySQLdb.Error as e:
        print(f" Error deleting employee: {e}")
        return False

# ---------------------- Flask Routes ----------------------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Employee Management API"}), 200

@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        name, email, age, position, salary = (
            data.get('name'), data.get('email'), data.get('age'),
            data.get('position'), data.get('salary')
        )

        # 🔹 Input validations
        if not all([name, email, age, position, salary]):
            return jsonify({"error": "All fields are required"}), 400
        if len(name) < 3:
            return jsonify({"error": "Name must be at least 3 characters"}), 400
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        if not (18 <= int(age) <= 65):
            return jsonify({"error": "Age must be between 18 and 65"}), 400
        if float(salary) < 5000:
            return jsonify({"error": "Salary must be at least 5000"}), 400

        # 🔹 Check for duplicate email
        existing_employee = get_employee_by_email(email)
        if existing_employee:
            return jsonify({"error": "Email already exists"}), 409

        # 🔹 Insert employee
        if not create_employee(name, email, age, position, salary):
            return jsonify({"error": "Database error while adding employee"}), 500

        return jsonify({"message": "Employee added successfully"}), 201

    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(get_all_employees()), 200

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    return jsonify(get_employee_by_id(id) or {"error": "Employee not found"}), 404

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee_route(id):
    data = request.json
    if not get_employee_by_id(id):
        return jsonify({"error": "Employee not found"}), 404
    update_employee(id, data['name'], data['email'], data['age'], data['position'], data['salary'])
    return jsonify({"message": "Employee updated successfully"}), 200

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee_route(id):
    if not get_employee_by_id(id):
        return jsonify({"error": "Employee not found"}), 404
    delete_employee(id)
    return jsonify({"message": "Employee deleted successfully"}), 200

# ---------------------- Run Flask App ----------------------
if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)


# In[ ]:




