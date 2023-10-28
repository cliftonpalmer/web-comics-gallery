from flask import Flask, render_template
import os
import re

app = Flask(__name__)
gallery_root = "/app/gallery"
get_num_regex = re.compile(r'\d+')

@app.route('/')
def render_gallery():
    gallery_names = []
    with os.scandir(gallery_root) as galleries:
        for gallery in galleries:
            if not gallery.is_file():
                gallery_names.append(gallery.name)
    gallery_names.sort()
    return render_template( 'gallery.html', galleries=gallery_names )

@app.route('/<gallery>')
def render_pages(gallery=None):
    page_names = []
    with os.scandir(gallery_root + "/" + gallery) as pages:
        for page in pages:
            if page.is_file() and page.name.endswith('.png') or page.name.endswith('.jpg'):
                page_names.append(page.name)
    page_names.sort()
    return render_template( 'pages.html', gallery=gallery, pages=page_names )

@app.route('/<gallery>/<page>')
def render_page(gallery=None, page=None):
    src = '/images/{}/{}'.format( gallery, page )

    page_num = int(get_num_regex.findall(page)[-1])
    page_num_str = str(page_num).rjust(3, '0')
    next_page_num_str = str(page_num + 1).rjust(3, '0')
    prev_page_num_str = str(page_num - 1).rjust(3, '0')

    prev_page_url = '/{}/{}'.format(gallery, page.replace(page_num_str, prev_page_num_str) )
    next_page_url = '/{}/{}'.format(gallery, page.replace(page_num_str, next_page_num_str) )

    return render_template( 'page.html',
        gallery=gallery, page=page, page_num=page_num,
        title=page, src=src, alt=page,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url )
