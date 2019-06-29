from flask import Flask, render_template, request, session, redirect, url_for
from log2file import Log
from dbcodes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is secret key'


dbmanager = DBManager('onlineOJ', 'ComPro32API', '127.0.0.1', 'root')


@app.route('/login', methods=["GET", "POST"])
def login():
    Log("进入login界面")

    if request.method == 'POST':
        Log("recieved POST")
        Log("session['LOGINED']:%s" % session.get('LOGINED'))
        if not session.get('LOGINED'):
            username = request.form['username']
            psd = request.form['password']
            Log("用户登入了,\nusename:%s\npassword:%s" % (username, psd))
            dbmanager.m_useTable('Customers')
            if not dbmanager.m_itemExists(['username, psd'], 'username="%s" AND psd="%s"' % (username, psd)):
                Log("登录失败")
                return render_template('login.html', loginfailed=False)
            else:
                Log("登录成功")
                session['LOGINED'] = True
                return redirect(url_for('questions'))

    return render_template('login.html')


@app.route('/questions', methods=["GET"])
def questions():
    return render_template("QuestionBank.html")


@app.route('/competition', methods=["GET"])
def competition():
    return render_template("Competition.html")


@app.route('/release', methods=["GET"])
def release():
    return render_template("Release.html")



@app.route('/signup', methods=["GET", "POST"])
def signup():
    Log("进入signup界面")
    dbmanager.logOn()
    if request.method == 'POST':
        username = request.form['username']
        psd = request.form['password']
        Log("用户注册, username:%s,password:%s" % (username, psd))
        dbmanager.m_useTable("Customers")
        if dbmanager.m_itemExists(['username', 'psd'], 'username="%s" AND psd="%s"' % (username, psd)):
            Log("用户存在，报错")
            return render_template('signup.html', signuped=False)
        Log("用户不存在，创建")
        dbmanager.m_insertItem([username, psd, 'NONE', 0, 0, 0])
        session['LOGINED'] = True
        return redirect(url_for('questions'))

    return render_template('signup.html')


@app.route('/', methods=['GET'])
def homepage():
    Log("进入主页")
    if not session.get('LOGINED'):
        session['LOGINED'] = False
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
