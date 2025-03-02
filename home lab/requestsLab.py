from flask import Flask, jsonify, request
from datetime import datetime

#    -----http request ----> [{request} ]
#
#
# global list [dish, dish ] <-
app = Flask(__name__)  # flask application

posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is my first post",
        "author": "John Doe",
        "date_posted": "2025-02-28T10:00:00"
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is my second post",
        "author": "John Doe",
        "date_posted": "2025-03-01T15:00:00"
    },
    {
        "id": 3,
        "title": "Third Post",
        "content": "This is my Third post",
        "author": "John Doe",
        "date_posted": "2025-03-02T18:00:00"
    }
]
post_id_counter = 3


@app.get('/posts')
def get_posts():
    print(request.remote_addr)
    print(request.headers["User-Agent"])
    return jsonify(posts)

@app.get('/post/<id>')
def get_post_by_id(id):
    id = int(id)
    for post in posts:
        if post["id"] == id:
            return jsonify(post), 203
    return "not found", 404


@app.route('/posts', methods=['POST'])
def create_post():
    global post_id_counter

    # Get JSON data from request
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data"}), 400

    # Validate required fields
    required_fields = ['title', 'content', 'author']
    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Create new post
    new_post = {
        "id": post_id_counter,
        "title": data['title'],
        "content": data['content'],
        "author": data['author'],
        "date_posted": datetime.utcnow().isoformat()
    }
    posts.append(new_post)
    post_id_counter += 1

    return jsonify({
        "success": True,
        "message": "Post created successfully",
        "post": new_post
    }), 201


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON data"}), 400

    for post in posts:
        if post["id"] == post_id:
            post.update({
                "title": data.get("title", post["title"]),
                "content": data.get("content", post["content"]),
                "author": data.get("author", post["author"]),
            })
            return jsonify({
                "success": True,
                "message": "Post updated successfully",
                "post": post
            }), 200

    return jsonify({"success": False, "message": "Post not found"}), 404


if __name__ == '__main__':
    app.run(port=80)