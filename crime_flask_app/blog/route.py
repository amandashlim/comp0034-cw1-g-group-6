from flask import Blueprint
import sqlite3
from flask import Flask, render_template

blog_bp = Blueprint('blog', __name__)


def get_db_blog_connection():
    conn = sqlite3.connect('database_blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@blog_bp.route('/blog')
def b():
    conn = get_db_blog_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('blog.html', posts=posts,title="Blog")