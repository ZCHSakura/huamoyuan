# -*- coding:utf-8 -*-
from flask import Flask, render_template, Blueprint, request
import json
import flask
import ast
import math
import requests
import MySQLdb

main = Blueprint('main', __name__)


@main.route('/get_search', methods=["POST", "GET"])
def get_search():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    search = []
    if request.method == 'POST':
        data = request.get_json(silent=True)
        typee = data['type']
        key = data['key']
        page = int(data['page'])
    else:
        typee = flask.request.args.get('type')
        key = flask.request.args.get('key')
        page = int(flask.request.args.get('page'))

    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    if int(typee) == 1:  # 作品名称
        sql = "select count(*) from all_book where name like %s"
        query_param = ['%%%s%%' % key]
        cursor.execute(sql, query_param)  # 执行SQL语句
        count = math.ceil(cursor.fetchone()[0] / 10)

        sql = "select * from all_book where name like %s LIMIT 10 OFFSET %s"
        query_param = ['%%%s%%' % key, (page - 1) * 10]
        cursor.execute(sql, query_param)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:
            data_item = {
                "id": row[0],
                "book_type": row[1],
                "name": row[2],
                "author": row[4],
                "dynasty": row[6],
                "intro": row[8],
                "content": row[11]
            }
            if data_item["content"] != None:
                data_item["content"] = ast.literal_eval(data_item["content"])

            if data_item["intro"] != None:
                data_item["intro"] = data_item["intro"].split("\0")

            search.append(data_item)

    elif int(typee) == 2:  # 作者
        sql = "select count(*) from all_book where author like %s"
        query_param = ['%%%s%%' % key]
        cursor.execute(sql, query_param)  # 执行SQL语句
        count = math.ceil(cursor.fetchone()[0] / 10)  # 获取所有记录列表

        sql = "select * from all_book where author like %s LIMIT 10 OFFSET %s"
        query_param = ['%%%s%%' % key, (page - 1) * 10]
        cursor.execute(sql, query_param)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:
            data_item = {
                "id": row[0],
                "book_type": row[1],
                "name": row[2],
                "author": row[4],
                "dynasty": row[6],
                "intro": row[8],
                "content": row[11]
            }
            if data_item["content"] != None:
                data_item["content"] = ast.literal_eval(data_item["content"])

            if data_item["intro"] != None:
                data_item["intro"] = data_item["intro"].split("\0")

            search.append(data_item)

    elif int(typee) == 3:  # 朝代
        key = key.replace('朝', '')

        sql = "select count(*) from all_book where dynasty like %s"
        query_param = ['%%%s%%' % key]
        cursor.execute(sql, query_param)  # 执行SQL语句
        count = math.ceil(cursor.fetchone()[0] / 10)  # 获取所有记录列表

        sql = "select * from all_book where dynasty like %s LIMIT 10 OFFSET %s"
        query_param = ['%%%s%%' % key, (page - 1) * 10]
        cursor.execute(sql, query_param)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:
            data_item = {
                "id": row[0],
                "book_type": row[1],
                "name": row[2],
                "author": row[4],
                "dynasty": row[6],
                "intro": row[8],
                "content": row[11]
            }
            if data_item["content"] != None:
                data_item["content"] = ast.literal_eval(data_item["content"])

            if data_item["intro"] != None:
                data_item["intro"] = data_item["intro"].split("\0")

            search.append(data_item)

    else:
        back = {"code": -1, "msg": "出了问题"}

        db.close()
        return json.dumps(back)

    db.close()
    back = {"code": 1, "pages": count, "search": search}
    return json.dumps(back)


