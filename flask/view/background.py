#-*- coding:utf-8 -*-
from flask import Flask, render_template, Blueprint, request
import json
import flask
import ast
import requests
import MySQLdb
from datetime import datetime

background = Blueprint('background', __name__)

@background.route('/get_info',methods=["POST","GET"])
def get_authorname():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    info_num = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    
    sql = "select count(*) from usr_info"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    usr_num=results[0][0]
    
    sql = "select count(*) from feedback"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    feedback1=results[0][0]
    
    sql = "select count(*) from addbookinfo"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    feedback2=results[0][0]
    feedback_num=feedback1+feedback2
    
    sql = "select count(*) from all_book"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    works_num=results[0][0]
    
    sql = "select count(*) from recommendation"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    recommendation_num=results[0][0]
    
    db.close()
    info_num={"usr_num":usr_num,"feedback_num":feedback_num,"works_num":works_num,"recommendation_num":recommendation_num}
    return json.dumps(info_num)
    
    
@background.route("/get_oneusr_info",methods=["POST","GET"])
def get_oneusr_info():
    usr_info=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        key = data['key']
    else:
        key = flask.request.args.get('key')
        
    print(key)
        
    sql = "select * from usr_info where phone_num ='{}'".format(key)
    cursor.execute(sql)  # 执行SQL语句
    result = cursor.fetchone()  # 获取记录
    if result!=None:
        data_item = {
            "phone_num":result[0],
            "nickname":result[1],
            "password":result[2],
            "email": result[3],
            "signature": result[4],
            "avatar":result[5],
            "gender": result[6],
            "birthday": result[7],
            "area": result[8],
            "registertime": result[9]
        }
        usr_info.append(data_item)
    
    sql = "select * from usr_info where nickname ='{}'".format(key)
    cursor.execute(sql)  # 执行SQL语句
    result = cursor.fetchone()  # 获取记录
    if result!=None:
        data_item = {
            "phone_num":result[0],
            "nickname":result[1],
            "password":result[2],
            "email": result[3],
            "signature": result[4],
            "avatar":result[5],
            "gender": result[6],
            "birthday": result[7],
            "area": result[8],
            "registertime": result[9]
        }
        usr_info.append(data_item)
    
    db.close()
    return json.dumps(usr_info)
    

@background.route("/get_usr_info",methods=["POST","GET"])
def get_usr_info():
    usr_info=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        
    sql = "select * from usr_info"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "phone_num":row[0],
            "nickname":row[1],
            "password":row[2],
            "email": row[3],
            "signature": row[4],
            "avatar":row[5],
            "gender": row[6],
            "birthday": row[7],
            "area": row[8],
            "registertime": row[9]
        }
        usr_info.append(data_item)
    db.close()
    return json.dumps(usr_info)
    

@background.route("/get_feedback_unread",methods=["POST","GET"])
def get_feedback_unread():
    feedback=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        
    sql = "select * from feedback where status = 'unread' order by id desc"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "address":row[2],
            "content": row[3],
            "createtime": row[4],
            "status":row[5]
        }
        feedback.append(data_item)
    db.close()
    return json.dumps(feedback)
    
    
@background.route("/get_feedback_read",methods=["POST","GET"])
def get_feedback_read():
    feedback=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        
    sql = "select * from feedback where status = 'read' order by id desc"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "address":row[2],
            "content": row[3],
            "createtime": row[4],
            "status":row[5]
        }
        feedback.append(data_item)
    db.close()
    return json.dumps(feedback)
    

@background.route("/update_feedback_status",methods=["POST","GET"])
def update_feedback_status():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')
        
    sql = "update feedback set status = 'read' where id = '{}'".format(id)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)


@background.route("/get_addbookinfo_unread",methods=["POST","GET"])
def get_addbookinfo_unread():
    addbookinfo=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        
    sql = "select * from addbookinfo where status = 'unread' order by id desc"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "name":row[2],
            "author": row[3],
            "time": row[4],
            "content":row[5],
            "createtime":row[6],
            "status":row[7]
        }
        addbookinfo.append(data_item)
    db.close()
    return json.dumps(addbookinfo)
    
    
@background.route("/get_addbookinfo_read",methods=["POST","GET"])
def get_addbookinfo_read():
    addbookinfo=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        
    sql = "select * from addbookinfo where status = 'read' order by id desc"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "name":row[2],
            "author": row[3],
            "time": row[4],
            "content":row[5],
            "createtime":row[6],
            "status":row[7]
        }
        addbookinfo.append(data_item)
    db.close()
    return json.dumps(addbookinfo)
    

@background.route("/update_addbookinfo_status",methods=["POST","GET"])
def update_addbookinfo_status():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')
        
    sql = "update addbookinfo set status = 'read' where id = '{}'".format(id)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        
        
