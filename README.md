# OncoKids Report Pipeline

<div align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python 3.11">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/version-1.0.0-orange.svg" alt="Version 1.0.0">
</div>

## 📋 Overview

This project provides a comprehensive pipeline for processing and analyzing OncoKids pathology reports. The pipeline extracts and standardizes genetic data from PDF reports, including DNA variants, RNA fusions, and CMA (Chromosomal Microarray) findings.

## 🧬 Features

- **PDF Processing**
  - Split large batch PDFs into individual OncoKids reports
  - Extract tables from PDF files using Camelot
  - Detect and separate reports by specimen ID

- **Data Extraction**
  - Extract DNA variant data (genes, mutations, frequencies)
  - Extract RNA fusion data
  - Extract CMA/CNV results

- **Data Integration**
  - Standardize column names and data formats
  - Merge data from multiple reports
  - Create integrated tables for DNA, RNA, and CMA findings

## 🏗️ Architecture

The project is organized with a modular structure:

```
project_root/
│
├── notebooks/          # Jupyter notebooks for each workflow step
│   ├── Split_OncoKids_by_keyword_page_detect.ipynb
│   ├── Extract_all_tables_camelot.ipynb
│   └── Integrated_DNA_RNA_CMA_Analysis.ipynb
│
├── src/                # Python modules with reusable functions
│   ├── pdf_utils.py    # PDF manipulation utilities
│   ├── file_utils.py   # File system operations
│   ├── table_utils.py  # Table extraction utilities
│   └── data_integration.py  # Data standardization and merging
│
├── data/               # Data directory (gitignored)
│   └── CoPath_All_pdfs/
│       └── OncoKids_split/
│
├── table/              # Extracted and processed tables (gitignored)
│   └── extracted_tables/
│       └── CoPath_OncoKids_All/
│
├── README.md           # Project documentation
├── .gitignore          # Gitignore file
└── requirements.txt    # Project dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Java Runtime Environment (required for Camelot)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/oncokids-report-pipeline.git
   cd oncokids-report-pipeline
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

The pipeline consists of three main steps:

1. **Split large PDF files into individual OncoKids reports**:
   ```bash
   python -m notebooks.Split_OncoKids_by_keyword_page_detect
   ```

2. **Extract tables from split PDFs**:
   ```bash
   python -m notebooks.Extract_all_tables_camelot
   ```

3. **Integrate and analyze data**:
   ```bash
   python -m notebooks.Integrated_DNA_RNA_CMA_Analysis
   ```

Alternatively, open and run the notebooks in a Jupyter environment:
```bash
jupyter notebook
```

## 📊 Data Processing Flow

The pipeline follows this workflow:

1. **PDF Splitting**: Identifies OncoKids reports in large PDFs using regular expressions and splits them into individual files named by specimen ID.

2. **Table Extraction**: Processes individual PDFs to extract tables containing genetic findings.

3. **Data Integration**: Standardizes and merges data from different reports:
   - DNA Variants: Standardizes gene names, mutations, and frequencies
   - RNA Fusions: Identifies fusion partners and classifies them
   - CMA Results: Standardizes copy number variants and genomic positions

## 🧪 Testing

To run tests:
```bash
python -m unittest discover tests
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Camelot-py for table extraction from PDFs
- PyPDF2 for PDF manipulation
- Pandas for data processing

## 👥 Contributors

- Your Name - Creator & Maintainer

## 📞 Contact

For questions or feedback, please open an issue in the GitHub repository.