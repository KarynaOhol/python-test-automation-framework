from Pages.incomeStatementsReportPage import IncomeStatementsReportPage
import pytest
import os
import yaml
import sys
from selenium import webdriver
from Pages.incomeStatementsReportPage import IncomeStatementsReportPage
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_selenium_config(config_name):
    module_dir = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
    # parent_dir = os.path.dirname(module_dir)
    parent_dir = os.path.dirname(os.path.dirname(module_dir))
    with open(os.path.join(parent_dir, 'Configs', config_name), 'r') as stream:
        config = yaml.safe_load(stream)
    return config['global']


@pytest.fixture(scope="function")
def open_income_statements_report_webpage():
    report_uri = get_selenium_config('config_selenium.yaml')['report_uri']
    delay = get_selenium_config('config_selenium.yaml')['delay']
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # service = Service(ChromeDriverManager().install())
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(report_uri)

    income_report = IncomeStatementsReportPage(driver, delay)
    # income_report.open_power_bi_report()
    yield income_report
    driver.close()