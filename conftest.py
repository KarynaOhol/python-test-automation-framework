import pytest

@pytest.fixture(scope='session', autouse=True)
def setup_allure_environment():
    import os

    # Create allure-results directory if it doesn't exist
    os.makedirs('allure-results', exist_ok=True)

    # Write environment properties
    with open('allure-results/environment.properties', 'w') as f:
        f.write('Test.Environment=Local\n')
        f.write('Python.Version=3.x\n')
        f.write('Test.Framework=pytest\n')
        f.write('API.Base.URL=https://jsonplaceholder.typicode.com\n')
        f.write('GCP.Bucket=gcp-public-data-nexrad-l2\n')
        f.write('AWS.Bucket=noaa-nexrad-level2\n')
