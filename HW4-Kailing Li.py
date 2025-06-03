#Problem1
import os

def csv_files(directory):
    csv_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                full_path = os.path.join(root, file)
                csv_list.append(full_path)
    return csv_list

# Problem2
import pandas as pd

def load_emission_csv(filepath, year):

    df = pd.read_csv(filepath)
    df["year"] = year
    return df

# Problem3
def load_emissions(directory):

    all_csv_files = csv_files(directory)  
    df_list = []

    for path in all_csv_files:
        filename = os.path.basename(path)
        year = ''.join(filter(str.isdigit, filename))  
        df = load_emission_csv(path, year) 
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

# Problem4
def merge_emissions_with_country(emissions_directory, country_code_path):
 
    emissions_df = load_emissions(emissions_directory)
    emissions_df = emissions_df.rename(columns={"Country": "country"})
    country_df = pd.read_csv(country_code_path)
    country_df = country_df.rename(columns={"name": "country"})
    country_df = country_df[["country", "alpha-2", "region", "sub-region"]]
    merged_df = emissions_df.merge(country_df, on="country", how="left")
    merged_df.to_csv("F:/Users/YOGA/Desktop/AAE718/4/merged_emissions_with_country.csv", index=False)
    return merged_df

# Problem5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def problem5_from_csv(merged_csv_path):
    df = pd.read_csv(merged_csv_path)
    
    plot_total_emissions_by_region(df)
    plot_log_per_capita_distribution(df)
    plot_avg_per_capita_by_region(df)

def plot_total_emissions_by_region(df):
    # Sum total CO2 emissions per region
    region_emissions = df.groupby("region")["Emissions.Type.CO2"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=region_emissions.index, y=region_emissions.values)
    plt.xticks(rotation=45)
    plt.title("Total CO2 Emissions by Region")
    plt.ylabel("Total Emissions (CO2)")
    plt.xlabel("Region")
    plt.tight_layout()
    plt.show()

def plot_log_per_capita_distribution(df):
    # Log-scaled histogram of per capita emissions
    df = df[df["Ratio.Per Capita"] > 0]  # Drop zero or negative values
    log_values = df["Ratio.Per Capita"].apply(lambda x: np.log(x))
    
    plt.figure(figsize=(8, 5))
    sns.histplot(log_values, bins=30, kde=True)
    plt.title("Log-Scaled Distribution of Per Capita Emissions")
    plt.xlabel("log(Per Capita Emissions)")
    plt.ylabel("Number of Countries")
    plt.tight_layout()
    plt.show()


def plot_avg_per_capita_by_region(df):
    # Regional average of per capita emissions
    df_clean = df[df["Ratio.Per Capita"] > 0]

    region_avg = df_clean.groupby("region")["Ratio.Per Capita"].mean().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=region_avg.index, y=region_avg.values)
    plt.title("Average Per Capita Emissions by Region")
    plt.ylabel("Average Per Capita Emissions")
    plt.xlabel("Region")
    plt.tight_layout()
    plt.show()

# Problem6
import pandas as pd

def dirty_data(filepath):
    df = pd.read_csv(filepath, header=None)

    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['First Class', 'Second Class', 'Standard Class', 'Same Day']
    
    cleaned_rows = []

    for i, segment in enumerate(segments):
        base_col = 1 + i * 5  

        for j, ship_mode in enumerate(ship_modes):
            col_idx = base_col + j  

            for row in range(2, df.shape[0]):  
                order_id = str(df.iloc[row, 0]).strip()

                if not order_id or order_id.lower().startswith("grand"):
                    continue  

                value = df.iloc[row, col_idx]

                if pd.notna(value): 
                    cleaned_rows.append({
                        'order_id': order_id,
                        'segment': segment,
                        'ship_mode': ship_mode,
                        'sales': float(value)
                    })

    return pd.DataFrame(cleaned_rows)

# Problem7
import pandas as pd

def school_data(file_path):
    colspecs = [
        (0, 2),     # FIPS State code
        (3, 8),     # District ID
        (9, 81),    # District Name
        (82, 90),   # Total Population
        (91, 99),   # Population 5-17
        (100, 108), # Population 5-17 in Poverty
    ]
    colnames = [
        "state_fips", "district_id", "district_name",
        "total_population", "pop_5_17", "poverty_5_17"
    ]
    
    df = pd.read_fwf(file_path, colspecs=colspecs, names=colnames, encoding="latin1")

    for col in ["total_population", "pop_5_17", "poverty_5_17"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# Just for check

#Problem1
directory_path = "F:/Users/YOGA/Desktop/AAE718/4/emissions"
csv_file_paths = csv_files(directory_path)

print(csv_file_paths)

#Problem2
df_2001 = load_emission_csv("F:/Users/YOGA/Desktop/AAE718/4/emissions/2001.csv", "2001")
print(df_2001.head())

#Problem3
emissions_df = load_emissions("F:/Users/YOGA/Desktop/AAE718/4/emissions")
print(emissions_df)

#Problem4
merge_emissions_with_country(
    emissions_directory="F:/Users/YOGA/Desktop/AAE718/4/emissions",
    country_code_path="F:/Users/YOGA/Desktop/AAE718/4/country_codes.csv"
)

#Problem5
problem5_from_csv("F:/Users/YOGA/Desktop/AAE718/4/merged_emissions_with_country.csv")

#Problem6
clean_df = dirty_data("F:/Users/YOGA/Desktop/AAE718/4/dirty_data_01.csv")
print(clean_df.shape)  
print(clean_df)

#Problem7
data_path = r"F:\Users\YOGA\Desktop\AAE718\4\school_data\ussd20.txt"
df = school_data(data_path)
print(df)
output_path = r"F:\Users\YOGA\Desktop\AAE718\4\school_data\school_data_cleaned.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")














