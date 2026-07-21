import os
import io
import sys
import tempfile
from typing import Optional, List, Dict
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos

# Ensure NLTK stopwords corpora is downloaded
try:
    import nltk
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
except Exception:
    pass


app = FastAPI(
    title="AI Resume Analyzer API",
    description="Interactive REST API for AI Resume Analysis, Resume Scoring, Skill Extraction, and Course Recommendations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response Models
class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
    database_connected: bool = Field(..., example=False)
    version: str = Field(..., example="1.0.0")


class CourseItem(BaseModel):
    title: str
    url: str


class CoursesResponse(BaseModel):
    category: str
    courses: List[CourseItem]


class ResumeAnalysisResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    page_count: int = 1
    predicted_field: str
    candidate_level: str
    resume_score: int
    extracted_skills: List[str]
    recommended_skills: List[str]
    recommended_courses: List[CourseItem]
    recommended_videos: Dict[str, List[str]]


class FeedbackRequest(BaseModel):
    name: str = Field(..., example="John Doe")
    email: str = Field(..., example="john@example.com")
    score: int = Field(..., ge=1, le=5, example=5)
    comments: str = Field(..., example="Great application!")


class FeedbackResponse(BaseModel):
    success: bool
    message: str


# Helper functions
def get_db_connection():
    try:
        import pymysql
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'cv'),
            port=int(os.getenv('MYSQL_PORT', '3306')),
            connect_timeout=3
        )
        return connection
    except Exception:
        return None


@app.get("/api/v1", summary="API Root", tags=["General"])
def read_root():
    return {
        "message": "Welcome to the AI Resume Analyzer API",
        "swagger_docs": "/docs",
        "redoc_docs": "/redoc",
    }



@app.get("/api/v1/health", response_model=HealthResponse, summary="Health Check", tags=["General"])
def health_check():
    conn = get_db_connection()
    db_ok = conn is not None
    if conn:
        conn.close()
    return HealthResponse(status="ok", database_connected=db_ok, version="1.0.0")


@app.get("/api/v1/courses", response_model=CoursesResponse, summary="Get Course Catalog", tags=["Recommendations"])
def get_courses(category: str = "ds"):
    """
    Get recommended courses by field category (`ds`, `web`, `android`, `ios`, `uiux`).
    """
    category_map = {
        "ds": ("Data Science", ds_course),
        "web": ("Web Development", web_course),
        "android": ("Android Development", android_course),
        "ios": ("iOS Development", ios_course),
        "uiux": ("UI/UX Design", uiux_course),
    }
    cat_lower = category.lower()
    if cat_lower not in category_map:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category '{category}'. Valid categories: {list(category_map.keys())}"
        )
    cat_name, course_tuples = category_map[cat_lower]
    courses = [CourseItem(title=c[0], url=c[1]) for c in course_tuples]
    return CoursesResponse(category=cat_name, courses=courses)


