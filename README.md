## Microservices File Structure

INFS605-Microservice-Assessment/  
├── docker-compose.yml  
├── README.md  
├── frontend/  
│   ├── Public/  
│   ├── src/  
│   ├── Dockerfile  
│   ├── index.html  
│   ├── package.json  
│   └── vite-config.js  
├── student-profile/  
│   ├── app.py  
│   ├── Dockerfile  
│   ├── init.sql  
│   ├── requirements.txt  
│   └── wait-for-it.sh  
├── catalog-backend/  
│   ├── app.py  
│   ├── Dockerfile  
│   ├── init.sql  
│   ├── requirements.txt  
│   └── wait-for-it.sh  
├── feedback-backend/  
│   ├── app.py  
│   ├── Dockerfile  
│   ├── init.sql  
│   ├── requirements.txt  
│   └── wait-for-it.sh  
├── email-service/  
│   ├── sent_emails/  
│   ├── app.py  
│   ├── Dockerfile  
│   ├── init.sql  
│   └── requirements.txt  
├── .env.example  
├── .gitignore  
├── docker-compose.yml  
├── LICENSE  
└── README.md  

Technologies used:
- Python + Flask
- Docker + Docker Compose
- PostgreSQL
- React + Tailwind CSS


## Start Instructions

### 1. Prerequisites
You must have Docker Desktop and Python3 installed

### 2. File Setup
Extract the zip file you have been send  
OR  
Clone the project from github with the command `git clone https://github.com/baileythorp04/INFS605-Microservices-Assessment.git`

### 3. Building the system

Ensure you have Docker Desktop running  

In the terminal, navigate to the folder which you just extracted or cloned this project into. It is the folder which contains docker-compose.yml

type, `docker-compose up -d --build`  

Once the containers have started, check in Docker Desktop that all the containers are running. If they are not all running, you may need to restart the containers by doing `docker-compose down` followed by `docker-compose up -d --build` again.

### 4. Running the system

Go to this address to access the frontend. You can use all of the services through this page: http://localhost:3000  

Go to these addresses to see entries in each respective database, including example data:
- http://localhost:5001/students
- http://localhost:5002/courses
- http://localhost:5003/feedback

### 7. API Endpoints

#### Student Profile Service (Provided by starter files) (http://localhost:5001)
- `GET /students` – list all students
- `GET /students/:id` – get a student
- `POST /students` – `{ name, email }`
- `PUT /students/:id` – update `{ name?, email? }`
- `DELETE /students/:id`
- `POST /students/:id/attendance` – `{ date: 'YYYY-MM-DD', status: 'Present|Absent|Late|Excused' }`

#### Course catalog service (http://localhost:5002)
This service is for creating and deleting courses.  
Courses are stored with Postgresql with this schema:  
{ "id": int, "name": str, "code": str, "year": int, "description": str }  

- `GET /courses` - list all courses
- `POST /courses` - `{ name, code, year, description }` - create one course

#### Feedback service (http://localhost:5003)
This service is for creating, deleting, and replying to feedback.
Feedback is stored with Postgresql with this schema:  
{ "id": int, "student_name": str, "email: str, "text": str, "reply" : str, "feedback_state" : str }

- `GET /feedback` - list all feedback
- `POST /feedback` - `{ name, email, text }` - create one feedback
- `POST /feedback/<int:feedback_id>/reply` - `{ reply }` - update `reply` and set `feedback_status` to 'replied'
- `DELETE /feedback/<int:feedback_id>` - delete one feedback

#### Email send service (http://localhost:5004)
This service is for sending email notifications whenever feedback is made or replied to.  
Instead of actually sending emails, emails are locally written as a .txt file in email-service/sent_emails/feedback-[datetime] 

- `POST /email/feedback` - send an email to an admin about feedback being created
- `POST /email/reply` - send an email to student about a reply to their feedback 
