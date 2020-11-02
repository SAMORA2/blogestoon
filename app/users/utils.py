import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from app import app, mail



def save_img(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_filename = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_filename)
    out_putsize = (160, 180)
    i = Image.open(form_picture)
    i.thumbnail(out_putsize)
    i.save(pic_path)
    return pic_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('درخواست بازنشانی پسورد',
                  sender='blogestoon@gmail.com',
                  recipients=[user.email])
    msg.body = f""":برای بازنشانی پسورد روی لینک زیر کلیک کنید 😀
    {url_for('users.reset_token',token=token,_external=True)}

   اگر فرآیند بازنشانی پسورد را دنبال نکنید چیزی تغییر نمی کند
    """
    mail.send(msg)
