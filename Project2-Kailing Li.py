# Part1
import pandas as pd

SPECIAL_COLUMNS = {"MCIF", "MADJ", "Trade", "Trans", "MDTY", "TOP", "SUB"}

INDUSTRY_TOTAL_CODES = {"T007", "T013", "T014", "T015", "T016", "T017"}

def load_sheet(file_path, sheet_name):
    df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None, skiprows=5)

    industry_codes = df_raw.iloc[0, 2:]
    industry_names = df_raw.iloc[1, 2:]
    industry_labels = [f"{code}" for code in industry_codes]

    data = df_raw.iloc[2:, :].copy()
    data.columns = ["commodity_code", "commodity_name"] + industry_labels

    data = data[pd.notnull(data["commodity_code"])]

    data = data[~data["commodity_name"].astype(str).str.contains("Total", case=False, na=False)]

    industry_to_keep = [
        col for col in industry_labels
        if ("Total" not in str(col)) and
           (col not in INDUSTRY_TOTAL_CODES or col in SPECIAL_COLUMNS)
    ]
    columns_to_keep = ["commodity_code", "commodity_name"] + industry_to_keep
    data = data[columns_to_keep]

    data.replace("...", pd.NA, inplace=True)
    data.iloc[:, 2:] = data.iloc[:, 2:].apply(pd.to_numeric, errors='coerce').fillna(0)

    df_long = data.melt(
        id_vars=["commodity_code", "commodity_name"],
        var_name="industry",
        value_name="value"
    )

    df_long["year"] = int(sheet_name)
    df_long = df_long.rename(columns={"commodity_code": "commodity"})
    df_long = df_long[["year", "commodity", "industry", "value"]]

    naics_df = data[["commodity_code", "commodity_name"]].copy()
    naics_df.columns = ["naics_code", "description"]

    assert pd.api.types.is_numeric_dtype(df_long["value"]), "The 'value' column must be numeric."


    return df_long, naics_df


def process_all_sheets(file_path):
    xl = pd.ExcelFile(file_path)
    all_data = []
    all_naics = []

    for sheet in xl.sheet_names:
        try:
            int(sheet)
            use_df, naics_df = load_sheet(file_path, sheet)
            all_data.append(use_df)
            all_naics.append(naics_df)
        except:
            continue

    full_use_df = pd.concat(all_data, ignore_index=True)
    full_naics_df = pd.concat(all_naics, ignore_index=True).drop_duplicates()

    return full_use_df, full_naics_df

#Check
if __name__ == "__main__":
    file_path = r"F:\Users\YOGA\Desktop\AAE718\project2\Supply_Tables_1997-2023_Summary.xlsx"
    use_df, naics_df = process_all_sheets(file_path)

    print(use_df)
    print(naics_df)
    print(use_df["value"].dtype)
    
    use_df.to_csv("clean_supply_data.csv", index=False)
    naics_df.to_csv("naics_lookup.csv", index=False)
    
# Part2
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# load data
current_path = os.getcwd()
csv_filename = 'clean_supply_data.csv'
data_path = os.path.join(current_path, csv_filename)
df = pd.read_csv(data_path)

# set output path
output_dir = current_path
os.makedirs(output_dir, exist_ok=True)

top_commodities = df.groupby('commodity')['value'].sum().nlargest(15)
top_industries = df.groupby('industry')['value'].sum().nlargest(15)

# Yearly Total Trend
yearly_total = df.groupby('year')['value'].sum().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=yearly_total, x='year', y='value', marker='o', linewidth=2)
plt.title('Yearly Total Trend (1997-2023)', fontsize=14)
plt.xlabel('Year (year)', fontsize=12)
plt.ylabel('Total (millions of dollars)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_dir}/yearly_total_trend.png', dpi=300)
plt.close()

# Top5 Commodities Trend
top5_commodities = top_commodities.index[:5].tolist()
top5_data = df[df['commodity'].isin(top5_commodities)]
top5_yearly = top5_data.groupby(['year', 'commodity'])['value'].sum().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=top5_yearly, x='year', y='value', hue='commodity', marker='o', linewidth=2)
plt.title('Top5_Commodities_Trend (1997-2023)', fontsize=14)
plt.xlabel('Year (year)', fontsize=12)
plt.ylabel('Supply (millions of dollars)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.legend(title='Commodity Code', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{output_dir}/top5_commodities_trend.png', dpi=300)
plt.close()

# MCIF Trend Analysis
mcif_industry = top_industries.index[:1].tolist()
mcif_data = df[df['industry'].isin(mcif_industry)]
mcif_yearly = mcif_data.groupby(['year', 'industry'])['value'].sum().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=mcif_yearly, x='year', y='value', hue='industry', marker='o', linewidth=2)
plt.title('MCIF Industry Trend Analysis', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('MCIF Value (millions of dollars)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.legend(title='Industry Code', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{output_dir}/mcif_industry_trend.png', dpi=300)
plt.close()

# Growth Rate Volatility
yearly_total = df.groupby('year')['value'].sum().reset_index()
yearly_total['growth_rate'] = yearly_total['value'].pct_change() * 100

# Calculate rolling volatility (3 years)
yearly_total['volatility'] = yearly_total['growth_rate'].rolling(window=3).std()

plt.figure(figsize=(12, 6))
sns.lineplot(data=yearly_total[3:], x='year', y='volatility', marker='o', linewidth=2, color='purple')
plt.title('Growth_Rate_Volatility (1997-2023)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Volatility (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_dir}/growth_rate_volatility.png', dpi=300)
plt.close()



    


