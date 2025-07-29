# 📄 AI-powered-Resume-Screener

An AI-powered Streamlit web application that ranks PDF resumes based on their relevance to a given job description or predefined job category.

## 🚀 Features

- ✅ Ranks multiple resumes using **semantic similarity** (Sentence Transformers)
- 📋 Choose from **predefined job categories** or enter a **custom Job Description (JD)**
- 🔍 Extracts and compares skills from resumes and JD
- 📈 Assigns a **similarity score** and provides **feedback suggestions**
- 📥 Allows users to **download top 3 matching resumes**

## 🛠️ Tech Stack

- Python 
- Streamlit 
- [Sentence-Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`)
- PyPDF2 (for extracting resume text)
- Pandas (for results display and sorting)

## 🚀 How It Works

1. **Select a Job Category** or **enter your own JD**
2. Upload PDF resumes
3. App extracts text and compares using **SentenceTransformer (all-MiniLM-L6-v2)**
4. Displays:
   - Match score (%)
   - Feedback on alignment
   - Option to download top 3 resumes

📁 Custom Job Description
You can either:

Choose a predefined category (with default qualifications + responsibilities)

OR input your own custom JD in plain text


## 🧠 Note on Accuracy

This is a **screening** tool — not a final selection system.  
- **Predefined JDs** are basic and may not reflect real job complexity.  
- **Custom JDs** are preferred for meaningful matching.  
- Skills are extracted via pattern matching and semantic comparison — results may vary based on resume formatting and content.



## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/srinija0208/AI-powered-Resume-Screener
cd AI-powered-Resume-Screener
```


2. **Install dependencies**
```
pip install -r requirements.txt
```

4. **Run the app**
```
streamlit run app.py
```

