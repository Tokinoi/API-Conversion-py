from flask import Flask

app = Flask("Hey")

@app.route('/')
def home():
    return "Bienvenue sur l'API Flask !"


if __name__ == '__main__':
    app.run(debug=True)
