# ENPM611 Project Application Template

This is the template for the ENPM611 class project. Use this template in conjunction with the provided data to implement an application that analyzes GitHub issues for the [poetry](https://github.com/python-poetry/poetry/issues) Open Source project and generates interesting insights.

This application template implements some of the basic functions:

- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. You can add other configuration paramters to the `config.json` file.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses you implemented will be run. You need to extend this module to call other analyses.

With the utility functions provided, you should focus on implementing creative analyses that generate intersting and insightful insights.

In addition to the utility functions, an example analysis has also been implemented in `example_analysis.py`. It illustrates how to use the provided utility functions and how to produce output.

## Setup

To get started, your team should create a fork of this repository. Then, every team member should clone your repository to their local computer. 


### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Download the data file (in `json` format) from the project assignment in Canvas and update the `config.json` with the path to the file. Note, you can also specify an environment variable by the same name as the config setting (`ENPM611_PROJECT_DATA_PATH`) to avoid committing your personal path to the repository.


### Run an analysis

With everything set up, you should be able to run the existing example analysis:

```
python run.py --feature 0
```

That will output basic information about the issues to the command line.


## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface sligthly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.

## Analysis Hosted Project - [Repolyzer](https://repolyzer.vercel.app/)

We've created the web-version of the analysis using ReactJS. We used Vibecoding to achieve the task. The LLM used was o4-mini by OpenAI. Here's the link to the hosted site for [Repolyzer](https://repolyzer.vercel.app/)

## Testing

### Overview

For Milestone 3, we implemented comprehensive unit tests to verify the functionality and stability of all analysis modules developed in the project. The goal was to ensure correctness, handle edge cases, and achieve the required test coverage as per project guidelines.

---

### Tested Modules

We wrote unit tests for the following analysis components:

| Module File                               | Description                                              |
|-------------------------------------------|----------------------------------------------------------|
| `analysis_contributor_vs_labelheatmap.py` | Heatmap of top 10 contributors vs labels                |
| `analysis_event_by_date.py`               | Event frequency by date                                 |
| `analysis_event_count_by_label.py`        | Count of events grouped by label                        |
| `analysis_issue_count_by_label.py`        | Total number of issues per label                        |
| `analysis_issue_creation_over_years.py`   | Annual trend in issue creation                          |
| `analysis_issue_per_event.py`             | Number of issues for each event type                    |
| `analysis_label_popularity.py`            | Label usage trends over time (Top 5 labels)             |
| `analysis_monthly_issue_trend.py`         | Monthly trend of issue creation                         |
| `analysis_open_issue_by_creator.py`       | Number of open issues per creator                       |
| `analysis_open_issue_duration.py`         | Duration analysis for how long issues remain open       |
| `analysis_type_of_events.py`              | Distribution of event types over time                   |

Tests were written using Python’s built-in `unittest` framework and mocked external dependencies like `DataLoader` and `matplotlib.pyplot.show` to isolate analysis logic.

---


### How to Run Tests

To run all test cases and generate a coverage report:

```bash
coverage run -m unittest discover
coverage report --omit="test_*"
```

## Test Coverage

| File                                       | Coverage |
|--------------------------------------------|----------|
| `analysis_contributor_vs_labelheatmap.py` | 100%     |
| `analysis_monthly_issue_trend.py`         | 100%     |
| `analysis_label_popularity.py`            | 100%     |
| `analysis_event_by_date.py`               | 98%      |
| `analysis_type_of_events.py`              | 95%      |
| **Overall Analysis Module Coverage**      | **100%** |
| **Total Codebase Coverage**               | 70%      |

> **Note:** Supporting files like `config.py`, `data_loader.py`, and `model.py` were not directly tested but were mocked to support analysis module testing.

---

##  Issues Found During Testing

### 1. Plotting Error in `analysis_type_of_events.py`

- **Issue**: A `matplotlib.units.ConversionError` was raised due to mixing incompatible datetime formats on the x-axis.
- **Cause**: Plotting `datetime64` objects without consistent axis formatting.
- **Fix Recommendation**: Explicitly convert dates using `pd.to_datetime()` or `.strftime('%Y-%m')`.

### 2. Incomplete Handling of Empty Inputs in Analysis Modules

- **Affected Modules**:
  - `analysis_contributor_vs_labelheatmap.py`
  - `analysis_label_popularity.py`
  - `analysis_monthly_issue_trend.py`

- **Issue**: When no valid data (e.g., labels or contributors) is available, the modules print a message but may continue executing and attempt to plot empty or misleading visuals.
- **Cause**: The scripts lack an early return or exit after detecting empty data scenarios.
- **Fix Recommendation**: Add a `return` statement immediately after the "No data found" message to halt execution cleanly and avoid unnecessary plotting.

### 3. Datatype Mismatch 

- **Issue**: A data mismatch between the assignee json value and what we are defaulting if there is none. The actual value is a list however we are defaulting an empty string
- **Fix Recommendation**: Default an empty list instead
