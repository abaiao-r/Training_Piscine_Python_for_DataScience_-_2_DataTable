import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from load_csv import load


def parse_number(value: str) -> float | None:
    """
    Converts string numbers like '10k' or '2.5M' into floats.

    Parameters:
        value (str): A string representing a number (may include suffix).

    Returns:
        float | None: The numeric value as float, or None if invalid.
    """
    try:
        value = value.strip().lower().replace(",", "")
        if value.endswith("k"):
            return float(value[:-1]) * 1_000
        if value.endswith("m"):
            return float(value[:-1]) * 1_000_000
        return float(value)
    except Exception:
        return None


def dataframe_to_dict(df, year: str) -> dict:
    """
    Converts a pandas DataFrame into a dictionary for a specific year.

    Parameters:
        df (pd.DataFrame): DataFrame loaded using pandas.
        year (str): Year column to extract.

    Returns:
        dict: A dictionary of {country: value} for that year.
    """
    data = {}

    if year not in df.columns:
        raise KeyError(f"Year '{year}' not found in dataset.")

    for country in df.index:
        raw_value = df.at[country, year]
        if isinstance(raw_value, str):
            value = parse_number(raw_value)
        else:
            value = raw_value

        if value is not None:
            data[country] = value

    return data


def setup_hover(fig, ax, sc, x_values, y_values, labels) -> None:
    """
    Sets up the hover functionality for the plot.

    Parameters:
        fig: The figure object of the plot.
        ax: The axes object of the plot.
        sc: The scatter object of the plot.
        x_values: The x coordinates of the scatter points.
        y_values: The y coordinates of the scatter points.
        labels: The labels for each scatter point.
    """
    annot = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(10, 10),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc="w"),
        arrowprops=dict(arrowstyle="->"),
    )
    annot.set_visible(False)

    def update_annot(ind) -> None:
        idx = ind["ind"][0]
        annot.xy = (x_values[idx], y_values[idx])
        text = labels[idx]
        annot.set_text(text)

    def hover(event) -> None:
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)


def plot_gdp_vs_life_expectancy(gdp_df, life_df, year: str) -> None:
    """
    Plots a scatter plot of GDP vs Life Expectancy for a given year with
    interactive hover tooltips.

    Parameters:
        gdp_df: GDP data (from load function)
        life_df: Life expectancy data (from load function)
        year (str): The year to display on the plot.
    """
    try:
        gdp_data = dataframe_to_dict(gdp_df, year)
        life_data = dataframe_to_dict(life_df, year)

        # ┌───────────────────────────────────────────────┐
        # │        Match countries present in both        │
        # └───────────────────────────────────────────────┘
        countries = set(gdp_data.keys()) & set(life_data.keys())

        x_values = []
        y_values = []
        labels = []

        for country in countries:
            gdp = gdp_data.get(country)
            life = life_data.get(country)
            if gdp is not None and life is not None:
                x_values.append(gdp)
                y_values.append(life)
                labels.append(f"{country}\nGDP: {int(gdp):,}")

        if not x_values or not y_values:
            print(f"No valid data to plot for {year}")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        sc = ax.scatter(x_values, y_values, alpha=0.6)

        plt.title(f"Life Expectancy vs GDP (PPP) in {year}")
        plt.xlabel("GDP per capita (PPP, inflation-adjusted)")
        plt.ylabel("Life Expectancy (years)")

        # Use log scale and readable numeric labels (no currency symbol)
        plt.xscale("log")
        plt.gca().xaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: f"{int(x):,}")
        )

        # Add grid and display
        plt.grid(False)
        plt.tight_layout()
        setup_hover(fig, ax, sc, x_values, y_values, labels)
        plt.show()

    except KeyError:
        print(f"Error: Year '{year}' is not available in the dataset.")
    except Exception as e:
        print(f"Unexpected error while plotting: {e}")


def main() -> None:
    """
    Main function to load data and visualize projections over several years.
    """
    try:
        # Dataset paths
        gdp_file = (
            "../income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
        )
        life_file = "../life_expectancy_years.csv"

        # Load data using pandas (allowed in load function only)
        gdp_data = load(gdp_file)
        life_data = load(life_file)

        if gdp_data is None or life_data is None:
            print("Failed to load one or both datasets.")
            return

        # Plot for multiple years
        years = [
            "1900",
        ]
        for year in years:
            plot_gdp_vs_life_expectancy(gdp_data, life_data, year)

    except Exception as e:
        print(f"Unexpected error in main: {e}")


if __name__ == "__main__":
    main()
