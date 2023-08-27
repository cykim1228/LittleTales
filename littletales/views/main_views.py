import os

from flask import Blueprint, render_template, send_from_directory
from flask import url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index() :

    return render_template('index.html')

@bp.route('/generated/<filename>')
def generated_file(filename):
    return send_from_directory(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'generated'), filename)