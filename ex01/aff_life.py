from load_csv import load
import matplotlib.pyplot as plt
from pandas import DataFrame, Series


def display_country_life_expectancy(country: str) -> None:
    """
    Loads the life expectancy dataset and plots the data for a given country.

    Args:
        country (str): The name of the country (e.g., "Portugal").

    Returns:
        None
    """
    try:
        data: DataFrame | None = load("../life_expectancy_years.csv")
        if data is None:
            print("Error: Could not load dataset.")
            return

        if country not in data.index:
            print(f"Error: Country '{country}' not found in dataset.")
            return

        row: Series = data.loc[country]
        years = row.index.astype(int)
        values = row.values.astype(float)

        plt.plot(years, values, label=country, color='green')
        plt.title(f"Life Expectancy Over Time in {country}")
        plt.xlabel("Year")
        plt.ylabel("Life Expectancy (Years)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


def main() -> None:
    # Hardcoded for your campus country: Portugal 🇵🇹
    display_country_life_expectancy("Portugal")


if __name__ == "__main__":
    main()
