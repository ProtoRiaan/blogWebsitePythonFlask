# Description

Welcome to my first web application. It is a basic blogging platform and is intended to showcase my IT skill set for prospective employers.

This version of the website currently uses python Flask and Jinja templates for the backend and HTML and bootstrap for the front end. The database is SQLite
but will be upgraded to PostgreSQL shortly.

This is just one iteration of my blog websites. Look for a SvelteKit, Druple and various Go based versions to come soon. 

# Deployment

Pull/Build the docker image and run with the following required environmental variables:

    FLASK_APP_KEY : The secret string for accessing your api
    FLASK_SERVER_NAME : the URI for your app
    EMAIL_USR : The username for you servers mailbox (used for sending password reset emails)
    EMAIL_PWD : The password for your servers mailbox (used for sending password reset emails)
You will need to map an external port to the container port 8000 where gunicorn serves the app. Also the application does not ship with database. You will need to init your own sqlite database!

# Contributing

Verified to work with python3.11 but not 3.12. Not sure what the oldest version of python is that works. 


Thanks for stopping by. 