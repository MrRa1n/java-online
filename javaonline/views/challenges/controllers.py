from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from flask_login import login_required, current_user

from javaonline.db.base import Session

import base64, os, uuid
from shutil import copy2
from javaonline.models.create_challenge_form import CreateChallengeForm
from javaonline.models.code import Code
from javaonline.models.resource import Resource
from javaonline.models.challenge import Challenge
from javaonline.utils.code_compiler import execute_java, compile_java

session = Session()

challenges_bp = Blueprint('challenges', __name__, template_folder='templates')

@challenges_bp.route('/challenges', methods=['GET', 'POST'])
@login_required
def index():
    challenges = session.query(Challenge).all()

    return render_template('challenges.html', challenges=challenges)

@challenges_bp.route('/challenges/<int:challenge>', methods=['GET', 'POST'])
@login_required
def challenge(challenge):
    c = session.query(Challenge).join(Code).join(Resource).filter(Challenge.challenge_id==challenge).first()
    split_folders = c.code[0].code_url.split('/')
    folder = split_folders[len(split_folders)-2]

    if request.method == 'GET':
        code = read_challenge_template(c.code[0].code_url)
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        tests = read_challenge_template(c.code[1].code_url)
        encoded_tests = base64.b64encode(tests.encode('utf-8')).decode('utf-8')

        return render_template('challenge.html', challenge=c, code=encoded_code, tests=encoded_tests)

    elif request.method == 'POST':
        decoded_code = base64.b64decode(request.form['code']).decode('utf-8')
        output = user_attempt(current_user.username, decoded_code, folder)
        return jsonify(output.decode('utf-8'))

    else:
        return redirect(url_for('challenges.index'))

def user_attempt(user, code, folder_name):
    challenge_dir = os.getcwd() + '/code/' + folder_name + '/solutions/' + user

    if not os.path.exists(challenge_dir):
        os.mkdir(challenge_dir, 0o755)

    code_file_name = 'Challenge.java'
    code_file_path = challenge_dir + '/' + code_file_name

    test_file_name = 'ChallengeTest.java'
    test_file_path = challenge_dir + '/' + test_file_name

    copy2(os.getcwd() + '/code/' + folder_name + '/ChallengeTest.java', challenge_dir)

    f_code = open(code_file_path, 'w+')
    f_code.write(code)
    f_code.close()

    compile_java(test_file_path)

    return execute_java(test_file_path)

@challenges_bp.route('/challenges/create', methods=['GET', 'POST'])
@login_required
def create_challenge():
    form = CreateChallengeForm()

    if request.method == 'GET':
        code = read_challenge_template(os.getcwd() + '/code/Challenge.java')
        tests = read_challenge_template(os.getcwd() + '/code/ChallengeTest.java')
        form.code.data = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        form.tests.data = base64.b64encode(tests.encode('utf-8')).decode('utf-8')

    if request.method == 'POST':
        title = form.title.data
        instructions = form.instructions.data

        decoded_code = base64.b64decode(form.code.data).decode('utf-8')
        decoded_test = base64.b64decode(form.tests.data).decode('utf-8')

        code_url, test_url = create_challenge_file(decoded_code, decoded_test)

        resource = form.resources.data

        challenge = Challenge(title=title, instructions=instructions)

        code = Code(url=code_url, type='template', challenge=challenge)
        test = Code(url=test_url, type='test', challenge=challenge)
        resource = Resource(url=resource, challenge=challenge)

        session.add(challenge)
        session.add(code)
        session.add(test)
        session.add(resource)

        session.commit()
        session.close()
        return redirect(url_for('challenges.index'))

    return render_template('create_challenge.html', form=form)

def create_challenge_file(code, test):
    challenge_dir = os.getcwd() + '/code/' + str(uuid.uuid4())
    os.mkdir(challenge_dir, 0o755)

    os.mkdir(challenge_dir + '/solutions', 0o755)

    code_file_name = 'Challenge.java'
    test_file_name = 'ChallengeTest.java'

    code_file_path = challenge_dir + '/' + code_file_name
    test_file_path = challenge_dir + '/' + test_file_name

    f_code = open(code_file_path, 'w+')
    f_code.write(code)
    f_code.close()

    f_test = open(test_file_path, 'w+')
    f_test.write(test)
    f_test.close()

    return code_file_path, test_file_path

def read_challenge_template(path):
    f = open(path, 'r')
    contents = f.read()
    f.close()

    return contents

