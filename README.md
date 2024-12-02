# StudentDatabaseManagement
This is our Project in IM2 | Student Database Management System
Francis Nino B. Yap | Asher Caleb N. Paquit | Terrence John N. Duterte

Student Database Management System (SDMS)
Features Overview
The Student Database Management System (SDMS) provides an intuitive interface to manage student-related data effectively. Below is a comprehensive overview of its key features:

1. Student Management
Purpose: Track and manage student data.

Features:

Add, edit, and delete student records.
Search and filter students by specific criteria such as name or email.
2. Course Management
Purpose: Organize and manage courses and their enrollment details.

Features:

Add, edit, and delete courses.
Assign teachers to courses.
Manage course enrollments for students.
3. Grade Management
Purpose: Track academic performance.

Features:

Assign grades to students in specific courses.
Update or view grades by student or course.
Generate grade reports.
4. Teacher Management
Purpose: Maintain teacher details and assigned courses.

Features:

Add, edit, and delete teacher records.
Assign courses to teachers.
Track teacher responsibilities and performance.
5. Admin Dashboard
Purpose: Provide an overview of key system statistics and administrative capabilities.

Features:

View summary statistics for students, teachers, and courses.
Manage user roles and permissions.
6. Scholarship and Financial Aid Management
Purpose: Simplify the management of student scholarships and financial aid.

Features:

Record and track scholarship eligibility and disbursement.
View and manage student financial aid applications.
Key Interface Features
User Dashboard: Displays an overview of students, courses, and grades.
Navigation Menu: Allows access to modules like Students, Courses, Teachers, and Financial Aid.
Search and Filter: Quickly find records using a global search or filters.
Responsive Design: Fully functional across desktop and mobile devices.
User Roles
Admin
Full access to all functionalities.
Create, edit, delete records, manage users, and update roles.
Teacher
Limited access to course and grade management.
Update student grades and manage course materials.
Student
View personal data and grades.
Apply for scholarships or financial aid.
Technologies Used
Frontend: HTML, CSS, JavaScript.
Backend: Python (Django framework).
Database: SQLite (Development) or MySQL/PostgreSQL (Production).
Other Tools: Figma (UI/UX design), Git (Version control).
Links
Gantt Chart: View here
UI/UX Design: View here
ERD: View here
Getting Started
Follow these steps to set up and run the project locally:

Prerequisites
Ensure you have the following installed on your system:

Python 3.x
Django
Virtualenv
Backend Setup
Clone the repository and navigate to the project directory:

bash
Copy code
git clone <repository_url>
cd StudentDatabaseManagement
Create a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:
bash
Copy code
venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source venv/bin/activate
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Apply the database migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser to access the Django admin interface:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to set up a username, email, and password.

Run the development server:

bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000/.
