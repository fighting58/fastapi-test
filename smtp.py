""" Send email """
import smtplib
import db
import random
from cryptography.fernet import Fernet


def send_new_password(email: str, message: str) -> dict:
    """ send email"""
    admin = db.get_admin()
    if admin:
        admin_email, admin_username, admin_password, admin_key = admin.values()
    user = db.get_user_by_email(email)
    print(f"To: {user['email']}")
    if not user:
        return {'message': f'{email}(user) not found'}
    if not admin:
        return {'message': 'No admin account'}

    sender_email = admin_email
    decrypt_password = Fernet(admin_key.encode()).decrypt(admin_password).decode()
    sender_password = decrypt_password

    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender_email, 'rrnmlsnrnhajqqvy')
            smtp.sendmail(sender_email, user['email'], message)
            smtp.quit()
    except Exception as e:
        return {"message": f"Error sending email \n{e}"}

    return {'message': f'send email to {email}'}


if __name__=='__main__':
    print(send_new_password('fighting58a@gmail.com', "Subject:Test mail\n\nit's a test message"))
