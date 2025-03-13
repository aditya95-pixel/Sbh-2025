# load packages==============================================================
from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pickle
import sqlite3
import os
import json
from decouple import config
import random
app = Flask(__name__)
app.secret_key = "secret key"
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS instructors (id INTEGER PRIMARY KEY AUTOINCREMENT,instructorid TEXT,instructorname TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY AUTOINCREMENT,roomno TEXT,seatcap INTEGER)')
    conn.execute('CREATE TABLE IF NOT EXISTS meetings (id INTEGER PRIMARY KEY AUTOINCREMENT, pid TEXT, time TEXT, day TEXT)')
    conn.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    courseno TEXT,
                    coursename TEXT,
                    maxstudents INTEGER,
                    instructorid TEXT,
                    FOREIGN KEY (instructorid) REFERENCES instructors (instructorid))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    dept_name TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS department_courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dept_id INTEGER,
                    course_id INTEGER,
                    FOREIGN KEY (dept_id) REFERENCES departments(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id))''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_id INTEGER,
            course_id INTEGER,
            section_name TEXT,
            max_students INTEGER,
            FOREIGN KEY (dept_id) REFERENCES departments(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')
    print("Table created successfully")
    conn.close()
class Data:
    def __init__(self):
        self._rooms = self._fetch_rooms()
        self._meeting_times = self._fetch_meeting_times()
        self._instructors = self._fetch_instructors()
        self._courses = self._fetch_courses()
        self._depts = self._fetch_departments()
        self._sections = self._fetch_sections()
    def _fetch_rooms(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT roomno, seatcap FROM rooms")
        rooms = [{"roomno": row[0], "seatcap": row[1]} for row in cursor.fetchall()]
        conn.close()
        return rooms

    def _fetch_meeting_times(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT time, day FROM meetings")
        meeting_times = [{"time": row[0], "day": row[1]} for row in cursor.fetchall()]
        conn.close()
        return meeting_times

    def _fetch_instructors(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT instructorid, instructorname FROM instructors")
        instructors = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return instructors

    def _fetch_departments(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, dept_name FROM departments")
        depts = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return depts

    # Modified to include course IDs
    def _fetch_courses(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, courseno, coursename, maxstudents, instructorid FROM courses")
        courses = [
            {
                "id": row[0],
                "courseno": row[1],
                "coursename": row[2],
                "maxstudents": row[3],
                "instructorid": row[4]
            } for row in cursor.fetchall()
        ]
        conn.close()
        return courses

    # Modified to fetch actual sections
    def _fetch_sections(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, dept_id, course_id FROM sections")
        return [
            {"id": row[0], "dept_id": row[1], "course_id": row[2]}
            for row in cursor.fetchall()
        ]

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_meetingTimes(self):
        return self._meeting_times

    def get_sections(self):
        return self._sections

init_sqlite_db()
#home
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html',username=session['username'])
    else:
        return redirect(url_for('login'))
#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash("Invalid login credentials. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')
#register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            # Generate the password hash using the default method
            hashed_password = generate_password_hash(password)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()

            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        else:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('register'))

    return render_template('register.html')
#logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))
@app.route("/instructor", methods=['GET', 'POST'])
def instructor():
    if request.method == 'POST':
        id = request.form['instructorid']
        name = request.form['instructorname']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM instructors WHERE instructorid=?", (id,))
        user = cursor.fetchone()
        if user:
            cursor.execute("UPDATE instructors SET instructorname=? WHERE instructorid=?", (name, id))
        else:
            cursor.execute("INSERT INTO instructors (instructorid, instructorname) VALUES (?, ?)", (id, name))
        conn.commit()  # Ensure the changes are saved
        conn.close()
        return redirect(url_for('instructor'))  # Redirect only after committing
    return render_template('instructor.html')
@app.route("/room", methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        roomno=request.form['roomno']
        seatcap=request.form['seatcap']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE roomno=?",(roomno,))
        user = cursor.fetchone()
        if user:
            cursor.execute("UPDATE rooms SET seatcap=? WHERE roomno=?",(seatcap,roomno))
        else:
            cursor.execute("INSERT INTO rooms (roomno,seatcap) VALUES (?, ?)", (roomno,seatcap))
        conn.commit()  # Ensure the changes are saved
        conn.close()
        return redirect(url_for('room'))  # Redirect only after committing
    return render_template('room.html')
@app.route("/meeting", methods=['GET', 'POST'])
def meeting():
    if request.method == 'POST':
        pid = request.form['pid']
        time = request.form['time']
        day = request.form['day']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meetings WHERE pid=? AND day=?", (pid, day))
        existing_meeting = cursor.fetchone()

        if existing_meeting:
            cursor.execute("UPDATE meetings SET time=? WHERE pid=? AND day=?", (time, pid, day))
        else:
            cursor.execute("INSERT INTO meetings (pid, time, day) VALUES (?, ?, ?)", (pid, time, day))
        
        conn.commit()
        conn.close()
        flash("Meeting time updated successfully!")
        return redirect(url_for('meeting'))
    
    return render_template('meeting.html')
@app.route("/courses", methods=['GET', 'POST'])
def courses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT instructorid, instructorname FROM instructors")
    instructors = cursor.fetchall()
    
    if request.method == 'POST':
        courseno = request.form['course_number']
        coursename = request.form['course_name']
        maxstudents = request.form['max_students']
        instructorid = request.form['instructor']
        
        cursor.execute("INSERT INTO courses (courseno, coursename, maxstudents, instructorid) VALUES (?, ?, ?, ?)", 
                       (courseno, coursename, maxstudents, instructorid))
        conn.commit()
        conn.close()
        return redirect(url_for('courses'))
    
    conn.close()
    return render_template('courses.html', instructors=instructors)
@app.route("/departments", methods=['GET', 'POST'])
def departments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        dept_name = request.form['dept_name']
        selected_courses = request.form.getlist('courses')  # Get multiple selected courses

        cursor.execute("INSERT INTO departments (dept_name) VALUES (?)", (dept_name,))
        dept_id = cursor.lastrowid  # Get the last inserted department ID

        for course_id in selected_courses:
            cursor.execute("INSERT INTO department_courses (dept_id, course_id) VALUES (?, ?)", (dept_id, course_id))
            cursor.execute("INSERT INTO sections (dept_id, course_id, section_name) VALUES (?, ?, ?)",
                          (dept_id, course_id, f"Section-{random.randint(100,999)}"))
        conn.commit()
        conn.close()
        return redirect(url_for('departments'))

    # Fetch all available courses
    cursor.execute("SELECT id, coursename FROM courses")
    courses = cursor.fetchall()
    conn.close()

    return render_template('departments.html', courses=courses)
POPULATION_SIZE = 30
NUMB_OF_ELITE_SCHEDULES = 2
TOURNAMENT_SELECTION_SIZE = 8
MUTATION_RATE = 0.05
VARS = {'generationNum': 0, 'terminateGens': False}

data = None
class Schedule:
    def __init__(self, data):
        self.data = data
        self.classes = []
        self.fitness = 0
        self.conflicts = 0
        self.is_fitness_changed = True

    def initialize(self):
        for section in self.data.get_sections():
            try:
                dept = next(d for d in self.data.get_depts() if d["id"] == section["dept_id"])
                course = next(c for c in self.data.get_courses() if c["id"] == section["course_id"])
                instructor = next(i for i in self.data.get_instructors() if i["id"] == course["instructorid"])
                
                # Store full objects, not just names
                for _ in range(random.randint(2, 3)):
                    self.classes.append({
                        "section": section,
                        "course": course,        # Full course dict
                        "dept": dept,           # Full dept dict
                        "instructor": instructor, # Full instructor dict
                        "room": random.choice(self.data.get_rooms()),
                        "time": random.choice(self.data.get_meetingTimes())
                    })
            except StopIteration:
                continue
        return self

    def calculate_fitness(self):
        # Add these checks
        # Prevent same course in same department multiple times
        department_courses = {}
        for cls in self.classes:
            key = f"{cls['dept']['id']}-{cls['course']['id']}"
            if key in department_courses:
                self.conflicts += 2  # Strong penalty
            department_courses[key] = True
        
        # Penalize instructor time conflicts heavily
        instructor_times = {}
        for cls in self.classes:
            key = f"{cls['instructor']['id']}-{cls['time']['day']}-{cls['time']['time']}"
            if key in instructor_times:
                self.conflicts += 3  # Very strong penalty
            instructor_times[key] = True

    def get_fitness(self):
        if self.is_fitness_changed:
            self.calculate_fitness()
            self.is_fitness_changed = False
        return self.fitness

class Population:
    def __init__(self, size, data):
        self.size = size
        self.data = data
        self.schedules = [Schedule(data).initialize() for _ in range(size)]

    def get_schedules(self):
        return self.schedules
class GeneticAlgorithm:
    def __init__(self, data):
        self.data = data

    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, population):
        new_population = Population(0, self.data)
        elites = population.get_schedules()[:NUMB_OF_ELITE_SCHEDULES]
        new_population.schedules.extend(elites)
        
        while len(new_population.schedules) < POPULATION_SIZE:
            parent1 = self._tournament_selection(population)
            parent2 = self._tournament_selection(population)
            child = self._crossover(parent1, parent2)
            new_population.schedules.append(child)
            
        return new_population

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate(population.schedules[i])
        return population

    def _crossover(self, parent1, parent2):
        child = Schedule(self.data)
        split_point = random.randint(0, len(parent1.classes))
        child.classes = parent1.classes[:split_point] + parent2.classes[split_point:]
        return child

    def _mutate(self, schedule):
        for cls in schedule.classes:
            if random.random() < MUTATION_RATE:
                # Ensure new room can accommodate course
                new_room = random.choice(self.data.get_rooms())
                while new_room["seatcap"] < cls["course"]["maxstudents"]:
                    new_room = random.choice(self.data.get_rooms())
                cls["room"] = new_room

    def _tournament_selection(self, population):
        tournament = random.sample(population.get_schedules(), TOURNAMENT_SELECTION_SIZE)
        return max(tournament, key=lambda x: x.get_fitness())

@app.route('/api/generation-number')
def apiGenNum():
    return jsonify({'genNum': VARS['generationNum']})

@app.route('/api/terminate')
def apiTerminateGens():
    VARS['terminateGens'] = True
    return redirect(url_for('home'))
@app.route('/timetable')
def timetable():
    data = Data()
    population = Population(POPULATION_SIZE, data)
    ga = GeneticAlgorithm(data)
    
    VARS['generationNum'] = 0
    VARS['terminateGens'] = False
    
    while VARS['generationNum'] < 100 and not VARS['terminateGens']:
        population = ga.evolve(population)
        population.schedules.sort(key=lambda x: x.get_fitness(), reverse=True)
        VARS['generationNum'] += 1
        print(f"Generation {VARS['generationNum']} - Best Fitness: {population.schedules[0].get_fitness()}")

    best_schedule = population.schedules[0]
    
    # Format data for template
    formatted_schedule = []
    for cls in best_schedule.classes:
        formatted_schedule.append({
            'department': cls['dept']['name'],
            'course': cls['course']['coursename'],
            'instructor': cls['instructor']['name'],
            'room': f"{cls['room']['roomno']} ({cls['room']['seatcap']} seats)",
            'day': cls['time']['day'],
            'time': cls['time']['time']
        })
    
    return render_template('timetable.html', schedule=formatted_schedule)
if __name__ == '__main__':
    app.run(debug=True)