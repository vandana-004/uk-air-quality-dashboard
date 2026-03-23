# uk-air-quality-dashboard
UK Air Quality data cleaning and dashboard project

# UK Air Quality Dashboard

A Python Dash dashboard analysing air quality across UK cities using DEFRA AURN data (2015–2023).

## Team

| Name    | Role                                |
|---------|-------------------------------------|
| Vandana | Data Lead                           |
| Nikhil  | Business & Documentation Lead       |
| Semih   | Coordinator                         |
| Vignesh | Technical Lead                      |

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/vandana-004/uk-air-quality-dashboard.git
cd uk-air-quality-dashboard

### 2. Install dependencies
pip install -r requirements.txt

### 3. Get the dataset
The cleaned dataset is too large for GitHub (~76MB).

Download it here: (https://drive.google.com/file/d/1JEjStQS0062ID1MG2usgNZ5Hw7l3iLWd/view?usp=sharing)

Save it to your local data/ folder:
your-repo/
  data/
    UK_Air_Quality_Cleaned.csv   ← put it here

Alternatively, generate it yourself:
- Download the raw dataset from Kaggle: https://www.kaggle.com/datasets/airqualityanthony/uk-defra-aurn-air-quality-data-2015-2023
- Run the cleaning script: python cleaning/data_cleaning.py

### 4. Run the dashboard
python dashboard/app.py


---

## Project Structure

cleaning/data_cleaning.py        - Data cleaning pipeline

dashboard/app.py                 - Main Dash application

dashboard/components/            - Individual dashboard components

sprint_docs/                     - Sprint documentation

data/                            - Local only, not on GitHub (see step 3)

---

## Data Source

UK DEFRA AURN Air Quality Data 2015–2023
https://www.kaggle.com/datasets/airqualityanthony/uk-defra-aurn-air-quality-data-2015-2023

Pollutants covered: NO2, PM2.5, PM10, CO, O3, SO2
Additional variables: wind speed, air temperature, site location, site type
```
