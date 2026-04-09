# cross-country-diet-and-health-analysis
Project analysing diets and health outcomes across countries looking for potential patterns and economic situation relations.

Requires Python 3.x

## Setup

1. Create a virtual environment:
   python3 -m venv venv

2. Activate it:
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

## Run

1. Open the analysis notebook:
   jupyter notebook

   ## Data

The cleaned dataset is included in `data/processed/clean_data.csv` for convenience.

Raw data was sourced from:
- Our World in Data

## Reproducibility (Optional)

To reproduce the dataset from raw data:

1. Place raw data files in `data/raw/`
2. Run:
   python src/data_cleaning.py
