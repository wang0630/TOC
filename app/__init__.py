from flask import Flask

# The way the application is created in the single-file version is very convenient 
# but it has one big drawback.
# Because the application is created in the global scope 
# there is no way to apply configuration changes dynamically
# by the time the script is running,
# the application instance has already been created
# application facatory
def create_app():
    # create the real app
    app=Flask(__name__)
    # import main blueprint
    from .main import main as mainBlueprint
    # register blueprint to the app
    app.register_blueprint(mainBlueprint)
    # attach route and error handler here
    return app