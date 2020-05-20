from flask import render_template
from app.main import bp
import app


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html', config=app.app.config)
