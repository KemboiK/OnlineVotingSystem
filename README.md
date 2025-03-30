# OnlineVotingSystem

# University Online Voting System  

## Overview  
The **University Online Voting System** is a web-based application built with **Django**, **SQLite3**, **HTML**, and **CSS**. It provides a simple and secure way for university students to vote online. The system includes separate interfaces for **administrators** and **voters**.  

## Features  

### 🔹 Admin Interface  
- Add and manage candidates  
- View voter statistics  
- Monitor election results in real-time  

### 🔹 Voter Interface  
- Simple and user-friendly voting process  
- Secure authentication for voters  
- Ability to view election results  

## Technologies Used  
- **Django** (Backend Framework)  
- **SQLite3** (Database)  
- **HTML, CSS** (Frontend and Styling)  

## Installation and Setup  

### 🛠 Prerequisites  
Ensure you have **Python** and **Django** installed on your system.  

### 📌 Steps to Run the Project  

#### # Clone the repository  
```bash
git clone https://github.com/KemboiK/OnlineVotingSystem.git
cd OnlineVotingSystem

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate     # For Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver

Now visit http://127.0.0.1:8000/ in your browser to access the system.

#📌 Usage
# Admin Access
Admins can log in at /admin/ to manage elections.
They can add candidates, view results, and monitor election statistics.
# Voter Access
Voters can log in and cast their votes through the main interface.
They can also view election results after voting.
#📊 Election Statistics
The system provides real-time election results.
Admins can track vote counts and voter participation.

#🤝 Contributors              
KemboiK
Benedict2002
MaithiaRobert
Feel free to contribute via pull requests!