# app分页搜索
@main.route('/get_search_app', methods=["POST", "GET"])
def get_search_app():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    search_list = []
    if request.method == 'POST':
        data = request.get_json(silent=True)
    else:
        key = flask.request.args.get('key')
        book_type = flask.request.args.get('book_type')
        page = int(flask.request.args.get('page'))

    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if key is not None:
        # 先获取总页数
        sql = "select count(*) from `all_book` where `name` like %s and `book_type` = %s LIMIT 10"
        query_param = ['%%%s%%' % key, book_type]
        cursor.execute(sql, query_param)  # 执行SQL语句
        count1 = cursor.fetchone()[0]
        # print(count1)
        first_page = math.ceil(count1 / 10)

        sql = "select count(*) from `all_book` where `author` like %s and `book_type` = %s LIMIT 10"
        query_param = ['%%%s%%' % key, book_type]
        cursor.execute(sql, query_param)  # 执行SQL语句
        count2 = cursor.fetchone()[0]
        # print(count1 + count2)
        second_page = math.ceil((count1 + count2) / 10)

        sql = "select count(*) from `all_book` where `dynasty` like %s and `book_type` = %s LIMIT 10"
        query_param = ['%%%s%%' % key, book_type]
        cursor.execute(sql, query_param)  # 执行SQL语句
        count3 = cursor.fetchone()[0]
        # print(count1 + count2 + count3)
        third_page = math.ceil((count1 + count2 + count3) / 10)

        # print(first_page, second_page, third_page)

        # 定义几个重要参数
        limit1 = 10
        limit2 = 10
        limit3 = 10
        offset1 = 0
        offset2 = 0
        offset3 = 0

        # 第一步先获取作品名中包含该关键字的部分
        if page <= first_page:
            offset1 = (page - 1) * 10
            # print("page:", page, "limit1:", limit1, "offset1:", offset1)

            sql = "select * from `all_book` where name like %s and `book_type` = %s LIMIT %s OFFSET %s"
            query_param = ['%%%s%%' % key, book_type, limit1, offset1]
            cursor.execute(sql, query_param)  # 执行SQL语句
            results = cursor.fetchall()  # 获取所有记录列表
            for row in results:
                data_item = {
                    "id": row[0],
                    "name": row[2],
                    "author": row[4],
                    "dynasty": row[6],
                    "intro": row[8],
                    "content": row[11]
                }
                if data_item["content"] != None:
                    data_item["content"] = ast.literal_eval(data_item["content"])
                    data_item["content"] = data_item["content"][0]

                if data_item["intro"] != None:
                    if len(data_item["intro"]) > 20:
                        data_item["intro"] = data_item["intro"][0:20] + "..."

                search_list.append(data_item)

            if page == first_page:
                remain_to_second = 10 - len(results)

        # 第二步获取作者中包含该关键字的部分
        if first_page <= page <= second_page:
            # 补足上一个部分剩余的内容，补足10条
            if page == first_page:
                limit2 = remain_to_second
                offset2 = 0
            else:
                offset2 = 10 * page - count1 - 10
            # print("page:", page, "  limit2:", limit2, "  offset2:", offset2)

            sql = "select * from all_book where author like %s and book_type = %s LIMIT %s OFFSET %s"
            query_param = ['%%%s%%' % key, book_type, limit2, offset2]
            cursor.execute(sql, query_param)  # 执行SQL语句
            results = cursor.fetchall()  # 获取所有记录列表
            for row in results:
                data_item = {
                    "id": row[0],
                    "name": row[2],
                    "author": row[4],
                    "dynasty": row[6],
                    "intro": row[8],
                    "content": row[11]
                }
                if data_item["content"] != None:
                    data_item["content"] = ast.literal_eval(data_item["content"])
                    data_item["content"] = data_item["content"][0]

                if data_item["intro"] != None:
                    if len(data_item["intro"]) > 20:
                        data_item["intro"] = data_item["intro"][0:20] + "..."

                search_list.append(data_item)

            if page == second_page:
                remain_to_third = 10 - len(results)

        # 第三步获取朝代中包含该关键字的部分
        if second_page <= page <= third_page:
            # 补足上一个部分剩余的内容，补足10条
            if page == second_page:
                limit3 = remain_to_third
                offset3 = 0
            else:
                offset3 = 10 * page - count1 - count2 - 10
            # print("page:", page, "  limit3:", limit3, "  offset3:", offset3)

            # 去掉朝字，扩大范围
            key = key.replace('朝', '')
            sql = "select * from all_book where dynasty like %s and book_type = %s LIMIT %s OFFSET %s"
            query_param = ['%%%s%%' % key, book_type, limit3, offset3]
            cursor.execute(sql, query_param)  # 执行SQL语句
            results = cursor.fetchall()  # 获取所有记录列表
            for row in results:
                data_item = {
                    "id": row[0],
                    "name": row[2],
                    "author": row[4],
                    "dynasty": row[6],
                    "intro": row[8],
                    "content": row[11]
                }
                if data_item["content"] != None:
                    data_item["content"] = ast.literal_eval(data_item["content"])
                    data_item["content"] = data_item["content"][0]

                if data_item["intro"] != None:
                    if len(data_item["intro"]) > 20:
                        data_item["intro"] = data_item["intro"][0:20] + "..."

                search_list.append(data_item)
        # 如果页面超范围
        if third_page < page:
            back = {"code": -1}
            db.close()
            return json.dumps(back)
    else:
        back = {"code": -1}
        db.close()
        return json.dumps(back)

    count = math.ceil((count1 + count2 + count3) / 10)
    back = {"code": 1, "pages": count, "data": search_list}
    db.close()
    return json.dumps(back)


