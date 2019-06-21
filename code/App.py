from flask import Flask, render_template, request, session, redirect, url_for
from log2file import Log
from dbcodes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this is secret key'

def initApp():
    session['dbManager'] = DBManager('onlineOJ', 'ComPro32API', 'localhost', 'root')
    session['LOGINED'] = False


@app.route('/login', methods=["GET", "POST"])
def login():
    Log("进入login界面")

    if request.method == 'POST':
        Log("recieved POST")
        Log("session['LOGINED']:%s" % session.get('LOGINED'))
        if session['LOGINED'] == False:
            username = request.form['username']
            psd = request.form['password']
            Log("user logined\nusename:%s\npassword:%s" % (username, psd))
            dbmanager = session['dbManager']
            dbmanager.m_useTable('Customers')
            if not dbmanager.m_itemExists(['username, psd'], 'username="%s" AND psd="%s"' % (username, psd)):
                Log("登录失败")
                return render_template('login.html', loginfailed=False)
            else:
                Log("登录成功")
                session['LOGINED'] = True
                return redirect(url_for('homepage'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    Log("进入注册页面")
    global reged
    reged = False
    if request.method == 'POST':
        username = request.form['username']
        psd = request.form['psd']
        dbmanager = session['dbManager']
        dbmanager.m_useTable('Customers')
        if not dbmanager.m_itemExists(['username, psd'], 'username="%s" AND psd="%s"' % (username, psd)):
            dbmanager.m_insertItem([username, psd, 'NONE', 0, 0, 0])
            Log("注册了新用户username:%s, psd:%s" % (username, psd))
            redirect(url_for('homepage'))
        else:
            Log("这个用户已经存在username:%s, psd:%s" % (username, psd))
            reged = True
    return render_template('signup.html', reged=reged)


@app.route('/', methods=['GET'])
def homepage():
    Log("进入主页")
    return render_template('homepage.html')


if __name__ == '__main__':
    initApp()
    app.run(debug=True)
