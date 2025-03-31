import requests
import json

# Base URL of the Flask app
base_url = "http://127.0.0.1:80"

# 1. GET all posts
def get_all_posts():
    response = requests.get(f"{base_url}/posts")
    print("GET /posts - Status Code:", response.status_code)
    print("Response:", response.json())

# 2. GET a post by ID
def get_post_by_id(post_id):
    response = requests.get(f"{base_url}/post/{post_id}")
    print(f"GET /post/{post_id} - Status Code:", response.status_code)
    print("Response:", response.json())

# 3. POST (create) a new post
def create_post():
    new_post = {
        "title": "Fourth Post",
        "content": "This is my fourth post",
        "author": "Jane Doe"
    }
    response = requests.post(f"{base_url}/posts", json=new_post)
    print("POST /posts - Status Code:", response.status_code)
    print("Response:", response.json())

# 4. PUT (update) an existing post
def update_post(post_id):
    updated_post = {
        "title": "Updated Post Title",
        "content": "Updated content of the post",
        "author": "Jane Doe"
    }
    response = requests.put(f"{base_url}/posts/{post_id}", json=updated_post)
    print(f"PUT /posts/{post_id} - Status Code:", response.status_code)
    print("Response:", response.json())

# 5. DELETE a post by ID
def delete_post(post_id):
    response = requests.delete(f"{base_url}/posts/{post_id}")
    print(f"DELETE /posts/{post_id} - Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    # Test all the actions one by one

    # Get all posts
    get_all_posts()

    # Get a post by ID
    get_post_by_id(1)

    # Create a new post
    create_post()

    # Update an existing post (post_id 2 in this case)
    update_post(2)

    # Delete a post (post_id 3 in this case)
    delete_post(3)

    # Get all posts again to verify deletion
    get_all_posts()
