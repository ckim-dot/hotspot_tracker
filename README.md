## 💬 Purpose
The purpose of this app is to streamline the hotspot management process.

## ⚙️ Major Functions
- Displays a list of hotspots and whether they're disabled/enabled
- Given an excel file with a list of overdue hotspots, this app automatically checks for which ones need their status changed
- Users can add hotspots manually

## 📦 Dependencies

### Dependencies
@heroicons/react@2.2.0  
framer-motion@12.7.4  
next@15.3.1  
react@19.1.0  
react-dom@19.1.0  
tailwindcss@4.1.4  

### Dev Dependencies
blinker==1.9.0
click==8.1.8
colorama==0.4.6
et_xmlfile==2.0.0
Flask==3.1.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
numpy==2.2.5
openpyxl==3.1.5
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
tzdata==2025.2
Werkzeug==3.1.3
xlrd==2.0.1

## 🛠️ Build/Deploy Instructions
### 1. Prerequisites
Flask version **3.1** or higher

It is recommended to make a virtual environment to manage these dependencies

### 2. Initiate a database
```bash
python3 init_db.py
```
this will generate your database.db file and provide dummy data

### 3. Start/Run the project locally
```bash
flask run
```
### 3. Deployment
This is deployed with AWS on an EC2 Instance. It is live here: http://3.17.179.24/
