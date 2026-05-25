import pandas as pd

def load_data():
    gdp = pd.read_csv("data/raw/gdp-per-capita-maddison-project-database/gdp-per-capita-maddison-project-database.csv")
    life_expectancy = pd.read_csv("data/raw/life-expectancy-hmd-unwpp/life-expectancy-hmd-unwpp.csv")
    calories = pd.read_csv("data/raw/daily-per-capita-caloric-supply/daily-per-capita-caloric-supply.csv")
    vegetables = pd.read_csv("data/raw/vegetable-consumption-per-capita/vegetable-consumption-per-capita.csv")
    income_groups = pd.read_csv("data/raw/world-bank-income-groups/world-bank-income-groups.csv")
    return gdp, life_expectancy, calories, vegetables, income_groups

def clean_data(gdp, life_expectancy, calories, vegetables, income_groups):
    # only use rows with non-missing values
    df = gdp.merge(life_expectancy, on=["Entity", "Code", "Year"], how="inner")
    df = df.merge(calories, on=["Entity", "Code", "Year"], how="inner")
    df = df.merge(vegetables, on=["Entity", "Code", "Year"], how="inner")
    df = df.merge(income_groups, on=["Entity", "Code", "Year"], how="inner")

    # Annotations are NA and country names are clean so Code is not needed
    df = df.drop(columns=["Code", "GDP per capita (Annotations)"])

    df = df.rename(columns={
        "Entity": "country",
        "Year": "year",
        "GDP per capita": "gdp_per_capita",
        "Life expectancy at birth, totals, period": "life_expectancy",
        "Daily calorie supply per person": "daily_calorie_supply_capita",
        "Vegetable supply per person": "yearly_vegetables_supply_kg_capita",
        "World Bank's income classification": "country_wb_income_group"
    })

    # Convert to g/day for easy comparison with calories
    df["daily_vegetables_supply_g_capita"] = (df["yearly_vegetables_supply_kg_capita"]/365)*1000

    df = df.drop(columns=["yearly_vegetables_supply_kg_capita"])

    # Max 127 countries have records before 1992, 145 after
    df = df[df["year"]>=1992]

    # Keep only countries for which data is present for all years
    n_years = df["year"].nunique()
    complete_countries = (
    df.groupby("country")["year"]
    .nunique()
    .loc[lambda x: x == n_years]
    .index
    )

    df = df[df["country"].isin(complete_countries)]

    # reorder so that income groups are the last column
    df = df[["country", "year", "gdp_per_capita", "life_expectancy",
        "daily_calorie_supply_capita",
        "daily_vegetables_supply_g_capita", "country_wb_income_group"]]
    return df

def save_data(df):
    df.to_csv("data/processed/clean_data.csv", index=False)

if __name__ == "__main__":
    gdp, life_expectancy, calories, vegetables, income_groups = load_data()
    df = clean_data(gdp, life_expectancy, calories, vegetables, income_groups)
    save_data(df)
    print("Data cleaned and saved in 'data/processed'.")

