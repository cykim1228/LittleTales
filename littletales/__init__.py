from flask import Flask

def create_app() :
    app = Flask(__name__, static_folder='images')

    # 주소를 분기하여 앱에 등록.
    from .views import main_views
    app.register_blueprint(main_views.bp)

    from .views import chat_views
    app.register_blueprint(chat_views.bp)

    from .views import face_views
    app.register_blueprint(face_views.bp)

    from .views import read_views
    app.register_blueprint(read_views.bp)

    return app