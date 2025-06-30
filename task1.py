import psycopg2

conn=psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="POSTGRES",
    port="5432"
)

cur=conn.cursor()

# employees tablosunu oluştur
cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        emp_id INTEGER PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        salary INTEGER NOT NULL,
        job_title VARCHAR(100) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        hire_date DATE NOT NULL
    );
""")

# employees tablosuna kayıt ekle
cur.executemany("""
    INSERT INTO employees (emp_id, first_name, last_name, salary, job_title, gender, hire_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (emp_id) DO NOTHING;
""", [
    (17679, 'Robert', 'Gilmore', 110000, 'Operations Director', 'Male', '2018-09-04'),
    (26650, 'Elvis', 'Ritter', 86000, 'Sales Manager', 'Male', '2017-11-24'),
    (30840, 'David', 'Barrow', 85000, 'Data Scientist', 'Male', '2019-12-02'),
    (49714, 'Hugo', 'Forester', 55000, 'IT Support Specialist', 'Male', '2019-11-22'),
    (51821, 'Linda', 'Foster', 95000, 'Data Scientist', 'Female', '2019-04-29'),
    (67323, 'Lisa', 'Wiener', 75000, 'Business Analyst', 'Female', '2018-08-09'),
    (70950, 'Rodney', 'Weaver', 87000, 'Project Manager', 'Male', '2018-12-20'),
    (71329, 'Gayle', 'Meyer', 77000, 'HR Manager', 'Female', '2019-06-28'),
    (76589, 'Jason', 'Christian', 99000, 'Project Manager', 'Male', '2019-01-21'),
    (97927, 'Billie', 'Lanning', 67000, 'Web Developer', 'Female', '2018-06-25')
])

# departments tablosunu oluştur
cur.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        emp_id INTEGER,
        dept_name VARCHAR(50) NOT NULL,
        dept_id INTEGER,
        PRIMARY KEY (emp_id, dept_id)
    );
""")

# departments tablosuna kayıt ekle
cur.executemany("""
    INSERT INTO departments (emp_id, dept_name, dept_id)
    VALUES (%s, %s, %s)
    ON CONFLICT DO NOTHING;
""", [
    (17679, 'Operations', 13),
    (26650, 'Marketing', 14),
    (30840, 'Operations', 13),
    (49823, 'Technology', 12),
    (51821, 'Operations', 13),
    (67323, 'Marketing', 14),
    (71119, 'Administrative', 11),
    (76589, 'Operations', 13),
    (97927, 'Technology', 12)
])


# 1. Find the employees who get paid more than Rodney Weaver.
cur.execute("""
    SELECT first_name, last_name, salary
    FROM employees
    WHERE salary > (SELECT salary FROM employees WHERE first_name='Rodney' AND last_name='Weaver');
""")
print("1. Employees paid more than Rodney Weaver:", cur.fetchall())

# 2. Find the average, min and max salaries
cur.execute("""
    SELECT AVG(salary), MIN(salary), MAX(salary)
    FROM employees;
""")
print("2. Average, Min, Max salaries:", cur.fetchone())

# 3. Employees whose salary is more than 87000 (first name, last name, salary)
cur.execute("""
    SELECT first_name, last_name, salary
    FROM employees
    WHERE salary > 87000;
""")
print("3. Employees with salary > 87000:", cur.fetchall())

# 4. Employees who work under the Operations department
cur.execute("""
    SELECT e.first_name, e.last_name
    FROM employees e
    JOIN departments d ON e.emp_id = d.emp_id
    WHERE d.dept_name = 'Operations';
""")
print("4. Employees in Operations department:", cur.fetchall())

# 5. Employees who work under the Technology department
cur.execute("""
    SELECT e.first_name, e.last_name
    FROM employees e
    JOIN departments d ON e.emp_id = d.emp_id
    WHERE d.dept_name = 'Technology';
""")
print("5. Employees in Technology department:", cur.fetchall())

# 6. Average salary of female employees
cur.execute("""
    SELECT AVG(salary)
    FROM employees
    WHERE gender = 'Female';
""")
print("6. Average salary of female employees:", cur.fetchone()[0])

# 7. Average salaries of each department
cur.execute("""
    SELECT d.dept_name, AVG(e.salary)
    FROM employees e
    JOIN departments d ON e.emp_id = d.emp_id
    GROUP BY d.dept_name;
""")
print("7. Average salaries by department:", cur.fetchall())

# 8. Oldest and newest employees
cur.execute("""
    SELECT first_name, last_name, hire_date
    FROM employees
    WHERE hire_date = (SELECT MIN(hire_date) FROM employees)
       OR hire_date = (SELECT MAX(hire_date) FROM employees);
""")
print("8. Oldest and newest employees:", cur.fetchall())

# 9. Hiring date and department of the highest paid employee
cur.execute("""
    SELECT e.hire_date, d.dept_name
    FROM employees e
    JOIN departments d ON e.emp_id = d.emp_id
    WHERE e.salary = (SELECT MAX(salary) FROM employees);
""")
print("9. Hiring date and department of highest paid employee:", cur.fetchall())

# 10. Hiring date and department of the lowest paid employee
cur.execute("""
    SELECT e.hire_date, d.dept_name
    FROM employees e
    JOIN departments d ON e.emp_id = d.emp_id
    WHERE e.salary = (SELECT MIN(salary) FROM employees);
""")
print("10. Hiring date and department of lowest paid employee:", cur.fetchall())


conn.commit()
cur.close()
conn.close()