@main.route('/get_detail', methods=["POST", "GET"])
def get_detail():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    detail = []
    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if type != None:  # 接收到了类型
        sql = "select * from all_book where id = {}".format(id)
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
                "cover": row[13],
                "picture2": row[14],
                "picture3": row[15],
                "collect_num": 0
            }
            if data_item["content"] != None:
                data_item["content"] = ast.literal_eval(data_item["content"])
            if data_item["annotation"] != None:
                data_item["annotation"] = ast.literal_eval(data_item["annotation"])

            sql = "select count(*) from collect where bookid = {}".format(data_item['id'])
            cursor.execute(sql)  # 执行SQL语句
            result = cursor.fetchone()  # 获取一条记录
            data_item['collect_num'] = result[0]

            detail.append(data_item)

    else:
        back = {"code": -1}
        db.close()
        return json.dumps(back)

    db.close()
    return json.dumps(detail)


@main.route('/get_author', methods=["POST", "GET"])
def get_author():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    author_info = []
    if request.method == 'POST':
        data = request.get_json(silent=True)
        author = data['author']
    else:
        author = flask.request.args.get('author')

    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    sql = "select * from author_info where name = '{}'".format(author)
    cursor.execute(sql)  # 执行SQL语句
    result = cursor.fetchone()  # 获取一条记录
    if result == None:
        back = [{"name": author, "intro": "没有查询到该作者信息"}]
        db.close()
        return json.dumps(back)
    data_item = {
        "name": result[1],
        "intro": result[2]
    }
    author_info.append(data_item)
    db.close()
    return json.dumps(author_info)


@main.route('/get_authorname', methods=["POST", "GET"])
def get_authorname():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    author_name = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    sql = "select name from author_info"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "name": row[0]
        }
        author_name.append(data_item)
    db.close()
    return json.dumps(author_name)


@main.route('/get_recommendation', methods=["POST", "GET"])
def get_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    recommendation = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    sql = "select * from recommendation where `show` = 1"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "date": row[3],
            "content": row[4],
            "picture": row[6],
            "collect_num": 0
        }
        sql = "select count(*) from collect_recommendation where recommendation_id = {}".format(data_item['id'])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取一条记录
        data_item['collect_num'] = result[0]

        recommendation.append(data_item)
    db.close()
    return json.dumps(recommendation)


@main.route('/get_one_recommendation', methods=["POST", "GET"])
def get_one_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    recommendation = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')

    sql = "select * from recommendation where `show` = 1 and `id` = %s"
    cursor.execute(sql, [id])  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "date": row[3],
            "content": row[4],
            "picture": row[6],
            "collect_num": 0
        }
        sql = "select count(*) from collect_recommendation where recommendation_id = {}".format(data_item['id'])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取一条记录
        data_item['collect_num'] = result[0]

        recommendation.append(data_item)
    db.close()
    return json.dumps(recommendation)


@main.route('/get_in_comment', methods=["POST", "GET"])
def get_in_comment():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    in_comment = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        recommendation_id = data['recommendation_id']
    else:
        recommendation_id = flask.request.args.get('recommendation_id')

    sql = "select * from in_comment where recommendation_id = '{}'".format(recommendation_id)
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "id": row[0],
            "nickname": row[1],
            "content": row[3],
            "createtime": row[4],
            "avatar": ""
        }
        sql = "select avatar from usr_info where nickname = '{}'".format(data_item['nickname'])
        cursor.execute(sql)  # 执行SQL语句
        result = cursor.fetchone()  # 获取一条记录
        data_item['avatar'] = result[0]

        in_comment.append(data_item)
    db.close()
    return json.dumps(in_comment)


@main.route("/get_all_type", methods=["POST", "GET"])
def get_all_type():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    all_type = []
    num_type = 0

    sql = "select type from all_type where type != 'recommendation'"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    for row in results:
        num_type += 1
        data_item = {
            "chinese": row[0],
            "english": row[0]
        }
        print(data_item['english'])
        if data_item['english'] == "poetry":
            data_item['chinese'] = "诗词"

        if data_item['english'] == "ancient_book":
            data_item['chinese'] = "古籍"

        all_type.append(data_item)

    db.close()
    back = {"num": num_type, "types": all_type}
    return json.dumps(back)


