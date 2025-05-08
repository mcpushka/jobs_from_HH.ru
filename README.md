# Job Requirements Dashboard

Automated collection, processing, and visualization of requirements (skills, experience, salary ranges) from 1,000+ job postings from hhru in an interactive dashboard.

In this project, I experimented and wrote all the necessary things on python code using the Streamlit framework.

---

## Contents

- [Quick Start](#-quick-start)   
- [File Descriptions](#-file-descriptions)  
- [Tech Stack](#-tech-stack)  

---

## Quick Start
1. **Download Data**
   https://www.kaggle.com/datasets/vyacheslavpanteleev1/hhru-it-vacancies-from-20211025-to-20211202
2. **Clone the repo**  
   ```bash
   git clone <repo_url>
   cd project
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
4. **Preprocess data**
   ```bash
   python src/preprocess.py
5. **Run the dashboard**
   ```bash
   streamlit run src/app.py
   http://localhost:8501

---
## File Descriptions
1. **clean_jobs.csv (created during data processing)**
- Cleaned and normalized dataset produced by preprocess.py.
2. **preprocess.py**
- Loads jobs.csv
- Cleans column names
- Extracts & normalizes skill lists
- Parses experience & salary ranges
- Saves clean_jobs.csv
3. **metrics.py**
- Library of functions for data analysis: load_clean_data(), top_skills(n), experience_distribution(), salary_distribution()
4. **app.py**
- Loads data & computes metrics via metrics.py
- Translates skills to English (using deep_translator)
- Renders three interactive charts with Plotly Express:
---
## Tech Stack
- Language: Python 3.8+
- Scraping: requests, BeautifulSoup
- Data Processing: pandas, re, deep_translator
- Visualization: plotly-express, altair
- Web App: Streamlit
  
