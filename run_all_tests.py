#!/usr/bin/env python3
"""
Script to run all tests (API, Database, UI) and generate a single Allure report.
"""

import subprocess
import os
import shutil
import sys
from pathlib import Path


def run_command(command, description):

    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'=' * 60}")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print("Output:", result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {description}:")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def clean_previous_results():

    directories_to_clean = [
        'allure-results',
        'allure-report'
    ]

    print(" Cleaning previous test results...")
    for directory in directories_to_clean:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"   Removed: {directory}")


def check_test_files():

    test_files = [
        'Tests/api/api_task.py',
        'Tests/database/test_database.py',
        'Tests/ui/login.py'
    ]

    missing_files = []
    existing_files = []

    for test_file in test_files:
        if os.path.exists(test_file):
            existing_files.append(test_file)
            print(f" Found: {test_file}")
        else:
            missing_files.append(test_file)
            print(f"Missing: {test_file}")

    return existing_files, missing_files


def main():

    print("Test Framework - DB, API, UI Tests Runner")
    print("=" * 60)

    # Clean previous results
    clean_previous_results()

    # Check test files
    print("\n Checking test files...")
    existing_files, missing_files = check_test_files()

    if missing_files:
        print(f"\n Warning: {len(missing_files)} test file(s) not found:")
        for file in missing_files:
            print(f"   - {file}")
        print("   Continuing with available test files...")

    if not existing_files:
        print(" No test files found! Please check your test file locations.")
        sys.exit(1)

    # Run all tests
    print(f"\n Running all available tests ({len(existing_files)} files)...")

    # Build pytest command to run all test files
    pytest_command = [
        'pytest',
        '--alluredir=allure-results',
        '-v',
        '--tb=short',
        '--continue-on-collection-errors'
    ]

    # Add existing test files to command
    pytest_command.extend(existing_files)

    test_success = run_command(
        pytest_command,
        f"All Tests ({', '.join([Path(f).stem for f in existing_files])})"
    )

    # Generate Allure report
    print("\n Generating Allure report...")
    report_success = run_command([
        'allure', 'generate',
        'allure-results',
        '--clean',
        '--single-file',
        '-o', 'allure-report'
    ], "Generate Allure Report")

    # Summary
    print(f"\n{'=' * 60}")
    print(" TEST EXECUTION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Test files found: {len(existing_files)}")
    print(f"Test files missing: {len(missing_files)}")

    if existing_files:
        print("Executed tests:")
        for file in existing_files:
            print(f"  ✓ {file}")

    if missing_files:
        print("Skipped tests (files not found):")
        for file in missing_files:
            print(f"   {file}")

    if test_success:
        print(f"\n Tests executed successfully!")
    else:
        print(f"\n⚠ Tests completed with some issues (check details above)")

    if report_success:
        report_path = os.path.abspath('allure-report/index.html')
        print(f"\n📊 Allure report generated:")
        print(f"   File: {report_path}")
        print(f"   URL:  file://{report_path}")

    print(f"\n{'=' * 60}")
    print(" Test execution completed!")
    print(f"{'=' * 60}")

    if not test_success and not any(existing_files):
        sys.exit(1)


if __name__ == "__main__":
    main()