# 获取目录
@main.route('/get_catelog', methods=["POST", "GET"])
def get_catelog():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    catelog = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')

    sql = "select id,chapterTitle,chapterName from gujizhangjie where bookId = %s ORDER BY chapterTitle, chapterName"
    cursor.execute(sql, [id])  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    print(results)
    if results:
        for row in results:
            data_item = {
                "id": row[0],
                "chapterTitle": row[1],
                "chapterName": row[2]
            }
            if data_item["chapterTitle"] == '':
                data_item["chapterTitle"] = None
            catelog.append(data_item)
        back = {"code": 1, "catelog": catelog}
    else:
        back = {"code": -1}
    db.close()
    return json.dumps(back)


@main.route('/get_reading', methods=["POST", "GET"])
def get_reading():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    reading = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = data['id']
    else:
        id = flask.request.args.get('id')

    sql = "select content,translation,annotation,note from gujizhangjie where id = %s"
    cursor.execute(sql, [id])  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    print(results)
    if results:
        for row in results:
            data_item = {
                "content": row[0],
                "translation": row[1],
                "annotation": row[2],
                "note": row[3]
            }
            if data_item["content"] == '':
                data_item["content"] = None
            else:
                data_item["content"] = ast.literal_eval(data_item["content"])
            if data_item["translation"] == '':
                data_item["translation"] = None
            else:
                data_item["translation"] = ast.literal_eval(data_item["translation"])
            if data_item["annotation"] == '':
                data_item["annotation"] = None
            else:
                data_item["annotation"] = ast.literal_eval(data_item["annotation"])
            if data_item["note"] == '':
                data_item["note"] = None
            else:
                data_item["note"] = ast.literal_eval(data_item["note"])
            reading.append(data_item)
        back = {"code": 1, "reading": reading}
    else:
        back = {"code": -1}
    db.close()
    return json.dumps(back)


# 插入古籍书签
@main.route("/insert_chaptermark", methods=["POST", "GET"])
def insert_chaptermark():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    if request.method == 'POST':
        data = request.get_json(silent=True)
        userNickname = data['userNickname']
        bookId = data['bookId']
        chapterId = data['chapterId']
        progess = data['progess']
    else:
        userNickname = flask.request.args.get('userNickname')
        bookId = flask.request.args.get('bookId')
        chapterId = flask.request.args.get('chapterId')
        progess = flask.request.args.get('progess')

    sql = "INSERT INTO chaptermark (userNickname,bookId,chapterId,progess,modifiedTime) VALUES (%s,%s,%s,%s,NOW())"
    try:
        # 执行sql语句
        cursor.execute(sql, [userNickname, bookId, chapterId, progess])
        # 提交到数据库执行
        db.commit()
        back = {"code": 1}
    except:
        # Rollback in case there is any error
        db.rollback()
        back = {"code": 0}

    db.close()
    return json.dumps(back)


# 获取古籍书签
@main.route('/get_chaptermark', methods=["POST", "GET"])
def get_chaptermark():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    mark = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        userNickname = data['userNickname']
        bookId = data['bookId']
    else:
        userNickname = flask.request.args.get('userNickname')
        bookId = flask.request.args.get('bookId')

    sql = "select id,chapterId,progess from chaptermark where userNickname = %s and bookId = %s order by id desc limit 1"
    cursor.execute(sql, [userNickname, bookId])  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    print(results)
    if results:
        for row in results:
            data_item = {
                "id": row[0],
                "chapterId": row[1],
                "progess": row[2]
            }
            mark.append(data_item)
        back = {"code": 1, "mark": mark}
    else:
        back = {"code": 0}
    db.close()
    return json.dumps(back)


# 获取所有诗词
@main.route('/get_all_poetry', methods=["POST", "GET"])
def get_all_poetry():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    poetry = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        page = int(data['page'])
    else:
        page = int(flask.request.args.get('page'))

    sql = "select count(*) from all_book where book_type = 'poetry'"
    cursor.execute(sql)  # 执行SQL语句
    count = math.ceil(cursor.fetchone()[0] / 10)  # 获取所有记录列表

    sql = "select * from all_book where book_type = 'poetry' LIMIT 10 OFFSET %s"
    cursor.execute(sql, [(page - 1) * 10])  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    if results:
        for row in results:
            data_item = {
                "id": row[0],
                "book_type": row[1],
                "name": row[2],
                "author": row[4],
                "dynasty": row[6],
                "intro": row[8],
                "content": row[11],
                "cover": row[13],
            }
            if data_item["content"] != None:
                data_item["content"] = ast.literal_eval(data_item["content"])

            if data_item["intro"] != None:
                data_item["intro"] = data_item["intro"].split("\0")

            poetry.append(data_item)
        back = {"code": 1, "pages": count, "poetry": poetry}
    else:
        back = {"code": 0}
    db.close()
    return json.dumps(back)


