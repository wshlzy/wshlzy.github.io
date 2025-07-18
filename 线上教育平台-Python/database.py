import pymysql
import MySQLdb
import pandas as pd
import os
import json

def get_conn():
    conn = pymysql.connect(
        host="localhost", port=3306,
        user="root", password="123456",
        database="pythonweb", charset="utf8"
    )
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    conn.close()
    cursor.close()

#插入 student 表
def insert_student(username,password):
    conn, cursor = get_conn()
    sql = 'insert into student (username, password)  values (%s,%s)'
    try:
        cursor.execute(sql,(username, password))
        conn.commit()
    except MySQLdb.IntegrityError as e:
        print("MySQL integrityError:",e)
    close(conn, cursor)

#插入 teacher 表
def insert_teacher(username,password):
    conn, cursor = get_conn()
    sql = 'insert into teacher_info  values (%s,%s)'
    try:
        cursor.execute(sql,(username, password))
        conn.commit()
    except MySQLdb.IntegrityError as e:
        print("MySQL IntegrityError:",e)
    close(conn, cursor)

#插入 choiceQA 表
def insert_choiceqa(tup):
    conn, cursor = get_conn()
    sql = 'insert into choiceqa  values (%s,%s,%s,%s,%s)'
    cursor.execute(sql,(tup[0],tup[1],tup[2],tup[3],tup[4]))
    conn.commit()
    close(conn, cursor)

#插入 choiceQB 表
def insert_choiceqb(tup):
    conn, cursor = get_conn()
    sql = 'insert into choiceqb values (%s,%s,%s,%s,%s)'
    cursor.execute(sql,(tup[0],tup[1],tup[2],tup[3],tup[4]))
    conn.commit()
    close(conn, cursor)

#插入 choiceQC 表
def insert_choiceqc(tup):
    conn, cursor = get_conn()
    sql = 'insert into choiceqc  values (%s,%s,%s,%s,%s)'
    cursor.execute(sql,(tup[0],tup[1],tup[2],tup[3],tup[4]))
    conn.commit()
    close(conn, cursor)

#插入 choiceQD 表
def insert_choiceqd(tup):
    conn, cursor = get_conn()
    sql = 'insert into choiceqd  values (%s,%s,%s,%s,%s)'
    cursor.execute(sql,(tup[0],tup[1],tup[2],tup[3],tup[4]))
    conn.commit()
    close(conn, cursor)

#插入 choiceQE 表
def insert_choiceqe(tup):
    conn, cursor = get_conn()
    sql = 'insert into choiceqe  values (%s,%s,%s,%s,%s)'
    cursor.execute(sql,(tup[0],tup[1],tup[2],tup[3],tup[4]))
    conn.commit()
    close(conn, cursor)

#插入 choiceQF 表
def insert_choiceqf(tup):
    conn, cursor = get_conn()
    sql = 'insert into choiceqf  values (%s,%s,%s,%s,%s)'
    cursor.execute(sql,(tup[0],tup[1],tup[2],tup[3],tup[4]))
    conn.commit()
    close(conn, cursor)
    

# 查询所有
def find_all():
    # 获取数据库连接和cursor
    conn, cursor = get_conn()
    # 执行查询操作
    sql = "select * from student"
    count = cursor.execute(sql)
    print(f"查询到了{count}条学生信息：")
    result = cursor.fetchall()
    for stu in result:
        print(stu)
    # 释放资源
    close(conn, cursor)
    # 返回查询到的所有用户信息
    return result


# 根据sid删除学员
def delete_stu(sid):
    conn, cursor = get_conn()
    sql = 'delete from student where sid=%s'
    count = cursor.execute(sql, [sid])
    # 提交事务
    conn.commit()
    # 释放资源
    close(conn, cursor)


# 根据sid查询某一个
def find_stu(sid):
    conn, cursor = get_conn()
    sql = 'select * from student where sid=%s'
    count = cursor.execute(sql, [sid])
    stu = cursor.fetchall()
    print(stu, '+++++++++')
    # 释放资源
    close(conn, cursor)
    return stu[0]

# 封装通用的查询方法
def query(sql,*args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),(),)的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close(conn, cursor)
    return res


# 获取left1中的数据，数据来源history
def get_left1():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def update_stu(sid, name, age, classes, score):
    conn, cursor = get_conn()
    sql = 'update student set name=%s, age=%s, classes=%s, score=%s where sid=%s'
    count = cursor.execute(sql, [name, age, classes, score, sid])
    # 提交事务
    conn.commit()
    # 释放资源
    close(conn, cursor)
