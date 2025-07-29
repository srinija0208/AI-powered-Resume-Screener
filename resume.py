import streamlit as st
import pandas as pd
import numpy as np
import re
import io
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util

job_categories = {
    "Data Scientist": {
        "Job Summary": "Develop and deploy data-driven solutions and predictive models to extract actionable insights from complex datasets.",
        "Key Responsibilities": "Data collection/cleaning, model building (ML, stats), analysis, and communicating findings.",
        "Qualifications": "Python, SQL, Machine Learning, statistics, data visualization tools (Tableau/Power BI)."
    },
    "Machine Learning Engineer": {
        "Job Summary": "Design, build, and deploy scalable machine learning systems and pipelines into production environments.",
        "Key Responsibilities": "ML model operationalization, MLOps, system integration, performance optimization.",
        "Qualifications": "Python, ML frameworks (TF/PyTorch), software engineering skills, cloud experience."
    },
    "Data Analyst": {
        "Job Summary": "Analyze large datasets to identify trends, create reports, and provide actionable business insights.",
        "Key Responsibilities": "Data gathering, descriptive analysis, dashboard creation, stakeholder reporting.",
        "Qualifications": "SQL, Excel, BI tools (Tableau/Power BI)."
    },
    "Business Intelligence Analyst": {
        "Job Summary": "Transform business requirements into insightful reports and dashboards using BI tools and data models.",
        "Key Responsibilities": "Requirements gathering, dashboard development, SQL querying, data analysis.",
        "Qualifications": "SQL, BI tools (Tableau/Power BI), data warehousing concepts."
    },
    "AI Research Engineer": {
        "Job Summary": "Conduct cutting-edge AI/ML research and translate novel algorithms into prototypes.",
        "Key Responsibilities": "Algorithm development, model experimentation, academic contributions, prototype building.",
        "Qualifications": "Master's/Ph.D., Python, deep learning frameworks (TF/PyTorch), strong math."
    },
    "MLOps Engineer": {
        "Job Summary": "Build and maintain CI/CD pipelines and infrastructure for efficient ML model deployment.",
        "Key Responsibilities": "Automation, cloud infrastructure management, containerization (Docker/Kubernetes), monitoring.",
        "Qualifications": "Cloud experience, CI/CD tools, scripting (Python/Bash), IaC."
    },
    "DevOps Engineer": {
        "Job Summary": "Ensure smooth software development and deployment using automated tools and cloud infrastructure.",
        "Key Responsibilities": "CI/CD implementation, configuration management, system monitoring, infrastructure scaling.",
        "Qualifications": "Linux, scripting, CI/CD, Docker/Kubernetes, AWS/Azure."
    },
    "Software Engineer": {
        "Job Summary": "Design, develop, and maintain software applications and systems.",
        "Key Responsibilities": "Write and test code, debug, integrate systems, collaborate with teams.",
        "Qualifications": "Programming in Java/Python/C++, problem-solving, Git, databases."
    },
    "Full Stack Developer": {
        "Job Summary": "Develop and maintain both front-end and back-end components of web/mobile applications.",
        "Key Responsibilities": "UI/UX development, API creation, database management, testing.",
        "Qualifications": "HTML/CSS/JS (frameworks), back-end language (Python/Node/Java), SQL/NoSQL, Git."
    },
    "Backend Developer": {
        "Job Summary": "Develop and optimize server-side logic, APIs, and database interactions.",
        "Key Responsibilities": "Build RESTful APIs, manage databases, integrate with front-end.",
        "Qualifications": "Node.js/Python/Java, SQL/NoSQL, server-side frameworks."
    },
    "Frontend Developer": {
        "Job Summary": "Create user-facing interfaces and improve user experience using modern web technologies.",
        "Key Responsibilities": "Design UI components, ensure responsiveness, connect APIs.",
        "Qualifications": "HTML, CSS, JavaScript, React/Angular/Vue."
    },
    "Cloud Engineer": {
        "Job Summary": "Design, implement, and manage secure and scalable cloud infrastructure and services.",
        "Key Responsibilities": "Cloud solution deployment (AWS/Azure/GCP), resource management, security, automation.",
        "Qualifications": "Cloud certifications, IaC (Terraform), scripting, networking."
    },
    "Cybersecurity Analyst": {
        "Job Summary": "Protect organizational systems and data from cyber threats, monitoring security and responding to incidents.",
        "Key Responsibilities": "Security monitoring, incident response, vulnerability assessment, policy enforcement.",
        "Qualifications": "Networking/OS knowledge, security tools experience, relevant certifications (e.g., CompTIA Security+)."
    },
    "Site Reliability Engineer (SRE)": {
        "Job Summary": "Ensure reliability, availability, and performance of production systems.",
        "Key Responsibilities": "Monitor systems, incident management, capacity planning, automation.",
        "Qualifications": "Linux, monitoring tools, programming, cloud knowledge."
    },
    "Data Engineer": {
        "Job Summary": "Design and maintain data pipelines and architectures for robust data flow and processing.",
        "Key Responsibilities": "ETL processes, data warehousing, pipeline optimization, data cleaning.",
        "Qualifications": "SQL, Python, Spark, Hadoop, cloud data platforms."
    },
    "Product Manager (Technical)": {
        "Job Summary": "Define and drive the roadmap for technical products, bridging the gap between engineering and business.",
        "Key Responsibilities": "Product strategy, requirements definition, stakeholder communication, roadmap prioritization.",
        "Qualifications": "Technical background (CS/Engg), understanding of DS/ML/AI, Agile experience, strong communication."
    },
    "QA Engineer / Automation Tester": {
        "Job Summary": "Ensure the quality and reliability of software through automated and manual testing.",
        "Key Responsibilities": "Write test cases, create automation scripts, report bugs, regression testing.",
        "Qualifications": "Selenium/PyTest, programming basics, CI/CD."
    },
    "Blockchain Developer": {
        "Job Summary": "Develop decentralized applications and blockchain-based systems.",
        "Key Responsibilities": "Smart contract development, dApp integration, blockchain architecture design.",
        "Qualifications": "Solidity, Ethereum, cryptography basics, Web3."
    },
    "Mobile App Developer": {
        "Job Summary": "Design and build mobile applications for Android and iOS platforms.",
        "Key Responsibilities": "App UI/UX, API integration, performance optimization.",
        "Qualifications": "Flutter/React Native/Swift/Kotlin, mobile SDKs."
    },
    "NLP Engineer": {
        "Job Summary": "Build NLP systems for text classification, summarization, sentiment analysis, etc.",
        "Key Responsibilities": "Text preprocessing, model training, embedding techniques, pipeline building.",
        "Qualifications": "NLP libraries (spaCy, NLTK, HuggingFace), ML, Python."
    },
    "Computer Vision Engineer": {
        "Job Summary": "Develop systems that interpret and process visual data using deep learning and image processing.",
        "Key Responsibilities": "Object detection, image classification, real-time processing.",
        "Qualifications": "OpenCV, deep learning (CNNs), TF/PyTorch, Python."
    },
    "Systems Engineer": {
        "Job Summary": "Deploy, maintain, and troubleshoot IT systems and infrastructure.",
        "Key Responsibilities": "System monitoring, upgrades, hardware/software maintenance.",
        "Qualifications": "Operating systems, hardware, IT certifications."
    },
    "IT Support Specialist": {
        "Job Summary": "Provide technical support and troubleshooting to ensure seamless IT operations.",
        "Key Responsibilities": "User support, system maintenance, ticket resolution.",
        "Qualifications": "Basic networking, Windows/Linux, communication skills."
    },
    "Technical Writer": {
        "Job Summary": "Create clear and concise technical documentation for software, systems, and user guides.",
        "Key Responsibilities": "Write manuals, guides, and online help systems.",
        "Qualifications": "Writing skills, tech background, tools like Markdown/LaTeX."
    },
    "UI/UX Designer": {
        "Job Summary": "Design intuitive and visually appealing user interfaces and experiences.",
        "Key Responsibilities": "User research, prototyping, wireframing, UI design.",
        "Qualifications": "Figma/Adobe XD, design thinking, usability principles."
    }
}

