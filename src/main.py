from flask import Flask

app = Flask("Hey")

@app.route('/')
def home():
    return "Bienvenue sur l'API Flask !"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

