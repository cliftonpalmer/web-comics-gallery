from flask import Flask, render_template
import os
import re

app = Flask(__name__)
gallery_root = "/app/gallery"
get_num_regex = re.compile(r'\d+')

### helper functions ###

def get_page_number_from_name(name):
    try:
        return int(get_num_regex.findall(name)[-1])
    except IndexError:
        print ("Index error on name " + name, flush=True)
        return -1

def get_file_text(filename):
    file_text = None
    try:
        with open(filename, 'r') as file:
            file_text = file.read()
    except:
        print("File not found:" + filename)
    return file_text

### routes ###

@app.route('/')
def render_gallery():
    gallery_names = []
    with os.scandir(gallery_root) as galleries:
        for gallery in galleries:
            if not gallery.is_file():
                gallery_names.append(gallery.name)
    gallery_names.sort()
    return render_template( 'gallery.html',
        title="My Comics",
        galleries=gallery_names
        )

@app.route('/<gallery>')
def render_pages(gallery=None):
    gallery_dir = gallery_root + "/" + gallery

    # get list of available pages in gallery
    template_pages = []
    with os.scandir(gallery_dir) as pages:
        for page in pages:
            if page.is_file() and page.name.endswith('.png') or page.name.endswith('.jpg'):
                template_pages.append({
                    'name': page.name, 
                    'number': get_page_number_from_name(page.name)
                    })
    template_pages = sorted(template_pages, key=lambda page: page['number'])

    # get header for gallery (if available)
    header_html = get_file_text(gallery_dir + "/header.html")

    # render!
    return render_template( 'pages.html',
        title=gallery,
        gallery=gallery,
        header=header_html,
        pages=template_pages
        )

@app.route('/<gallery>/<int:page_num>')
def render_page(gallery=None, page_num=None):

    # find a page that I think corrosponds to this page number
    page_name = None
    with os.scandir(gallery_root + "/" + gallery) as pages:
        for page in pages:
            if page.is_file():
                num = get_page_number_from_name(page.name)
                if int(page_num) == int(num):
                    page_name = page.name
                    break

    # if found, create src link to that page
    if page_name:
        src = '/images/{}/{}'.format( gallery, page_name )
        prev_page_url = "/{}/{}".format( gallery, page_num - 1)
        next_page_url = "/{}/{}".format( gallery, page_num + 1)

        return render_template( 'page.html',
            gallery=gallery, page_num=page_num,
            title='{} {}'.format(gallery, page_num), src=src, alt=page_name,
            prev_page_url=prev_page_url,
            next_page_url=next_page_url )
    else:
        return 'No page found'