# common_skills = ["python", "sql", "excel", "machine learning", "deep learning", "data analysis", 
#                  "pandas", "numpy", "scikit-learn", "communication", "visualization", "UI design",
#                  "power bi", "tableau", "nlp", "tensorflow", "keras", "r", "java", "OpenCV","CI/CD",
#                  "Deep Learning", "cloud experience","tableu","docker","kubernetes","git","databases",
#                  "Networking", "Linux", "Agile", "Selenium", "PyTest", "JavaScript", "HTML","Spark","hadoop",
#                  ]


## load model 

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

st.title("📄 AI Powered Resume Screener")

# Step 1: Select category
selected_category = st.selectbox("Choose a Job Category", ["-- Select --"] + list(job_categories.keys()))
use_custom_jd = st.checkbox("Use Custom Job Description")

# JD Construction
job_description = ""
if use_custom_jd:
    job_description = st.text_area("Enter Custom Job Description")
elif selected_category != "-- Select --":
    jd_dict = job_categories.get(selected_category)
    if jd_dict:
        job_description = f"""Job Title: {selected_category}
Summary: {jd_dict.get('Job Summary', '')}
Responsibilities: {jd_dict.get('Key Responsibilities', '')}
Qualifications Required: {jd_dict.get('Qualifications', '')}"""



