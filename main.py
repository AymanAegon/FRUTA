from create_app import create_app
from flask import render_template

# creating the flask app
app = create_app()

# to handle the page not found error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=False)