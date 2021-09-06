#more configuration variables:
#https://flask-sqlalchemy.palletsprojects.com/en/2.x/config
#https://flask.palletsprojects.com/en/1.1.x/config/


class Config(object):
    """
    common configuration
    """
    #put any configurations here that are common across all enviornments
    SECRET_KEY='admin@123'

    # SQLAlCHEMY_DATABASE_URI='<USE_DATABASE>://<USERNAME>:<PASSWORD>@<IP>/<DATABASE_NAME>'
    SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/student_info'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True

class ProductionConfig(Config):
    DEBUG=False

app_config={
    'development':DevelopmentConfig,
    'production':ProductionConfig
}

