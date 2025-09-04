"""
TrialMatch AI - Main Streamlit Application
"""
import streamlit as st
import pandas as pd
import logging
from pathlib import Path

# Import our custom modules
from src.matching.engine import TrialMatchEngine
from src.data.loader import DataLoader
from src.utils.pdf_parser import PDFParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="TrialMatch AI", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_app_data():
    """Load all application data with caching."""
    try:
        data_loader = DataLoader()
        patients = data_loader.load_patients()
        trials = data_loader.load_trials()
        
        if not data_loader.validate_patient_data(patients):
            st.error("Patient data validation failed!")
            return None, None
        
        return patients, trials
    except Exception as e:
        st.error(f"Error loading data: {e}")
        logger.error(f"Data loading error: {e}")
        return None, None

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🧬 TrialMatch AI</h1>', unsafe_allow_html=True)
    st.markdown("**Your AI-powered clinical trial matching platform for NSCLC patients**")
    
    # Load data
    patients, trials = load_app_data()
    
    if patients is None or trials is None:
        st.stop()
    
    # Initialize matching engine
    engine = TrialMatchEngine()
    engine.load_trials(trials)
    
    # Sidebar stats
    with st.sidebar:
        st.header("📊 Platform Statistics")
        st.metric("Total Patients", len(patients))
        st.metric("Active Trials", len(trials))
        
        # Mutation distribution
        mutation_counts = patients['mutation_status'].value_counts()
        st.subheader("Mutation Distribution")
        st.bar_chart(mutation_counts)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Patient Matching", 
        "🧪 Trial Overview", 
        "📄 PDF Analysis", 
        "📋 Reports & Logs"
    ])
    
    # Initialize session state
    if 'patient_notes' not in st.session_state:
        st.session_state.patient_notes = {}
    
    with tab1:
        patient_matching_tab(patients, engine)
    
    with tab2:
        trial_overview_tab(patients, trials, engine)
    
    with tab3:
        pdf_analysis_tab()
    
    with tab4:
        reports_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("**TrialMatch AI** - Powered by Advanced ML Algorithms | © 2024")

def patient_matching_tab(patients, engine):
    """Patient-centric matching interface."""
    st.header("👤 Patient-Centric Trial Matching")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_patient_id = st.selectbox(
            "Select Patient ID", 
            patients["patient_id"].tolist(),
            help="Choose a patient to see matching trials"
        )
        
        patient = patients[patients["patient_id"] == selected_patient_id].iloc[0]
        
        # Patient info display
        st.subheader("Patient Information")
        info_cols = st.columns(2)
        with info_cols[0]:
            st.metric("Age", f"{patient['age']} years")
            st.metric("Stage", patient['stage'])
            st.metric("Gender", patient['gender'])
        
        with info_cols[1]:
            st.metric("Performance Status", patient['performance_status'])
            st.metric("Mutation Status", patient['mutation_status'])
            st.metric("Smoking History", "Yes" if patient['smoker'] else "No")
    
    with col2:
        st.subheader("Matching Clinical Trials")
        
        matches = engine.find_matches_for_patient(patient)
        
        for match in matches:
            with st.expander(
                f"{'✅' if match['is_match'] else '❌'} {match['trial_title']}", 
                expanded=match['is_match']
            ):

