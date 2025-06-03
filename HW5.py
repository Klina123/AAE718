import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Problem 1
def problem_1():
    df = pd.read_csv("SOCR-HeightWeight.csv")
    df = df[["Height(Inches)", "Weight(Pounds)"]]
    df.columns = ["Height", "Weight"]

    # Matplotlib
    plt.figure(figsize=(6, 4))
    plt.scatter(df["Height"], df["Weight"])
    plt.title("Matplotlib: Height vs Weight")
    plt.xlabel("Height (inches)")
    plt.ylabel("Weight (pounds)")
    plt.tight_layout()
    plt.show()
    plt.close()

    # Seaborn
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=df, x="Height", y="Weight")
    plt.title("Seaborn: Height vs Weight")
    plt.xlabel("Height (inches)")
    plt.ylabel("Weight (pounds)")
    plt.tight_layout()
    plt.show()
    plt.close()

# Problem 2
def problem_2():
    df = pd.read_csv("SOCR-HeightWeight.csv")

    # Matplotlib: side-by-side histograms
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.hist(df["Height(Inches)"], bins=20)
    plt.title("Height (Inches)")
    plt.xlabel("Height(Inches)")
    plt.ylabel("Count")

    plt.subplot(1, 2, 2)
    plt.hist(df["Weight(Pounds)"], bins=20)
    plt.title("Weight (Pounds)")
    plt.xlabel("Weight(Pounds)")
    plt.ylabel("Count")

    plt.tight_layout()
    plt.savefig("problem2_matplotlib.png")
    plt.show()
    plt.close()

    # Seaborn: side-by-side histograms
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    sns.histplot(df["Height(Inches)"], bins=20)
    plt.title("Height (Inches)")

    plt.subplot(1, 2, 2)
    sns.histplot(df["Weight(Pounds)"], bins=20)
    plt.title("Weight (Pounds)")

    plt.tight_layout()
    plt.savefig("problem2_seaborn.png")
    plt.show()
    plt.close()

    height_std = df["Height(Inches)"].std()
    weight_std = df["Weight(Pounds)"].std()
    print("Height STD:", round(height_std, 2))
    print("Weight STD:", round(weight_std, 2))

# Problem 3
def problem_3():
    df = pd.read_csv("SOCR-HeightWeight.csv")

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x="Height(Inches)", y="Weight(Pounds)", alpha=0.6, color='black', s=20)
    sns.regplot(data=df, x="Height(Inches)", y="Weight(Pounds)", scatter=False, color="blue", line_kws={"linewidth": 2}, ci=95)
    plt.title("Seaborn: Height vs Weight with Trend Line")
    plt.xlabel("Height (inches)")
    plt.ylabel("Weight (pounds)")
    plt.tight_layout()
    plt.show()
    plt.close()

# Problem 4
def problem_4():
    df = pd.read_csv("company_sales_data.csv")

    # Plot 1
    plt.figure(figsize=(10, 6))
    plt.plot(df["month_number"], df["total_profit"], marker='o')
    plt.title("Total Profit Over Months")
    plt.xlabel("Month")
    plt.ylabel("Total Profit")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("problem4_profit.png")
    plt.show()
    plt.close()

    # Plot 2
    plt.figure(figsize=(10, 6))
    product_columns = ["facecream", "facewash", "toothpaste", "bathingsoap", "shampoo", "moisturizer"]
    for product in product_columns:
        plt.plot(df["month_number"], df[product], marker='o', label=product)
    plt.title("Product Sales Over Time")
    plt.xlabel("Month")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.tight_layout()
    plt.savefig("problem4_product_lines.png")
    plt.show()
    plt.close()

    # Plot 3
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="facecream", y="facewash")
    plt.title("Facecream vs Facewash Sales")
    sns.regplot(data=df, x="facecream", y="facewash", scatter=False, color="blue", line_kws={"linewidth": 2}, ci=95)
    plt.tight_layout()
    plt.savefig("problem4_facecream_facewash.png")
    plt.show()
    plt.close()

# Problem 5
def problem_5():
    df = pd.read_csv("crop_production.csv")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna(subset=["Value"])

    # Plot 1
    usa_wheat_df = df[(df["LOCATION"] == "USA") & (df["SUBJECT"] == "WHEAT") & (df["MEASURE"] == "THND_TONNE")]
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=usa_wheat_df, x="TIME", y="Value", marker="o")
    plt.title("Wheat Production in USA Over Time")
    plt.xlabel("Year")
    plt.ylabel("Production (Thousand Tonnes)")
    plt.tight_layout()
    plt.savefig("5_1_usa_wheat_trend.png")
    plt.show()
    plt.close()

    # Plot 2
    yield_df = df[df["MEASURE"] == "TONNE_HA"]
    avg_yield = yield_df.groupby("SUBJECT")["Value"].mean().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_yield, x="Value", y="SUBJECT", palette="viridis")
    plt.title("Average Yield per Crop (Tonnes per Hectare)")
    plt.xlabel("Average Yield")
    plt.ylabel("Crop Type")
    plt.tight_layout()
    plt.savefig("5_2_yield_by_crop.png")
    plt.show()
    plt.close()

    # Plot 3
    rice_df = df[(df["SUBJECT"] == "RICE") & (df["MEASURE"] == "THND_TONNE")]
    top_rice_producers = rice_df.groupby("LOCATION")["Value"].mean().nlargest(8).reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_rice_producers, x="Value", y="LOCATION", palette="Oranges_r")
    plt.title("Top 8 Countries by Average Rice Production")
    plt.xlabel("Avg Production (Thousand Tonnes)")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig("5_3_rice_production_top8.png")
    plt.show()
    plt.close()

# Just for check
if __name__ == "__main__":
    problem_1()
    problem_2()
    problem_3()
    problem_4()
    problem_5()
