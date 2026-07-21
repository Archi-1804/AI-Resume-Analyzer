# Deployment Plan for AI Resume Analyzer

## 1. Recommended deployment target
Use a cloud platform that supports Python web apps and a managed MySQL database. A good fit is:
- App hosting: Render or Railway
- Database: managed MySQL service such as Railway MySQL or a cloud MySQL instance
- Optional containerization: Docker for repeatable deployments

## 2. Pre-deployment preparation
### Code changes needed
- Replace hard-coded database credentials in the app with environment variables.
- Make the app use a production-safe database connection instead of local-only settings.
- Make file paths robust so the app works when launched from the hosting platform.
- Ensure the app can run with the correct host and port settings for the cloud environment.
- Add a health check route or a simple startup verification step.

### Environment variables
Create a `.env` or platform secret variables with:
- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`
- `MYSQL_PORT`
- `STREAMLIT_SERVER_PORT`
- `STREAMLIT_SERVER_ADDRESS`

## 3. Dependency and runtime setup
- Use Python 3.10 or 3.11 for compatibility.
- Install dependencies from the app requirements file.
- Ensure the spaCy English model is installed during deployment.
- Verify that NLTK resources are downloaded at startup or pre-bundled.

## 4. Database setup
- Provision a MySQL database in the cloud.
- Create the `cv` database and required tables.
- Confirm that the app can connect successfully from the hosting environment.
- Set up backups and basic monitoring for the database.

## 5. Deployment steps
### Option A: Render / Railway deployment
1. Push the project to GitHub.
2. Create a new web service for the Streamlit app.
3. Point it to the app entry file:
   - `App/App.py`
4. Set the build command to install dependencies and download NLP assets.
5. Set the start command to run the Streamlit app on the assigned port.
6. Attach the managed MySQL database and provide connection secrets.
7. Deploy and verify the app loads successfully.

### Suggested start command
```bash
streamlit run App/App.py --server.port $PORT --server.address 0.0.0.0
```

## 6. Verification checklist
After deployment, confirm:
- The homepage loads without errors.
- Resume upload works.
- Resume parsing and recommendations generate results.
- User data and feedback entries are written to the database.
- Uploaded resumes are stored correctly.
- Admin views and export features function properly.

## 7. Production hardening
- Use secrets management instead of storing credentials in code.
- Add logging and error handling for failed database writes.
- Consider object storage for uploaded resumes if the app grows in usage.
- Set up basic uptime monitoring and alerts.
- Keep dependency versions pinned for stable deployments.

## 8. Suggested rollout order
1. Deploy to a staging environment first.
2. Test with sample resumes and database writes.
3. Move to production after successful validation.
4. Monitor logs and user feedback after launch.

## 9. Final recommendation
For this project, the most practical path is to deploy the Streamlit app to Render or Railway, connect it to a managed MySQL service, and harden the app for environment-based configuration before the first production release.
