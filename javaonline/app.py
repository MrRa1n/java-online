from . import *

from javaonline.configurer import read_config, configure_logger

from javaonline.views.home.controllers import home_bp
from javaonline.views.login.controllers import login_bp
from javaonline.views.challenges.controllers import challenges_bp
from javaonline.views.register.controllers import register_bp

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(challenges_bp)
app.register_blueprint(register_bp)

read_config(app)
configure_logger(app)