from flask import Flask

from os.path import dirname, join
from . import user, db


app = Flask(__name__)

app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI="sqlite:///" +
    join(dirname(dirname(__file__)), "database.sqlite"),
)

db.init_app(app)

app.register_blueprint(user.bp)




# @ app.before_request
# def before_request():
#     """
#     Load a user object into `g.user` before each request.
#     """
#     if auth.oidc.user_loggedin:
#         g.user = auth.okta_client.get_user(auth.oidc.user_getfield("sub"))
#     else:
#         g.user = None


# class CustomJSONEncoder(JSONEncoder):
#     "Add support for serializing timedeltas"

#     def default(o):
#         if type(o) == datetime.timedelta:
#             return str(o)
#         elif type(o) == datetime.datetime:
#             return o.isoformat()
#         else:
#             return super().default(o)


# app.json_encoder = CustomJSONEncoder

# @app.errorhandler(404)
# def page_not_found(e):
#     """Render a 404 page."""
#     return render_template("404.html"), 404


# @app.errorhandler(403)
# def insufficient_permissions(e):
#     """Render a 403 page."""
#     return render_template("403.html"), 403
