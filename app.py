from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rollno TEXT NOT NULL,
        course TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/", methods=["GET", "POST"])
def home():

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    # Add Student
    if request.method == "POST":
        name = request.form["name"]
        rollno = request.form["rollno"]
        course = request.form["course"]

        cur.execute(
            "INSERT INTO students(name, rollno, course) VALUES(?,?,?)",
            (name, rollno, course)
        )

        conn.commit()

    # Search Student
    search = request.args.get("search")

    if search:
        cur.execute(
            "SELECT * FROM students WHERE name LIKE ? OR rollno LIKE ?",
            ('%' + search + '%', '%' + search + '%')
        )
    else:
        cur.execute("SELECT * FROM students")

    students = cur.fetchall()

    conn.close()

    return render_template("index.html", students=students)


# Delete Student
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


# Edit Student
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("students.db")
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        rollno = request.form["rollno"]
        course = request.form["course"]

        cur.execute(
            "UPDATE students SET name=?, rollno=?, course=? WHERE id=?",
            (name, rollno, course, id)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()

    conn.close()

    return render_template("edit.html", student=student)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)