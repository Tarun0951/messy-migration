from flask import Flask, jsonify
from routes.user_routes import user_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return jsonify({"message": "User Management System"}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)