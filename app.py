from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
# from flask_pymongo import PyMongo

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=host)
db = client.get_default_database()
items = db.items
comments = db.comments
app.config["MONGO_URI"] = "mongodb://localhost:27017/Contractor"


@app.route("/")
def index():
    # home page
    return render_template("index.html", items=items.find())

@app.route('/create/item')
def create_item():
    """Create a new item."""
    item = {'title': '', 'description': '', 'price': ''}

    return render_template("new.html", item=item, title='Add item')

@app.route('/create', methods=['POST'])
def item_submit():
    """Submit a new item."""
    item = {
        'title': request.form.get('title'),
        'created_at': request.form.get('created_at'),
        'description': request.form.get('description'),
        'price': request.form.get('description'),
        'image': request.form.get('image'),

    }
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('item_show', item_id=item_id))


@app.route('/item/<item_id>')
def item_show(item_id):
    """Show a single playlist."""
    item = items.find_one({'_id': ObjectId(item_id)})
    # Add the below line:
    item_comments = comments.find({'item_id': ObjectId(item_id)})
    # Edit the return statement to be the following:
    return render_template('show.html', item=item, comments=item_comments)


@app.route('/items/<item_id>/edit')
def playlists_edit(item_id):
    """Show the edit form for a playlist."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('edit.html', item=item, title='Edit Playlist')

@app.route('/items/<item_id>', methods=['POST'])
def playlists_update(item_id):
    """Submit an edited playlist."""
  #  videos = video_url_creator(video-ids)

    updated_item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('image'),
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})
    return redirect(url_for('item_show', item_id=item_id))

@app.route('/items/<item_id>/delete', methods=['POST'])
def playlists_delete(item_id):
    """Delete one playlist."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('index'))


@app.route('/about')
def about():
    """About"""
    return render_template('about.html')

# ########## COMMENT ROUTES ##########


@app.route('/items/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'item_id': ObjectId(request.form.get('item_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('item_show', item_id=request.form.get('item_id')))

@app.route('/item/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('item_show', item_id=comment.get('item_id')))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))