@app.post("/api/v1/analyze", response_model=ResumeAnalysisResponse, summary="Analyze Resume PDF", tags=["Resume Analysis"])
async def analyze_resume(file: UploadFile = File(...)):
    """
    Upload a resume PDF file to parse skills, candidate details, score the resume, and retrieve tailored recommendations.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported."
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        from pyresparser import ResumeParser
        from App import pdf_reader

        # Parse text and resume data
        try:
            resume_data = ResumeParser(tmp_path).get_extracted_data()
        except Exception:
            resume_data = {}

        try:
            extracted_text = pdf_reader(tmp_path)
        except Exception:
            extracted_text = ""

        page_count = len(extracted_text.split('\f')) if extracted_text else 1
        page_count = max(page_count, 1)

        name = resume_data.get('name') if resume_data else None
        email = resume_data.get('email') if resume_data else None
        mobile_number = resume_data.get('mobile_number') if resume_data else None
        extracted_skills = resume_data.get('skills', []) if resume_data and resume_data.get('skills') else []

        # Keywords for field matching
        ds_keywords = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit', 'scikit-learn', 'data science', 'pandas', 'numpy']
        web_keywords = ['react', 'django', 'node', 'javascript', 'html', 'css', 'vue', 'angular', 'web development', 'express']
        android_keywords = ['android', 'android studio', 'java', 'kotlin', 'flutter', 'xml']
        ios_keywords = ['ios', 'swift', 'cocoa', 'xcode', 'objective-c']
        uiux_keywords = ['ux', 'user experience', 'ui', 'user interface', 'adobe xd', 'figma', 'wireframe', 'prototype']

        skills_text_lower = ' '.join(extracted_skills).lower() + ' ' + extracted_text.lower()

        reco_field = 'General'
        course_list = []

        if any(k in skills_text_lower for k in ds_keywords):
            reco_field = 'Data Science'
            course_list = ds_course
        elif any(k in skills_text_lower for k in web_keywords):
            reco_field = 'Web Development'
            course_list = web_course
        elif any(k in skills_text_lower for k in android_keywords):
            reco_field = 'Android Development'
            course_list = android_course
        elif any(k in skills_text_lower for k in ios_keywords):
            reco_field = 'iOS Development'
            course_list = ios_course
        elif any(k in skills_text_lower for k in uiux_keywords):
            reco_field = 'UI/UX Design'
            course_list = uiux_course

        # Experience & Candidate Level
        cand_level = 'Fresher'
        if 'experience' in skills_text_lower or 'senior' in skills_text_lower:
            cand_level = 'Experienced'

        # Calculate Score
        score = 0
        if extracted_skills:
            score += min(len(extracted_skills) * 5, 40)
        if 'objective' in skills_text_lower or 'summary' in skills_text_lower:
            score += 20
        if 'education' in skills_text_lower or 'degree' in skills_text_lower:
            score += 20
        if 'project' in skills_text_lower:
            score += 20
        score = min(max(score, 20), 100)

        # Recommended skills
        rec_skills_map = {
            'Data Science': ['Python', 'Pandas', 'NumPy', 'Scikit-Learn', 'TensorFlow', 'PyTorch', 'SQL'],
            'Web Development': ['JavaScript', 'HTML5', 'CSS3', 'React', 'Node.js', 'TypeScript', 'REST API'],
            'Android Development': ['Kotlin', 'Java', 'Android SDK', 'Jetpack Compose', 'Room', 'Retrofit'],
            'iOS Development': ['Swift', 'SwiftUI', 'Xcode', 'CoreData', 'UIKit'],
            'UI/UX Design': ['Figma', 'Adobe XD', 'Wireframing', 'User Research', 'Prototyping'],
        }
        recommended_skills = rec_skills_map.get(reco_field, ['Communication', 'Problem Solving', 'Git', 'Agile'])

        courses = [CourseItem(title=c[0], url=c[1]) for c in course_list[:5]]

        return ResumeAnalysisResponse(
            name=name,
            email=email,
            mobile_number=mobile_number,
            page_count=page_count,
            predicted_field=reco_field,
            candidate_level=cand_level,
            resume_score=score,
            extracted_skills=extracted_skills,
            recommended_skills=recommended_skills,
            recommended_courses=courses,
            recommended_videos={
                "resume_videos": resume_videos,
                "interview_videos": interview_videos
            }
        )

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/api/v1/feedback", response_model=FeedbackResponse, summary="Submit Feedback", tags=["Feedback"])
def submit_feedback(data: FeedbackRequest):
    """
    Submit user feedback and rating.
    """
    conn = get_db_connection()
    if conn:
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor = conn.cursor()
            insertfeed_sql = "insert into user_feedback values (0,%s,%s,%s,%s,%s)"
            cursor.execute(insertfeed_sql, (data.name, data.email, str(data.score), data.comments, timestamp))
            conn.commit()
            conn.close()
            return FeedbackResponse(success=True, message="Feedback submitted successfully.")
        except Exception as e:
            return FeedbackResponse(success=False, message=f"Database insert error: {str(e)}")
    return FeedbackResponse(success=True, message="Feedback received (Database offline).")


# Streamlit Launcher & Reverse Proxy
import subprocess
import time
import httpx
from fastapi import Request, Response
from fastapi.responses import HTMLResponse

STREAMLIT_PROCESS = None

def ensure_streamlit_running():
    global STREAMLIT_PROCESS
    if STREAMLIT_PROCESS is None or STREAMLIT_PROCESS.poll() is not None:
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            os.path.join(BASE_DIR, "App.py"),
            "--server.port", "8501",
            "--server.address", "127.0.0.1",
            "--server.headless", "true"
        ]
        STREAMLIT_PROCESS = subprocess.Popen(cmd, cwd=BASE_DIR)
        time.sleep(3)

@app.on_event("startup")
def startup_event():
    ensure_streamlit_running()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"], include_in_schema=False)
async def proxy_streamlit(request: Request, path: str):
    if path in ["docs", "redoc", "openapi.json"] or path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")
    
    ensure_streamlit_running()

    target_url = f"http://127.0.0.1:8501/{path}"
    if request.query_params:
        target_url += f"?{request.query_params}"

    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            req_content = await request.body()
            resp = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=req_content
            )
            resp_headers = dict(resp.headers)
            resp_headers.pop("transfer-encoding", None)
            resp_headers.pop("content-encoding", None)
            return Response(content=resp.content, status_code=resp.status_code, headers=resp_headers)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Streamlit is loading...</h3><p style='color:gray;'>{str(e)}</p><script>setTimeout(function(){location.reload()}, 3000)</script>", status_code=200)



from fastapi import WebSocket
import websockets
import asyncio

@app.websocket("/{path:path}")
async def websocket_proxy(websocket: WebSocket, path: str):
    await websocket.accept()
    target_ws = f"ws://127.0.0.1:8501/{path}"
    try:
        async with websockets.connect(target_ws) as target_socket:
            async def forward_to_target():
                try:
                    while True:
                        msg = await websocket.receive()
                        if "text" in msg and msg["text"]:
                            await target_socket.send(msg["text"])
                        elif "bytes" in msg and msg["bytes"]:
                            await target_socket.send(msg["bytes"])
                except Exception:
                    pass

            async def forward_to_client():
                try:
                    async for msg in target_socket:
                        if isinstance(msg, str):
                            await websocket.send_text(msg)
                        else:
                            await websocket.send_bytes(msg)
                except Exception:
                    pass

            await asyncio.gather(forward_to_target(), forward_to_client())
    except Exception:
        try:
            await websocket.close()
        except Exception:
            pass


