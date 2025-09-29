import os
import time
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

# --------------------Database Connection--------------------#

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    while True:
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            return conn
        except OperationalError as e:
            print(f"Database connection failed: {e}")
            time.sleep(5)

#--------------------Ensure Table Exists--------------------#
@app.before_first_request
def setup_tables():
    """Created required tables if they do not exist."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            firstname VARCHAR(50), 
            lastname VARCHAR(50),
            birthdate DATE,
            email VARCHAR(100),
            enrolled_date DATE
        );
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            description TEXT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

#------------------------Student API------------------------#


@app.route('/students', methods=['POST'])
def add_student():
    """Insert a new student into the database."""
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO students (firstname, lastname, birthdate, email, enrolled_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING student_id;
        """, [
            data.get('firstname'),
            data.get('lastname'),
            data.get('birthdate'),
            data.get('email'),
            data.get('enrolled_date'),
        ])
        student_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": 'student added successfully', "student_id": student_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/students', methods=['GET'])
def get_students():
        """Retrieve all students from the database."""
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM students;")
            students = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify(students), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
        """Retrieve a single student by ID."""
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM students WHERE student_id = %s;", (student_id,))
            student = cur.fetchone()
            cur.close()
            conn.close()
            if student:
                return jsonify(student), 200
            else:
                return jsonify({"error": "Student not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
#------------------------Item API------------------------#
@app.route('/items', methods=['POST'])
def add_item():
    """Insert a new item into the database."""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id;",
        (name, description)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': new_id, 'name': name, 'description': description}), 201
    
@app.route('/items', methods=['GET'])
def get_items():
    """Retrieve all items from the database."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM items;")
    items = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {'id': item[0], "name": item[1], "description": item[2]} for item in items
    ])

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve a single item by ID."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, description FROM items WHERE id = %s;", (item_id,))
    item = cur.fetchone()
    cur.close()
    conn.close()

    if item is None:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify({'id': item[0], 'name': item[1], 'description': item[2]})
    
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item by ID."""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name and not description:
        return jsonify({"error": 'At least one of name or description is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE id = %s;", (item_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    
    cur.execute(
        "UPDATE items SET name = %s, description = %s WHERE id = %s;",
        (name, description, item_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'id': item_id, 'name': name, 'description': description})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item by ID."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items WHERE id = %s;", (item_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    
    cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': f'item {item_id} deleted successfully'})

#------------------------Run App------------------------#
if __name__ == '__main__':
    #Example: postgresql://username:password@localhost:5432/mydatabase
    os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@my_postgres:5432/cruddb'
    app.run(host='0.0.0.0', port=5000, debug=True)
    # metrics = PrometheusMetrics(app)