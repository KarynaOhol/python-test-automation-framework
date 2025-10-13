import allure
import boto3
import pytest
import requests
from botocore import UNSIGNED
from botocore.config import Config
from google.cloud import storage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



@pytest.fixture(scope='function')
def provide_config():
    config = {'prefix': '2024/01/01/KTLX/', 'gcp_bucket_name': "gcp-public-data-nexrad-l2",
              'aws_bucket_name': 'noaa-nexrad-level2',
              's3_anon_client': boto3.client('s3', config=Config(signature_version=UNSIGNED)),
              'gcp_storage_anon_client': storage.Client.create_anonymous_client()}
    return config


@pytest.fixture(scope='function')
def list_gcs_blobs(provide_config):
    config = provide_config
    blobs = config['gcp_storage_anon_client'].list_blobs(config['gcp_bucket_name'], prefix=config['prefix'])
    objects = [blob.name for blob in blobs]
    return objects


@pytest.fixture(scope='function')
def list_aws_blobs(provide_config):
    config = provide_config
    response = config['s3_anon_client'].list_objects(Bucket=config['aws_bucket_name'], Prefix=config['prefix'])
    objects = [content['Key'] for content in response['Contents']]
    return objects


@pytest.fixture(scope='function')
def provide_posts_data():
    base_url = "https://jsonplaceholder.typicode.com"
    try:
        response = requests.get(f"{base_url}/posts", timeout=10)
        if response.status_code != 200:
            pytest.skip(f"JSONPlaceholder API not accessible. Status code: {response.status_code}")
    except requests.RequestException as e:
        pytest.skip(f"JSONPlaceholder API not accessible: {str(e)}")

    return {
        'base_url': base_url,
        'test_user_id': 3,
        'expected_posts_count': 10
    }

@pytest.fixture(scope='function')
def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Use ChromeDriverManager for automatic driver management
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    # Cleanup
    driver.quit()

# @pytest.fixture(scope='session', autouse=True)
# def setup_allure_environment():
#     import os
#
#     # Create allure-results directory if it doesn't exist
#     os.makedirs('allure-results', exist_ok=True)
#
#     # Write environment properties
#     with open('allure-results/environment.properties', 'w') as f:
#         f.write('Test.Environment=Local\n')
#         f.write('Python.Version=3.x\n')
#         f.write('Test.Framework=pytest\n')
#         f.write('API.Base.URL=https://jsonplaceholder.typicode.com\n')
#         f.write('GCP.Bucket=gcp-public-data-nexrad-l2\n')
#         f.write('AWS.Bucket=noaa-nexrad-level2\n')

@pytest.fixture(scope='function', autouse=True)
def log_test_info(request):
    test_name = request.node.name
    allure.attach(
        f"Test: {test_name}\nModule: {request.module.__name__}",
        name="Test Information",
        attachment_type=allure.attachment_type.TEXT
    )