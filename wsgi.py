"""Web Server Gateway Interface"""

##################
# FOR PRODUCTION
####################
from src.app import app

if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(host='127.0.0.1', debug=True)