@background.route("/insert_notice",methods=["POST","GET"])
def insert_notice():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        phone_num = data['phonenum']
        content = data['content']
    else:
        phone_num = flask.request.args.get('phone_num')
        content = flask.request.args.get('content')
    
    #phone_num="13572761631"
    #content="插入公告测试"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    sql = "insert into notice (phone_num,content,createtime) values ('{}','{}','{}')".format(phone_num,content,now)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)

#########################管理作品#####################################
@background.route("/insert_works",methods=["POST","GET"])
def insert_works():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        book_type = data['book_type']
        name = data['name']
        othername = data['othername']
        author = data['author']
        country = data['country']
        dynasty = data['dynasty']
        time = data['time']
        intro = data['intro']
        form = data['form']
        style = data['style']
        content = data['content']
        annotation = data['annotation']
        picture1 = data['picture1']
        picture2 = data['picture2']
        picture3 = data['picture3']
    else:
        book_type = flask.request.args.get('book_type')
        name = flask.request.args.get('name')
        othername = flask.request.args.get('othername')
        author = flask.request.args.get('author')
        country = flask.request.args.get('country')
        dynasty = flask.request.args.get('dynasty')
        time = flask.request.args.get('time')
        intro = flask.request.args.get('intro')
        form = flask.request.args.get('form')
        style = flask.request.args.get('style')
        content = flask.request.args.get('content')
        annotation = flask.request.args.get('annotation')
        picture1 = flask.request.args.get('picture1')
        picture2 = flask.request.args.get('picture2')
        picture3 = flask.request.args.get('picture3')
    
    sql = "insert into all_book (book_type,name,othername,author,country,dynasty,time,intro,form,style,content,annotation,picture1,picture2,picture3) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(book_type,name,othername,author,country,dynasty,time,intro,form,style,content,annotation,picture1,picture2,picture3)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        
        
@background.route("/update_works",methods=["POST","GET"])
def update_works():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
        book_type = data['book_type']
        name = data['name']
        othername = data['othername']
        author = data['author']
        country = data['country']
        dynasty = data['dynasty']
        time = data['time']
        intro = data['intro']
        form = data['form']
        style = data['style']
        content = data['content']
        annotation = data['annotation']
        picture1 = data['picture1']
        picture2 = data['picture2']
        picture3 = data['picture3']
    else:
        id = flask.request.args.get('id')
        book_type = flask.request.args.get('book_type')
        name = flask.request.args.get('name')
        othername = flask.request.args.get('othername')
        author = flask.request.args.get('author')
        country = flask.request.args.get('country')
        dynasty = flask.request.args.get('dynasty')
        time = flask.request.args.get('time')
        intro = flask.request.args.get('intro')
        form = flask.request.args.get('form')
        style = flask.request.args.get('style')
        content = flask.request.args.get('content')
        annotation = flask.request.args.get('annotation')
        picture1 = flask.request.args.get('picture1')
        picture2 = flask.request.args.get('picture2')
        picture3 = flask.request.args.get('picture3')
    
    print(data)
    
    sql = "update all_book set book_type='{}',name='{}',othername='{}',author='{}',country='{}',dynasty='{}',time='{}',intro='{}',form='{}',style='{}',content='{}',annotation='{}',picture1='{}',picture2='{}',picture3='{}' where id ={}".format(book_type,name,othername,author,country,dynasty,time,intro,form,style,content,annotation,picture1,picture2,picture3,id)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        

@background.route("/delete_works",methods=["POST","GET"])
def delete_works():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')
    
    sql = "delete from all_book where id ={}".format(id)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        
        
@background.route('/get_background_search_works',methods=["POST","GET"])
def get_background_search_works():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    works = []
    if request.method == 'POST':
        data = request.get_json(silent=True)
        name = data['name']
        book_type = data['book_type']
    else:
        name = flask.request.args.get('name')
        book_type = flask.request.args.get('book_type')
    
    print(data)
    
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    
    if book_type=="all_type":
        sql = "select * from all_book where name like '%{}%'".format(name)
    else:
        sql = "select * from all_book where name like '%{}%' and book_type = '{}'".format(name,book_type)
        
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    for row in results:
        data_item = {
            "id": row[0],
            "book_type": row[1],
            "name": row[2],
            "othername": row[3],
            "author": row[4],
            "country": row[5],
            "dynasty": row[6],
            "time": row[7],
            "intro": row[8],
            "form": row[9],
            "style": row[10],
            "content": row[11],
            "annotation": row[12],
            "picture1": row[13],
            "picture2": row[14],
            "picture3": row[15]
        }
        
        works.append(data_item)
    
    db.close()
    return json.dumps(works)


