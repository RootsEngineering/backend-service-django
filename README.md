# backend-project-template

## Welcome
Hello! Welcome to the backend engineering task as part of your interview process with Deel as a Python/Django developer! This task should take about 1-3 hours of your time. As you're completing the tasks below, make sure you document your process including any snags you hit, trade-offs you made, or shortcuts you decided to take. Your decision-making process is equally as important as the completion of these tasks.

### Requirements
- Docker

### Set-up Instructions
This project is already fully configured to launch. You will only need to add data to the DB to get started.

Clone this repository, navigate into the root directory, and boot up using `docker-compose up directory`. This command will pull the base python image, install requirements, migrate and launch the local server.

To add some data, open another shell and connect to the running container with `docker-compose exec directory bash`. You can then navigate into the directory `cd mysite`, and launch the shell with `./manage.py shell`.

### Data & Models
The models in this app are very simple. There are only 3 you need to worry about:
1) The `User` model. This model contains basic attributes from Django, with only the addition of `Company` and `reports_to` foreign keys.
2) The `Company` model. All `User`s have a `Company`. It is a natural grouping for a Enterprise SaaS product.
3) The `Token` object (`from rest_framework.authtoken.models import Token`). This will be used for authenticating a `User` over the API.

To add some data, you can use `create_user`.
```python
>>> from directory.models import *
>>> company = Company.objects.create(name="Test Company")  # Create a new Company
>>> user = User.objects.create_user(username=..., first_name=..., last_name=..., company=company)  # Add a user to the Company.
>>> from rest_framework.authtoken.models import Token  # Import the Token model
>>> token = Token.objects.create(user=user)  # Create an API Token for this new user.
>>> print(token.key)  # Display the API key for this User.
```

You will likely need to add more data to the DB to properly implement the requirements for the tasks below. Creating a script would *probably* be useful. :wink:

### Tasks
1) Make sure that for the `/users` endpoint, that only users for the calling user's company are shown.
2) Update the `reports` action in `UsersViewSet` to return all reports _down_ the reporting tree, recursively.
3) Add another action, similar to `reports`, called `managers`, that does the inverse of `reports`. It should return all users _up_ the reporting tree from the designated user.
4) Add a [filter](https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter) for the `/users` endpoint that returns only users that have at least 1 report.
5) Add an inverse to #4 and include a filter to return all users without any reports.
6) Add tests. A `mysite/directory/tests/tests.py` file is configured for you. Add tests there. To run the tests, open a second shell and use the `docker-compose exec directory bash` command to enter the running container. Then run the tests with `./manage.py test -v 2`.

### Follow-up Questions
1) Provide a few bullet points of optimizations or improvements you would make if given more time.
2) Any cool feature ideas that you could add as well with minimal effort?


Good luck!