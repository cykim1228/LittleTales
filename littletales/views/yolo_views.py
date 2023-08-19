from flask import Blueprint, render_template
from flask import url_for
from werkzeug.utils import redirect

bp = Blueprint('littleyolo', __name__, url_prefix='/littleyolo')

@bp.route('/')
def yolo_index() :

    return render_template('little_yolo.html')
