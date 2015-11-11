This project is a small application which has one page that takes a number n
in range 1-100. The service will return:
- a value calculated from the difference of the square of the sum of all
natural numbers 1-n and the sum of the squares of all numbers 1-n
- the number of times this number has been input to the system
- the time of request

1. Setup

From your virtualenv, install packages via pip:

- pip install -r requirements.txt

Next, open config.py and put your postgresql user's username and password
in Config.PG_USER and Config.PG_PASSWORD respectively.

Then, to create the database and the testing database, and insert our model
into the database (note this would go in a dedicated script in a larger
structured project)

- python models.py

2. Running the application

To start, simply run

- python run.py

Then for a number n between 1 and 100, navigate on your browser to
localhost:8000/difference?number=[n goes here].  Other numbers, non-numbers,
and blank values will return an error message and code.

3. Testing

nosetests :)

Be sure you haven't dropped the testing database.

4. Next steps for project

- A frontend.  I was looking to build a simple AngularJS UI which would display
the value upon inputting a number, but did not have the time

- Find a better database session, closer to ZopeTransactionManager.  My only
view uses db.session.commit(), which is something that can cause conflict if
an external function also tries to commit, and can be forgotten.  Depending on setup,
it could cause a problem with the test database, if anything besides basic
tables (triggers, functions, views) are needed for the test database to run
correctly (current setup implies they are not)

A decorator could be a solution, but needs to be sure it doesn't commit bad data.

- Structured directories.  I'm new to flask and couldn't quite figure out how
to structure the files outside of a flat directory and make the imports work
correctly
