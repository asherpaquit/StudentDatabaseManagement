🎓 Student Database Management System (SDMS)
A powerful and intuitive platform for managing student-related data efficiently.

✨ Features Overview
The Student Database Management System (SDMS) provides a wide array of features to streamline student data management:

🧑‍🎓 1. Student Management
Purpose: Track and manage student data.
Features:

➕ Add, ✏️ edit, and ❌ delete student records.
🔍 Search and filter students by criteria (e.g., name or email).


📚 2. Course Management
Purpose: Organize and manage courses and enrollment details.
Features:

➕ Add, ✏️ edit, and ❌ delete courses.
👩‍🏫 Assign teachers to courses.
👥 Manage course enrollments for students.


🏆 3. Grade Management
Purpose: Monitor academic performance.
Features:

✅ Assign grades to students.
🛠️ Update or view grades by student or course.
📈 Generate grade reports.


🧑‍🏫 4. Teacher Management
Purpose: Maintain teacher details and course assignments.
Features:

➕ Add, ✏️ edit, and ❌ delete teacher records.
📋 Assign courses to teachers.
📊 Track teacher responsibilities.


🛠️ 5. Admin Dashboard
Purpose: Provide summary statistics and administrative tools.
Features:

📊 View statistics (e.g., total students, courses).
👤 Manage user roles and permissions.


💰 6. Scholarship and Financial Aid Management
Purpose: Simplify management of financial aid.
Features:

📝 Record and track scholarship eligibility.
💳 Manage disbursements and applications.

🌟 Key Interface Features
📊 User Dashboard: Overview of students, courses, and grades.
🧭 Navigation Menu: Access modules (Students, Courses, Teachers).
🔍 Search and Filter: Locate records with ease.
📱 Responsive Design: Functional across devices.


👥 User Roles
Role	Permissions
Admin	Full access to create, edit, and delete records. Manage user roles.
Teacher	Manage course enrollments and update student grades.
Student	View personal data and grades. Apply for scholarships.


🛠️ Technologies Used
Frontend: HTML, CSS, JavaScript
Backend: Python (Django framework)
Database: SQLite (Dev) / MySQL/PostgreSQL (Prod)
Other Tools: Figma (UI/UX), Git (Version Control)


📂 Getting Started
Prerequisites
Ensure you have the following installed:

Python 3.x
Django
Virtualenv
Backend Setup

1.Clone the repository:
bash
Copy code
git clone <repository_url>
cd StudentDatabaseManagement

2.Create a virtual environment:
bash
Copy code
python -m venv venv

3.Activate the environment:
On Windows:
bash

Copy code
venv\Scripts\activate

On macOS/Linux:
bash
Copy code
source venv/bin/activate


Install dependencies:
bash
Copy code
pip install -r requirements.txt


Apply migrations:
bash
Copy code
python manage.py makemigrations
python manage.py migrate


Create a superuser:
bash
Copy code
python manage.py createsuperuser


Run the development server:
bash
Copy code
python manage.py runserver
Access the app at http://127.0.0.1:8000/.
📎 Links
📅 Gantt Chart
🎨 UI/UX Design
📋 ERD

