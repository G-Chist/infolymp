from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Note, Note2
from . import db
import json
import math
import random
import time

note = ""

def discr(a, b, c): pass
def evendigits(a): pass

def z1(a, b, c):
    res = int(math.pow(b, 2) - 4 * a * c)
    with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt", "a") as file1:
        file1.write(str(res) + "\n")

def z2(a):
    res = 0
    while a > 0:
        if a % 10 % 2 == 0:
            res += a % 10
        a //= 10
    with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt", "a") as file1:
        file1.write(str(res) + "\n")

def logicsolve(a):
    ldict = {
        "&": " and ",
        "|": " or ",
        "+": " or ",
        "v": " or ",
        "*": " and ",
        "^": " and ",
        "=": " == ",
        "-": " not "
    }
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    a = ''.join(i for i in a if i != " ")
    if a[-2::] == "=0" or a[-2::] == "=1":
        a = "(" + a[:-2:] + ")=" + a[-1::]
    else:
        a = "(" + a + ")=1"
    vars = 0
    used = ""
    vararr = []
    table = []
    for i in a:
        if i in alphabet and i not in used:
            vars += 1
            used += i
            vararr.append(i)
    for i in range(1, vars):
        q = int(2 ** (vars - i))
        group = "0" * q + "1" * q
        table.append(group * int((int(2 ** vars) / len(group))))
    table.append("01" * int((int(2 ** vars) / 2)))
    answers = []
    for k in range(2 ** vars):
            b = a
            for letter in vararr:
                row = vararr.index(letter)
                b = b.replace(letter, table[row][k])
            for key in ldict.keys():
                b = b.replace(key, str(ldict[key]))
            b = b.replace("not  ==", "!=")
            b = b.replace("==  not", "!=")
            if eval(b):
                answers.append(''.join(i[k] for i in table))
    count = len(answers)
    return (answers, count)

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/results', methods=['GET', 'POST'])
@login_required
def results():

    message1 = ""
    message2 = ""

    try:
        with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/submit/submitted.txt", "r") as file:
            logins = file.read().split('\n')

        for i in logins:
            if i != "" and i[-1] == "1":
                message1 += i[:-2:] + ": "
                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/submit/" + str(i) + ".txt", "r") as file:
                    m1 = file.read().split('\n')
                    for i in range(len(m1)):
                        if m1[i] == "":
                            m1.pop(i)
                    message1 = message1 + max(m1, key = lambda x: int(x)) + "\n"
        message1 = list(set(message1.split('\n')))
        for i in range(len(message1)):
            if message1[i] == '\n':
                message1.pop(i)
        message1 = '\n'.join(message1)

        for i in logins:
            if i != "" and i[-1] == "2":
                message2 += i[:-2:] + ": "
                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/submit/" + str(i) + ".txt", "r") as file:
                    m2 = file.read().split('\n')
                    for i in range(len(m2)):
                        if m2[i] == "":
                            m2.pop(i)
                    message2 = message2 + max(m2, key = lambda x: int(x)) + "\n"
        message2 = list(set(message2.split('\n')))
        for i in range(len(message2)):
            if message2[i] == '\n':
                message2.pop(i)
        message2 = '\n'.join(message2)

    except FileNotFoundError:
        pass

    return render_template("results.html", user=current_user, message1=message1, message2=message2)

@views.route('/task1', methods=['GET', 'POST'])
@login_required
def task1():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Программа слишком короткая!', category='error')
        if ("file" in note) or ("eval" in note) or ("exec" in note) or ("import" in note):
            flash('В программе были использованы запрещённые команды!', category='error')
        else:
            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt', 'w').close()
            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'w').close()
            counter = 0
            st = time.time()
            rterror = False

            for i in range(50):
                if time.time() - st < 6:
                    a = random.randint(0, 1000)
                    b = random.randint(0, 100)
                    c = random.randint(0, 1000)
                    exec(note + """\nwith open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'a') as file2:\n   file2.write(str(discr(a, b, c)) + "\\n")""")
                    z1(a, b, c)
                else:
                    rterror = True
                    break

            for i in range(50):
                if time.time() - st < 6:
                    a = random.randint(-1000, 0)
                    b = random.randint(-100, 0)
                    c = random.randint(-1000, 0)
                    exec(note + """\nwith open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'a') as file2:\n   file2.write(str(discr(a, b, c)) + "\\n")""")
                    z1(a, b, c)
                else:
                    rterror = True
                    break

            if not rterror:
                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt", "r") as file1:
                    lines1 = file1.read().split('\n')

                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt", "r") as file2:
                    lines2 = file2.read().split('\n')

                for i in range(50):
                    if lines1[i] == lines2[i]:
                        counter += 1

                for i in range(50, 100):
                    if lines1[i] == lines2[i]:
                        counter += 1

                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/submit/" + str(current_user.first_name) + "_1.txt", "a+") as file:
                    file.write(str(counter)  + "\n")
                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/submit/submitted.txt", "a+") as file:
                    file.write(str(current_user.first_name) + '_1' + "\n")

            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt', 'w').close()
            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'w').close()

            note = counter

            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Решение добавлено!', category='success')

    return render_template("task1.html", user=current_user)

@views.route('/task2', methods=['GET', 'POST'])
@login_required
def task2():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Программа слишком короткая!', category='error')
        if ("file" in note) or ("eval" in note) or ("exec" in note) or ("import" in note):
            flash('В программе были использованы запрещённые команды!', category='error')
        else:
            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt', 'w').close()
            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'w').close()
            counter = 0
            st = time.time()
            rterror = False

            for i in range(50):
                if time.time() - st < 6:
                    a = random.randint(0, 10000)
                    exec(note + """\nwith open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'a') as file2:\n   file2.write(str(evendigits(a)) + "\\n")""")
                    z2(a)
                else:
                    rterror = True
                    break

            for i in range(50):
                if time.time() - st < 6:
                    a = random.randint(-10000, 0)
                    exec(note + """\nwith open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'a') as file2:\n   file2.write(str(evendigits(a)) + "\\n")""")
                    z2(a)
                else:
                    rterror = True
                    break

            if not rterror:
                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt", "r") as file1:
                    lines1 = file1.read().split('\n')

                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt", "r") as file2:
                    lines2 = file2.read().split('\n')

                for i in range(50):
                    if lines1[i] == lines2[i]:
                        counter += 1

                for i in range(50, 100):
                    if lines1[i] == lines2[i]:
                        counter += 1

                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/submit/" + str(current_user.first_name) + "_2.txt", "a+") as file:
                    file.write(str(counter)  + "\n")
                with open("/home/infolymp/Flask-Web-App-Tutorial-main/filedump/submit/submitted.txt", "a+") as file:
                    file.write(str(current_user.first_name) + '_2' + "\n")

            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-good.txt', 'w').close()
            open('/home/infolymp/Flask-Web-App-Tutorial-main/filedump/reserve-user.txt', 'w').close()

            note = counter
            new_note = Note2(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Решение добавлено!', category='success')

    return render_template("task2.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-note2', methods=['POST'])
def delete_note2():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note2.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/logictasks', methods=['GET', 'POST'])
def logictasks():
    count = ""
    groups = ""
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Уравнение слишком короткое!', category='error')
        else:
            try:
                count = str(logicsolve(note)[1]) + '\n'
                groups = '\n'.join(logicsolve(note)[0])
            except:
                pass
    return render_template("logictasks.html", count=count, groups=groups)
