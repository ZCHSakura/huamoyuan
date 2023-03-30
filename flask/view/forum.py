#-*- coding:utf-8 -*-
from flask import Flask, render_template, Blueprint, request
import json
import flask
import ast
import requests
import MySQLdb
from datetime import datetime

forum = Blueprint('forum', __name__)


@forum.route("/get_out_post_list",methods=["POST","GET"])
def get_out_post_list():
    out_post_list=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
        
    sql = "select * from out_post"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "title":row[2],
            "content": row[3],
            "createtime": row[4],
            "comment_num":0,
            "avatar":"",
            "last_comment_time":""
        }
        sql = "select count(*) from out_comment where post_id = '{}'".format(data_item['id'])
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取一条记录
        data_item['comment_num']=results[0][0]
        
        sql = "select avatar from usr_info where nickname = '{}'".format(data_item['nickname'])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取一条记录
        data_item['avatar']=result[0]
        
        if len(data_item["content"])>20:
            data_item["content"]=data_item["content"][0:20]+"..."
            
        sql = "select id,createtime from out_comment where post_id = '{}' order by id desc".format(data_item['id'])
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取一条记录
        if len(results)==0:
            data_item['last_comment_time']=data_item['createtime']
        else:
            data_item['last_comment_time']=results[0][1]
        
        out_post_list.append(data_item)
    db.close()
    return json.dumps(out_post_list)
    
    
@forum.route("/get_out_comment",methods=["POST","GET"])
def get_out_comment():
    out_post_detail=[]
    out_comment=[]
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data)
        post_id = data['post_id']
    else:
        post_id = flask.request.args.get('post_id')
        
    ################帖子部分###################
    sql = "select * from out_post where id = '{}'".format(post_id)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "title":row[2],
            "content": row[3],
            "createtime": row[4],
            "comment_num":0,
            "avatar":""
        }
        sql = "select count(*) from out_comment where post_id = '{}'".format(data_item['id'])
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取一条记录
        data_item['comment_num']=results[0][0]
        
        sql = "select avatar from usr_info where nickname = '{}'".format(data_item['nickname'])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取一条记录
        data_item['avatar']=result[0]
        
        out_post_detail.append(data_item)
        
    ################评论部分###################    
    sql = "select * from out_comment where post_id = '{}'".format(post_id)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取记录
    for row in results:
        data_item = {
            "id":row[0],
            "nickname":row[1],
            "post_id":row[2],
            "replyid": row[3],
            "content": row[5],
            "createtime":row[6],
            "avatar":""
        }
        sql = "select avatar from usr_info where nickname = '{}'".format(data_item['nickname'])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取一条记录
        data_item['avatar']=result[0]
        
        out_comment.append(data_item)
    db.close()
    back={"code":1,"out_post":out_post_detail,"out_comment":out_comment}
    return json.dumps(back)
    
    
@forum.route("/insert_out_comment",methods=["POST","GET"])
def insert_out_comment():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
        post_id = data['post_id']
        replyid = data['replyid']
        content = data['content']
        
    else:
        nickname = request.args.get('nickname')
        post_id = request.args.get('post_id')
        replyid = request.args.get('replyid')
        content = request.args.get('content')
    
    
    #nickname = "zch"
    #recommendation_id=3
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #content="测试"
    
    sql="insert into out_comment (nickname,post_id,replyid,content,createtime) values ('{}',{},{},'{}','{}')".format(nickname,post_id,replyid,content,now)
    
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        back={"code":1}
        return json.dumps(back)
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        back={"code":0}
        return json.dumps(back)
        
        
@forum.route("/insert_out_post",methods=["POST","GET"])
def insert_out_post():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')    
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    
    if request.method == 'POST':
        data = request.get_json(silent=True)
        nickname = data['nickname']
        title = data['title']
        content = data['content']
        
    else:
        nickname = request.args.get('nickname')
        title = request.args.get('title')
        content = request.args.get('content')
    
    
    #nickname = "zch"
    #recommendation_id=3
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #content="测试"
    
    sql="insert into out_post (nickname,title,content,createtime) values ('{}','{}','{}','{}')".format(nickname,title,content,now)
    
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        back={"code":1}
        return json.dumps(back)
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        back={"code":0}
        return json.dumps(back)    