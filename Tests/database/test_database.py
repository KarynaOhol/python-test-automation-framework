import pytest
import allure
import pyodbc
import psycopg2
import os
import yaml


def load_test_config():
    """Load test configuration data."""
    # config_path = os.path.join(os.path.dirname(__file__), 'config_SQL_tests.yaml')
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Configs', 'config_SQL_tests.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Get smoke tests for parametrization
def get_smoke_tests():
    config = load_test_config()
    return [
        test for test in config['tests']
        if test.get('test_type') == 'smoke'
    ]

def get_critical_tests():
    config = load_test_config()
    return [
        test for test in config['tests']
        if test.get('test_type') == 'critical'
    ]


class TestDatabaseFramework:
    """Database testing framework with smoke and critical path tests."""

    @allure.feature("Database Tests")
    @allure.story("Smoke Tests")
    @pytest.mark.smoke
    @pytest.mark.parametrize("test_config", get_smoke_tests(), ids=lambda test: test['name'])
    def test_smoke_tests(self, db_cursor, test_config):
        """Execute smoke tests for database objects existence."""
        with allure.step(f"Executing smoke test: {test_config['name']}"):
            allure.dynamic.title(test_config['name'])
            allure.dynamic.description(test_config.get('description', 'No description provided'))

            self._execute_sql_test(db_cursor, test_config)

    @allure.feature("Database Tests")
    @allure.story("Critical Path Tests")
    @pytest.mark.critical
    @pytest.mark.parametrize("test_config", get_critical_tests(), ids=lambda test: test['name'])
    def test_critical_path_tests(self, db_cursor, test_config):
        """Execute critical path tests for business logic validation."""
        with allure.step(f"Executing critical test: {test_config['name']}"):
            allure.dynamic.title(test_config['name'])
            allure.dynamic.description(test_config.get('description', 'No description provided'))

            self._execute_sql_test(db_cursor, test_config)

    def _execute_sql_test(self, db_cursor, test_config):
        """Execute SQL test and validate results."""
        sql_query = test_config['sql']

        with allure.step(f"Executing SQL query"):
            allure.attach(sql_query, name="SQL Query", attachment_type=allure.attachment_type.TEXT)

            try:
                db_cursor.execute(sql_query)
                result = db_cursor.fetchone()
                actual_value = result[0] if result else None

                allure.attach(str(actual_value), name="Query Result", attachment_type=allure.attachment_type.TEXT)

            except (pyodbc.Error, psycopg2.Error) as e:
                allure.attach(str(e), name="Database Error", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Database error occurred: {e}")

        with allure.step("Validating test results"):
            self._validate_result(actual_value, test_config)

    def _validate_result(self, actual_value, test_config):
        """Validate the test result against expected values."""
        test_name = test_config['name']

        # Handle different validation types
        if 'expected' in test_config:
            expected_value = test_config['expected']
            allure.attach(
                f"Expected: {expected_value}, Actual: {actual_value}",
                name="Comparison",
                attachment_type=allure.attachment_type.TEXT
            )

            assert actual_value == expected_value, \
                f"Test '{test_name}' failed: Expected {expected_value}, but got {actual_value}"

        elif 'expected_min' in test_config:
            expected_min = test_config['expected_min']
            allure.attach(
                f"Expected minimum: {expected_min}, Actual: {actual_value}",
                name="Comparison",
                attachment_type=allure.attachment_type.TEXT
            )

            assert actual_value >= expected_min, \
                f"Test '{test_name}' failed: Expected minimum {expected_min}, but got {actual_value}"

        elif 'expected_max' in test_config:
            expected_max = test_config['expected_max']
            allure.attach(
                f"Expected maximum: {expected_max}, Actual: {actual_value}",
                name="Comparison",
                attachment_type=allure.attachment_type.TEXT
            )

            assert actual_value <= expected_max, \
                f"Test '{test_name}' failed: Expected maximum {expected_max}, but got {actual_value}"

        else:
            pytest.fail(f"No validation criteria defined for test '{test_name}'")
