from flask import Flask, make_response, render_template, request, redirect, send_from_directory, abort, url_for, jsonify, flash
from jinja2 import TemplateNotFound
import mysql.connector
import database
import os
import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer
#html文件在内容需要根据 用户输入、调用的数据库数据，或其他运行时产生的信息生成或更改时，应该被放在templates文件夹下

#生成 Flask 实例，变量名是什么不重要
app = Flask(__name__)
app.secret_key = "123456"


#选择客户端页面
@app.route('/')
def select_role():
    return render_template("home.html")

# @app.route('/proxy')
# def proxy():
#     target_url = request.args.get('url')
#     if not target_url:
#         return "URL parameter is missing", 400

    # response = requests.get(target_url)
    # headers = {key: value for (key, value) in response.headers.items() if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']}
    # return Response(response.content, headers=headers, status=response.status_code)

# 登出
@app.route('/logout')
def log_out():
    return render_template("home.html")    


# ------------------ 学生端功能模块 -------------------- #
#学生端登陆界面
@app.route('/stud_login')
def stud_login():
    return render_template("student/stud_login.html")

#当在学生端登陆时，调用数据库检查登录信息
@app.route('/stud_check_login', methods=['GET', 'POST'])
def stud_check_login():
    # 拿到用户输入的用户名和密码
    username = request.values.get('username')
    password = request.values.get('password')
    # 从数据库调用登录信息
    records = database.find_all()

    for record in records:
        if username == record[0] and password == record[1]:
            response = make_response(redirect(url_for('stud_homepage')))
            response.set_cookie('username', username, max_age=86400)
            return response
        
    flash("*账号或密码错误", 'error')
    return redirect('/stud_login')

#学生注册页面
@app.route('/student_regist')
def student_regist():
        return render_template("student/stud_regist.html")

#当在学生端注册成功后，将注册信息插入到学生数据库
@app.route('/regist_over', methods=['GET','POST'])
def stud_regist_over():
    if request.method != 'POST':
        flash("申请方式异常，请重试", 'error-method')
        return redirect("/student_regist")
    
    username = request.values.get('username')
    password = request.values.get('password')
    print(username, password)
    result = database.insertion(username, password)
        
    if (result):
        return render_template("student/stud_login.html")
    else:
        flash("当前用户名已被使用", 'error-insertion')
        return redirect("/student_regist")

#学生端主页面
@app.route('/stud_homepage')
def stud_homepage():
    return render_template("student/stud_homepage.html")
    
#学生端主页面 作业清单
@app.route('/homework')
def homework():
    records = []
    results = database.find_all_hw()
    for row in results:
        records.append({
            'course': row[1], # 课程名称
            'knowledge': row[2] # 课程知识点
        })
    return render_template("homework.html", records=records)

#学生端查看AI生成作业
@app.route('/AI_DB',methods=['POST','GET'])
def DB_search():
    course = request.form.get("course")
    knowledge = request.form.get("knowledge")
    print(course, knowledge)
    result = database.AI_stu(course, knowledge)
    return render_template('student/0113.html', result=result)

#学生端主页面 测验清单
@app.route('/quiz_list')
def quiz_list():
    return render_template("quizcheck.html")

#学生端主页面 日程清单
@app.route('/schedule')
def schedule():
    return render_template("schedule.html")

#学生端主页面 通知清单
@app.route('/notice')
def notice():
    return render_template("inform.html")





# ------------------ 教师端功能模块 -------------------- #
#教师端登陆界面
@app.route('/teacher_login')
def teacher_login():
    return render_template("teacher/teacher_login.html")

#当在教师端登陆时，调用数据库检查登录信息
@app.route('/teacher_check_login', methods=['GET','POST'])
def teacher_check_login():
    # 拿到用户输入的用户名和密码
    username = request.values.get('username')
    password = request.values.get('password')
    # 从数据库调用登录信息
    records = database.find_all()

    for record in records:
        if username == record[0] and password == record[1]:
            response = make_response(redirect(url_for('teacher_homepage')))
            response.set_cookie("username", username)
            return response
        
    flash("*账号或密码错误", 'error')
    return redirect('/teacher_login')

#教师注册页面
@app.route('/teacher_regist')
def teacher_register():
    return render_template("/teacher/teacher_register.html")

