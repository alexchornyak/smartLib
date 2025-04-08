Library Management System aka SmartLib

Overview:
The Library Management and Automation System is a web-based application designed to streamline the borrowing, searching, and returning of books. 
Built using Django, HTML, CSS, and JavaScript, the system integrates the Google Books API to enhance book searches.

Features:

User Authentication: Secure login and registration system.

Book Borrowing: Users can borrow books with automated due date tracking.

Book Searching: Utilizes the Google Books API for enhanced search functionality.

Book Returning: Tracks book return status.

Admin Dashboard: Manages books, users, and transactions.

Prerequisites:
- sudo apt-get install python
- pip install django
- python -m venv venv
  - Optional but recommended
 
How to Run:
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver
- All set!
