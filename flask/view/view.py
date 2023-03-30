#-*- coding:utf-8 -*-
from flask import Flask, render_template, Blueprint, request
import json
import flask
import ast
import requests
import MySQLdb
from jsms import Jsms

test = Blueprint('test', __name__)

db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')

jsms_client = Jsms('d2de292b23920b34894495cf', '1d4bedff14f151384f57aa2b')


@test.route('/send_code')
def send_code():
    rr = jsms_client.send_code('13572761631', '1')
    print(rr)
    return json.dumps('1')

@test.route('/get_search')
def get_search():
    search = []
    type = flask.request.args.get('type')
    key = flask.request.args.get('key')
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    if type == '1':     #作品名称
        sql = "select * from peotry where name like '%{}%'".format(key)
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:
            data_item = {
                #"id": row[0],
                "name": row[1],
                "author": row[2],
                "dynasty": row[3],
                #"form": row[4],
                #"style": row[5],
                "content": row[6],
                #"annotation": row[7]
                "type":"peotry"
            }
            data_item["content"]=ast.literal_eval(data_item["content"])
            #data_item["annotation"]=ast.literal_eval(data_item["annotation"])
            search.append(data_item)
    elif type == '2':    #作者
        sql = "select * from peotry where author like '%{}%'".format(key)
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:
            data_item = {
                #"id": row[0],
                "name": row[1],
                "author": row[2],
                "dynasty": row[3],
                #"form": row[4],
                #"style": row[5],
                "content": row[6],
                #"annotation": row[7]
                "type":"peotry"
            }
            data_item["content"]=ast.literal_eval(data_item["content"])
            #data_item["annotation"]=ast.literal_eval(data_item["annotation"])
            search.append(data_item)
    elif type == '3':    #朝代
        sql = "select * from peotry where dynasty like '%{}%'".format(key)
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:
            data_item = {
                #"id": row[0],
                "name": row[1],
                "author": row[2],
                "dynasty": row[3],
                #"form": row[4],
                #"style": row[5],
                "content": row[6],
                #"annotation": row[7]
                "type":"peotry"
            }
            data_item["content"]=ast.literal_eval(data_item["content"])
            #data_item["annotation"]=ast.literal_eval(data_item["annotation"])
            search.append(data_item)
    else:
        return "can not find"
        
    return json.dumps(search)


@test.route("/get_feedback",methods=["POST","GET"])
def get_feedback():
    feedback=[]
    nickname = "zch"#flask.request.args.get('nickname')
    if request.method == 'POST':
        data = request.get_json(silent=True)
    else:
        address = request.args.get('address')
        content = request.args.get('detail')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "INSERT INTO feedback(nickname,address,content) VALUES('{}','{}','{}')".format(nickname,data['address'],data['detail'])

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return "success"
    except:
        # Rollback in case there is any error
        db.rollback()
        return "fail"
        

@test.route("/get_addbookInfo",methods=["POST","GET"])
def get_addbookInfo():
    nickname = "zch"#flask.request.args.get('nickname')
    if request.method == 'POST':
        data = request.get_json(silent=True)
    else:
        address = request.args.get('address')
        content = request.args.get('detail')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "INSERT INTO addbookinfo(nickname,name,author,time,content) VALUES('{}','{}','{}','{}','{}')".format(nickname,data['name'],data['author'],data['time'],data['detail'])

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return "success"
    except:
        # Rollback in case there is any error
        db.rollback()
        return "fail"
        
        
@test.route("/is_nickname_exist")
def is_nickname_exist():
# 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
    else:
        nickname = request.args.get('nickname')
        
# SQL 查询语句
    sql = "select * from usr_info where nickname ='{}'".format(nickname)

   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    if (len(results)==0):
        return "1"  #不存在同名
    elif (len(results)==1):
        return "0"  #存在同名
    else:
        return "-1" #出错

    
@test.route('/get_name',methods=["POST", "GET"])
def get_name():
    tt={"code":200}
    return tt
    if request.method == 'POST':
        data = request.get_json(silent=True)
    else:
        address = request.args.get('address')
        content = request.args.get('detail')
    print(data)
    print(data['address'])
    print(data['detail'])
    return "111"

@test.route("/aaa")
def hello():
    return "Hello World!!!!"


@test.route("/bbb")
def bbb():
    a=[1,2,3]
    data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'f': 5}]
    return json.dumps(a[3])


@test.route('/ccc')
def get_dat():
    dic = {"name": "python"}
    return json.dumps(dic)

@test.route("/ddd")
def ddd():
    # db.create_all()
    user1 = Ddd(name="jjj")
    user2 = Ddd(name="bbb")
    db.session.add_all([user1, user2])
    db.session.commit()
    return "ok"

@test.route("/eee")
def eee():
    eeee=[]
    # 打开数据库连接


# 使用cursor()方法获取操作游标
    cursor = db.cursor()

# SQL 查询语句
    sql = "select * from ddd"

   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
	#author=row[2]
	#dynasty=row[3]
	#form=row[4]
	#style=row[5]
	#content=row[6]
      # 打印结果
        eeee.append(name)

# 关闭数据库连接
    return json.dumps(eeee)

@test.route("/fff")
def fff():
    ffff=[]
# 使用cursor()方法获取操作游标
    cursor = db.cursor()

# SQL 查询语句
    sql = "select * from peotry where author ='屈原'"

   # 执行SQL语句
    cursor.execute(sql)
   # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        data_item={
            "id":row[0],
            "name":row[1],
            "author":row[2],
            "dynasty":row[3],
            "form":row[4],
            "style":row[5],
            "content":row[6],
            "annotation":row[7]
        }
        data_item["content"]=ast.literal_eval(data_item["content"])
        data_item["annotation"]=ast.literal_eval(data_item["annotation"])
        ffff.append(data_item)

# 关闭数据库连接
    return json.dumps(ffff)
