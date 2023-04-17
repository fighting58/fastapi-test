__doc__ = """ main page """

import db

print(db.create_user_table())
print(db.create_admin_table())

print(db.add_admin('fighting58@gmail.com', 'Kim Byoung-woo', 'ithinkthere4i@m'))
print(db.add_user('fighting58a@gmail.com', 'K.B.W.', 'atfirst#1', 'user'))
print(db.add_user('fighting58b@gmail.com', 'Kim.B.W.', 'atfirst#1', 'user'))

