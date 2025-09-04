# 🧬 TrialMatch AI

**AI-Powered Clinical Trial Matching Platform for NSCLC Patients**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app/)

🎯 Problem Statement

Despite clinical trials offering access to cutting-edge treatments, only 2–5% of adult cancer patients participate in them.
Several systemic barriers drive this underutilization:

Manual, time-consuming trial matching workflows

Complex and inconsistent eligibility criteria

Lack of standardized patient-trial pairing tools

Limited awareness among both clinicians and patients

 🔎 _Source:_ [ASCO Educational Book, 2020](https://ascopubs.org/doi/full/10.1200/EDBK_156686)

🔎 _Source:_ [PMC Systematic Review: Enrollment Rates in Cancer Trials](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6410951/)


🌍 Market Opportunity

**Market Size:** The global Clinical Trial Management System (CTMS) market is valued at **USD 2.02 billion in 2024**, projected to reach **USD 6.60 billion by 2034**, with a **CAGR of 12.57%** from 2025 to 2034.

💡 _Source:_ [Precedence Research, 2024 – Clinical Trial Management System Market](https://www.precedenceresearch.com/clinical-trial-management-system-market)


## 💡 Solution

TrialMatch AI automates patient-trial matching using AI + rules, reducing hours of work to seconds.

### 🔑 Key Features

🔍 **Smart Matching Engine**  
🤖 **AI-Powered PDF Processing**  
👥 **Multi-User Collaboration**  
📊 **Analytics & Insights**

## 🚀 Live Demo

**[👉 Try TrialMatch AI](https://your-app-url.streamlit.app/)**

![Dashboard](assets/screenshots/main-dashboard.png)


## 🏗️ Technical Architecture
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  Streamlit Web Interface                                        │
│  ├── Patient-Centric Views                                      │
│  ├── Trial-Centric Views                                        │
│  ├── PDF Upload & Processing                                    │
│  └── Analytics & Reporting                                      │
└─────────────────┬───────────────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Core Business Logic                                            │
│  ├── TrialMatchEngine     (Matching Algorithms)                 │
│  ├── DataLoader          (Data Management)                      │
│  ├── PDFParser           (Document Processing)                  │
│  └── Validation          (Data Integrity)                       │
└─────────────────┬───────────────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────────────┐
│                     DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  Patient Data (CSV)                                            │
│  Trial Data (JSON)                                            │
│  PDF Documents                                                │
└─────────────────────────────────────────────────────────────────┘
⚡ Quick Start
Prerequisites

Python 3.9+
OpenAI API key (for PDF features)

Installation
bash# Clone the repository
git clone https://github.com/your-username/trialmatch-ai-pro.git
cd trialmatch-ai-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
📊 Key Metrics & Results

200 sample patients processed
5 clinical trials in database
Sub-second matching response times
Multi-criteria matching algorithm
PDF document parsing with AI

🛠️ Tech Stack

Frontend: Streamlit
Backend: Python, Pandas
AI/ML: OpenAI GPT-4
Data Processing: PDF parsing, CSV handling
Visualization: Plotly, Matplotlib
Testing: Pytest

📚 Documentation

API Documentation
Architecture Guide
Deployment Guide

⚠️ Important Disclaimer
This software is for demonstration and educational purposes only.

❌ NOT intended for actual clinical decision-making or patient care
❌ NOT FDA approved or validated for clinical use
❌ NOT HIPAA compliant for production healthcare use
❌ Should NOT be used to make actual treatment decisions

Always consult qualified healthcare professionals for patient care decisions.
For production use in healthcare environments, additional validation, compliance measures, and regulatory approvals would be required.
🤝 Contributing
This is primarily a portfolio project, but feedback and suggestions are welcome!

Fork the repository
Create a feature branch
Make your changes
Submit a pull request

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
MIT License Summary

✅ Commercial use
✅ Modification
✅ Distribution
✅ Private use
❌ Liability
❌ Warranty

📧 Contact & Support
Created by: Amal Abdi

📧 Email: amalabdi19@outlook.com
💼 LinkedIn: 
🐙 GitHub: @amikxn
🌐 Portfolio: 


🔗 Quick Links

Live Demo
Documentation
Issues
License


Built with ❤️ for improving clinical trial access and patient outcomes.


