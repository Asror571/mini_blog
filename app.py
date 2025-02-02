from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"

# JSON faylni yuklash
def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# JSON faylga yozish
def save_posts(posts):
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=4)

# Bosh sahifa (barcha postlar + qidiruv)
@app.route("/", methods=["GET", "POST"])
def index():
    posts = load_posts()
    query = request.args.get("q", "")
    if query:
        posts = [post for post in posts if query.lower() in post["title"].lower()]
    return render_template("index.html", posts=posts, query=query)

# Yangi post qo‘shish
@app.route("/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        posts = load_posts()
        new_post = {
            "id": len(posts) + 1,
            "title": title,
            "content": content,
            "created_at": created_at
        }
        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))
    
    return render_template("add.html")

# Blog tafsilotlarini ko‘rish
@app.route("/blogs/<int:post_id>")
def blog_detail(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return "Post topilmadi", 404
    return render_template("detail.html", post=post)

# Blogni o‘chirish
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    posts = load_posts()
    posts = [p for p in posts if p["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
