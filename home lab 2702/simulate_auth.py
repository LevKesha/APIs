import requests
from requests.auth import HTTPBasicAuth
import json

# Base URL of the Flask app
base_url = "http://127.0.0.1:80"

# Correct credentials for Basic Authentication
username = "admin"
password = "password123"

# Incorrect credentials for testing failure
wrong_username = "wronguser"
wrong_password = "wrongpassword"

# 1. GET all posts
def get_all_posts():
    response = requests.get(f"{base_url}/posts", auth=HTTPBasicAuth(username, password))
    print("GET /posts - Status Code:", response.status_code)
    print("Response:", response.json())

# 2. GET a post by ID
def get_post_by_id(post_id):
    response = requests.get(f"{base_url}/post/{post_id}", auth=HTTPBasicAuth(username, password))
    print(f"GET /post/{post_id} - Status Code:", response.status_code)
    print("Response:", response.json())

# 3. POST (create) a new post
def create_post():
    new_post = {
        "title": "Fourth Post",
        "content": "This is my fourth post",
        "author": "Jane Doe"
    }
    response = requests.post(f"{base_url}/posts", json=new_post, auth=HTTPBasicAuth(username, password))
    print("POST /posts - Status Code:", response.status_code)
    print("Response:", response.json())

# 4. PUT (update) an existing post
def update_post(post_id):
    updated_post = {
        "title": "Updated Post Title",
        "content": "Updated content of the post",
        "author": "Jane Doe"
    }
    response = requests.put(f"{base_url}/posts/{post_id}", json=updated_post, auth=HTTPBasicAuth(username, password))
    print(f"PUT /posts/{post_id} - Status Code:", response.status_code)
    print("Response:", response.json())

# 5. DELETE a post by ID
def delete_post(post_id):
    response = requests.delete(f"{base_url}/posts/{post_id}", auth=HTTPBasicAuth(username, password))
    print(f"DELETE /posts/{post_id} - Status Code:", response.status_code)
    print("Response:", response.json())

# Failure scenarios

# 6. GET all posts with wrong credentials (Should fail)
def get_all_posts_wrong_credentials():
    response = requests.get(f"{base_url}/posts", auth=HTTPBasicAuth(wrong_username, wrong_password))
    print("GET /posts with wrong credentials - Status Code:", response.status_code)
    print("Response:", response.json())

# 7. POST (create) a new post with wrong credentials (Should fail)
def create_post_wrong_credentials():
    new_post = {
        "title": "Failed Post",
        "content": "This post should fail",
        "author": "Jane Doe"
    }
    response = requests.post(f"{base_url}/posts", json=new_post, auth=HTTPBasicAuth(wrong_username, wrong_password))
    print("POST /posts with wrong credentials - Status Code:", response.status_code)
    print("Response:", response.json())

# 8. PUT (update) an existing post with wrong credentials (Should fail)
def update_post_wrong_credentials(post_id):
    updated_post = {
        "title": "Failed Update",
        "content": "This update should fail",
        "author": "Jane Doe"
    }
    response = requests.put(f"{base_url}/posts/{post_id}", json=updated_post, auth=HTTPBasicAuth(wrong_username, wrong_password))
    print(f"PUT /posts/{post_id} with wrong credentials - Status Code:", response.status_code)
    print("Response:", response.json())

# 9. DELETE a post with wrong credentials (Should fail)
def delete_post_wrong_credentials(post_id):
    response = requests.delete(f"{base_url}/posts/{post_id}", auth=HTTPBasicAuth(wrong_username, wrong_password))
    print(f"DELETE /posts/{post_id} with wrong credentials - Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    # Test all the actions one by one

    # Get all posts with correct credentials
    get_all_posts()

    # Get a post by ID with correct credentials
    get_post_by_id(1)

    # Create a new post with correct credentials
    create_post()

    # Update an existing post (post_id 2 in this case) with correct credentials
    update_post(2)

    # Delete a post (post_id 3 in this case) with correct credentials
    delete_post(3)

    # Get all posts again to verify deletion
    get_all_posts()

    # Failure scenarios with wrong credentials
    get_all_posts_wrong_credentials()
    create_post_wrong_credentials()
    update_post_wrong_credentials(2)
    delete_post_wrong_credentials(3)
