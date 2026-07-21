# Render Deployment Guide for AI Resume Analyzer

## 1. Project structure note
This app is a Streamlit project located in the `App` folder. The main entry file is:
- `App/App.py`

## 2. Prepare the repository
Before deploying on Render:
1. Commit all changes to GitHub.
2. Ensure the project contains:
   - `App/App.py`
   - `App/requirements.txt`
   - `App/Courses.py`
   - `App/Logo/`
   - `App/nltk_data/` if you want to bundle NLP resources

## 3. Render service configuration
Create a new Web Service on Render.

### Basic settings
- Name: `ai-resume-analyzer`
- Environment: `Python`
- Build Command:
  ```bash
  pip install -r App/requirements.txt
  python -m spacy download en_core_web_sm
  ```
- Start Command:
  ```bash
  streamlit run App/App.py --server.port $PORT --server.address 0.0.0.0
  ```

## 4. Environment variables
Add these as Render environment variables:
- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`
- `MYSQL_PORT=3306`
- `STREAMLIT_SERVER_PORT=10000`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`

## 5. Database setup
Render does not provide MySQL by default, so you should use:
- Render Managed PostgreSQL only if you refactor the app
- Or an external MySQL service such as Railway MySQL, PlanetScale-compatible MySQL, or a cloud MySQL host

Because the current app uses `PyMySQL`, you can connect to any MySQL-compatible service.

## 6. Code changes required before deployment
The app currently uses hard-coded database connection details. Update it to read from environment variables.

### Recommended change pattern
Replace code like this:
```python
connection = pymysql.connect(host='localhost',user='root',password='Dreams@181204',db='cv')
```

With something like:
```python
import os
import pymysql

connection = pymysql.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', ''),
    database=os.getenv('MYSQL_DB', 'cv'),
    port=int(os.getenv('MYSQL_PORT', 3306)),
)
```

## 7. Important deployment note
Render may not be ideal for this app as-is because:
- It depends on MySQL
- It uses NLP libraries and spaCy model downloads
- It may need persistent file storage for uploaded resumes

## 8. Recommended deployment flow
1. Push the project to GitHub.
2. Create a new Render Web Service.
3. Connect the GitHub repository.
4. Set the build and start commands.
5. Add the environment variables.
6. Connect to your MySQL database.
7. Deploy and test.

## 9. Verification checklist
After deployment, verify:
- The app homepage opens.
- Resume upload works.
- Parsing and recommendations are generated.
- Database inserts succeed.
- The admin section loads.

## 10. Best practice
For a smoother deployment, keep the app in a single folder structure and ensure all assets such as the logo and uploaded-resume folder are available at runtime.