#当在教师端注册成功后，将注册信息插入到教师数据库
@app.route('/teacher_regist_over', methods=['GET','POST'])
def teacher_regist_over():
    if request.method == 'POST':
        username = request.values.get('teacher_user')
        password = request.values.get('teacher_password')
        print(username, password)
        database.insert_teacher(username,password)
        return render_template("teacher/teacher_login.html")
    else:
        abort(404)

#教师端主页面
@app.route('/teacher_homepage')
def teacher_homepage():
    return render_template("teacher/teacher_homepage.html")

#教师通过AI上传作业
@app.route('/AIgenerate', methods=['POST', 'GET'])
def AIgenerate():
    course = request.form['course']
    type = request.form['type']
    amount = request.form['amount']
    data = database.AIcaller(course, type, amount)
    file_path = os.path.join('static/js', 'AI_data.json')

    # 将数据写入JSON文件
    with open(file_path, 'w') as json_file:
        json.dump({'data': data}, json_file)
    
    # 返回成功状态
    return jsonify(success=True)

@app.route('/AIupdate',methods=['POST','GET'])
def AIupdate():
    course = request.values.get("course")
    type = request.values.get("select_Type")
    database.AIupdate(course,type)

@app.route('/chuti')
def chuti():
    return render_template("teacher/2124.html")

#教师发布作业
@app.route('/receive_homework')
def receive_homework():
    return render_template("hw_receive.html")

#接收学生的习题数据，并上传到不同习题的数据库；从习题1到习题6
@app.route('/submit_Question', methods=['GET', 'POST'])
def quiz_question():
    answers = {}
    if request.method == 'POST':
        # 处理表单提交的数据
        user = request.form['username']
        table = request.form['database']
        for i in range(5):
            Qtype = request.form['Qtype' + str(i + 1)]
            sequence = request.form['sequence' + str(i + 1)]
            selected = request.form.get('cQ' + str(i), '')
            answer = request.form['answer' + str(i + 1)]
            answers[f'Question {i+1}'] = {
                'selected': selected,
                'answer': answer
            }

            tup = (table,sequence,Qtype,user,selected,answer)
            print(tup)
            database.insert_choiceQ(tup)

        return jsonify({'message': 'Answers submitted successfully', 'answers': answers})
    else:
        return jsonify({'message': 'Answers failed to submit', 'answers': answers})
    
#查询所有学生数据
@app.route('/find_stus')
def find_stus():
    # 1.查询数据库所有的学员信息
    stus = database.find_stus()
    # 2.跳转界面是携带数据
    data = {
        "stus": stus
    }
    return render_template('stu_info.html', **data)

#提交Ajax申请，调用mysql数据库，根据数据创建json文件
@app.route('/send_ajax', methods=['POST'])
def send_ajax():
    try:
        conn, cursor = database.get_conn()
        databaseName = request.form.get('database')

        histogram = {
            "graph_Name": "histogram",
            "第一类正确数量": 0,
            "第二类正确数量": 0,
            "第三类正确数量": 0,
            "第四类正确数量": 0,
            "第五类正确数量": 0
        }

        type_list = [
            {"graph_Name": "第一类", "A": 0, "B": 0, "C": 0, "D": 0},
            {"graph_Name": "第二类", "A": 0, "B": 0, "C": 0, "D": 0},
            {"graph_Name": "第三类", "A": 0, "B": 0, "C": 0, "D": 0},
            {"graph_Name": "第四类", "A": 0, "B": 0, "C": 0, "D": 0},
            {"graph_Name": "第五类", "A": 0, "B": 0, "C": 0, "D": 0}
        ]

        type_names = ["type1", "type2", "type3", "type4", "type5"]
        choices = ["A", "B", "C", "D"]
        type_labels = ["第一类", "第二类", "第三类", "第四类", "第五类"]

        for i, name in enumerate(type_names):
            for choice in choices:
                query = f"SELECT COUNT(*) FROM {databaseName} WHERE type='{name}' AND choice='{choice}'"
                cursor.execute(query)
                result = cursor.fetchone()
                number = result[0] if result else 0
                type_list[i][choice] = number

        for name, label in zip(type_names, type_labels):
            query = f"SELECT COUNT(*) FROM {databaseName} WHERE type='{name}' AND choice=answer"
            cursor.execute(query)
            result = cursor.fetchone()
            number = result[0] if result else 0
            histogram[f"{label}正确数量"] = number
            print(f"{label} {number}")

        histogram = [histogram]

        conn.close()

        # 指定相对路径
        relative_path1 = os.path.join("static/js", "data.json")
        relative_path2 = os.path.join("static/js", "data2.json")

        # 确保目录存在并保存JSON文件
        for path, data in zip([relative_path1, relative_path2], [type_list, histogram]):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=6)
        
        return jsonify({'message': 'JSON files created successfully'})
    except Exception as e:
        print(e)
        return jsonify({'message': f'Error creating JSON files: {e}'}), 500
    
