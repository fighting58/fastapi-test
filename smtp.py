""" Send email """
import smtplib
import db
from cryptography.fernet import Fernet

def send_email(email: str, message: str) -> dict:
    """ send email"""
    admin = db.get_admin()
    if admin:
        admin_email, _, admin_password, admin_key = admin.values()
    else:
        return {'message': 'No admin account'}

    sender_email = admin_email
    decrypt_password = Fernet(admin_key.encode()).decrypt(admin_password).decode()
    sender_password = decrypt_password

    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=15) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, email, message)
            smtp.quit()
    except Exception as e:
        return {"message": f"Error sending email \n{e}"}

    return {'message': f'send email to {email}'}
