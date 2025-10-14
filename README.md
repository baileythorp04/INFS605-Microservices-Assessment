# INFS605-Assignment2-Starter-Files
This is a starter application for a BCIS second-year INFS605 Microservices programming assignment. It includes a containerized student-profile service (Python + Flask), a PostgreSQL database, a React (Vite) admin UI to list/search/add/delete students and record attendance and docker-compose.yml. Students are invited to extend the system by adding their own microservices and deploying a small-scale distributed application.

## License

Code in this repository is licensed under the [MIT License](LICENSE).

Assignment instructions, diagrams, and documentation (non-code) are licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

## Microservices Assignment Starter

This repository provides a starter  application for your programming assignment in the INFS605 Microservices course (BCIS Year 2).

You are provided with:
- A `student-profile` microservice built in Flask
- A PostgreSQL container for persistence
- A shared `docker-compose.yml` to deploy services
- a React (Vite) `student-profile` front end with an admin user interface

microservices-assignment/
├── docker-compose.yml
├── README.md
├── frontend/
│   ├── Public/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── vite-config.js
├── student-profile/
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

Your task is to build additional microservices, connect them using Docker Compose, and demonstrate a small, functional microservices architecture with clear service boundaries.

Start small, and iterate!

You can use this as a starting point for your assignment and consider adding further services – a Course Catalog Service, a Feedback Service, a Notification Service, a Grades Service (that can store and retrieve grades for students and courses), a Timetable Service (that can show weekly schedules for students or lecturers) an Assignment Tracker (shows coming and submitted assignments), a Room Booking Service (for team meetings), or come more generic services such as – an Image Upload Service, a Search Service, a Logging or Audit Trail Service, Frontend UI, PDF Generator, System Metrics Service. Or perhaps add the Adminer service from the week 6 tutorial class to directly access the PostGres student-db.

## Getting Started

### 1. Prerequisites
- Docker
- Docker-Compose 
- Python (if running services outside of Docker)
[If on Ubuntu: sudo apt install docker-compose]
[If on Ubuntu: sudo snap install docker]

Or if running this code locally on your laptop you will need: 
- Docker Desktop
- Python3

### 2. Pull the repository

Option 1. Use 'git clone' in your VS Code development environment

First install Git: If you haven't installed Git on your local device, download and install Git from the official Git website here: https://git-scm.com/downloads 

You can then do either of these:
(a) If you have the default 'Welcome page' open in VS Code (usually it is set to open on startup) there is a link 4 down called 'Clone Git Repository...' Click that.
(b) Or if you don't have any folders open, you will see a "Clone Repository" button in the Source Control tab. Click that. [Click the Source Control icon (the three circles connected by lines) in the Activity Bar on the left side of the VS Code window.]
(c) Ctrl+Shift+P (Windows/Linux) or Cmd+Shift+P (macOS) to open the Command Palette. Type 'git clone' and select the "Git: Clone" command....

Then type https://github.com/JB-Connect/INFS605-Assignment2-Starter-Files

This will pull the repository and ask you what folder you would like to place them in locally on your computer. Find a folder you can easily locate and click Save.

Then click 'Open' to open the repository folder in VS Code. You will see some files and folders. 

Open the Readme.md file to read the instructions for this particular repository. Then proceed to step 3 below.

Option 2. Download a zip file and extract the starter files

In your web browser visit: https://github.com/JB-Connect/INFS605-Assignment2-Starter-Files

On Github, click on the green '<> Code' button and choose the option 'Download ZIP'. Save it in a folder you can easily locate and click Save.

In File Explorer (Windows) or Finder (Mac) extract all the contents of the zip file. 

Option 3. Clone straight into your Ubuntu server or on your Virtual Machine running on VirtualBox.

Type, 'git clone https://github.com/JB-Connect/INFS605-Assignment2-Starter-Files.git'

You may be prompted to enter your GitHub username and password. You may need to request access rights depending on your server setup. 

Then type, cd INFS605-Assignment2-Starter-Files to enter the repository.

### 3. Building and running the System

First, run Docker Desktop if you are deploying locally. You need Docker Desktop running on Windows (and MacOS) for Docker commands like docker-compose to work.

Next, in Terminal:

type, docker-compose up -d --build

Then go make a cup of tea or do some light cardio while it builds, installs and runs. 

- API: http://localhost:5001
- Frontend: http://localhost:3000

- open http://localhost:5001/students [to see what the contents of a json query of the database contain]

### 4. Error on build?

If you get the error "unable to get image 'postgres:15': error during connect: Get "http:..." or "unable to get image 'vm-version-admin-frontend': error during connect: Get "http...", try:

docker-compose up -d --build

or try, docker-compose up -d
[without the --build]

You may also need to update your Docker Desktop or Docker engine on your server (on the Virtual Machine) or to the latest version. [on Ubuntu - sudo apt install docker-ce --only-upgrade]

### 5. Error - env: 'bash\r': No such file or directory

The error message "env: 'bash\r': No such file or directory" indicates that a script is attempting to execute a shebang line that includes Windows-style carriage return characters (\r) in the interpreter path, making it an invalid path in a Unix-like environment (such as Linux or macOS). (or vice versa)

