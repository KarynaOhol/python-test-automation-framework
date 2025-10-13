import pytest
import yaml
import pyodbc
import psycopg2
from contextlib import contextmanager
import os
import subprocess
import allure



def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical path test"
    )
    if config.getoption("--generate-allure"):
        config._allure_generate = True


# def pytest_sessionfinish(session, exitstatus):
#     """Generate allure report after test session finishes."""
#     if hasattr(session.config, '_allure_generate') and session.config._allure_generate:
#         allure_results_dir = session.config.getoption('--alluredir')
#         if allure_results_dir and os.path.exists(allure_results_dir):
#             report_dir = os.path.join(os.getcwd(), 'allure-report')
#             subprocess.run([
#                 'allure', 'generate', allure_results_dir,
#                 '--clean', '--single-file', '-o', report_dir
#             ], check=False)
#             print(f"Allure report generated in: {report_dir}")


@pytest.fixture(scope="session")
def config():
    """Load configuration from YAML file."""
    config_path = os.path.join(os.path.dirname(__file__), 'config_SQL_tests.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="session")
def db_config():
    """Database connection configuration."""
    return {
        'postgres': {
            'host': 'localhost',
            'database': 'dwh_hw_db',
            'user': 'postgres',
            'password': 'admin',
            'port': '5432'
        }
    }

@contextmanager
def connect_to_postgres(db_config):
    """Context manager for PostgreSQL connection."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port']
        )
        yield conn.cursor()
    finally:
        if conn:
            conn.close()


@pytest.fixture(scope="function")
def db_cursor(db_config):
    """Fixture to provide database cursor with automatic cleanup."""
    db_type = os.environ.get('DB_TYPE', 'postgres')

    if db_type == 'postgres':
        with connect_to_postgres(db_config['postgres']) as cursor:
            yield cursor
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--generate-allure",
        action="store_true",
        default=False,
        help="Generate allure report after test run"
    )

