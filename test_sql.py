from website.models import User, Note

users = User.query.all()

for user in users:
    print(user.email)
    print(user.first_name)
    print(user.last_name)
    print('--------------------------------')