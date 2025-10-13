import allure
import requests

@allure.feature("API Testing")
@allure.story("User Posts Validation")
@allure.title("Test user with 10 posts creation")
@allure.description("Verify that 10 posts were created for user ID=3 using JSONPlaceholder API")
def test_user_with_posts(provide_posts_data):
    post_data = provide_posts_data
    user_id = post_data['test_user_id']
    expected_posts_count = post_data['expected_posts_count']
    base_url = post_data['base_url']

    with allure.step(f"Fetch posts for user ID={user_id}"):
        response = requests.get(f"{base_url}/posts?userId={user_id}")
        response.raise_for_status()
        posts_data = response.json()
    with allure.step(f"Verify posts count equals {expected_posts_count}"):
        actual_posts_count = len(posts_data)
        allure.attach(
            f"Expected: {expected_posts_count}, Actual: {actual_posts_count}",
            name="Posts Count Comparison",
            attachment_type=allure.attachment_type.TEXT
        )
        assert actual_posts_count == expected_posts_count, \
            f"Expected {expected_posts_count} posts for user {user_id}, but got {actual_posts_count}"


@allure.feature("Cloud Storage Testing")
@allure.story("Data Migration Validation")
@allure.title("Test data presence between GCP source and AWS staging")
@allure.description("Verify that data for specific date exists in both GCP source bucket and AWS staging bucket")
def test_data_is_presented_between_staging_raw(list_gcs_blobs, list_aws_blobs, provide_config):
    config = provide_config
    date_prefix = config['prefix']
    with allure.step(f"Verify GCP bucket contains data for prefix: {date_prefix}"):
        gcs_objects = list_gcs_blobs
        allure.attach(
            f"GCP Bucket: {config['gcp_bucket_name']}\nPrefix: {date_prefix}\nObjects found: {len(gcs_objects)}",
            name="GCP Bucket Info",
            attachment_type=allure.attachment_type.TEXT
        )
    assert len(gcs_objects) > 0, \
        f"No objects found in GCP bucket '{config['gcp_bucket_name']}' with prefix '{date_prefix}'"

    with allure.step(f"Verify AWS bucket contains data for prefix: {date_prefix}"):
        aws_objects = list_aws_blobs
        allure.attach(
            f"AWS Bucket: {config['aws_bucket_name']}\nPrefix: {date_prefix}\nObjects found: {len(aws_objects)}",
            name="AWS Bucket Info",
            attachment_type=allure.attachment_type.TEXT
        )
        assert len(aws_objects) > 0, \
            f"No objects found in AWS bucket '{config['aws_bucket_name']}' with prefix '{date_prefix}'"

    with allure.step("Compare data consistency between buckets"):
        # Log the first few objects from each bucket for comparison
        gcs_sample = gcs_objects[:5] if len(gcs_objects) >= 5 else gcs_objects
        aws_sample = aws_objects[:5] if len(aws_objects) >= 5 else aws_objects

        comparison_info = f"""
                GCP Objects Sample ({len(gcs_objects)} total):
                {chr(10).join(gcs_sample)}

                AWS Objects Sample ({len(aws_objects)} total):
                {chr(10).join(aws_sample)}
                """

        allure.attach(
            comparison_info,
            name="Bucket Objects Comparison",
            attachment_type=allure.attachment_type.TEXT
        )

        assert len(gcs_objects) > 0 and len(aws_objects) > 0, \
            "Both buckets should contain data for the specified date prefix"
