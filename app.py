from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import api
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)
app.register_blueprint(api, url_prefix='/api')

@app.route("/")
def home():
    return "Hello, world!"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 to make the app accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)