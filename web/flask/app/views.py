from flask import render_template, redirect, url_for, request

from app import app
from models_app import Package_app, Version_app
from forms import SearchForm

def get_letters():
    from modules.packages_prefixes import packages_prefixes
    return packages_prefixes

def get_path_links(package, version="", path_to=""):
    """
    returns the path hierarchy with urls, to use with 'You are here:'
    """
    pathl = []
    pathl.append((package, url_for('source', package=package)))
    if version != "":
        pathl.append((version, url_for('source', package=package,
                                       version=version)))
    if path_to != "":
        prev_path = ""
        for p in path_to.split('/'):
            pathl.append((p, url_for('source', package=package,
                                     version=version,
                                     path_to=prev_path+p)))
            prev_path += p+"/"
    return pathl

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/doc/')
def doc():
    return render_template('doc.html', url_prefix="http://example.net")

@app.route('/', methods=['POST', 'GET']) # navigation
@app.route('/nav/', methods=['POST', 'GET'])
def index():
    searchform = SearchForm()
    if searchform.validate_on_submit():
        return redirect(url_for("search",
                                packagename=searchform.packagename.data))
    return render_template('index.html',
                           searchform=searchform,
                           letters=get_letters())

#@app.route('/nav/search/', methods=['POST'])
@app.route('/nav/search/<packagename>/')
def search(packagename):
    packagename = packagename.replace('%', '').replace('_', '')
    exact_matching = Package_app.query.filter_by(name=packagename).first()
    other_results = Package_app.query.filter(
        Package_app.name.contains(packagename)).order_by(Package_app.name)
    return render_template('search.html',
                           exact_matching=exact_matching,
                           other_results=other_results)

@app.route('/nav/list/')
@app.route('/nav/list/<int:page>/')
def list(page=1):
    packages = Package_app.query.order_by(
        Package_app.name).paginate(page, 20, False)
    return render_template('list.html',
                           packages=packages)

@app.route('/nav/letter/')
@app.route('/nav/letter/<letter>')
def letter(letter='a'):
    if letter in get_letters():
        packages = Package_app.query.filter(
            Package_app.name.startswith(letter)).order_by(Package_app.name)
        return render_template("letter.html",
                               packages=packages)
    else:
        return render_template('404.html'), 404


@app.route('/src/<package>/')
@app.route('/src/<package>/<version>/')
@app.route('/src/<package>/<version>/<path:path_to>/', methods=['POST', 'GET'])
def source(package, version="", path_to=None):
    #if version == "": # we list the versions for this package
    #    return render_template("source_package.html") # todo
    
    import os
    from flask import safe_join
    if path_to is None:
        path_to = ""
    sources_path = os.path.join(app.config['SOURCES_FOLDER'],
                                package, version, path_to)
    sources_path_server = os.path.join(app.config['SOURCES_SERVER'],
                                       package, version, path_to)

    if os.path.isdir(sources_path): # we list the files in this folder
        def quickurl(f):
            if version == "":
                return url_for('source', package=package, version=f)
            elif path_to == "":
                return url_for('source', package=package,
                               version=version, path_to=f)
            else:
                return url_for('source', package=package,
                               version=version,
                               path_to=path_to+"/"+f)
        
        files = sorted((f, quickurl(f)) for f in os.listdir(sources_path)
                       if os.path.isfile(os.path.join(sources_path, f)))

        dirs = sorted((d, quickurl(d)) for d in os.listdir(sources_path)
                      if os.path.isdir(os.path.join(sources_path, d)))
        
        return render_template("source_folder.html",
                               files=files, dirs=dirs,
                               pathl=get_path_links(package, version, path_to),
                               parentfolder=(version != ""))
                                 # we want '..', except for a package file
    
    elif os.path.exists(sources_path): # it's a file, we return the source code
        def msg_strtodict(msg):
            msgsplit = msg.split(':')
            msgdict = dict()
            try:
                msgdict['position'] = int(msgsplit[0])
            except ValueError:
                msgdict['position'] = 1
            try:
                msgdict['title'] = msgsplit[1]
            except IndexError:
                msgdict['title'] = ""
            try:
                msgdict['message'] = ":".join(msgsplit[2:])
            except IndexError:
                msgdict['message'] = ""
            return msgdict

        try:
            hl = request.args.get('hl')
        except (KeyError, ValueError, TypeError):
            hl = None
        try:
            msg = request.args.get('msg')
            msg = msg_strtodict(msg)
        except (KeyError, ValueError, TypeError):
            msg = None
        
        nlines = 1
        with open(sources_path) as sfile:
            for line in sfile: nlines += 1 # counts the total number of lines
        from modules.sourcecode import SourceCodeIterator
        return render_template("source_file.html",
                               code = SourceCodeIterator(sources_path,
                                                         hl=hl),
                               nlines=nlines, msg=msg,
                               pathl=get_path_links(package, version, path_to))
    else: # 404
        return render_template('404.html'), 404
