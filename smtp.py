import smtplib
import db
import random
import base64

admin = db.get_admin()
if admin:
   admin_email, admin_username, admin_password = admin.values()

def send_new_password(email: str, massage: str) -> dict:
    user = db.get_user_by_email(email)
    if not user:
        return {'message': f'{email}(user) not found'}
    if not admin:
        return {'message': f'No admin account'}

    sender_email = admin_email
    decoded_password = base64.b64decode(admin_password)
    sender_password = decoded_password.decode('utf-8')

    try:
        with smtplib.SMTP('smtp.gamil.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.sendemail(sender_email, user['email'], message)
    except Exception as e:
        return {"message": "Error sending email"}
    
    return {'message': f'send email to {email}'}
