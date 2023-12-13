from flask import Flask
from flaskext.mysql import MySQL
import config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '19082010069_MariskaReginaRahmaPutri'
    app.config['MYSQL_DATABASE_HOST'] = config.DATABASE_CONFIG['host']
    app.config['MYSQL_DATABASE_USER'] = config.DATABASE_CONFIG['user']
    app.config['MYSQL_DATABASE_PASSWORD'] = config.DATABASE_CONFIG['password']
    app.config['MYSQL_DATABASE_DB'] = config.DATABASE_CONFIG['database']
    mysql.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app