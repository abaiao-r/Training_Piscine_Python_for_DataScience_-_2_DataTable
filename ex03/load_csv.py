import pandas as pd


def load(path: str) -> pd.DataFrame | None:
    """
    Loads a CSV dataset from the given path using pandas.

    Parameters:
        path (str): The file path to the CSV dataset.

    Returns:
        pd.DataFrame | None: The loaded DataFrame, or None if loading fails.
    """
    try:
        # Try reading the CSV file
        data: pd.DataFrame = pd.read_csv(path, index_col=0)

        # Print the shape of the dataset
        print(f"Loading dataset of dimensions {data.shape}")
        return data

    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return None
    except pd.errors.ParserError:
        print("Error: File format not recognized or file is not a valid CSV.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
