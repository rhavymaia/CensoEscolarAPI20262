from helpers.application import app
from helpers.api import api

api.init_app(app)


def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()
