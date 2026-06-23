# Job Seeker Portal

A web-based **Job Seeker Portal** developed as a **BCA Major Project**. The platform allows job seekers to register, build their profiles, and search/apply for jobs, while employers can register, post job openings, and manage applications from candidates.

## 📌 Features

### For Job Seekers
- Separate registration and login
- Create and update profile
- Browse and search job listings
- Apply for jobs directly through the portal
- Track applied jobs

### For Employers
- Separate registration and login
- Post new job openings
- Edit or remove job listings
- View and manage applications received from job seekers

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Django |
| Database | MySQL |

## ⚙️ Installation & Setup

1. Clone the repository
```bash
   git clone https://github.com/devbypratima/job-seeker-portal.git
   cd job-seeker-portal
```

2. Create and activate a virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Configure the MySQL database in `settings.py` with your credentials

5. Run migrations
```bash
   python manage.py makemigrations
   python manage.py migrate
```http://127.0.0.1:8000/ ## 🎯 Objective

The goal of this project is to bridge the gap between job seekers and employers by providing a simple, centralized platform where job seekers can find relevant opportunities and employers can find suitable candidates efficiently.

## 👩‍💻 Author

**Pratima Bairagi**
BCA Major Project

## 📄 License

This project is created for academic purposes as part of the BCA curriculum.


6. Start the development server
```bash
   python manage.py runserver
```

7. Open the project in your browser
   
