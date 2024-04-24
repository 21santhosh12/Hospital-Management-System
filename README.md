Hospital Management System
Introduction
The Hospital Management System is a web application built using Flask, SQLAlchemy, and other technologies.
It aims to streamline the management processes within a hospital, including patient bookings, doctor information management, and user authentication.

Features
User Authentication: Users can sign up, log in, and log out securely.
Patient Booking: Patients can book appointments with doctors specifying their details such as name, gender, disease, etc.
Doctor Management: Doctors can be added to the system along with their respective departments.
View Bookings: Users can view their booked appointments.
Edit and Delete Bookings: Users can modify or cancel their bookings.
Search: Search functionality to find available departments.
Technologies Used
Flask: Web framework used to build the application.
SQLAlchemy: ORM (Object-Relational Mapping) used for interacting with the database.
Flask-Login: Provides user session management.
Werkzeug: Used for password hashing and checking.
MySQL: Database used for storing application data.
Installation
Clone the repository:
bash
Copy code
git clone <repository-url>
Install dependencies:
Copy code
pip install -r requirements.txt
Set up the database:
Create a MySQL database named hospital_management.
Update config.json with your database credentials.
Run the application:
Copy code
python app.py
Access the application in your browser at http://localhost:5000.
Usage
Upon accessing the application, users can sign up or log in.
After logging in, users can perform various actions such as booking appointments, viewing bookings, etc.
Doctors can be added via the doctor management interface.
Users can edit or delete their bookings as needed.
The search feature allows users to check the availability of departments.
Contributing
Contributions are welcome! If you'd like to contribute to this project, feel free to open an issue or submit a pull request.

License
This project is licensed under the MIT License.
