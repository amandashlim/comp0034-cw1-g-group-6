from my_flask_app import create_app

app = create_app()


@app.route('/')
def index():
    return 'This is the home page for my_flask_app'
