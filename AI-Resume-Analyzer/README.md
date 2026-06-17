<img width="950" height="450" alt="WhatsApp Image 2026-06-17 at 1 36 13 AM" src="https://github.com/user-attachments/assets/18d73664-80eb-48e1-8609-5f6dac27c91f" />

# ?? AI Resume Analyzer
An AI-powered resume analysis platform that leverages Natural Language Processing (NLP) and Machine Learning to evaluate resumes, identify key skills, predict suitable career domains, and provide personalized recommendations for professional growth.

---

## ?? Overview

<img width="800" height="600" alt="WhatsApp Image 2026-06-17 at 12 44 24 AM" src="https://github.com/user-attachments/assets/21ac15a1-5ff4-4e55-a0d7-56c62d5f32e7" />

AI Resume Analyzer is designed to help job seekers understand and improve their resumes through intelligent data extraction and analysis. The application automatically parses uploaded resumes, identifies relevant skills and keywords, evaluates candidate profiles, and generates actionable insights through an interactive dashboard.

The platform streamlines resume evaluation and assists users in making informed career decisions by highlighting strengths, uncovering skill gaps, and recommending learning opportunities.

---

## ? Features

### ????? Candidate Features

- ?? Upload resumes in PDF format
- ?? Automatic resume parsing and information extraction
- ?? Skill identification and classification
- ?? Resume score generation
- ?? Career domain prediction
- ?? Personalized skill recommendations
- ?? Course and learning recommendations
- ?? Resume improvement suggestions
- ?? Experience-level assessment
- ?? Interactive analysis dashboard

### ?? Admin Features

- ?? Candidate data management
- ??? Resume database monitoring
- ? User feedback tracking
- ?? Analytics and reporting
- ?? Data export functionality
- ?? Visualization of user statistics

---

## ??? Technology Stack

### ?? Frontend

- Streamlit
- HTML
- CSS
- JavaScript

### ?? Backend

- Python

### ??? Database

- MySQL

### ?? Libraries & Tools

- Pandas
- Plotly
- NLTK
- spaCy
- PyResParser
- PDFMiner

---

## ?? Workflow

1. ?? User uploads a resume in PDF format.
2. ?? Resume content is extracted and processed.
3. ?? NLP techniques identify important skills and keywords.
4. ?? Career domains are predicted based on resume content.
5. ?? The application generates:Resume Score
6. Skill Recommendations
7. Career Domain Prediction
8. Learning Suggestions
9. Resume Improvement Tips
10. ?? Results are displayed through an interactive dashboard.

---

## ?? Installation

### ?? Clone the Repository

`
git clone https://github.com/your-username/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
`

### ?? Create a Virtual Environment

`
python -m venv venv
`

### ?? Activate the Virtual Environment
**Windows**

`
venv\Scripts\activate
`
**Linux / macOS**

`
source venv/bin/activate
`

### ?? Install Dependencies

`
pip install -r requirements.txt
`

### ?? Download Required NLP Model

`
python -m spacy download en_core_web_sm
`

### ??? Configure MySQL Database
Create a MySQL database and update the database credentials in the project configuration.

`
CREATE DATABASE cv;
`

### ?? Run the Application

`
streamlit run App.py
`

---

## ?? Project Structure

`
AI-Resume-Analyzer
�
+-- App.py
+-- requirements.txt
+-- Courses/
+-- Uploaded_Resumes/
+-- pyresparser/
+-- Assets/
+-- README.md
`

---

## ?? Use Cases

- Resume evaluation and optimization
- Placement preparation for students
- Career guidance and skill assessment
- Candidate profile analysis
- Recruitment support and screening

---

## ?? Future Enhancements

- Advanced recommendation engine
- Enhanced resume scoring algorithms
- Additional career domain support
- Improved analytics dashboard
- Better user experience and performance

---

## ????? Author
Developed as an intelligent Resume Analysis and Career Recommendation Platform using NLP, Machine Learning, Data Analytics, and Data Visualization technologies.

---
? If you found this project helpful, consider giving it a star!
