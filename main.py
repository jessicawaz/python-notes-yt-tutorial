from website import create_app

# create_app() imported from __init__.py
app = create_app()

# run a Flask app (web server start)
if __name__ == '__main__':
    app.run(debug=True)