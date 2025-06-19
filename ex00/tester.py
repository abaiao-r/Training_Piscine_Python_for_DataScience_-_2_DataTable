from pandas import DataFrame
from load_csv import load

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def print_result(msg: str, status: str) -> None:
    """Prints the result of a test with appropriate color coding.
    Args:
        msg (str): The message to print.
        status (str): The status of the test ('pass', 'fail', 'error').
    """

    if status == "pass":
        print(f"{GREEN}[PASS]{RESET} {msg}")
    elif status == "fail":
        print(f"{RED}[FAIL]{RESET} {msg}")
    elif status == "error":
        print(f"{YELLOW}[ERROR]{RESET} {msg}")
    else:
        print(msg)


def test_valid_csv() -> None:
    print("Test 1: Valid CSV file")
    try:
        df: DataFrame | None = load("../life_expectancy_years.csv")
        if df is not None:
            print_result("Loaded valid CSV file.", "pass")
            print(df)
        else:
            print_result("Could not load the dataset.", "fail")
    except Exception as e:
        print_result(f"Test failed due to exception: {e}", "error")


def test_non_existent_file() -> None:
    print("\nTest 2: Non-existent file")
    try:
        df: DataFrame | None = load("non_existent_file.csv")
        if df is None:
            print_result("Correctly handled non-existent file.", "pass")
        else:
            print_result(
                "Should have returned None for non-existent file.", "fail")
    except Exception as e:
        print_result(f"Exception for non-existent file: {e}", "error")


def test_bad_format() -> None:
    print("\nTest 3: Bad format (txt file)")
    try:
        df: DataFrame | None = load("bad_format.txt")
        if df is None:
            print_result("Correctly handled bad format file.", "pass")
        else:
            print_result(
                "Should have returned None for bad format file.", "fail")
    except Exception as e:
        print_result(f"Exception for bad format file: {e}", "error")


def test_empty_csv() -> None:
    print("\nTest 4: Empty CSV file")
    try:
        df: DataFrame | None = load("empty.csv")
        if df is None:
            print_result("Correctly handled empty file.", "pass")
        else:
            print_result("Should have returned None for empty file.", "fail")
    except Exception as e:
        print_result(f"Exception for empty file: {e}", "error")


def test_wrong_extension() -> None:
    print("\nTest 5: Wrong extension (but valid CSV content)")
    try:
        df: DataFrame | None = load("../valid_but_wrong_ext.data")
        if df is not None:
            print_result(
                "Loaded file with wrong extension (if supported).", "pass")
            print(df)
        else:
            print_result(
                "Could not load file with wrong extension "
                + "(acceptable if not supported).",
                "info"
            )
    except Exception as e:
        print_result(f"Exception for wrong extension: {e}", "error")


def main() -> None:
    test_valid_csv()
    test_non_existent_file()
    test_bad_format()
    test_empty_csv()
    test_wrong_extension()


if __name__ == "__main__":
    main()