#########################管理推荐文章#####################################
@background.route("/insert_recommendation",methods=["POST","GET"])
def insert_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        title = data['title']
        author = data['author']
        date = data['date']
        content = data['content']
        picture1 = data['picture1']
        picture2 = data['picture2']
        picture3 = data['picture3']
    else:
        title = flask.request.args.get('title')
        author = flask.request.args.get('author')
        date = flask.request.args.get('date')
        content = flask.request.args.get('content')
        picture1 = flask.request.args.get('picture1')
        picture2 = flask.request.args.get('picture2')
        picture3 = flask.request.args.get('picture3')
    
    sql = "insert into recommendation (title,author,date,content,picture1,picture2,picture3) values ('{}','{}','{}','{}','{}','{}','{}')".format(title,author,date,content,picture1,picture2,picture3)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        
        
@background.route("/update_recommendation",methods=["POST","GET"])
def update_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
        title = data['title']
        author = data['author']
        date = data['date']
        content = data['content']
        picture1 = data['picture1']
        picture2 = data['picture2']
        picture3 = data['picture3']
    else:
        id = flask.request.args.get('id')
        title = flask.request.args.get('title')
        author = flask.request.args.get('author')
        date = flask.request.args.get('date')
        content = flask.request.args.get('content')
        picture1 = flask.request.args.get('picture1')
        picture2 = flask.request.args.get('picture2')
        picture3 = flask.request.args.get('picture3')
    
    print(data)
    
    sql = "update recommendation set title='{}',author='{}',date='{}',content='{}',picture1='{}',picture2='{}',picture3='{}' where id ={}".format(title,author,date,content,picture1,picture2,picture3,id)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        

@background.route("/delete_recommendation",methods=["POST","GET"])
def delete_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')
    
    sql = "delete from recommendation where id ={}".format(id)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        
        
@background.route('/get_background_search_recommendation',methods=["POST","GET"])
def get_background_search_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    recommendation = []
    if request.method == 'POST':
        data = request.get_json(silent=True)
        title = data['title']
    else:
        title = flask.request.args.get('title')
    
    print(data)
    
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    
    sql = "select * from recommendation where title like '%{}%'".format(title)
        
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    for row in results:
        data_item = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "date": row[3],
            "content": row[4],
            "picture1": row[6],
            "picture2": row[7],
            "picture3": row[8]
        }
        
        recommendation.append(data_item)
    
    db.close()
    return json.dumps(recommendation)


###########################################################################################
@background.route("/get_notice",methods=["POST","GET"])
def get_notice():
    notice=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        
    sql = "select * from notice order by id desc"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "phone_num":row[1],
            "content":row[2],
            "createtime": row[3]
        }
        notice.append(data_item)
    db.close()
    return json.dumps(notice)
    
    
@background.route("/search_out_post",methods=["POST","GET"])
def search_out_post():
    out_post=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        title = data['title']
    else:
        title = flask.request.args.get('title')
    
    sql = "select * from out_post where title like '%{}%' order by id desc".format(title)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "title":row[2],
            "content": row[3],
            "createtime": row[4]
        }
        out_post.append(data_item)
    db.close()
    return json.dumps(out_post)


@background.route("/delete_out_post",methods=["POST","GET"])
def delete_out_post():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')
    
    sql = "delete from out_post where id ={}".format(id)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        
@background.route("/insert_book_type",methods=["POST","GET"])
def insert_book_type():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        book_type = data['book_type']
    else:
        book_type = flask.request.args.get('book_type')
    
    sql = "insert into all_type (type) values ('{}')".format(book_type)
    
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        back={"code":1}
        db.close()
        return json.dumps(back)
    except:
        # Rollback in case there is any error
        db.rollback()
        back={"code":0}
        db.close()
        return json.dumps(back)
        
        
@background.route("/get_top5_works",methods=["POST","GET"])
def get_top5_works():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    top5_works=[]
    
    sql = "select bookid,sum(time) as A from history group by bookid order by A desc"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    print(results)
    for row in results[:5]:
        sql = "select name from all_book where id = {}".format(row[0])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取记录
        data_item = {
            "name":result[0],
            "time":int(row[1])
        }
        top5_works.append(data_item)
    db.close()
    return json.dumps(top5_works)
    
    
@background.route("/get_top3_recommdation",methods=["POST","GET"])
def get_top3_recommdation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    top5_works=[]
    
    sql = "select recommendation_id,sum(time) as A from history_recommendation group by recommendation_id order by A desc"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    print(results)
    for row in results[:3]:
        sql = "select title from recommendation where id = {}".format(row[0])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取记录
        data_item = {
            "title":result[0],
            "time":int(row[1])
        }
        top5_works.append(data_item)
    db.close()
    return json.dumps(top5_works)