# 🎓 Student Database Management System (SDMS)
## Overview
A web-based Student Management System built with Django, providing functionalities for administrators, teachers, and students. 
This system includes course management, student enrollment, grading, and user profile management.


## 📝Specifications for Functionality 

### - Admin Management
Admin user creation and management

### - Teacher Management
- Teacher user creation and management
- Course assignment to teachers

### - Student Management
- Student user creation and management
- Enrollment in courses
- Viewing grades

### - Course Management
- Course creation and management
- Teacher and student assignment to courses

### - Grading System
- Assignment of grades by teachers
- Viewing grades by students

## 📊Gant Chart
![image](https://github.com/user-attachments/assets/0cb2ccbe-22cd-4ed1-b60b-e119fa4c14e4)  

## 🎨UI/UX
![image](https://github.com/user-attachments/assets/ee30bcbb-39d6-4333-ae68-79edd5a9359b)
![image](https://github.com/user-attachments/assets/037b50ca-b5ca-4f7f-a025-92c6ed91783e)
![image](https://github.com/user-attachments/assets/17ff2780-7e72-4c32-9944-2c5799e9f0ac)

## 🛠 Tech Stack
- Backend: Django
- Database: SQLite
- Frontend: HTML, JavaScript, CSS
- Other Tools: Figma (UI/UX), Git (Version Control)

## 🚀 Installation

1. Clone the repository

```bash
git clone https://github.com/Kuugang/redditclone-django.git
cd redditclone-django
```

  

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

  

3. Install dependencies

```bash
pip install -r requirements.txt
```

  
4. Create .env file

```bash
touch .env
```

5. Configure environment variables in `.env`

```bash
DATABASE_HOST = 'YOUR DATABASE HOST'
DATABASE_NAME = 'YOUR DATABASE NAME'
DATABASE_PORT = 'YOUR DATABASE PORT'
DATABASE_USER = 'YOUR DATABASE USER'
DATABASE_PASSWORD = 'YOUR DATABASE PASSWORD'
GOOGLE_OAUTH_CLIENT_ID= 'YOUR GOOGLE WEB APP OAUTH CLIENT ID'
EMAIL_HOST_USER = 'YOUR EMAIL HOST USER'
EMAIL_HOST_PASSWORD = 'YOUR EMAIL HOST PASSWORD'
```
  
6. Run migrations and seeding

```bash
python manage.py migrate
python manage.py populate_topics
```

7. Collect static files

```bash
python manage.py collectstatic
```

8. Start the development server

```bash
python manage.py runserver
```
## 🔒 Security Note

-   Never commit `.env` file to version control
-   Use a `.gitignore` file to exclude sensitive credentials
-   Rotate credentials periodically
  

## 🤝 Contributing

1. Fork the repository

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Request

