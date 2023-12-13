import os
import shutil
import pandas as pd
import argparse
import logging


# JSON File format/structure used
"""
{
    "test_case_id": 1,
    "test_case_name": "Request Access Test",
    "status": "passed",
    "duration": 2.019,
    "timestamps": "2023-10-31T06:31:28Z",
}

Above is an example of a test case object. This dictionary contains data for each test case executed.
- test_case_id: This is the unique id of each test case.
- test_case_name: This is the name of the test.
- status: This represents the state of the test case. Passed or Failed.
- duration: The execution time in seconds for the test case.
- timestamps: Represents the exact date and time when the test case was executed.


NOTE: This script assumes an array of objects, containing the above mentioned structure and format.
"""


# This is a decorator function to handle and log any errors
def error_handler_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise  # re-throw the last exception

    return wrapper


@error_handler_decorator
def json_to_csv(json_file_location: str) -> pd.DataFrame:
    """
    Function to convert a JSON file into a pandas dataframe.
    Pandas dataframes are very useful to analyze and visualize data.
    The built-in methods from the pandas dataframe are used to streamline
    most data operations.
    """

    # Reading JSON file to store it in a pandas dataframe
    return pd.read_json(json_file_location)


@error_handler_decorator
def dataframe_to_csv(dataframe: pd.DataFrame, csv_file_location: str) -> None:
    """
    Function to convert a pandas dataframe into a CSV file.
    """

    # Converting pandas dataframe into a CSV using pandas built in method
    dataframe.to_csv(csv_file_location, index=False)

    print(f"Data converted to {csv_file_location} successfully!")


@error_handler_decorator
def export_csv(csv_file_name: str, export_location: str) -> None:
    """
    Function to export the CSV file to a specified location.
    The CSV File is copied from the temporary location in the filesystem
    to the specified location, then the temporary file is removed.
    """

    # Creating the desired directory location in case it does not exist.
    # If it not exist, its only overriten
    os.makedirs(export_location, exist_ok=True)

    # Making sure the final CSV location have the correct filepath
    csv_file_path = os.path.join(export_location, os.path.basename(csv_file_name))

    # Creating a copy of the CSV in the desired location on the filesystem
    shutil.copy(csv_file_name, csv_file_path)

    # Deleting the generated CSV to have only one copy in the desired location filesystem
    os.remove(csv_file_name)
    print(f"CSV file was exported sucessfully to: {csv_file_path}")


@error_handler_decorator
def metrics_report(df: pd.DataFrame) -> None:
    """
    Funtion to calculate and display different metrics like:
    Number of tests executed.
    Number of tests passed.
    Number of tests failed.
    Average execution time for all test cases.
    Minimum execution time among all test cases.
    Maximum execution time among all test cases.
    """

    # Obtaining the number of rows of the results data in dataframe
    # using the len method on the dataframe.
    print(f"- Number of test cases executed: {len(df)}")

    # Using the .sum() built in method from the pandas library,
    # for easier agregations on the 'status' column values.
    print(f"- Test cases passed: {(df['status'] == 'passed').sum()}")

    # Using the .sum() built in method from the pandas library,
    # for easier agregations on the 'status' column values.
    print(f"- Test cases failed: {(df['status'] == 'failed').sum()}")

    # Using the .mean() built in method from the pandas library,
    # for easier agregations on the 'duration' column values.
    print(
        f"- Average test case execution time: {round(df['duration'].mean(), 2)} seconds"
    )

    # Using the .max() built in method from the pandas library,
    # for easier agregations on the 'duration' column values.
    print(
        f"- Maximum test case execution time: {round(df['duration'].max(), 2)} seconds"
    )

    # Using the .min() built in method from the pandas library,
    # for easier agregations on the 'duration' column values.
    print(
        f"- Minimum test case execution time: {round(df['duration'].min(), 2)} seconds"
    )


# When you run the file as a script by passing the file object to your Python interpreter,
# the expression __name__ == "__main__" returns True.
if __name__ == "__main__":
    # Setting the description of the Arguments.
    parser = argparse.ArgumentParser(description="Test Results Analysis")

    # Argument to set the specified json file location on the filesystem.
    parser.add_argument("--json_file_location", type=str, help="Path to the JSON file.")

    # Argument to set the specified csv file name to save it on the filesystem.
    parser.add_argument("--csv_file_name", type=str, help="CSV Name")

    # Argument to set the specified the location to export the csv on the filesystem.
    parser.add_argument(
        "--export_location", type=str, help="Path to desired export location."
    )

    # The arguments passed are parsed
    args = parser.parse_args()

    # The dataframe is created using the json file
    df = json_to_csv(args.json_file_location)

    # The csv is created from the dataframe using the csv_file_name argument
    dataframe_to_csv(df, args.csv_file_name)

    # The created csv is then exported to the specified location passed in the argument
    export_csv(args.csv_file_name, args.export_location)

    # Finally, the desired metrics are the printed into the console
    metrics_report(df)
