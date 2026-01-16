# UIDAI Hackathon - Trend & Anomaly Detection Analysis

![Python](https://img.shields.io/badge/Python-3.14-blue.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📊 Project Overview

Advanced data analysis project for the UIDAI Hackathon that analyzes over **3 million Aadhaar records** to identify trends and detect anomalies in enrolment and demographic update patterns across 53 Indian states.

### 🎯 Key Findings

- **3,077,729 records** analyzed from 53 states
- **4 statistical outliers** detected using IQR method
- **CRITICAL**: West Bengal (57x ratio) and Odisha (50x ratio) require immediate investigation
- **92.5% of states** show normal, healthy patterns

## 🖼️ Visualizations

All visualizations are generated at **300 DPI** publication quality and saved in the `output_visualizations/` folder.

### Basic Analysis (2 Visualizations)
1. **Trend Analysis** - Age group enrolment distribution
2. **Anomaly Detection** - Top 10 states with highest update-to-enrolment ratios

### Advanced Analysis (3 Visualizations)
3. **Statistical Outlier Detection** - Box plot with IQR method
4. **Risk Heatmap** - Top 20 states risk intensity map
5. **Volume vs. Risk** - Dual-axis combo chart showing correlation

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.14+
pip (Python package manager)
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/uidai-hackathon-analysis.git
cd uidai-hackathon-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Analysis

**Option 1: Run both analyses**
```bash
python trend_anomaly_analysis.py
python advanced_anomaly_detection.py
```

**Option 2: One-click execution (Windows)**
```bash
run_analysis.bat
```

All visualizations will be saved in the `output_visualizations/` folder.

## 📁 Project Structure

```
uidai-hackathon-analysis/
├── output_visualizations/          # All generated visualizations (300 DPI)
│   ├── trend_analysis.png
│   ├── anomaly_detection.png
│   ├── advanced_boxplot_outliers.png
│   ├── advanced_risk_heatmap.png
│   └── advanced_combo_chart.png
│
├── api_data_aadhar_enrolment/      # Enrolment data (3 CSV files)
├── api_data_aadhar_demographic/    # Demographic update data (5 CSV files)
│
├── docs/                           # Documentation & Presentation Materials
│   ├── README_DOCS.txt             # Guide to all documentation
│   ├── QUICK_REFERENCE.txt         # Key facts and numbers
│   ├── VISUALIZATION_GUIDE.txt     # Guide to all visualizations
│   ├── ANALYSIS_REPORT.txt         # Complete detailed report
│   ├── PRESENTATION_SUMMARY.txt    # Presentation guide
│   ├── FINAL_PROJECT_SUMMARY.txt   # Project summary
│   ├── PROJECT_COMPLETE.txt        # Success checklist
│   ├── GIT_SETUP_GUIDE.txt         # GitHub upload guide
│   ├── GITHUB_QUICK_START.txt      # Quick GitHub guide
│   └── ADVANCED_ANALYSIS_GUIDE.txt # Advanced methods guide
│
├── trend_anomaly_analysis.py       # Basic analysis script
├── advanced_anomaly_detection.py   # Advanced analysis script
├── run_analysis.bat                # One-click execution (Windows)
├── git_upload.bat                  # Git upload helper (Windows)
│
├── README.md                       # This file (GitHub homepage)
├── requirements.txt                # Python dependencies
└── .gitignore                      # Git ignore rules
```

## 📈 Analysis Methodology

### Data Processing
- **Dynamic file loading** - Automatically discovers and loads CSV files
- **Data cleaning** - Handles missing values and date formatting
- **State-level aggregation** - Groups data by state for analysis

### Statistical Methods
- **IQR Method** - Identifies statistical outliers (threshold: 26.21)
- **Correlation Analysis** - Volume vs. Risk correlation: -0.372
- **Normalization** - MinMax scaling for heatmap visualization

### Visualization Techniques
- Box plots for outlier detection
- Heatmaps for multi-dimensional risk assessment
- Dual-axis charts for correlation analysis
- Professional styling with Seaborn

## 🔍 Key Insights

### Critical Anomalies
| Rank | State | Ratio | Status |
|------|-------|-------|--------|
| 1 | WESTBENGAL | 57.0 | 🚨 CRITICAL |
| 2 | ODISHA | 50.0 | 🚨 CRITICAL |
| 3 | Daman & Diu | 30.7 | ⚠️ HIGH |
| 4 | Chandigarh | 30.6 | ⚠️ HIGH |

### Statistical Summary
- **Mean Ratio**: 12.77
- **Median Ratio**: 9.40
- **Outlier Threshold**: 26.21 (IQR method)
- **Outliers Detected**: 4 states (7.5%)
- **Normal States**: 49 states (92.5%)

### Correlation Insight
- **Volume vs. Risk**: -0.372 (negative correlation)
- **Interpretation**: Higher volume states tend to have lower risk ratios
- **Implication**: Small states show disproportionately high update activity

## 💡 Recommendations

### Immediate Actions
1. Investigate West Bengal and Odisha for extreme ratios (50-57x)
2. Review data collection processes in high-anomaly states
3. Standardize state naming conventions across data sources

### Short-term (1-3 months)
1. Implement automated data quality checks
2. Create real-time anomaly detection dashboard
3. Set up alerts for unusual patterns
4. Conduct district-level analysis for high-anomaly states

### Long-term (3-6 months)
1. Integrate with population census data
2. Build predictive models for fraud detection
3. Develop comprehensive data quality framework
4. Train staff on data quality best practices

## 🛠️ Technologies Used

- **Python 3.14** - Core programming language
- **pandas** - Data manipulation and analysis
- **matplotlib** - Data visualization
- **seaborn** - Statistical data visualization
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning utilities (MinMaxScaler)

## 📊 Dataset Information

- **Total Records**: 3,077,729
- **Enrolment Records**: 1,006,029 (3 CSV files)
- **Update Records**: 2,071,700 (5 CSV files)
- **States Covered**: 53
- **Time Period**: March 2025
- **Data Categories**: Age groups (0-5, 5-17, 18+), Geographic (State, District, Pincode)

## 📖 Documentation

Comprehensive documentation is provided in the following files:

- **QUICK_REFERENCE.txt** - Quick facts, numbers, and Q&A prep
- **VISUALIZATION_GUIDE.txt** - Detailed guide to all 5 visualizations
- **ANALYSIS_REPORT.txt** - Complete technical analysis report
- **PRESENTATION_SUMMARY.txt** - Slide-by-slide presentation guide
- **FINAL_PROJECT_SUMMARY.txt** - Complete project summary

## 🎤 Presentation Guide

### For 5-Minute Presentation
Use: `anomaly_detection.png` + `advanced_risk_heatmap.png`

### For 10-Minute Presentation
Use: `trend_analysis.png` + `anomaly_detection.png` + `advanced_combo_chart.png`

### For 15-Minute Presentation
Use: All 5 visualizations

See `PRESENTATION_SUMMARY.txt` for detailed presentation strategies.

## 🤝 Contributing

This is a hackathon project. If you'd like to contribute or have suggestions:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

## 🙏 Acknowledgments

- UIDAI for providing the hackathon opportunity
- Data sources: Aadhaar enrolment and demographic update records
- Python community for excellent data science libraries

## 📞 Contact

For questions or feedback, please open an issue or contact [your.email@example.com]

---

**⭐ If you find this project useful, please consider giving it a star!**

---

*Generated: January 16, 2026*  
*Status: Complete and Ready for Presentation*  
*Quality: Publication-grade (300 DPI visualizations)*