# Extract text from PDFs
def extract_text_from_pdfs(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text.strip()

# Feedback Generator (simplified — removed missing skills feedback)
def generate_feedback(score):
    if score >= 80:
        return "Excellent match! Your resume is highly aligned with the job."
    elif 60 <= score < 80:
        return "Good match. You meet most requirements, but there's room to improve."
    elif 40 <= score < 60:
        return "Moderate match. Consider tailoring your resume more closely to the job description."
    else:
        return "Low match. Significant gaps detected — revise your resume to better reflect relevant skills and experiences."

# Upload resumes
uploaded_files = st.file_uploader("Upload Resumes (PDFs)", type=["pdf"], accept_multiple_files=True)

# Main Logic
if job_description.strip():
    if job_description.strip() and uploaded_files:
        st.subheader("Ranking Resumes")

        results = []
        for file in uploaded_files:
            resume_text = extract_text_from_pdfs(file)
            resume_embedding = model.encode(resume_text, convert_to_tensor=True)
            job_embedding = model.encode(job_description, convert_to_tensor=True)

            similarity = util.cos_sim(job_embedding, resume_embedding)[0].item()
            similarity_score = round(similarity * 100, 2)

            results.append({
                'Resume': file.name,
                'Similarity Score': similarity_score,
                'Suggestions': generate_feedback(similarity_score),
                'FileObj': file
            })

        results_df = pd.DataFrame(results).sort_values(by='Similarity Score', ascending=False)
        st.dataframe(results_df.drop(columns=['FileObj']).reset_index(drop=True))

        top_resume = results_df.iloc[0]
        st.success(f"✅ Best Match: {top_resume['Resume']} ({top_resume['Similarity Score']}%)")

        # Download Top 3
        st.subheader("📥 Download Top 3 Matching Resumes")
        top3_df = results_df.head(3).reset_index(drop=True)

        for idx, row in top3_df.iterrows():
            file_bytes = row['FileObj'].read()
            st.download_button(
                label=f"Download {row['Resume']} ({row['Similarity Score']}%)",
                data=file_bytes,
                file_name=row['Resume'],
                mime='application/pdf',
                key=f"download_button_{idx}"
            )

elif uploaded_files:
    st.warning("Please provide either a custom JD or select a job category.")