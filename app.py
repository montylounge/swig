import os, sys
from urlparse import urlparse, urlunparse
from flask import Flask, send_from_directory, request, redirect
from jinja2.exceptions import TemplateNotFound

PROJECT_ROOT = os.path.dirname(__file__)
WWW_ROOT = os.path.join(PROJECT_ROOT, 'www')
STATIC_ROOT = os.path.join(WWW_ROOT, 'static')
WWW_URL = "www.YOURWEBSITE.com"

app = Flask(__name__, static_folder=STATIC_ROOT, template_folder=WWW_ROOT)

@app.before_request
def redirect_nonwww():
    """Redirect non-www requests to www."""
    urlparts = urlparse(request.url)
    if urlparts.netloc == WWW_URL.replace("www.",""):
        urlparts_list = list(urlparts)
        urlparts_list[1] = WWW_URL
        return redirect(urlunparse(urlparts_list), code=301)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_ROOT, 'favicon.ico', mimetype='image/png')

@app.route('/robots.txt')
def robots():
    return send_from_directory(WWW_ROOT, 'robots.txt', mimetype='text/plain')

@app.route('/<path:filename>')
def serve_html(filename):
    return send_from_directory(WWW_ROOT, filename)

@app.route('/')
def serve_index():
    return send_from_directory(WWW_ROOT, 'index.html')

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory(WWW_ROOT, '404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return send_from_directory(WWW_ROOT, '500.html'), 500

"""
Example of a redirect if ever needed.

@app.route('/some-old-page.html')
#def serve_soon():
     return redirect('http://www.SOME_NEW_PAGE.com', 301)
"""

if __name__ == "__main__":
	app.run()

