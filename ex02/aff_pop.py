from load_csv import load
import matplotlib.pyplot as plt
from pandas import DataFrame, Series


def convert_population_str(value: str) -> float:
    """
    Converts population strings like '2.5M', '850K', '1.2B' to floats.
    """
    try:
        if isinstance(value, (int, float)):
            return float(value)
        value = value.strip()
        if value.endswith("K"):
            return float(value[:-1]) * 1_000
        elif value.endswith("M"):
            return float(value[:-1]) * 1_000_000
        elif value.endswith("B"):
            return float(value[:-1]) * 1_000_000_000
        else:
            return float(value)
    except Exception:
        return 0.0  # fallback if conversion fails


def display_population_comparison(country1: str, country2: str) -> None:
    """
    Loads population data and compares two countries between 1800 and 2050.

    Args:
        country1 (str): The first country (e.g., "Portugal").
        country2 (str): The second country to compare (e.g., "Germany").

    Returns:
        None
    """
    try:
        data: DataFrame | None = load("../population_total.csv")
        if data is None:
            print("Error: Could not load dataset.")
            return

        if country1 not in data.index or country2 not in data.index:
            print(
                f"Error: One or both countries not found: "
                f"{country1}, {country2}"
            )
            return

        # Select only years from 1800 to 2050
        selected_years = [
            col for col in data.columns if 1800 <= int(col) <= 2050]
        years = list(map(int, selected_years))

        pop1: Series = data.loc[country1, selected_years] \
            .apply(convert_population_str) / 1_000_000
        pop2: Series = data.loc[country2, selected_years] \
            .apply(convert_population_str) / 1_000_000

        # Plot both countries
        plt.plot(years, pop1, label=country1, color='green')
        plt.plot(years, pop2, label=country2, color='blue')

        plt.title(f"Population Comparison: {country1} vs {country2}")
        plt.xlabel("Year")
        plt.ylabel("Population (in millions)")
        plt.legend()
        plt.grid(False)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


def main() -> None:
    display_population_comparison("Portugal", "Belgium")  # 🇵🇹 vs be


if __name__ == "__main__":
    main()
