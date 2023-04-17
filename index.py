__doc__ = """ main page """

import db
import smtp

print(db.create_user_table())
print(db.create_admin_table())

print(db.add_admin('fighting58@gmail.com', 'Kim Byoung-woo', 'rrnmlsnrnhajqqvy'))

print(db.add_user('fighting58a@gmail.com', 'K.B.W.', 'atfirst#1', 'user'))
print(db.add_user('fighting58b@gmail.com', 'Kim.B.W.', 'atfirst#1', 'user'))

print(smtp.send_new_password('fighting58a@gmail.com', "Subject:Test mail\n\nit's a test message"))