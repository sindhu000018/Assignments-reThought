import sqlite3
import argparse

# Connect to SQLite
conn = sqlite3.connect('school.db')
cursor = conn.cursor()

# Create Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES Teacher(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    class_id INTEGER,
    FOREIGN KEY (class_id) REFERENCES Class(id)
)
''')

conn.commit()

# Print Help Menu Always
print("\n==== School Database CLI ====")
print("Available commands:")
print("--add-teacher [name]                : Add a teacher")
print("--add-class [name] [teacher_id]     : Add a class with a teacher")
print("--add-student [name] [class_id]     : Add a student to a class")
print("--query class_students --id [id]    : List students in a class")
print("--query teacher_students --id [id]  : List all students for a teacher")
print("--query class_with_teacher --id [id]: List students in a class with the teacher")
print("--list-teachers                     : List all teachers with their IDs")
print("--list-classes                      : List all classes with their IDs and teacher IDs")
print("--list-students                     : List all students with their class IDs")
print("================================\n")

# Argument Parsing
parser = argparse.ArgumentParser(description='School DB CLI')
parser.add_argument('--add-teacher', nargs=1)
parser.add_argument('--add-class', nargs=2)
parser.add_argument('--add-student', nargs=2)
parser.add_argument('--query', choices=['class_students', 'teacher_students', 'class_with_teacher'])
parser.add_argument('--id', type=int)
parser.add_argument('--list-teachers', action='store_true')
parser.add_argument('--list-classes', action='store_true')
parser.add_argument('--list-students', action='store_true')

args = parser.parse_args()

# Add Teacher
if args.add_teacher:
    cursor.execute("INSERT INTO Teacher (name) VALUES (?)", (args.add_teacher[0],))
    conn.commit()
    print("✅ Teacher added.")

# Add Class
if args.add_class:
    cursor.execute("INSERT INTO Class (name, teacher_id) VALUES (?, ?)", (args.add_class[0], args.add_class[1]))
    conn.commit()
    print("✅ Class added.")

# Add Student
if args.add_student:
    cursor.execute("INSERT INTO Student (name, class_id) VALUES (?, ?)", (args.add_student[0], args.add_student[1]))
    conn.commit()
    print("✅ Student added.")

# Query: Students in a Class
if args.query == 'class_students':
    cursor.execute("SELECT id, name FROM Student WHERE class_id = ?", (args.id,))
    students = cursor.fetchall()
    print(f"📘 Students in Class ID {args.id}:")
    for s in students:
        print(f"ID: {s[0]}, Name: {s[1]}")

# Query: Students for a Teacher
if args.query == 'teacher_students':
    cursor.execute('''
        SELECT Student.id, Student.name
        FROM Student
        JOIN Class ON Student.class_id = Class.id
        WHERE Class.teacher_id = ?
    ''', (args.id,))
    students = cursor.fetchall()
    print(f"📘 Students for Teacher ID {args.id}:")
    for s in students:
        print(f"ID: {s[0]}, Name: {s[1]}")

# Query: Students in a Class with Teacher Name
if args.query == 'class_with_teacher':
    cursor.execute('''
        SELECT Student.name, Class.name, Teacher.name
        FROM Student
        JOIN Class ON Student.class_id = Class.id
        JOIN Teacher ON Class.teacher_id = Teacher.id
        WHERE Class.id = ?
    ''', (args.id,))
    rows = cursor.fetchall()
    print(f"📘 Students in Class ID {args.id} with Teacher:")
    for row in rows:
        print(f"Student: {row[0]}, Class: {row[1]}, Teacher: {row[2]}")

# List Teachers
if args.list_teachers:
    cursor.execute("SELECT id, name FROM Teacher")
    rows = cursor.fetchall()
    print("📋 Teachers:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}")

# List Classes
if args.list_classes:
    cursor.execute("SELECT id, name, teacher_id FROM Class")
    rows = cursor.fetchall()
    print("📋 Classes:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Teacher ID: {row[2]}")

# List Students
if args.list_students:
    cursor.execute("SELECT id, name, class_id FROM Student")
    rows = cursor.fetchall()
    print("📋 Students:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Class ID: {row[2]}")

conn.close()