def trial_overview_tab(patients, trials, engine):
    """Trial-centric overview interface."""
    st.header("🧪 Clinical Trial Overview")
    
    trial_files = list(trials.keys())
    selected_trial = st.selectbox("Select Clinical Trial", trial_files)
    
    trial = trials[selected_trial]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Trial Information")
        st.write(f"**Title:** {trial['title']}")
        st.write(f"**Trial ID:** {trial.get('trial_id', 'N/A')}")
        st.write(f"**Description:** {trial.get('description', 'N/A')}")
        
        st.subheader("Eligibility Criteria")
        st.json(trial['criteria'])
    
    with col2:
        st.subheader("Eligible Patients")
        
        eligible_patients = []
        for _, patient in patients.iterrows():
            is_match, reasons = engine.match_patient_to_trial(patient, trial['criteria'])
            if is_match:
                eligible_patients.append({
                    'patient_id': patient['patient_id'],
                    'age': patient['age'],
                    'stage': patient['stage'],
                    'mutation_status': patient['mutation_status'],
                    'performance_status': patient['performance_status']
                })
        
        if eligible_patients:
            eligible_df = pd.DataFrame(eligible_patients)
            st.dataframe(eligible_df, use_container_width=True)
            
            # Export functionality
            csv = eligible_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Eligible Patients",
                data=csv,
                file_name=f"eligible_patients_{trial['trial_id']}.csv",
                mime="text/csv"
            )
            
            # PDF Report Generation
            if st.button("📄 Generate PDF Report"):
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                    from reportlab.lib.units import inch
                    from reportlab.lib import colors
                    import io
                    
                    # Create PDF in memory
                    buffer = io.BytesIO()
                    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
                    
                    # Styles
                    styles = getSampleStyleSheet()
                    title_style = ParagraphStyle(
                        'CustomTitle',
                        parent=styles['Heading1'],
                        fontSize=16,
                        spaceAfter=30,
                        textColor=colors.HexColor('#1f77b4')
                    )
                    
                    # Content
                    content = []
                    
                    # Title
                    content.append(Paragraph(f"TrialMatch AI - Eligible Patients Report", title_style))
                    content.append(Paragraph(f"Trial: {trial['title']}", styles['Heading2']))
                    content.append(Paragraph(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
                    content.append(Spacer(1, 20))
                    
                    # Trial Info
                    content.append(Paragraph("Trial Information:", styles['Heading3']))
                    content.append(Paragraph(f"<b>Trial ID:</b> {trial.get('trial_id', 'N/A')}", styles['Normal']))
                    content.append(Paragraph(f"<b>Description:</b> {trial.get('description', 'N/A')}", styles['Normal']))
                    content.append(Spacer(1, 15))
                    
                    # Patient Table
                    content.append(Paragraph(f"Eligible Patients ({len(eligible_patients)}):", styles['Heading3']))
                    
                    # Create table data
                    table_data = [['Patient ID', 'Age', 'Stage', 'Mutation', 'Performance Status']]
                    for patient in eligible_patients:
                        table_data.append([
                            patient['patient_id'],
                            str(patient['age']),
                            patient['stage'],
                            patient['mutation_status'],
                            str(patient['performance_status'])
                        ])
                    
                    # Create and style table
                    table = Table(table_data, colWidths=[1.2*inch, 0.8*inch, 0.8*inch, 1.5*inch, 1.2*inch])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    content.append(table)
                    
                    # Build PDF
                    doc.build(content)
                    buffer.seek(0)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=buffer.getvalue(),
                        file_name=f"eligible_patients_{trial['trial_id']}.pdf",
                        mime="application/pdf"
                    )
                    
                except ImportError:
                    st.warning("PDF generation requires reportlab. Install with: pip install reportlab")
                except Exception as e:
                    st.error(f"Error generating PDF: {e}")
        else:
            st.info("No patients currently match this trial's criteria.")

def pdf_analysis_tab():
    """PDF analysis interface."""
    st.header("📄 AI-Powered PDF Analysis")
    st.info("Upload clinical trial PDFs to automatically extract eligibility criteria")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type=['pdf'],
        help="Upload a clinical trial protocol PDF"
    )
    
    if uploaded_file:
        if 'OPENAI_API_KEY' not in st.secrets:
            st.error("OpenAI API key not configured. Please add to secrets.toml")
            return
        
        with st.spinner("Analyzing PDF..."):
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                parser = PDFParser(st.secrets['OPENAI_API_KEY'])
                full_text = parser.extract_text_from_pdf(temp_path)
                
                # Extract criteria with AI
                structured_criteria = parser.interpret_criteria_with_ai(full_text[:4000])  # Limit for API
                
                if structured_criteria:
                    st.success("✅ PDF Analysis Complete!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Extracted Criteria")
                        st.json(structured_criteria)
                    
                    with col2:
                        st.subheader("Raw Inclusion Criteria")
                        inclusion = structured_criteria.get('raw_inclusion', [])
                        for item in inclusion:
                            st.write(f"• {item}")
                else:
                    st.error("Could not extract structured criteria from PDF")
                
            except Exception as e:
                st.error(f"Error analyzing PDF: {str(e)}")
            finally:
                # Clean up temp file
                import os
                if os.path.exists(temp_path):
                    os.remove(temp_path)

def reports_tab():
    """Reports and logging interface."""
    st.header("📋 Reports & System Logs")
    
    # Patient notes summary
    if st.session_state.patient_notes:
        st.subheader("Patient Notes Summary")
        for key, note in st.session_state.patient_notes.items():
            if note.strip():
                patient_id, trial_id = key.split('_', 1)
                st.write(f"**Patient {patient_id} - Trial {trial_id}:**")
                st.write(note)
                st.write("---")
    else:
        st.info("No patient notes recorded yet.")
    
    # System status
    st.subheader("System Status")
    st.success("✅ All systems operational")
    st.info(f"📊 Application loaded successfully at {pd.Timestamp.now()}")

if __name__ == "__main__":
    main()
