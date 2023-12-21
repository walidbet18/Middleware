from flask import Flask

# Créer une instance de l'application Flask
app = Flask(__name__)

# Route par défaut
@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    # Démarrer l'application sur localhost, port 5000
    app.run(debug=True)
