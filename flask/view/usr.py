# -*- coding:utf-8 -*-
from flask import Flask, render_template, Blueprint, request
import json
import flask
import ast
import requests
import base64
import MySQLdb
import os
from datetime import datetime
from jsms import Jsms
import hashlib

usr = Blueprint('usr', __name__)


@usr.route("/get_feedback", methods=["POST", "GET"])
def get_feedback():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        data = request.get_json(silent=True)
        sql = "INSERT INTO feedback(nickname,address,content,createtime,status) VALUES('{}','{}','{}','{}','{}')".format(
            data['nickname'], data['address'], data['detail'], now, "unread")
    else:
        nickname = request.args.get('nickname')
        address = request.args.get('address')
        detail = request.args.get('detail')
        sql = "INSERT INTO feedback(nickname,address,content,createtime,status) VALUES('{}','{}','{}','{}','{}')".format(
            nickname, address, detail, now, "unread")

    print(sql)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back = {"code": 1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back = {"code": 0}
        db.close()
        return json.dumps(back)


@usr.route("/get_addbookInfo", methods=["POST", "GET"])
def get_addbookInfo():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        data = request.get_json(silent=True)
        sql = "INSERT INTO addbookinfo(nickname,name,author,time,content,createtime,status) VALUES('{}','{}','{}','{}','{}','{}','{}')".format(
            data['nickname'], data['name'], data['author'], data['time'], data['detail'], now, "unread")
    else:
        address = request.args.get('address')
        author = request.args.get('author')
        time = request.args.get('time')
        detail = request.args.get('detail')
        sql = "INSERT INTO addbookinfo(nickname,name,author,time,content,createtime,status) VALUES('{}','{}','{}','{}','{}','{}','{}')".format(
            nickname, name, author, time, detail, now, "unread")

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back = {"code": 1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back = {"code": 0}
        db.close()
        return json.dumps(back)


@usr.route("/is_nickname_exist", methods=["POST", "GET"])
def is_nickname_exist():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        sql = "select * from usr_info where nickname ='{}'".format(data['nickname'])
    else:
        nickname = request.args.get('nickname')
        sql = "select * from usr_info where nickname ='{}'".format(nickname)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    db.close()
    if (len(results) == 0):  # 不存在同名
        back = {"code": 1}
        return json.dumps(back)
    elif (len(results) == 1):  # 存在同名
        back = {"code": 0}
        return json.dumps(back)
    else:  # 出错
        back = {"code": -1}
        return json.dumps(back)


@usr.route("/is_phone_exist", methods=["POST", "GET"])
def is_phone_exist():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        sql = "select * from usr_info where phone_num ='{}'".format(data['phone_num'])
    else:
        phone_num = request.args.get('phone_num')
        sql = "select * from usr_info where phone_num ='{}'".format(phone_num)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    db.close()
    if (len(results) == 0):  # 不存在该手机号
        back = {"code": 1}
        return json.dumps(back)
    elif (len(results) == 1):  # 存在该手机号
        back = {"code": 0}
        return json.dumps(back)
    else:  # 出错
        back = {"code": -1}
        return json.dumps(back)


@usr.route("/register", methods=["POST", "GET"])
def register():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
        # 创建md5对象
        m = hashlib.md5()

        b = data['password'].encode(encoding='utf-8')
        m.update(b)
        password_md5 = m.hexdigest()
        sql = "INSERT INTO usr_info(phone_num,nickname,password,avatar,registertime) VALUES('{}','{}','{}','{}')".format(
            data['phone_num'], data['nickname'], password_md5, 'zchsakura.top/static/avatar/default.jpg', now)
    else:
        phone_num = request.args.get('phone_num')
        nickname = request.args.get('nickname')
        password = request.args.get('password')
        # 创建md5对象
        m = hashlib.md5()

        b = password.encode(encoding='utf-8')
        m.update(b)
        password_md5 = m.hexdigest()
        sql = "INSERT INTO usr_info(phone_num,nickname,password,avatar,registertime) VALUES('{}','{}','{}','{}')".format(
            phone_num, nickname, password_md5, 'zchsakura.top/static/avatar/default.jpg', now)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back = {"code": 1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back = {"code": 0}
        db.close()
        return json.dumps(back)


@usr.route("/login", methods=["POST", "GET"])
def login():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
        phone_num = data['phone_num']
        password = data['password']
    else:
        phone_num = request.args.get('phone_num')
        password = request.args.get('password')

    # 创建md5对象
    m = hashlib.md5()

    # Tips
    # 此处必须encode
    # 若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
    # 因为python3里默认的str是unicode
    # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
    b = password.encode(encoding='utf-8')
    m.update(b)
    password_md5 = m.hexdigest()

    print(password_md5)

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)
    cursor.execute(sql)  # 执行SQL语句
    result = cursor.fetchone()  # 获取记录
    if result:
        if password_md5 == result[2]:
            back = {"code": 1}
            db.close()
            return json.dumps(back)
        else:
            back = {"code": 0}
            db.close()
            return json.dumps(back)
    else:
        back = {"code": 0}
        db.close()
        return json.dumps(back)


@usr.route("/upload_avatar", methods=["POST"])
def upload_avatar():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    phone_num = request.values.get('phone_num')
    print(phone_num)

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取记录
    result = cursor.fetchall()
    if len(result) == 0:  # 不存在该手机号
        back = {"code": -1}
        db.close()
        return json.dumps(back)
    else:
        file = request.files['file']
        print(file)
        print(file.filename)
        file.filename = phone_num + '.jpg'
        save_dir = "/var/www/static/avatar/"
        sql_dir = "zchsakura.top/static/avatar/"
        url = save_dir + file.filename
        sql_url = sql_dir + file.filename
        if os.path.exists(url):
            os.remove(url)
        file.save(url)
        sql = "UPDATE usr_info SET avatar = '{}' WHERE phone_num = '{}'".format(sql_url, phone_num)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            back = {"code": 1}
            db.close()
            return json.dumps(back)
        except:
            # Rollback in case there is any error
            db.rollback()
            back = {"code": 0}
            db.close()
            return json.dumps(back)


@usr.route("/upload_avatar_web", methods=["POST", "GET"])
def upload_avatar_web():
    phone_num = request.values.get('phone_num')
    print(phone_num)
    file = request.files['file']
    print(file.filename)
    return "0"
    # phone_num = data['phone_num']
    # file = data['file']
    # image = base64.b64decode(file)
    # print(image)
    # with open('1.txt', 'wb') as f:
    #    f.write(image)

    # save_dir="/www/wwwroot/www.chineseculture.xyz/avatar/"
    # url=save_dir+file['name']
    # if(os.path.exists(url)):
    #    os.remove(url)
    # file.save(url)
    back = {"code": 0}
    return json.dumps(back)


@usr.route("/upload_email", methods=["POST", "GET"])
def upload_email():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
        email = data['email']
    else:
        phone_num = flask.request.args.get('phone_num')
        email = flask.request.args.get('email')

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取记录
    result = cursor.fetchall()
    if (len(result) == 0):  # 不存在该手机号
        back = {"code": -1}
        db.close()
        return json.dumps(back)
    else:
        sql = "UPDATE usr_info SET email = '{}' WHERE phone_num = '{}'".format(email, phone_num)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            back = {"code": 1}
            db.close()
            return json.dumps(back)
        except:
            # Rollback in case there is any error
            db.rollback()
            back = {"code": 0}
            db.close()
            return json.dumps(back)


@usr.route("/upload_nickname", methods=["POST", "GET"])
def upload_nickname():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
        nickname = data['nickname']
    else:
        phone_num = flask.request.args.get('phone_num')
        nickname = flask.request.args.get('nickname')

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取记录
    result = cursor.fetchall()
    if (len(result) == 0):  # 不存在该手机号
        back = {"code": -1}
        db.close()
        return json.dumps(back)
    else:
        sql = "UPDATE usr_info SET nickname = '{}' WHERE phone_num = '{}'".format(nickname, phone_num)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            back = {"code": 1}
            db.close()
            return json.dumps(back)
        except:
            # Rollback in case there is any error
            db.rollback()
            back = {"code": 0}
            db.close()
            return json.dumps(back)


@usr.route("/upload_signature", methods=["POST", "GET"])
def upload_signature():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
        signature = data['signature']
    else:
        phone_num = flask.request.args.get('phone_num')
        signature = flask.request.args.get('signature')

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取记录
    result = cursor.fetchall()
    if (len(result) == 0):  # 不存在该手机号
        back = {"code": -1}
        db.close()
        return json.dumps(back)
    else:
        sql = "UPDATE usr_info SET signature = '{}' WHERE phone_num = '{}'".format(signature, phone_num)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            back = {"code": 1}
            db.close()
            return json.dumps(back)
        except:
            # Rollback in case there is any error
            db.rollback()
            back = {"code": 0}
            db.close()
            return json.dumps(back)


@usr.route("/upload_gender", methods=["POST", "GET"])
def upload_gender():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
        gender = data['gender']
    else:
        phone_num = flask.request.args.get('phone_num')
        gender = flask.request.args.get('gender')

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取记录
    result = cursor.fetchall()
    if (len(result) == 0):  # 不存在该手机号
        back = {"code": -1}
        db.close()
        return json.dumps(back)
    else:
        sql = "UPDATE usr_info SET gender = '{}' WHERE phone_num = '{}'".format(gender, phone_num)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            back = {"code": 1}
            db.close()
            return json.dumps(back)
        except:
            # Rollback in case there is any error
            db.rollback()
            back = {"code": 0}
            db.close()
            return json.dumps(back)


@usr.route("/upload_area", methods=["POST", "GET"])
def upload_area():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
        area = data['area']
    else:
        phone_num = flask.request.args.get('phone_num')
        area = flask.request.args.get('area')

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)

    # 执行SQL语句
    cursor.execute(sql)
    # 获取记录
    result = cursor.fetchall()
    if (len(result) == 0):  # 不存在该手机号
        back = {"code": -1}
        db.close()
        return json.dumps(back)
    else:
        sql = "UPDATE usr_info SET area = '{}' WHERE phone_num = '{}'".format(area, phone_num)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            back = {"code": 1}
            db.close()
            return json.dumps(back)
        except:
            # Rollback in case there is any error
            db.rollback()
            back = {"code": 0}
            db.close()
            return json.dumps(back)


@usr.route("/get_usr_info", methods=["POST", "GET"])
def get_usr_info():
    usr_info = []
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
    else:
        phone_num = request.args.get('phone_num')

    sql = "select * from usr_info where phone_num ='{}'".format(phone_num)
    cursor.execute(sql)  # 执行SQL语句
    result = cursor.fetchone()  # 获取记录
    data_item = {
        "nickname": result[1],
        "email": result[3],
        "signature": result[4],
        "avatar": result[5],
        "gender": result[6],
        "birthday": result[7],
        "area": result[8]
    }
    usr_info.append(data_item)
    db.close()
    return json.dumps(usr_info)


@usr.route("/is_collect", methods=["POST", "GET"])
def is_collect():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        book_type = data['type']
        bookid = data['bookid']
        nickname = data['nickname']
    else:
        book_type = request.args.get('type')
        bookid = request.args.get('bookid')
        nickname = request.args.get('nickname')

    # book_type = "ancient_book"
    # bookid = 569
    # nickname = "周日天就是个不锈钢憨"

    if book_type == "recommendation":  # 如果是推荐文章
        sql = "select * from collect_recommendation where recommendation_id ={} and nickname = '{}'".format(bookid,
                                                                                                            nickname)
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取记录
        db.close()
        if len(results) == 1:
            back = {"code": 1}
            return json.dumps(back)
        elif len(results) == 0:
            back = {"code": 0}
            return json.dumps(back)
        else:
            back = {"code": -1}
            return json.dumps(back)

    else:  # 不是推荐文章
        sql = "select * from collect where bookid ={} and nickname = '{}' and book_type = '{}'".format(bookid, nickname,
                                                                                                       book_type)
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取记录
        db.close()
        if len(results) == 1:
            back = {"code": 1}
            return json.dumps(back)
        elif len(results) == 0:
            back = {"code": 0}
            return json.dumps(back)
        else:
            back = {"code": -1}
            return json.dumps(back)


@usr.route("/change_collect", methods=["POST", "GET"])
def change_collect():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        operate = data['operate']
        book_type = data['type']
        nickname = data['nickname']
        bookid = data['bookid']
    else:
        operate = request.args.get('operate')
        book_type = request.args.get('type')
        nickname = request.args.get('nickname')
        bookid = request.args.get('bookid')

    if book_type == "recommendation":  # 是推荐文章
        if operate == "add":
            sql = "insert into collect_recommendation (nickname,recommendation_id) values ('{}',{})".format(nickname,
                                                                                                            bookid)
        elif operate == "delete":
            sql = "delete from collect_recommendation where nickname = '{}' and recommendation_id = {}".format(nickname,
                                                                                                               bookid)
    else:  # 不是推荐文章
        if operate == "add":
            sql = "insert into collect (nickname,bookid,book_type) values ('{}',{},'{}')".format(nickname, bookid,
                                                                                                 book_type)
        elif operate == "delete":
            sql = "delete from collect where nickname = '{}' and bookid = {}".format(nickname, bookid)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        back = {"code": 1}
        return json.dumps(back)
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        back = {"code": 0}
        return json.dumps(back)


@usr.route("/insert_in_comment", methods=["POST", "GET"])
def insert_in_comment():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
        recommendation_id = data['recommendation_id']
        content = data['content']

    else:
        nickname = request.args.get('nickname')
        recommendation_id = request.args.get('recommendation_id')
        content = request.args.get('content')

    # nickname = "zch"
    # recommendation_id=3
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # content="测试"

    sql = "insert into in_comment (nickname,recommendation_id,content,createtime) values ('{}',{},'{}','{}')".format(
        nickname, recommendation_id, content, now)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        back = {"code": 1}
        return json.dumps(back)
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        back = {"code": 0}
        return json.dumps(back)


@usr.route("/get_usr_out_post", methods=["POST", "GET"])
def get_usr_out_post():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    usr_out_post = []

    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
    else:
        nickname = request.args.get('nickname')

    sql = "select * from out_post where nickname ='{}'".format(nickname)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    for row in results:
        data_item = {
            "id": row[0],
            "nickname": row[1],
            "title": row[2],
            "content": row[3],
            "createtime": row[4],
        }

        if len(data_item["content"]) > 20:
            data_item["content"] = data_item["content"][0:20] + "..."

        usr_out_post.append(data_item)
    db.close()
    return json.dumps(usr_out_post)


@usr.route("/get_collect_recommendation", methods=["POST", "GET"])
def get_collect_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    collect_recommendation = []

    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
    else:
        nickname = request.args.get('nickname')

    # nickname="zch"

    sql = "select recommendation_id from collect_recommendation where nickname ='{}' order by id desc".format(nickname)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    print(results)
    for row in results:
        sql = "select * from recommendation where id ={}".format(row[0])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取所有记录列表
        data_item = {
            "id": result[0],
            "title": result[1],
            "author": result[2],
            "date": result[3],
            "content": result[4],
            "picture": result[6]
        }

        collect_recommendation.append(data_item)

    db.close()

    numofdata = len(collect_recommendation)
    back = {"code": 1, "num": numofdata, "data": collect_recommendation}

    return json.dumps(back)


@usr.route("/get_collect_works", methods=["POST", "GET"])
def get_collect_works():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    collect_works = []

    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
        book_type = data['book_type']
    else:
        nickname = request.args.get('nickname')
        book_type = request.args.get('book_type')

    # nickname="周日神"
    # book_type="recommendation"

    sql = "select bookid from collect where nickname ='{}' and book_type = '{}' order by id desc".format(nickname,
                                                                                                         book_type)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    print(results)
    for row in results:
        sql = "select * from all_book where id ={}".format(row[0])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取所有记录列表
        data_item = {
            "id": result[0],
            "name": result[2],
            "author": result[4],
            "dynasty": result[6],
            "intro": result[8],
            "content": result[11]
        }
        if data_item["content"] != None:
            data_item["content"] = ast.literal_eval(data_item["content"])
            data_item["content"] = data_item["content"][0]

        if data_item["intro"] != None:
            if len(data_item["intro"]) > 20:
                data_item["intro"] = data_item["intro"][0:20] + "..."

        collect_works.append(data_item)

    db.close()

    numofdata = len(collect_works)
    back = {"code": 1, "num": numofdata, "data": collect_works}

    return json.dumps(back)


@usr.route("/insert_history", methods=["POST", "GET"])
def insert_history():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        book_type = data['book_type']
        nickname = data['nickname']
        bookid = data['bookid']
    else:
        book_type = request.args.get('book_type')
        nickname = request.args.get('nickname')
        bookid = request.args.get('bookid')

    if book_type == "recommendation":  # 是推荐文章
        sql = "select * from history_recommendation where nickname ='{}' and recommendation_id = '{}'".format(nickname,
                                                                                                              bookid)
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        if len(results) == 1:
            sql = "update history_recommendation set time=time+1 where nickname = '{}' and recommendation_id = '{}'".format(
                nickname, bookid)
        elif len(results) == 0:
            sql = "insert into history_recommendation (nickname,recommendation_id) values ('{}',{})".format(nickname,
                                                                                                            bookid)
        else:
            db.close()
            back = {"code": -1}
            return json.dumps(back)
    else:  # 不是推荐文章
        sql = "select * from history where nickname ='{}' and bookid = '{}' and book_type = '{}'".format(nickname,
                                                                                                         bookid,
                                                                                                         book_type)
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        if len(results) == 1:
            sql = "update history set time=time+1 where nickname = '{}' and bookid = '{}' and book_type = '{}'".format(
                nickname, bookid, book_type)
        elif len(results) == 0:
            sql = "insert into history (nickname,bookid,book_type) values ('{}',{},'{}')".format(nickname, bookid,
                                                                                                 book_type)
        else:
            db.close()
            back = {"code": -1}
            return json.dumps(back)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        back = {"code": 1}
        return json.dumps(back)
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        back = {"code": 0}
        return json.dumps(back)


@usr.route("/get_history_recommendation", methods=["POST", "GET"])
def get_history_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    history_recommendation = []

    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
    else:
        nickname = request.args.get('nickname')

    # nickname="zch"

    sql = "select recommendation_id from history_recommendation where nickname ='{}' order by id desc".format(nickname)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    print(results)
    for row in results:
        sql = "select * from recommendation where id ={}".format(row[0])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取所有记录列表
        data_item = {
            "id": result[0],
            "title": result[1],
            "author": result[2],
            "date": result[3],
            "content": result[4],
            "picture": result[6]
        }

        history_recommendation.append(data_item)

    db.close()

    numofdata = len(history_recommendation)
    back = {"code": 1, "num": numofdata, "data": history_recommendation}

    return json.dumps(back)


@usr.route("/get_history_works", methods=["POST", "GET"])
def get_history_works():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    history_works = []

    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
        book_type = data['book_type']
    else:
        nickname = request.args.get('nickname')
        book_type = request.args.get('book_type')

    # nickname="周日神"
    # book_type="recommendation"

    sql = "select bookid from history where nickname ='{}' and book_type = '{}' order by id desc".format(nickname,
                                                                                                         book_type)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    print(results)
    for row in results:
        sql = "select * from all_book where id ={}".format(row[0])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取所有记录列表
        data_item = {
            "id": result[0],
            "name": result[2],
            "author": result[4],
            "dynasty": result[6],
            "intro": result[8],
            "content": result[11]
        }
        if data_item["content"] != None:
            data_item["content"] = ast.literal_eval(data_item["content"])
            data_item["content"] = data_item["content"][0]

        if data_item["intro"] != None:
            if len(data_item["intro"]) > 20:
                data_item["intro"] = data_item["intro"][0:20] + "..."

        history_works.append(data_item)

    db.close()

    numofdata = len(history_works)
    back = {"code": 1, "num": numofdata, "data": history_works}

    return json.dumps(back)


# 发送手机验证码
@usr.route("/phone_captcha_send", methods=["POST", "GET"])
def phone_captcha_send():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
    else:
        phone_num = request.args.get('phone_num')

    jc = Jsms('d2de292b23920b34894495cf', '1d4bedff14f151384f57aa2b')

    # 一波发送验证码操作
    result = jc.send_code(phone_num, '1')
    print(result)
    msgId = result['msg_id']

    sql = "INSERT INTO sendCaptcha (`phone`, `msgId`) VALUES (%s, %s)"
    try:
        # 执行SQL语句
        cursor.execute(sql, [phone_num, msgId])
        # 提交修改
        db.commit()
        back = {"code": 1}
    except:
        # 发生错误时回滚
        db.rollback()
        back = {"code": 0}

    db.close()
    return json.dumps(back)


# 验证手机验证码
@usr.route("/phone_captcha_verify", methods=["POST", "GET"])
def phone_captcha_verify():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phone_num']
        captcha = data['captcha']
    else:
        phone_num = request.args.get('phone_num')
        captcha = request.args.get('captcha')

    sql = "SELECT `id`,`msgId` FROM sendCaptcha WHERE phone = %s ORDER BY `id` DESC LIMIT 1"
    cursor.execute(sql, [phone_num])
    msgId = cursor.fetchone()['msgId']  # 获取记录
    db.close()

    jc = Jsms('d2de292b23920b34894495cf', '1d4bedff14f151384f57aa2b')

    # 一波发送验证验证码操作
    resp = jc.verify_code(msgId, captcha)
    print(resp)
    result = resp['is_valid']

    if result is True:
        back = {"code": 1}
    else:
        back = {"code": 0}

    return json.dumps(back)
