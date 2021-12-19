# backend-service-django

## Summary 

#### I tried to solve this task, however I am not sure if answers are 100% correct :) Let me address 'tasks' from readme:

1. Make sure that for the /users endpoint, that only users for the calling user's company are shown.
- Achieved that by adding additional `filter` to `get_queryset` method in `UsersViewSet`.
2. Update the reports action in UsersViewSet to return all reports down the reporting tree, recursively.
- Created function which searches for all reports down the tree of reports and returns list of pks so that we can filter `Users` out later.
4. Add another action, similar to reports, called managers, that does the inverse of reports. It should return all users up the reporting tree from the designated user.
- Same as above. Only one struggle was that I didn't know if user from which we start should be returned in response or not. I decided 'not', because we want only reports/managers.
6. Add a filter for the /users endpoint that returns only users that have at least 1 report.
7. Add an inverse to #4 and include a filter to return all users without any reports.
- Those both I achieved by adding `BooleanFilter` to `UsersFilterSet`, so when `with_reports=True` is added to the `users/?` endpoint it will respond with adequate answer. Same with `with_reports=False`. 
- 
9. Add tests. A mysite/directory/tests/tests.py file is configured for you. Add tests there. To run the tests, open a second shell and use the docker-compose exec directory bash command to enter the running container. Then run the tests with ./manage.py test -v 2.
- Added tests for some 400 responses, and scenarios from above points. 


## Follow-up questions from task:

### Provide a few bullet points of optimizations or improvements you would make if given more time.
If given more time I would like to add:
- Separated script to run tests more convinently
- Factory to create Users and Companies for testing purposes 
- Script to populate db executable easier 
- And I would like to think (and check some Django related stuff) if maybe functions to find recursively reports and managers shoudn't be moved to some `service` section. 

### Any cool feature ideas that you could add as well with minimal effort?
- Separated endpoint for Company to check various things like - employees, headcount, maybe even some cool statistics like % of man and woman in the company (if we collect such data), also how many people joined the comapny. 
- Regarding users we can also check number of reports per managers (to optimise it later) which manager have highest cout of not_active users (maybe some problems there). 
