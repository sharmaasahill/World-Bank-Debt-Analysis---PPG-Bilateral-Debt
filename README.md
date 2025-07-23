# World Bank Debt Analysis - PPG Bilateral Debt

## Overview

This project analyzes the World Bank's PPG (Public and Publicly Guaranteed) Bilateral Debt data, offering insights into global debt trends, country-specific debt burdens, and the dynamics of international financial support between India and South Asian countries.

## Objective

Recent headlines like "South Asia in Chinese Debt Trap", "Economic crisis in Sri Lanka", and "Failing economy of Pakistan" sparked curiosity about bilateral lending relationships between countries. Using Python, I developed scripts to download and analyze PPG Bilateral Debt data between India and its neighboring countries.

The project collects and analyzes data of PPG bilateral lending between India and six South Asian countries: **Bangladesh, Bhutan, Sri Lanka, Nepal, Maldives, and Myanmar**. Data spanning 20 years has been wrangled, analyzed, and visualized through both Excel dashboards and an interactive web application.

## About the Dataset

The dataset includes detailed PPG Bilateral debt data between India and the six South Asian countries, obtained using the World Bank API. Each dataset contains:

- **Year**: Year of debt data
- **Debtor**: Debtor country code
- **Debt in US$**: Amount of debt in US dollars
- **YoY Growth %**: Year-over-year growth percentage of bilateral debt

All 6 datasets are combined, cleaned, wrangled, and analyzed in the comprehensive Excel dashboard.

**Data Source**: World Bank International Debt Statistics (Primary data)

## Interactive Web Application

A modern, interactive web application has been built using Streamlit to make the analysis more accessible and user-friendly.

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Application**:
   ```bash
   streamlit run app.py
   ```

### Features

- **Interactive Country Selection**: Choose from 6 South Asian countries
- **Time Period Filtering**: Select custom year ranges (1972-2020)
- **Real-Time Visualizations**: Interactive charts and graphs
- **Comparative Analysis**: Side-by-side country comparisons
- **Custom Reports**: Generate and download analysis reports
- **Data Export**: Download filtered data as CSV files

### Deployment

The application is ready for deployment to Streamlit Cloud. The repository includes all necessary configuration files for seamless deployment.

## Project Structure

```
World-Bank-Debt-Analysis---PPG-Bilateral-Debt/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .streamlit/config.toml          # Streamlit configuration
├── .gitignore                      # Git ignore file
├── README.md                       # This file
├── Bilateral Debt Data/            # Excel data files (6 countries)
├── Python Scripts/                 # Original analysis scripts
├── Country Code Data/              # Country code references
├── Project Report.pdf              # Detailed project report
├── Bilateral Debt Analysis.xlsx    # Combined analysis dashboard
└── Bilateral Debt Analysis Presentation.pptx
```

## Original Script Guidelines

For users interested in the original data collection process:

1. **Debtor Country Codes**: Use the [Debtor Country Code Script](Python%20Scripts/Debtor%20Country%20Code%20Script.py) or download the [Debtor Country Code Excel file](Country%20Code%20Data/Debtor%20Country%20Code.xlsx)

2. **Creditor Country Codes**: Use the [Creditor Country Code Script](Python%20Scripts/Creditor%20Country%20Code%20Script.py) or download the [Creditor Country Code Excel file](Country%20Code%20Data/Creditor%20Country%20Code.xlsx)

3. **Data Collection**: Use the [PPG Bilateral Debt Script](Python%20Scripts/PPG%20Bilateral%20Debt%20Script.ipynb) to collect data from the World Bank API

## Key Findings

1. **Total Debt Growth**: PPG Bilateral Lending increased from less than $500 million in 2000 to about $45 billion in 2020

2. **Country Distribution**: 
   - **Bhutan** has been the biggest debtor country, receiving almost $18 billion over 20 years
   - **Nepal** has received the least bilateral lending, amounting to less than $1 billion

3. **Growth Trends**: Total bilateral lending shows a positive growth rate over the last 20 years

4. **Economic Impact**: Total bilateral lending to neighboring countries is approximately 1.2% of India's overall GDP

5. **Risk Assessment**: In the event of default by any neighboring country, the impact on India's financial sector would be minimal (based on the analyzed data)

## Technologies Used

- **Python**: Data analysis and processing
- **Streamlit**: Interactive web application
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **World Bank API**: Data collection
- **Excel**: Data storage and initial analysis

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding new analyses

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Built with ❤️ for better understanding of international debt relationships** 