import os
from flask import Flask, send_from_directory, redirect, render_template
from jinja2.exceptions import TemplateNotFound

PROJECT_ROOT = os.path.dirname(__file__)
WWW_ROOT = os.path.join(PROJECT_ROOT, 'www')
STATIC_ROOT = os.path.join(WWW_ROOT, 'static')

app = Flask(__name__, static_folder=STATIC_ROOT, template_folder=WWW_ROOT)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_ROOT, 'favicon.ico', mimetype='image/png')

@app.route('/robots.txt')
def robots():
    return send_from_directory(WWW_ROOT, 'robots.txt', mimetype='text/plain')

@app.route('/<path:filename>')
def serve_html(filename):

	if filename[-1] == "/":
		filename = "%sindex.html" % filename

	try:
		return render_template(filename)
	except TemplateNotFound, e:
		"""
		Because this is a simple static site we're going to raise a 404 
		if a template is not found. We still pass along the exception for 
		analysis.
		"""
		return page_not_found(e)

@app.route('/')
def serve_index():
	return serve_html("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return serve_html('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return serve_html('500.html'), 500

"""
Example of a redirect if ever needed.

@app.route('/some-old-page.html')
#def serve_soon():
     return redirect('http://www.SOME_NEW_PAGE.com', 301)
"""

if __name__ == "__main__":
	app.run()