Many modern text editors (like VS Code, Sublime Text, Notepad++) allow you to change the line ending format of a file from CRLF to LF. So this can be tedious, however, update the wait-for-it.sh file in the student-profile folder to LF and then save it.

### 6. Running the System on VirtualBox

You could use the same Ubuntu server you have running on the virtual machine you used in the INFS605 tutorial classes. Create a new "assignment2" folder extract the contents of the zip file or cloned repository from GitHub into your new assignment2 folder.

You will need to open 3 new ports (if they are not open already):

Host Port: 3000 + Guest Port: 3000
Host Port: 5001 + Guest Port: 5001
Host Port: 5432 + Guest Port: 5432

If you are using VirtualBox to host your application on Ubuntu you will need to set up Port Forwarding Rules to allow your services to run on Localhost ports 5001, 5432 and 3000. 
1. In Machine/Settings (and in Expert mode, or click Advanced in the Network settings) under Network set a new protocol with TCP Host Port 5001 and Guest Port 5001. That will map port 5001 in the student-services container to port 5001 of your browser for the API. 
2. Then set another new protocol with TCP Host Port 3000 and Guest Port 3000. That will map port 3000 in the frontend container to port 3000 of your browser.
3. Then set another new protocol with TCP Host Port 5432 and Guest Port 5432. That will map port 5432 in the postgres container for the database to port 5432 of your browser.  

For the React frontend to work you will also need to install the Node Package Manager (npm) on your Ubuntu server running on the virtual machine:

sudo apt install nodejs npm -y

[enter your password]
[the password is "microservices" if you are using the VM from the INFS605 tutorial class]

### 7. API Endpoints

#### Student Profile Service (http://localhost:5001)
- `GET /students` – list all students
- `GET /students/:id` – get a student
- `POST /students` – `{ name, email }`
- `PUT /students/:id` – update `{ name?, email? }`
- `DELETE /students/:id`
- `POST /students/:id/attendance` – `{ date: 'YYYY-MM-DD', status: 'Present|Absent|Late|Excused' }`

## Environment Variables

- DB URL is passed via `DATABASE_URL` inside docker-compose.
- Postgres is seeded from `student-profile/init.sql` on first startup (volume-less).

[Copy `.env.example` to `.env` if needed.]

## Screenshots

Include screenshots or screen recordings as you compose, run and test the system. Especially capture any errors you encounter and note how you resolved them.

### 8. Troubleshooting containers

If you have trouble stopping containers with docker-compose-down then you might have some permission errors if you are running as admin from root and the container network endpoints are running with local users.
Docker refusing to kill a container. It usually happens because:
- The Docker daemon is running as root, but your user doesn’t have the right privileges.
- The container is in a bad / zombie state (hung process inside).
- You’re in a VM (Ubuntu on VirtualBox) and Docker sometimes glitches with cgroups. 

1. Kill via container process ID (PID)
Find each container service IDs [each should have a 4 digit service number] using:
ps aux | grep containerd-shim

Then kill them manually:
sudo kill -9 <pid>

Then docker-compose down

2. Use sudo (superuser do)
sudo docker stop assignment_frontend_1
sudo docker rm assignment_frontend_1

3. Force kill
sudo docker rm -f assignment_frontend_1

or

docker rm -f $(docker ps -aq)

4. Restart the entire Docker service
sudo systemctl restart docker

5. Delete the entire virtual machine and reboot
After cleanup 
docker ps -a   # the services running should be empty

docker-compose build --no-cache
docker-compose up -d

## Fixing Docker "Permission Denied" Errors
When you first use Docker inside your Ubuntu VM, you may see errors like:
"permission denied while trying to connect to the Docker daemon socket" 

This happens because Docker runs as root, and your user doesn’t yet have permission to manage containers.

Fix (do this once per VM)

Run the following commands in your Ubuntu terminal:
sudo groupadd docker
sudo usermod -aG docker $USER 
[On VirtualBox Ubuntu "sudo usermod -aG docker infs605"]

Then log out and log back in (or restart your VM).

# Verify
After logging back in, check your groups:
groups $USER
[On VirtualBox Ubuntu "groups infs605"]

You should see "docker" listed.

Then test Docker without sudo:
docker ps

If it works, you should be good to go.
Important: Typically you must log out and back in (or restart Ubuntu) for the group change to take effect.

## Fixing ERROR: for student-profile 'ContainerConfig'
The KeyError: 'ContainerConfig' is a Docker Compose version mismatch issue.
Docker images (especially ones built with newer Docker versions) don’t expose ContainerConfig in their metadata by default anymore.

To install a v2 of docker-compose on Ubuntu:
sudo apt-get remove docker-compose -y
sudo apt-get update
sudo apt-get install docker-compose-plugin -y

[enter your password]
[the password is "microservices" if you are using the VM from the INFS605 tutorial class]

Then test:
docker compose version

[*** Note: With the updated version we no longer use the dash with docker - so "docker compose" and not "docker-compose"]

Then:
docker compose build --no-cache
docker compose up -d