# 获取所有古籍
@main.route('/get_all_ancient_book', methods=["POST", "GET"])
def get_all_ancient_book():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    ancient_book = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        page = int(data['page'])
    else:
        page = int(flask.request.args.get('page'))

    sql = "select count(*) from all_book where book_type = 'ancient_book'"
    cursor.execute(sql)  # 执行SQL语句
    count = math.ceil(cursor.fetchone()[0] / 10)  # 获取所有记录列表
    print(count)

    sql = "select * from all_book where book_type = 'ancient_book' LIMIT 10 OFFSET %s"
    cursor.execute(sql, [(page - 1) * 10])  # 执行SQL语句
    results = cursor.fetchall()  # 获取所有记录列表
    if results:
        for row in results:
            data_item = {
                "id": row[0],
                "book_type": row[1],
                "name": row[2],
                "author": row[4],
                "dynasty": row[6],
                "intro": row[8],
                "content": row[11],
                "cover": row[13],
            }
            if data_item["content"] != None:
                data_item["content"] = ast.literal_eval(data_item["content"])

            if data_item["intro"] != None:
                data_item["intro"] = data_item["intro"].split("\0")

            ancient_book.append(data_item)
        back = {"code": 1, "pages": count, "ancient_book": ancient_book}
    else:
        back = {"code": 0}
    db.close()
    return json.dumps(back)


# 获取朝代列表
@main.route('/get_all_dyansty', methods=["POST", "GET"])
def get_all_dyansty():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    dynasty_list = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    sql = "select * from dynasty"
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        for row in results:
            data_item = {
                "id": row[0],
                "name": row[1],
                "time": row[2],
                "img": row[3],
                "intro": row[4]
            }
            dynasty_list.append(data_item)
        back = {"code": 1, "dynasty_list": dynasty_list}
    else:
        back = {"code": 0}
    db.close()
    return json.dumps(back)


# 随机获取四个推荐文章
@main.route('/get_random_recommendation', methods=["POST", "GET"])
def get_random_recommendation():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    recommendation = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    sql = "SELECT * FROM recommendation WHERE `show` = 1 ORDER BY RAND() LIMIT 4"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "id": row[0],
            "title": row[1],
            "picture": row[6]
        }
        recommendation.append(data_item)
    db.close()
    return json.dumps(recommendation)


# 随机获取三个图
@main.route('/get_random_painting', methods=["POST", "GET"])
def get_random_painting():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    painting = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    sql = "SELECT * FROM homepage ORDER BY RAND() LIMIT 3"
    cursor.execute(sql)  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "id": row[0],
            "name": row[1],
            "author": row[5],
            "img": row[2],
        }
        painting.append(data_item)
    db.close()
    return json.dumps(painting)


# 获取所有书画
@main.route('/get_all_painting', methods=["POST", "GET"])
def get_all_painting():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    painting = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        page = int(data['page'])
    else:
        page = int(flask.request.args.get('page'))

    sql = "select count(*) from homepage"
    cursor.execute(sql)  # 执行SQL语句
    count = math.ceil(cursor.fetchone()[0] / 4)  # 获取所有记录列表

    sql = "SELECT * FROM homepage LIMIT 4 OFFSET %s"
    cursor.execute(sql, [(page - 1) * 4])  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "id": row[0],
            "name": row[1],
            "author": row[5],
            "img": row[2],
            "dynasty": row[6],
            "size": row[7],
            "pixel": row[8],
            "intro": row[9],
        }
        painting.append(data_item)
    db.close()
    back = {"code": 1, "pages": count, "painting": painting}
    return json.dumps(back)


# 获取一个书画大图
@main.route('/get_one_painting', methods=["POST", "GET"])
def get_one_painting():
    db = MySQLdb.connect("59.110.223.221", "root", "zch621", "tietouwa", charset='utf8')
    painting = []
    cursor = db.cursor()  # 使用cursor()方法获取操作游标

    if request.method == 'POST':
        data = request.get_json(silent=True)
        id = int(data['id'])
    else:
        id = int(flask.request.args.get('id'))

    sql = "SELECT * FROM homepage WHERE `id` = %s"
    cursor.execute(sql, [id])  # 执行SQL语句
    results = cursor.fetchall()  # 获取一条记录
    for row in results:
        data_item = {
            "id": row[0],
            "content": row[4]
        }
        painting.append(data_item)
    db.close()
    return json.dumps(painting)
