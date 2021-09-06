from myapp import create_app
import os
from myapp import db

config_name=os.getenv('FLASK_CONFIG','development')#Default is 'development' if Flask_config is not set
app=create_app(config_name)



if __name__=="__main__":
    with app.app_context():
      db.create_all()
    app.run(debug=True)