@app.route('/manage')
def manage():
    return render_template("Manage.html")

#教师将学生添加到对应的课程
@app.route('/manage_student', methods=['POST','GET'])
def manage_student():
    studentID = request.values.get("studentID")
    teacherID = request.values.get("teacherID")
    course = request.values.get("course")
    tup = (studentID,course,teacherID)
    print(tup)
    database.insert_manage_stud(tup)






@app.route('/hw_confirm',methods=['POST','GET'])
def hwcf():
    question = request.form["question"]
    course = request.form["course"]
    cookie = request.form["cookie"]
    type = request.form["type"]
    answer = request.form['answer']
    conn, cursor = database.get_conn()
    sql = f'insert into hw_Confirm values({cookie},{course},{type},{answer})'
    count = cursor.execute(sql)
    # 提交事务
    conn.commit()
    # 释放资源
    database.close(conn, cursor)


#调取在 type 文件夹下的文件
#习题1
@app.route('/quiz1')
def menu_quiz1():
    return render_template("type/quiz1/quiz1.html")

@app.route('/quiz1_video')
def menu_video1():
    return render_template("type/quiz1/video.html")

@app.route('/quiz1_ppt')
def menu_ppt1():
    return render_template("type/quiz1/ppt.html")

@app.route('/quiz1_textbook')
def menu_textbook1():
    return render_template("type/quiz1/textbook.html")   

@app.route('/quiz1_type1')
def quiz1_type1():
    return render_template("type/quiz1/type1.html")

@app.route('/quiz1_type2')
def quiz1_type2():
    return render_template("type/quiz1/type2.html")

@app.route('/quiz1_type3')
def quiz1_type3():
    return render_template("type/quiz1/type3.html")

@app.route('/quiz1_type4')
def quiz1_type4():
    return render_template("type/quiz1/type4.html")

@app.route('/quiz1_type5')
def quiz1_type5():
    return render_template("type/quiz1/type5.html")

@app.route('/quiz1_Question')
def quiz1_question():
    return render_template("type/quiz1/Question.html")

@app.route('/statistic1')
def graph1():
    return render_template("type/quiz1/graph.html")



#习题2
@app.route('/quiz2')
def menu_quiz2():
    return render_template("type/quiz2/quiz2.html")

@app.route('/quiz2_video')
def menu_video2():
    return render_template("type/quiz2/video.html")

@app.route('/quiz2_ppt')
def menu_ppt2():
    return render_template("type/quiz2/ppt.html")

@app.route('/quiz2_textbook')
def menu_textbook2():
    return render_template("type/quiz1/textbook.html") 

@app.route('/quiz2_type1')
def quiz2_type1():
    return render_template("type/quiz2/type1.html")

@app.route('/quiz2_type2')
def quiz2_type2():
    return render_template("type/quiz2/type2.html")

@app.route('/quiz2_type3')
def quiz2_type3():
    return render_template("type/quiz2/type3.html")

@app.route('/quiz2_type4')
def quiz2_type4():
    return render_template("type/quiz2/type4.html")

@app.route('/quiz2_type5')
def quiz2_type5():
    return render_template("type/quiz2/type5.html")

@app.route('/quiz2_Question')
def quiz2_question():
    return render_template("type/quiz2/Question.html")

@app.route('/statistic2')
def graph2():
    return render_template("type/quiz2/graph.html")


#习题 3 
@app.route('/quiz3')
def menu_quiz3():
    return render_template("type/quiz3/quiz3.html")

@app.route('/quiz3_video')
def menu_video3():
    return render_template("type/quiz3/video.html")

@app.route('/quiz3_ppt')
def menu_ppt3():
    return render_template("type/quiz3/ppt.html")

@app.route('/quiz3_textbook')
def menu_textbook3():
    return render_template("type/quiz1/textbook.html") 

@app.route('/quiz3_type1')
def quiz3_type1():
    return render_template("type/quiz3/type1.html")

