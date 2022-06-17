from django.db import connection
cursor = connection.cursor()
cursor.execute("alter table Advertisement DROP column image")