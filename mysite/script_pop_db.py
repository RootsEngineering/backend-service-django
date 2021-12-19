from django.db import connection

from directory.models import User, Company

def script_populating_db():
    cursor = connection.cursor()

    cursor.execute("delete from directory_user")
    cursor.execute("delete from directory_company")

    company = Company.objects.create(id =1, name="Test Company")
    User.objects.create_user(id=1, username='a1', first_name='a', last_name='a', reports_to_id=None, company=company)
    User.objects.create_user(id=2, username='b1', first_name='b', last_name='b', reports_to_id=1, company=company)
    User.objects.create_user(id=3, username='c1', first_name='c', last_name='c', reports_to_id=2, company=company)
    User.objects.create_user(id=4, username='d1', first_name='d', last_name='d', reports_to_id=3, company=company)
    User.objects.create_user(id=5, username='e1', first_name='e', last_name='e', reports_to_id=3, company=company)
    User.objects.create_user(id=6, username='f1', first_name='f', last_name='f', reports_to_id=5, company=company)


    company2 = Company.objects.create(id =2, name="Test Company2")
    User.objects.create_user(id=7, username='a2', first_name='a', last_name='a', reports_to_id=None, company=company2)
    User.objects.create_user(id=8,username='b2', first_name='b', last_name='b', reports_to_id=7, company=company2)
    User.objects.create_user(id=9,username='c2', first_name='c', last_name='c', reports_to_id=8, company=company2)
    User.objects.create_user(id=10,username='d2', first_name='d', last_name='d', reports_to_id=9, company=company2)
    User.objects.create_user(id=11,username='e2', first_name='e', last_name='e', reports_to_id=7, company=company2)
    User.objects.create_user(id=12,username='f2', first_name='f', last_name='f', reports_to_id=9, company=company2)
