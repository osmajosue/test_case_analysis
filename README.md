# Test Data Analysis


This script processes test results stored in a JSON file. It converts the data to a Pandas DataFrame, creates a CSV, exports it, and provides metrics like the number of tests executed, passed, failed, average execution time, and more. Command-line arguments enable specifying file locations and names. Error handling is implemented using a decorator. The script aims to streamline the analysis and reporting of test results with flexibility in input and output file locations.


## Setup

In order to setup the script to work, I used pipenv virtual environment manager. To install it, use this command:

```bash
pip install pipenv
```

Then, in order to activate the virtual environment, run:

```bash
pipenv shell
```

To install script dependencies, run:

```bash
pipenv install
```

All the libraries needed are in the Pipfile.


## Script Usage

In order to run the script, you need to run this command inside the pipenv shell:

```bash
python scripts/result_analysis.py --json_file_location {JSON_FILEPATH} --csv_file_name {DESIRED_CSV_NAME} --export_location {DESIRED_LOCATION_FILEPATH}
```

### Arguments

#### --json_file_location

This is the path for the JSON file that is going to be used for this script.
The JSON file should have the following format/structure:

```json
[
 {
    "test_case_id": 1,
    "test_case_name": "Request Access Test",
    "status": "passed",
    "duration": 2.019,
    "timestamps": "2023-10-31T06:31:28Z",
 },
 {
    "test_case_id": 2,
    "test_case_name": "Login Test",
    "status": "failed",
    "duration": 2.418,
    "timestamps": "2023-09-13T05:08:18Z"
 }
]
```

This object contains data for each test case executed.
- test_case_id: This is the unique id of each test case.
- test_case_name: This is the name of the test.
- status: This represents the state of the test case. Passed or Failed.
- duration: The execution time in seconds for the test case.
- timestamps: Represents the exact date and time when the test case was executed.

#### --csv_file_name

This is a string indicating the desired name for the CSV file to be created.

Example:

```
results.csv
```

#### --export_location

This is a string indicating the desired filepath for the CSV file to be exported.

Example:

```
results/
```


### Example usage

```bash
python scripts/result_analysis.py --json_file_location tests/result.json --csv_file_name results.csv --export_location results/
```

