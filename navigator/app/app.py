from flask import Flask, render_template
import os
import re

app = Flask(__name__)
gallery_root = "/app/gallery"
gallery_desc_filename = "description.html"
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

def get_page_number_from_name(name):
    try:
        return int(get_num_regex.findall(name)[-1]) 
    except IndexError:
        print ("Index error on name " + name, flush=True)
        return -1

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

    # get description for gallery (if available)
    desc_filename = gallery_dir + "/" + gallery_desc_filename
    description = None
    try:
        with open(desc_filename, 'r') as file:
            description = file.read()
    except:
        print("Description file not found at " + desc_filename)

    # render!
    return render_template( 'pages.html',
        gallery=gallery,
        description=description,
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
            title=page_name, src=src, alt=page_name,
            prev_page_url=prev_page_url,
            next_page_url=next_page_url )
    else:
        return 'No page found'
