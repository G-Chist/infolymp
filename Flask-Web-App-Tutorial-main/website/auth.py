from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from random import randint
import smtplib

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Вход выполнен успешно!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль, попробуйте ещё раз.', category='error')
        else:
            flash('Адрес не существует.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

code = 0
first_name = ''
password1 = ''
email = ''
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    global code, first_name, email, password1
    if request.method == 'POST':
        try:
            if (request.form['emailcodebutton'] == "Получить код"):
                email = request.form.get('email')
                first_name = request.form.get('firstName')
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')

                user = User.query.filter_by(email=email).first()
                if user:
                    flash('Адрес уже зарегистрирован.', category='error')
                elif len(email) < 4:
                    flash('Адрес должен быть длиннее 3 символов.', category='error')
                elif len(first_name) < 2:
                    flash('ФИО должно быть длиннее 1 символа.', category='error')
                elif len(first_name) > 50:
                    flash('ФИО должно быть короче 50 символов.', category='error')
                elif len(first_name.split()) < 3:
                    flash('Введите фамилию, имя и отчество через пробел', category='error')
                elif password1 != password2:
                    flash('Пароли не совпадают.', category='error')
                elif len(password1) < 7:
                    flash('Пароль должен быть не короче 7 символов.', category='error')
                else:
                    flash('На вашу почту выслан код от itbraincorporated@gmail.com. Введите его в поле ниже и нажмите кнопку регистрации.', category='success')
                    sender = "itbraincorporated@gmail.com"
                    password = "PASSWORD"
                    receiver = email
                    code = str(randint(100001, 999999)).encode("utf-8")
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender, password)
                    server.sendmail(sender, receiver, code)
        except:
            pass

        try:
            if (request.form['regbutton'] == "Зарегистрироваться"):
                mailcode = request.form.get('mailcode', "")
                if mailcode.encode("utf-8") == code:
                    new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    flash('Аккаунт создан!', category='success')
                    return redirect(url_for('views.home'))
                else:
                    flash('Код не совпадает с отправленным на почту', category='error')
        except Exception as error:
            pass

    return render_template("sign_up.html", user=current_user)