@app.route('/quiz3_type2')
def quiz3_type2():
    return render_template("type/quiz3/type2.html")

@app.route('/quiz3_type3')
def quiz3_type3():
    return render_template("type/quiz3/type3.html")

@app.route('/quiz3_type4')
def quiz3_type4():
    return render_template("type/quiz3/type4.html")

@app.route('/quiz3_type5')
def quiz3_type5():
    return render_template("type/quiz3/type5.html")

@app.route('/quiz3_Question')
def quiz3_question():
    return render_template("type/quiz3/Question.html")

@app.route('/statistic3')
def graph3():
    return render_template("type/quiz3/graph.html")



#习题 4
@app.route('/quiz4')
def menu_quiz4():
    return render_template("type/quiz4/quiz4.html")

@app.route('/quiz4_video')
def menu_video4():
    return render_template("type/quiz4/video.html")

@app.route('/quiz4_ppt')
def menu_ppt4():
    return render_template("type/quiz4/ppt.html")

@app.route('/quiz4_textbook')
def menu_textbook4():
    return render_template("type/quiz1/textbook.html") 

@app.route('/quiz4_type1')
def quiz4_type1():
    return render_template("type/quiz4/type1.html")

@app.route('/quiz4_type2')
def quiz4_type2():
    return render_template("type/quiz4/type2.html")

@app.route('/quiz4_type3')
def quiz4_type3():
    return render_template("type/quiz4/type3.html")

@app.route('/quiz4_type4')
def quiz4_type4():
    return render_template("type/quiz4/type4.html")

@app.route('/quiz4_type5')
def quiz4_type5():
    return render_template("type/quiz4/type5.html")

@app.route('/quiz4_Question')
def quiz4_question():
    return render_template("type/quiz4/Question.html")

@app.route('/statistic4')
def graph4():
    return render_template("type/quiz4/graph.html")


#习题 5 
@app.route('/quiz5')
def menu_quiz5():
    return render_template("type/quiz5/quiz5.html")

@app.route('/quiz5_video')
def menu_video5():
    return render_template("type/quiz5/video.html")

@app.route('/quiz5_ppt')
def menu_ppt5():
    return render_template("type/quiz5/ppt.html")

@app.route('/quiz5_textbook')
def menu_textbook5():
    return render_template("type/quiz1/textbook.html") 

@app.route('/quiz5_type1')
def quiz5_type1():
    return render_template("type/quiz5/type1.html")

@app.route('/quiz5_type2')
def quiz5_type2():
    return render_template("type/quiz5/type2.html")

@app.route('/quiz5_type3')
def quiz5_type3():
    return render_template("type/quiz5/type3.html")

@app.route('/quiz5_type4')
def quiz5_type4():
    return render_template("type/quiz5/type4.html")

@app.route('/quiz5_type5')
def quiz5_type5():
    return render_template("type/quiz5/type5.html")

@app.route('/quiz5_Question')
def quiz5_question():
    return render_template("type/quiz5/Question.html")

@app.route('/statistic5')
def graph5():
    return render_template("type/quiz5/graph.html")



#习题 6 
@app.route('/quiz6')
def menu_quiz6():
    return render_template("type/quiz6/quiz6.html")

@app.route('/quiz6_video')
def menu_video6():
    return render_template("type/quiz6/video.html")

@app.route('/quiz6_ppt')
def menu_ppt6():
    return render_template("type/quiz6/ppt.html")

@app.route('/quiz6_textbook')
def menu_textbook6():
    return render_template("type/quiz1/textbook.html") 

@app.route('/quiz6_type1')
def quiz6_type1():
    return render_template("type/quiz6/type1.html")

@app.route('/quiz6_type2')
def quiz6_type2():
    return render_template("type/quiz6/type2.html")

@app.route('/quiz6_type3')
def quiz6_type3():
    return render_template("type/quiz6/type3.html")

@app.route('/quiz6_type4')
def quiz6_type4():
    return render_template("type/quiz6/type4.html")

@app.route('/quiz6_type5')
def quiz6_type5():
    return render_template("type/quiz6/type5.html")

@app.route('/quiz6_Question')
def quiz6_question():
    return render_template("type/quiz6/Question.html")

@app.route('/statistic6')
def graph6():
    return render_template("type/quiz6/graph.html")


if __name__ ==  '__main__':
    app.run()