📘 Assignment Management System

A Flask-based web application for managing student assignments, evaluations, announcements, and course-related workflows in a college environment. 
The system provides separate interfaces for Students, Teachers, and Admins, enabling efficient handling of assignments, submissions, marks, and updates.

🚀 Features

👨‍🎓 Student Features
View available assignments uploaded by teachers
Submit assignment files online
View submitted assignments and check marks once evaluated
Receive important announcements
Update profile details

👩‍🏫 Teacher Features
Upload new assignments along with deadlines and course information
View assignment submissions from students
Evaluate student submissions and update marks
View and edit personal profile
Post announcements to students

🛠 Admin Features
Manage all users (students & teachers)
Oversee all assignments and submissions
Publish and manage announcements
Control system-level settings and workflows

🧱 Tech Stack

Component	Technology
Frontend	HTML, CSS, JavaScript
Backend	Flask (Python)
Database	Firebase Firestore
Auth System	Firebase Authentication
Storage	Firebase Cloud Storage

📂 Project Structure
/templates       --> All HTML templates (student, teacher, admin)
static/          --> CSS, JS, images
app.py           --> Main Flask application
README.md        --> Documentation

🔐 Authentication & Authorization
The application includes role-based authentication:
Email/Password login
Roles: Administrator, Teacher, Student
Secure Firebase token validation
Session-based access restrictions

📤 Assignment Workflow

Teacher uploads an assignment with name, file, and deadline
Students view the assignment and submit their work
Teacher reviews submissions, evaluates, and updates marks
Students can check marks and comments once published

📨 Announcements Module
Admins and Teachers can post announcements visible to all students and teachers for important updates.

🏁 How to Run the Project

Clone the repository
git clone <repo-url>
cd assignment-management

Install dependencies
pip install -r requirements.txt

Add google-services.json and Firebase credentials

Run the Flask app
python app.py

🎯 Purpose
This project was developed to simplify assignment distribution, submission tracking, evaluation, 
and announcement management in a college system, making academic communication faster and more organized.
