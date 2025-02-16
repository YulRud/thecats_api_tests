# The Cats API Tests

This project is a demo for API testing using the free [The Cat API](https://thecatapi.com/). 
It demonstrates how to perform various API operations such as GET, POST, and DELETE on the following edpoints:
 - **GET /v1/images/search**: an endpoint that retrieves links to the cats images and has various request parameters and object fields in response to test
 - **GET /v1/images/:image_id**: an endpoint that retrieves a link to the cat image by cat image id
 - **GET /v1/favourites**: an endpoint that retrieves a link between an image and a user
 - **GET /v1/favourites/:favourite_id**: an endpoint that retrieves a link between an image and a user by favorite id
 - **POST /v1/favourites**: an endpoint that allows to create a link between an image and a user
 - **DELETE /v1/favourites/:favourite_id**: an endpoint that delets a link between an image and a user by favorite id

## Libraries Used

- `requests`: For making HTTP requests.
- `pytest`: For writing and running tests.
- `assertpy`: For making assertions in tests.
- `cerberus`: For validating API response schemas.
- `pytest-html`: For creattion an html-report for the test run results
 
## Features

- **API Client**: The set of clients for making API requests for different groups of endpoints
- **Logging**: Logging of API requests and responses, start and end of the tests
- **Schema Validation**: Validation of API responses using Cerberus.
- **HTML Reporting**: generation html report for test results
- **Fixtures**: using fixture for providing authorization, test data creation, and test data clean up
- **Test parametrization**: using parametrization to avoid tests duplication
- **Test dependency**: to set the correct relation between tests and how they are depended on each other

## Prerequisites

- Python 3.13 or higher
- Pipenv for managing dependencies

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/YulRud/thecats_api_tests.git
    cd thecats_api_tests
    ```

2. **Set up and run virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install pipenv**:
    ```bash
    pipenv install
    ```

5. **Activate the pip environment**:
    ```bash
    pipenv shell
    ```

6. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Project Structure

The project structure is organized as follows:

```
thecats_api_tests/
├── assertion/                      # Package containing additional possible assertions used in tests
├── client/                         # Package containing API client implementations
├── factory/                        # Package containing modules for test object generations
├── fixtures/                       # Package containing fixtures, that can be used through the project
├── reports/                        # Package where HTML report for test run is generated (the latest report is there)
├── tests/                          # Package containing all test cases
├── utils/                          # Package containing utility modules (logger, constants, parameters, other utils)
├── requirements.txt                # File listing project dependencies
├── README.md                       # Project README file
├── pytest.ini                      # Pytest configuration file
├── config.py                       # A file with authorization settings. 
└── test.log                        # A file with logs for the project. The latest sample of logs is left there  

NOTE: if API_KEY stops working, that means it has exceeded it's free requests limits. Please, generate your own api key here https://thecatapi.com/signup and use it in the running tests
```

## Running the Tests

To run the tests, use the following command:
```bash
python -m pytest
```
NOTE: all settings for test run are hidden in **pytest.ini**. A generated test report will be saved in reports/ directrory