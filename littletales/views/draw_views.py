from flask import Blueprint, request, render_template

bp = Blueprint('littledraw', __name__, url_prefix='/littledraw')

@bp.route('/')
def draw_index() :

    return render_template('little_input.html')

@bp.route('/canvas', methods=['POST'])
def draw_canvas() :
    animal_name = request.form.get('animal')
    print('판별된 동물 : ', animal_name)

    return render_template('little_draw.html', animal_name=animal_name)

