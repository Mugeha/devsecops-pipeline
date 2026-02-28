"""
Sample Vulnerable Web Application
Used to test the DevSecOps security pipeline
"""

from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret
SECRET_KEY = "super_secret_key_12345"
API_KEY = "sk-1234567890abcdef"

# VULNERABILITY 2: SQL Injection
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('users.db')
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor = conn.execute(query)
    user = cursor.fetchone()
    conn.close()
    return str(user)

# VULNERABILITY 3: XSS
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Vulnerable to XSS
    template = f"""
    <html>
        <body>
            <h1>Search Results for: {query}</h1>
        </body>
    </html>
    """
    return render_template_string(template)

# VULNERABILITY 4: Path Traversal
@app.route('/file/<path:filename>')
def get_file(filename):
    # Vulnerable to path traversal
    file_path = os.path.join('/var/data/', filename)
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except:
        return "File not found"

# VULNERABILITY 5: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    # Vulnerable to command injection
    result = os.popen(f'ping -c 1 {host}').read()
    return result

# VULNERABILITY 6: Insecure deserialization
@app.route('/load')
def load_data():
    import pickle
    data = request.args.get('data', '')
    # Vulnerable to insecure deserialization
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

# VULNERABILITY 7: Information disclosure
@app.route('/debug')
def debug():
    # Exposes sensitive information
    return {
        'secret_key': SECRET_KEY,
        'api_key': API_KEY,
        'env_vars': dict(os.environ)
    }

if __name__ == '__main__':
    # VULNERABILITY 8: Debug mode in production
    app.run(debug=True, host='0.0.0.0')