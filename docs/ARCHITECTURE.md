# TrialMatch AI - Technical Architecture

## System Overview

TrialMatch AI is designed as a modular, scalable platform for clinical trial patient matching with the following core components:

## Architecture Diagram
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
