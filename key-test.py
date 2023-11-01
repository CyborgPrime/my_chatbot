import os

print("FLASK_SECRET_KEY:", os.environ.get("FLASK_SECRET_KEY", "Not found"))
