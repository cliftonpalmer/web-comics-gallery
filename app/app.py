from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def render_gallery():
    items = ['LittleWilly', 'foo', 'bar']
    return render_template( 'gallery.html', gallery_items=items )
