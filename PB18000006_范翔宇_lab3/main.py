import functools

from flask import Flask, session
from flask import redirect
from flask import request, make_response
from flask import render_template
from flask import url_for
from flask import jsonify

from db import *
from check import *

# 生成一个app
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'lab3'

# 对app执行请求页面地址到函数的绑定
@app.route("/", methods=("GET", "POST"))
def initpage():
    return redirect(url_for('home'))

@app.route("/home", methods = ("GET", "POST"))
def home():
    if request.method == "POST":
        if 'accountManage' in request.form:
            return redirect(url_for('accountManage'))
        elif 'customerManage' in request.form:
            return redirect(url_for('customerManage'))
        elif 'loanManage' in request.form:
            return redirect(url_for('loanManage'))
        elif 'statistics' in request.form:
            return redirect(url_for('statistics'))
    else:
        return render_template("home.html")




#账户管理
@app.route("/accountManage/", methods = ("GET", "POST"))
def accountManage():
    data_check = dbfunc ('select * from checkaccounts')
    data_save=dbfunc('select * from saveaccounts')
    data = data_check + data_save
    print(data)
    return render_template ('accountManage.html',userlist_check=data_check,userlist_save=data_save)

#返回到增加界面
@app.route ("/addAcc/")
def adAcc():
    return render_template ('addAcc.html')

#查询账户
@app.route("/searchAcc/", methods = ("GET", "POST"))
def searchAcc():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        accountID = delSpace(str(data['accountID']))
        cusID = delSpace(str(data['cusID']))
        bank = str(data['bank'])
        #输入检查
        if accountID != "" and not accIDcheck(accountID):
            return '<script>alert("账户号输入有误");location.href="/searchAcc";</script>'
        if cusID != "" and not IDcheck(cusID):
            return '<script>alert("客户身份证号输入有误");location.href="/searchAcc";</script>'
        flag = 0    
        sql_check = "select * from checkaccounts where "
        sql_save = "select * from saveaccounts where "
        if(cusID != ""):
            flag = 1
            sql_check = sql_check + "cusID='" + cusID + "'"
            sql_save = sql_save + "cusID='" + cusID + "'"
        if(accountID != "" and flag == 1):
            sql_check = sql_check + " and accountID='" + accountID + "'"
            sql_save = sql_save + " and accountID='" + accountID + "'"
        elif(accountID != ""):
            flag = 1
            sql_check = sql_check + "accountID='" + accountID + "'"
            sql_save = sql_save + "accountID='" + accountID + "'"
        if(bank != "" and flag == 1):
            sql_check = sql_check + " and bank='" + bank + "'"
            sql_save = sql_save + " and bank='" + bank + "'"
        elif(bank != ""):
            flag = 1
            sql_check = sql_check + "bank='" + bank + "'"
            sql_save = sql_save + "bank='" + bank + "'"
        if(flag == 1):
            data_check = dbfunc (sql_check)
            data_save = dbfunc (sql_save)
            if not (data_check or data_save):
                return '<script>alert("查无此账户");location.href="/searchAcc";</script>'
            else:
                return render_template ('searchAcc.html',userlist_check=data_check,userlist_save=data_save)
        else:
            return '<script>alert("请输入至少一个帐户信息");location.href="/searchAcc";</script>'
    else:
        return render_template("searchAcc.html")

#增加帐户
@app.route ("/addsacc/",methods=("GET", "POST"))  # 注意post大写,因为post是通过form.data传数据所以下面用request.form
def addsacc():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        accountID = delSpace(str(data['accountID']))
        money = delSpace(str(data['money']))
        settime = delSpace(str(data['settime']))
        accounttype = str(data['accounttype'])
        bank = str(data['bank'])
        cusID = (delSpace(str(data['cusID']))).split(";")
        visit = delSpace(str(data['settime']))
        interestrate = delSpace(str(data['interestrate']))
        savetype = delSpace(str(data['savetype']))
        overdraft = delSpace(str(data['overdraft']))
        #输入检测
        if accountID != "" and not accIDcheck(accountID):
            return '<script>alert("账户号输入有误");location.href="/addAcc";</script>'
        if settime != "" and not datecheck(settime):
            return '<script>alert("日期输入有误");location.href="/addAcc";</script>'
        if(money == ""):
            return '<script>alert("余额不能为空");location.href="/addAcc";</script>'
        elif(float(money) < 0):
            return '<script>alert("余额不能为负");location.href="/addAcc";</script>'
        for i in range(len(cusID)):
            if(cusID[i] != ""):
                if cusID != "" and not IDcheck(cusID[i]):
                    return '<script>alert("客户身份证号输入有误");location.href="/addAcc";</script>'
                cusData = dbfunc("select cusID from customer where cusID = '" + cusID[i] + "'")
                if(len(cusData) == 0):
                    return '<script>alert("存在不在系统中的客户");location.href="/addAcc";</script>'
        if(accounttype == "save"):
            sqlAccounts = "insert into accounts values ("
            if(accountID != ""):
                sqlAccounts = sqlAccounts + "'" + accountID + "',"
            else:
                return '<script>alert("添加失败，账户号不能为空");location.href="/addAcc";</script>'
            if(money != ""):
                sqlAccounts = sqlAccounts + money + ","
            else:
                return '<script>alert("添加失败，余额不能为空");location.href="/addAcc";</script>'
            if(settime != ""):
                sqlAccounts = sqlAccounts + "'" + settime + "',"
            else:
                return '<script>alert("添加失败，开户日期不能为空");location.href="/addAcc";</script>'
            sqlAccounts = sqlAccounts + "'save')"
            print(sqlAccounts)
            resAccounts = dbfunc (sqlAccounts,m='w')
            if resAccounts:
                sqlSaveacc = "insert into saveacc values (" 
                sqlSaveacc = sqlSaveacc + "'" + accountID + "',"
                if(interestrate != ""):
                    sqlSaveacc = sqlSaveacc + "" + interestrate + ","
                else:
                    sqlSaveacc = sqlSaveacc + "null,"
                if(savetype != ""):
                    sqlSaveacc = sqlSaveacc + "'" + savetype + "')"
                else:
                    sqlSaveacc = sqlSaveacc + "null" + ")"
                print(sqlSaveacc)
                resSaveacc = dbfunc(sqlSaveacc,m='w')
                if resSaveacc:
                    for i in range(len(cusID)):
                        sqlCusforacc = "insert into cusforacc values (" 
                        sqlCusforacc = sqlCusforacc + "'" + accountID + "',"
                        if(bank != ""):
                            sqlCusforacc = sqlCusforacc + "'" + bank + "',"
                        else:
                            return '<script>alert("添加失败，开户银行不能为空");location.href="/addAcc";</script>'
                        if(cusID[i] != ""):
                            sqlCusforacc = sqlCusforacc + "'" + cusID[i] + "',"
                        else:
                            return '<script>alert("添加失败，客户身份证号不能为空");location.href="/addAcc";</script>'
                        if(visit != ""):
                            sqlCusforacc = sqlCusforacc + "'" + visit + "',"
                        else:
                            sqlCusforacc = sqlCusforacc + "null,"
                        sqlCusforacc = sqlCusforacc + "'save')"
                        resCusforacc = dbfunc(sqlCusforacc,m='w')
                        if not resCusforacc:
                            dbfunc("delete from accounts where accountID = '" + accountID + "'",m='w')
                            dbfunc("delete from saveacc where accountID = '" + accountID + "'",m='w')
                            dbfunc("delete from cusforacc where accountID = '" + accountID + "'",m='w')
                            return '<script>alert("添加失败，请检查输入");location.href="/addAcc";</script>'
                    return '<script>alert("添加成功");location.href="/accountManage";</script>'
                else:
                    delet = dbfunc("delete from accounts where accountID = '" + accountID + "'",m='w')
                    if(delet):
                        print("delete accounts")
                    return '<script>alert("添加失败，请检查输入");location.href="/addAcc";</script>' 
            else:
                return '<script>alert("添加失败，请检查输入");location.href="/addAcc";</script>'
        elif(accounttype == "check"):
            sqlAccounts = "insert into accounts values ("
            if(accountID != ""):
                sqlAccounts = sqlAccounts + "'" + accountID + "',"
            else:
                return '<script>alert("添加失败，账户号不能为空");location.href="/addAcc";</script>'
            if(money != ""):
                sqlAccounts = sqlAccounts + money + ","
            else:
                return '<script>alert("添加失败，余额不能为空");location.href="/addAcc";</script>'
            if(settime != ""):
                sqlAccounts = sqlAccounts + "'" + settime + "',"
            else:
                return '<script>alert("添加失败，开户日期不能为空");location.href="/addAcc";</script>'
            sqlAccounts = sqlAccounts + "'check')"
            print(sqlAccounts)
            resAccounts = dbfunc (sqlAccounts,m='w')
            if resAccounts:
                sqlCheckacc = "insert into checkacc values (" 
                sqlCheckacc = sqlCheckacc + "'" + accountID + "',"
                if(overdraft != ""):
                    sqlCheckacc = sqlCheckacc + overdraft + ")"
                else:
                    sqlCheckacc = sqlCheckacc + "null" + ")"
                print(sqlCheckacc)
                resCheckacc = dbfunc(sqlCheckacc,m='w')
                if resCheckacc:
                    for i in range(len(cusID)):
                        sqlCusforacc = "insert into cusforacc values (" 
                        sqlCusforacc = sqlCusforacc + "'" + accountID + "',"
                        if(bank != ""):
                            sqlCusforacc = sqlCusforacc + "'" + bank + "',"
                        else:
                            return '<script>alert("添加失败，开户银行不能为空");location.href="/addAcc";</script>'
                        if(cusID[i] != ""):
                            sqlCusforacc = sqlCusforacc + "'" + cusID[i] + "',"
                        else:
                            return '<script>alert("添加失败，客户身份证号不能为空");location.href="/addAcc";</script>'
                        if(visit != ""):
                            sqlCusforacc = sqlCusforacc + "'" + visit + "',"
                        else:
                            sqlCusforacc = sqlCusforacc + "null,"
                        sqlCusforacc = sqlCusforacc + "'check')"
                        resCusforacc = dbfunc(sqlCusforacc,m='w')
                        if not resCusforacc:
                            dbfunc("delete from accounts where accountID = '" + accountID + "'",m='w')
                            dbfunc("delete from saveacc where accountID = '" + accountID + "'",m='w')
                            dbfunc("delete from cusforacc where accountID = '" + accountID + "'",m='w')
                            return '<script>alert("添加失败，请检查输入");location.href="/addAcc";</script>'
                    return '<script>alert("添加成功");location.href="/accountManage";</script>'
                else:
                    delet = dbfunc("delete from accounts where accountID = '" + accountID + "'",m='w')
                    if(delet):
                        print("delete accounts")
                    return '<script>alert("添加失败，请检查输入");location.href="/addAcc";</script>' 
            else:
                return '<script>alert("添加失败，请检查输入");location.href="/addAcc";</script>'
    else:
        return render_template("addAcc.html")

# 返回到更改界面
@app.route ('/changeAcc/')
def chAcc():
    idd = request.args.get ('ID')
    print(idd)
    idd = idd[1:-1].split(',')
    print(idd)
    acc = idd[0].strip()
    typ = idd[1].strip()
    cus = idd[2].strip()
    if(typ == "'save'"):
        sql = "select * from saveaccounts where accountID=" + acc + " and cusID=" + cus
    else:
        sql = "select * from checkaccounts where accountID=" + acc + " and cusID=" + cus
    print(sql)
    data = dbfunc (sql)
    if(typ == "'save'"):
        datalist = data[0]
        print(type(datalist))
        datalist = datalist + ("",)
    else:
        datalist = data[0][:7]
        check = data[0][7]
        datalist = datalist + ("","",check)
    #客户信息列表
    data_cus = dbfunc ("select cusID,visit from cusforacc where accountID=" + acc)
    return render_template ('changeAcc.html',userlist = (datalist,),userlist_cus = data_cus)

# 检察更改的数据并更新数据库----改
@app.route ('/chasacc/',methods=("GET", "POST"))
def chasAcc():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        accountID = str(data['accountID'])
        money = delSpace(str(data['money']))
        accounttype = str(data['accounttype'])
        interestrate = delSpace(str(data['interestrate']))
        savetype = delSpace(str(data['savetype']))
        overdraft = delSpace(str(data['overdraft']))
        if(money == ""):
            return '<script>alert("余额不能为空");location.href="/accountManage";</script>'
        elif(float(money) < 0):
            return '<script>alert("余额不能为负");location.href="/accountManage";</script>'

        if(overdraft != "" and float(overdraft) < 0):
            return '<script>alert("透支额不能为负");location.href="/accountManage";</script>'

        #修改
        flag1 = 0
        flag2 = 0
        #accounts
        sql = "update accounts set money="
        sql = sql + money + " where accountID='" + accountID + "'"
        print(sql)
        res = dbfunc (sql, m='w')
        if res:
            flag1 = 1
        
        if(accounttype == "save"):
            #saveacc
            sql = "update saveacc set interestrate=" 
            if(interestrate != "" and interestrate != "None"):
                sql = sql + interestrate + ",savetype="
            else:
                sql = sql + "null,savetype="
            if(savetype != "" and savetype != "None"):
                sql = sql + "'" + savetype + "'"
            else:
                sql = sql + "null"
            sql = sql + "where accountID='" + accountID + "'"
            res = dbfunc(sql,m='w')
            if res:
                flag2 = 1
        else:
            #checkacc
            sql = "update checkacc set overdraft=" 
            if(overdraft != "" and overdraft != "None"):
                sql = sql + overdraft
            else:
                sql = sql + "null"
            sql = sql + "where accountID='" + accountID + "'"
            res = dbfunc(sql,m='w')
            if res:
                flag2 = 1
        
        if flag1 == 1 and flag2 == 1:
            return '<script>alert("余额及账户特性更新成功");location.href="/accountManage";</script>'
        elif flag1 == 1 and flag2 == 0:
            return '<script>alert("余额更新成功");location.href="/accountManage";</script>'
        elif flag1 == 0 and flag2 == 1:
            return '<script>alert("账户特性更新成功");location.href="/accountManage";</script>'
        else:
            return '<script>alert("更新失败");location.href="/accountManage";</script>'
    else:
        return render_template("changeAcc.html")


# 返回到所有者更改界面
@app.route ('/addAccCus/')
def addAccCus():
    accountID = request.args.get ('ID')
    return render_template ('addAccCus.html',userlist = accountID)

#增加所有者
@app.route ("/addsacccus/",methods=("GET", "POST"))  # 注意post大写,因为post是通过form.data传数据所以下面用request.form
def addsacccus():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        accountID = delSpace(str(data['accountID']))
        cusID = delSpace(str(data['cusID']))
        visit = delSpace(str(data['visit']))
        #tag
        accounttype = dbfunc("select accounttype from accounts where accountID='"+accountID+"'")[0][0]
        bank = dbfunc("select bank from cusforacc where accountID='"+accountID+"'")[0][0]
        #输入检测
        if cusID != "" and not IDcheck(cusID):
            return '<script>alert("账户号输入有误");location.href="/accountManage";</script>'
        if visit != "" and not datecheck(visit):
            return '<script>alert("日期输入有误");location.href="/accountManage";</script>'
        if(cusID != ""):
            cusData = dbfunc("select cusID from customer where cusID = '" + cusID + "'")
            if(len(cusData) == 0):
                return '<script>alert("不能添加不在系统中的客户");location.href="/accountManage";</script>'
        sql = "insert into cusforacc values (" 
        sql = sql + "'" + accountID + "','" + bank + "','" + cusID + "',"
        if(visit != ""):
            sql = sql + "'" + visit + "','"
        else:
            sql = sql + "null" + ",'"
        sql = sql + accounttype + "')"
        res = dbfunc(sql,m="w")
        if res:
            return '<script>alert("添加成功");location.href="/accountManage";</script>'
        else:
            return '<script>alert("添加失败");location.href="/accountManage";</script>'
    else:
        return render_template("addAccCus.html")

# 返回到所有者更改界面
@app.route ('/chAccCus/')
def chAccCus():
    idd = request.args.get ('ID')
    idd = idd[1:-1].split(',')
    accountID = idd[0].strip()
    cusID= idd[1].strip()
    sql = "select accountID,cusID,visit from cusforacc where accountID=" + accountID + "and cusID=" + cusID
    datalist = dbfunc (sql)
    print(datalist)
    return render_template ('changeAccCus.html',userlist = datalist)

# 检察更改的数据并更新数据库----改所有者
@app.route ('/chasacccus/',methods=("GET", "POST"))
def chasAccCus():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        accountID = str(data['accountID'])
        cusID = str(data['cusID'])
        visit = delSpace(str(data['visit']))

        #输入检测
        if visit != "" and not datecheck(visit):
            return '<script>alert("日期输入有误");location.href="/accountManage";</script>'

        #cusforacc
        sql = "update cusforacc set visit='"
        sql = sql + visit + "' where accountID='" + accountID + "' and cusID='" + cusID + "'"
        print(sql)
        res = dbfunc (sql, m='w')
        if res:
            return '<script>alert("最近访问日期更新成功");location.href="/accountManage";</script>'
        else:
            return '<script>alert("更新失败");location.href="/accountManage";</script>'
    else:
        return render_template("changeAccCus.html")

# 删除数据----删所有者
@app.route ('/delacccus/')
def deacccus():
    idd = request.args.get ('ID')
    idd = idd[1:-1].split(',')
    accountID = idd[0].strip()
    cusID= idd[1].strip()
    sql = "select cusID from cusforacc where accountID=" + accountID
    data = dbfunc(sql)
    if(len(data) <= 1):
        return '<script>alert("只有一个所有者，不能删除");location.href="/accountManage";</script>'
    else:
        sql = "delete from cusforacc where cusID=" + cusID + "and accountID=" + accountID
        res = dbfunc (sql,m='w')
        if res:
            return '<script>alert("删除成功");location.href="/accountManage";</script>'
        else:
            return '<script>alert("删除失败");location.href="/accountManage";</script>'

# 删除数据----删账户
@app.route ('/delacc/')
def deacc():
    accountID = request.args.get ('ID')
    print(accountID)
    sql = "delete from accounts where accountID='" + accountID + "'"
    res = dbfunc (sql,m='w')
    if res:
        return '<script>alert("删除成功");location.href="/accountManage";</script>'
    else:
        return '<script>alert("删除失败");location.href="/accountManage";</script>'





#客户管理
@app.route("/customerManage/", methods = ("GET", "POST"))
def customerManage():
    data = dbfunc ('select * from customer')
    print(data)
    return render_template ('customerManage.html',userlist=data)

#查询客户
@app.route("/searchCustom/", methods = ("GET", "POST"))
def search():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        cusID = delSpace(str(data['cusID']))
        cusname = delSpace(str(data['cusname']))
        loanres = delSpace(str(data['loanres']))
        accres = delSpace(str(data['accres']))
        #输入检测
        if cusname != "" and not namecheck(cusname):
            return '<script>alert("客户姓名输入有误");location.href="/searchCustom";</script>'
        if cusID != "" and not IDcheck(cusID):
            return '<script>alert("客户身份证号输入有误");location.href="/searchCustom";</script>'
        if loanres != "" and not IDcheck(loanres):
            return '<script>alert("贷款负责人输入有误");location.href="/searchCustom";</script>'
        if accres != "" and not IDcheck(accres):
            return '<script>alert("账户负责人输入有误");location.href="/searchCustom";</script>'

        flag = 0    
        sql = "select * from customer where "
        if(cusID != ""):
            flag = 1
            sql = sql + "cusID='" + cusID + "'"
        if(cusname != "" and flag == 1):
            sql = sql + " and cusname='" + cusname + "'"
        elif(cusname != ""):
            flag = 1
            sql = sql + "cusname=\"" + cusname + "\""
        if(loanres != "" and flag == 1):
            sql = sql + " and loanres='" + loanres + "'"
        elif(loanres != ""):
            flag = 1
            sql = sql + "loanres='" + loanres + "'"
        if(accres != "" and flag == 1):
            sql = sql + " and accres='" + accres + "'"
        elif(accres != ""):
            flag = 1
            sql = sql + "accres='" + accres + "'"
        if(flag == 1):
            data = dbfunc (sql)
            if data:
                return render_template ('searchCustom.html',userlist=data)
            else:
                return '<script>alert("查无此客户");location.href="/searchCustom";</script>'
        else:
            return '<script>alert("请输入至少一个客户信息");location.href="/searchCustom";</script>'
    else:
        return render_template("searchCustom.html")

#返回到增加界面
@app.route ("/addCustom/")
def ad():
    return render_template ('addCustom.html')

#增加客户
@app.route ("/addscus/",methods=("GET", "POST"))  # 注意post大写,因为post是通过form.data传数据所以下面用request.form
def addscus():
    if request.method == "POST":
        data = dict(request.form)
        print(str(data['cusID']))
        cusID = delSpace(str(data['cusID']))
        cusname = delSpace(str(data['cusname']))
        cusphone = delSpace(str(data['cusphone']))
        address = delSpace(str(data['address']))
        contactphone = delSpace(str(data['contactphone']))
        contactname = delSpace(str(data['contactname']))
        contactemail = delSpace(str(data['contactemail']))
        relation = delSpace(str(data['relation']))
        loanres = delSpace(str(data['loanres']))
        accres = delSpace(str(data['accres']))
        print(cusID)
        #输入检测
        if cusname != "" and not namecheck(cusname):
            return '<script>alert("客户姓名输入有误");location.href="/addCustom";</script>'
        if contactname != "" and not namecheck(contactname):
            return '<script>alert("联系人姓名输入有误");location.href="/addCustom";</script>'
        if cusID != "" and not IDcheck(cusID):
            return '<script>alert("客户身份证号输入有误");location.href="/addCustom";</script>'
        if loanres != "" and not IDcheck(loanres):
            return '<script>alert("贷款负责人身份证号输入有误");location.href="/addCustom";</script>'
        if accres != "" and not IDcheck(accres):
            return '<script>alert("账户负责人身份证号输入有误");location.href="/addCustom";</script>'

        if(loanres != ""):
            loanresData = dbfunc("select empID from employee where empID = '" + loanres + "'")
            if(len(loanresData) == 0):
                return '<script>alert("贷款负责人查无此员工");location.href="/addCustom";</script>'
        if(accres != ""):
            accresData = dbfunc("select empID from employee where empID = '" + accres + "'")
            if(len(accresData) == 0):
                return '<script>alert("账户负责人查无此员工");location.href="/addCustom";</script>'
        if(cusID == "" or cusname == "" or cusphone == "" or contactphone == "" or contactname == "" or relation == ""):
            return '<script>alert("请完善相关信息");location.href="/addCustom";</script>'
        sql = "insert into customer values ('"
        #客户姓名带单引号处理
        sql = sql + cusID + "',\"" + cusname + "\",'" + cusphone + "',"
        if(address != ""):
            sql = sql + "'" + address + "',"
        else:
            sql = sql + "null,"
        sql = sql + "'" + contactphone + "',\"" + contactname + "\","
        if(contactemail != ""):
            sql = sql + "'" + contactemail + "',"
        else:
            sql = sql + "null,"
        sql = sql + "'" + relation + "',"
        if(loanres != ""):
            sql = sql + "'" + loanres + "',"
        else:
            sql = sql + "null,"
        if(accres != ""):
            sql = sql + "'" + accres + "')"
        else:
            sql = sql + "null" + ")"
        print(sql)
        res = dbfunc (sql,m='w')
        if res:
            return '<script>alert("添加成功");location.href="/customerManage";</script>'
        else:
            return '<script>alert("添加失败，请检查输入");location.href="/addCustom";</script>'
    else:
        return render_template("addCustom.html")

# 返回到更改界面
@app.route ('/changeCustom/')
def ch():
    idd = request.args.get ('cusID')
    sql = "select * from customer where cusID='" + idd + "'"
    data = dbfunc (sql)
    return render_template ('changeCustom.html',userlist=data)

# 检察更改的数据并更新数据库----改
@app.route ('/chas/',methods=("GET", "POST"))
def chas():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        cusID = str(data['cusID'])
        cusname = delSpace(str(data['cusname']))
        cusphone = delSpace(str(data['cusphone']))
        address = delSpace(str(data['address']))
        contactphone = delSpace(str(data['contactphone']))
        contactname = delSpace(str(data['contactname']))
        contactemail = delSpace(str(data['contactemail']))
        relation = delSpace(str(data['relation']))
        loanres = delSpace(str(data['loanres']))
        accres = delSpace(str(data['accres']))

        #输入检测
        if cusID != "" and not IDcheck(cusID):
            return '<script>alert("客户身份证号输入有误");location.href="/customerManage";</script>'
        if loanres != "" and loanres != "None" and not IDcheck(loanres):
            return '<script>alert("贷款负责人身份证号输入有误");location.href="/customerManage";</script>'
        if accres != "" and accres != "None" and not IDcheck(accres):
            return '<script>alert("账户负责人身份证号输入有误");location.href="/customerManage";</script>'

        if(loanres != "" and loanres != "None"):
            loanresData = dbfunc("select empID from employee where empID = '" + loanres + "'")
            if(len(loanresData) == 0):
                return '<script>alert("贷款负责人查无此员工");location.href="/customerManage";</script>'
        if(accres != "" and accres != "None"):
            accresData = dbfunc("select empID from employee where empID = '" + accres + "'")
            if(len(accresData) == 0):
                return '<script>alert("账户负责人查无此员工");location.href="/customerManage";</script>'
        sql = "update customer set cusID='"
        sql = sql + cusID + "', cusname=\"" + cusname + "\", cusphone='" + cusphone + "', address="
        if(address != "" and address != "None"):
            sql = sql + "'" + address + "',contact_phone="
        else:
            sql = sql + "null, contact_phone="
        sql = sql + "'" + contactphone + "', contact_name=\"" + contactname + "\", contact_Email="
        if(contactemail != "" and contactemail != "None"):
            sql = sql + "'" + contactemail + "', relation="
        else:
            sql = sql + "null, relation="
        sql = sql + "'" + relation + "', loanres="
        if(loanres != "" and loanres != "None"):
            sql = sql + "'" + loanres + "', accres="
        else:
            sql = sql + "null, accres="
        if(accres != "" and accres != "None"):
            sql = sql + "'" + accres + "' "
        else:
            sql = sql + "null "
        sql = sql + "where cusID='" + cusID + "'"
        print(sql)
        res = dbfunc (sql, m='w')
        if res:
            return '<script>alert("更新成功");location.href="/customerManage";</script>'
        else:
            return '<script>alert("更新失败");location.href="/customerManage";</script>'
    else:
        return render_template("changeCustom.html")

# 删除数据----删
@app.route ('/del/')
def de():
    idd = request.args.get ('cusID')
    data_acc = dbfunc("select accountID from cusforacc where cusID='"+idd+"'")
    data_loan = dbfunc("select loanID from cusforloan where cusID='"+idd+"'")
    if(len(data_acc) != 0):
        return '<script>alert("客户存在关联账户，不可删除");location.href="/customerManage";</script>'
    if(len(data_loan) != 0):
        return '<script>alert("客户存在贷款记录，不可删除");location.href="/customerManage";</script>'
    sql = "delete from customer where cusID='" + idd + "'"
    res = dbfunc (sql,m='w')
    if res:
        return '<script>alert("删除成功");location.href="/customerManage";</script>'
    else:
        return '<script>alert("删除失败");location.href="/customerManage";</script>'



#贷款管理
@app.route("/loanManage/", methods = ("GET", "POST"))
def loanManage():
    data_loan = dbfunc ('select * from loan')
    data_cus=dbfunc('select * from cusforloan')
    data_pay = dbfunc('select * from payinfo')
    print(data_loan)
    return render_template ('loanManage.html',userlist_loan=data_loan,userlist_cus=data_cus,userlist_pay=data_pay)

#返回到增加界面
@app.route ("/addLoan/")
def adLoan():
    return render_template ('addLoan.html')

#增加贷款
@app.route ("/addsloan/",methods=("GET", "POST"))  # 注意post大写,因为post是通过form.data传数据所以下面用request.form
def addsloan():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        loanID = delSpace(str(data['loanID']))
        money = delSpace(str(data['money']))
        bank = str(data['bank'])
        cusID = (delSpace(str(data['cusID']))).split(";")

        #输入检测
        if loanID != "" and not loanIDcheck(loanID):
            return '<script>alert("贷款号输入有误");location.href="/addLoan";</script>'

        for i in range(len(cusID)):
            if(cusID[i] != ""):
                if not IDcheck(cusID[i]):
                    return '<script>alert("客户身份证号输入有误");location.href="/addLoan";</script>'
                cusData = dbfunc("select cusID from customer where cusID = '" + cusID[i] + "'")
                if(len(cusData) == 0):
                    return '<script>alert("存在不在系统中的客户");location.href="/addLoan";</script>'
        sqlLoan = "insert into loan values ("
        if(loanID != ""):
            sqlLoan = sqlLoan + "'" + loanID + "',"
        else:
            return '<script>alert("添加失败，贷款号不能为空");location.href="/addLoan";</script>'
        if(money == ""):
            return '<script>alert("添加失败，所贷金额不能为空");location.href="/addLoan";</script>'
        elif(float(money) <= 0):
            return '<script>alert("添加失败，所贷金额必须为正");location.href="/addLoan";</script>'
        else:
            sqlLoan = sqlLoan + money + ","
        sqlLoan = sqlLoan + "'" + bank + "',"
        #state
        sqlLoan = sqlLoan + "'0')"
        res = dbfunc(sqlLoan,m='w')
        if res:
            for i in range(len(cusID)):
                sqlCus = "insert into cusforloan values ("
                sqlCus = sqlCus + "'" + loanID + "',"
                if(cusID[i] != ""):
                    sqlCus = sqlCus + "'" + cusID[i] + "')"
                else:
                    return '<script>alert("添加失败，客户身份证号不能为空");location.href="/addLoan";</script>'
                res = dbfunc(sqlCus,m='w')
                if not res:
                    print(res)
                    dbfunc("delete from loan where loanID = '" + loanID + "'",m='w')
                    dbfunc("delete from cusforloan where loanID = '" + loanID + "'",m='w') 
                    return '<script>alert("添加所有者失败，请检查输入");location.href="/addLoan";</script>'
            return '<script>alert("添加成功");location.href="/loanManage";</script>'     
        else:
            return '<script>alert("添加贷款失败，请检查输入");location.href="/addLoan";</script>'       
    else:
        return render_template("addLoan.html")


#返回到发放界面
@app.route ("/addPay/")
def adPay():
    return render_template ('addPay.html')

#发放贷款
@app.route ("/addspay/",methods=("GET", "POST"))  # 注意post大写,因为post是通过form.data传数据所以下面用request.form
def addspay():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        loanID = delSpace(str(data['loanID']
))
        cusID = delSpace(str(data['cusID']
))
        money = delSpace(str(data['money']
))
        paytime = delSpace(str(data['paytime']
))

        #输入检测
        if paytime != "" and not datecheck(paytime):
            return '<script>alert("发放日期输入有误");location.href="/addPay";</script>'
        if(loanID != ""):
            if not loanIDcheck(loanID):
                return '<script>alert("贷款号输入有误");location.href="/addPay";</script>'
            loanData = dbfunc("select loanID from loan where loanID = '" + loanID + "'")
            if(len(loanData) == 0):
                return '<script>alert("查无此贷款");location.href="/addPay";</script>' 
        if(cusID != ""):
            if not IDcheck(cusID):
                return '<script>alert("客户身份证号输入有误");location.href="/addPay";</script>'
            cusData = dbfunc("select cusID from cusforloan where loanID = '" + loanID + "' and cusID='"+cusID+"'")
            if(len(cusData) == 0):
                return '<script>alert("该客户不在贷款所有者中");location.href="/addPay";</script>'
        sql = "insert into payinfo values ("
        if(loanID != ""):
            sql = sql + "'" + loanID + "',"
        else:
            return '<script>alert("贷款号不能为空");location.href="/addPay";</script>'
        if(cusID != ""):
            sql = sql + "'" + cusID + "',"
        else:
            return '<script>alert("客户身份证号不能为空");location.href="/addPay";</script>'
        if(money == ""):
            return '<script>alert("发放金额不能为空");location.href="/addPay";</script>'
        elif(float(money) <= 0.0):
            return '<script>alert("发放金额必须为正");location.href="/addPay";</script>'
        else:
            sql = sql + money + ","
        if(paytime != ""):
            sql = sql + "'" + paytime + "')"
        else:
            return '<script>alert("发放日期不能为空");location.href="/addPay";</script>'
        res = dbfunc(sql,m='w')
        if not res: 
            return '<script>alert("发放贷款失败，请检查输入");location.href="/addPay";</script>'
        else:
            return '<script>alert("添加成功");location.href="/loanManage";</script>'           
    else:
        return render_template("addPay.html")

#查询贷款
@app.route("/searchLoan/", methods = ("GET", "POST"))
def searchLoan():
    if request.method == "POST":
        data = dict (request.form)
        print (data)
        loanID = delSpace(str(data['loanID']
))
        cusID = delSpace(str(data['cusID']
))
        bank = str(data['bank']
)
        state = str(data['state']
)
        flag = 0  

        #输入检测
        if loanID != "" and not loanIDcheck(loanID):
            return '<script>alert("贷款号输入有误");location.href="/searchLoan";</script>'
        if cusID != "" and not IDcheck(cusID):
            return '<script>alert("客户身份证号输入有误");location.href="/searchLoan";</script>'

        #loan 
        sql = "select loanID from loan where "
        if(loanID != ""):
            flag = 1
            sql = sql + "loanID = '"+loanID+"'" 
        if(bank != "" and flag == 1):
            sql = sql + " and bank='" + bank + "'"
        elif(bank != ""):
            flag = 1
            sql = sql + "bank='" + bank + "'"
        if(state != "" and flag == 1):
            sql = sql + " and state='" + state + "'"
        elif(state != ""):
            flag = 1
            sql = sql + "state='" + state + "'"
        if(flag == 1):
            data1 = dbfunc (sql)
            if not data1:
                return '<script>alert("查无此贷款");location.href="/searchLoan";</script>'
        else:
            data1 = ()
        #cusforloan
        flag2 = 0
        if(cusID != ""):
            flag2 = 1
            sql = "select loanID from cusforloan where cusID='" + cusID + "'"
            data2 = dbfunc (sql)
            if not data2:
                return '<script>alert("查无此贷款");location.href="/searchLoan";</script>'
        else:
            data2 = ()
        print(data1)
        print(data2)
        ID = []
        if(flag == 0 and flag2 == 0):
            return '<script>alert("请输入至少一个贷款信息");location.href="/searchLoan";</script>'
        elif(flag == 1 and flag2 == 1):
            for i in range(len(data1)):
                for j in range(len(data2)):
                    if(data1[i] == data2[j]):
                        ID.append(data1[i])
        elif(flag == 1):
            for i in range(len(data1)):
                ID.append(data1[i])
        else:
            for i in range(len(data2)):
                ID.append(data2[i])
        print(ID)
        data_loan = ()
        data_cus = ()
        data_pay = ()
        for i in range(len(ID)):
            data_loan = data_loan + dbfunc("select * from loan where loanID='"+ID[i][0]
+"'")
            data_cus = data_cus + dbfunc("select * from cusforloan where loanID='"+ID[i][0]
+"'")
            data_pay = data_pay + dbfunc("select * from payinfo where loanID='"+ID[i][0]
+"'")
        print(data_loan)
        print(data_cus)
        print(data_pay)
        if not (data_loan or data_cus or data_pay):
            return '<script>alert("查无此贷款");location.href="/searchLoan";</script>'
        else:
            return render_template ('searchLoan.html',userlist_loan=data_loan,userlist_cus=data_cus,userlist_pay=data_pay)
    else:
        return render_template("searchLoan.html")


# 删除数据----删发放
@app.route ('/delloan/')
def deloan():
    loanID = request.args.get ('ID')
    print(loanID)
    sql = "delete from loan where loanID='" + loanID + "'"
    res = dbfunc (sql,m='w')
    if res:
        return '<script>alert("删除成功");location.href="/loanManage";</script>'
    else:
        return '<script>alert("删除失败");location.href="/loanManage";</script>'



#业务统计
@app.route("/statistics/", methods = ("GET", "POST"))
def statistics():
    if request.method == "POST":
        data = dict (request.form)
        year = delSpace(str(data['year']
))
        #输入检测
        if(year == ""):
            return '<script>alert("年份不能为空");location.href="/statistics";</script>'
        elif not checkYear(year):
            return '<script>alert("年份输入有误，请输入4位数字作为年份");location.href="/statistics";</script>'

        startlist=[year,"01","01"]
        endlist=[year,"12","31"]
        #year
        startdate = startlist[0] + "-" + startlist[1] + "-" + startlist[2]
        enddate = endlist[0] + "-" + endlist[1] + "-" + endlist[2]
        loan_year,save_year = dbcount(startdate,enddate)
        #season
        start_mon = ["01","04","07","10"]
        end_mon = ["03","06","09","12"]
        end_day = ["31","30","30","31"]
        loan_season=[[],[],[],[]]
        save_season=[[],[],[],[]]
        for i in range(4):
            startlist = [year,start_mon[i],"01"]
            endlist = [year,end_mon[i],end_day[i]]
            startdate = startlist[0] + "-" + startlist[1] + "-" + startlist[2]
            enddate = endlist[0] + "-" + endlist[1] + "-" + endlist[2]
            loan_season[i],save_season[i] = dbcount(startdate,enddate)
        #month
        month=["01","02","03","04","05","06","07","08","09","10","11","12"]
        loan_month=[[],[],[],[],[],[],[],[],[],[],[],[]]
        save_month=[[],[],[],[],[],[],[],[],[],[],[],[]]
        for i in range(12):
            if(month[i] == "04" or month[i] == "06" or month[i] == "09" or month[i] == "11"):
                endday = "30"
            elif(month[i] == "02" and leapYear(year)):
                endday = "29"
            elif(month[i] == "02" and not leapYear(year)):
                endday = "28"
            else:
                endday = "31"
            startlist = [year,month[i],"01"]
            endlist = [year,month[i],endday]
            startdate = startlist[0] + "-" + startlist[1] + "-" + startlist[2]
            enddate = endlist[0] + "-" + endlist[1] + "-" + endlist[2]
            loan_month[i],save_month[i] = dbcount(startdate,enddate)

        #year
        ly=[["Beijing branch",0,0],["Shanghai branch",0,0],["Hefei branch",0,0]]
        sy=[["Beijing branch",0,0],["Shanghai branch",0,0],["Hefei branch",0,0]]
        if(len(loan_year) != 0):
            for i in range(len(loan_year)):
                for j in range(3):
                    #tag
                    if(loan_year[i][0] == ly[j][0]):
                        ly[j][1] = loan_year[i][1]
                        ly[j][2] = loan_year[i][2]
        if(len(save_year)!=0):
            for i in range(len(save_year)):
                for j in range(3):
                    if(save_year[i][0] == sy[j][0]):
                        sy[j][1] = save_year[i][1]
                        sy[j][2] = save_year[i][2]
        #season
        lsm=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        lsc=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        ssm=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        ssc=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        for i in range(4):
            for j in range(3):
                if(len(loan_season[i])!=0):
                    for k in range(len(loan_season[i])):
                        if(loan_season[i][k][0] == lsm[j][0]):
                            lsm[j][i+1]=loan_season[i][k][1]
                            lsc[j][i+1]=loan_season[i][k][2]
        for i in range(4):
            for j in range(3):
                if(len(save_season[i])!=0):
                    for k in range(len(save_season[i])):
                        if(save_season[i][k][0] == ssm[j][0]):
                            ssm[j][i+1]=save_season[i][k][1]
                            ssc[j][i+1]=save_season[i][k][2]
        #month
        lmm=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        lmc=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        smm=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        smc=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        for i in range(12):
            for j in range(3):
                if(len(loan_month[i])!=0):
                    for k in range(len(loan_month[i])):
                        if(loan_month[i][k][0] == lmm[j][0]):
                            lmm[j][i+1]=loan_month[i][k][1]
                            lmc[j][i+1]=loan_month[i][k][2]
        for i in range(12):
            for j in range(3):
                if(len(save_month[i])!=0):
                    for k in range(len(save_month[i])):
                        if(save_month[i][k][0] == smm[j][0]):
                            smm[j][i+1]=save_month[i][k][1]
                            smc[j][i+1]=save_month[i][k][2]

        return render_template ('statistics.html',ly=ly,sy=sy,lsm=lsm,lsc=lsc,ssm=ssm,ssc=ssc,lmm=lmm,lmc=lmc,smm=smm,smc=smc)
    else:
        return render_template("statistics.html")


@app.route("/chart/", methods = ("GET", "POST"))
def chart():
    if request.method == "POST":
        data = dict (request.form)
        year = delSpace(str(data['year']))
        #输入检测
        if(year == ""):
            return '<script>alert("年份不能为空");location.href="/chart";</script>'
        elif not checkYear(year):
            return '<script>alert("年份输入有误，请输入4位数字作为年份");location.href="/chart";</script>'

        startlist=[year,"01","01"]
        endlist=[year,"12","31"]
        #season
        start_mon = ["01","04","07","10"]
        end_mon = ["03","06","09","12"]
        end_day = ["31","30","30","31"]
        loan_season=[[],[],[],[]]
        save_season=[[],[],[],[]]
        for i in range(4):
            startlist = [year,start_mon[i],"01"]
            endlist = [year,end_mon[i],end_day[i]]
            startdate = startlist[0] + "-" + startlist[1] + "-" + startlist[2]
            enddate = endlist[0] + "-" + endlist[1] + "-" + endlist[2]
            loan_season[i],save_season[i] = dbcount(startdate,enddate)
        #month
        month=["01","02","03","04","05","06","07","08","09","10","11","12"]
        loan_month=[[],[],[],[],[],[],[],[],[],[],[],[]]
        save_month=[[],[],[],[],[],[],[],[],[],[],[],[]]
        for i in range(12):
            if(month[i] == "04" or month[i] == "06" or month[i] == "09" or month[i] == "11"):
                endday = "30"
            elif(month[i] == "02" and leapYear(year)):
                endday = "29"
            elif(month[i] == "02" and not leapYear(year)):
                endday = "28"
            else:
                endday = "31"
            startlist = [year,month[i],"01"]
            endlist = [year,month[i],endday]
            startdate = startlist[0] + "-" + startlist[1] + "-" + startlist[2]
            enddate = endlist[0] + "-" + endlist[1] + "-" + endlist[2]
            loan_month[i],save_month[i] = dbcount(startdate,enddate)

        #season
        lsm=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        lsc=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        ssm=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        ssc=[["Beijing branch",0,0,0,0],["Shanghai branch",0,0,0,0],["Hefei branch",0,0,0,0]]
        for i in range(4):
            for j in range(3):
                if(len(loan_season[i])!=0):
                    for k in range(len(loan_season[i])):
                        if(loan_season[i][k][0] == lsm[j][0]):
                            lsm[j][i+1]=loan_season[i][k][1]
                            lsc[j][i+1]=loan_season[i][k][2]
        for i in range(4):
            for j in range(3):
                if(len(save_season[i])!=0):
                    for k in range(len(save_season[i])):
                        if(save_season[i][k][0] == ssm[j][0]):
                            ssm[j][i+1]=save_season[i][k][1]
                            ssc[j][i+1]=save_season[i][k][2]
        #month
        lmm=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        lmc=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        smm=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        smc=[["Beijing branch",0,0,0,0,0,0,0,0,0,0,0,0],
        ["Shanghai branch",0,0,0,0,0,0,0,0,0,0,0,0],["Hefei branch",0,0,0,0,0,0,0,0,0,0,0,0]]
        for i in range(12):
            for j in range(3):
                if(len(loan_month[i])!=0):
                    for k in range(len(loan_month[i])):
                        if(loan_month[i][k][0] == lmm[j][0]):
                            lmm[j][i+1]=loan_month[i][k][1]
                            lmc[j][i+1]=loan_month[i][k][2]
        for i in range(12):
            for j in range(3):
                if(len(save_month[i])!=0):
                    for k in range(len(save_month[i])):
                        if(save_month[i][k][0] == smm[j][0]):
                            smm[j][i+1]=save_month[i][k][1]
                            smc[j][i+1]=save_month[i][k][2]
        #去头
        lsm=[lsm[0][1:],lsm[1][1:],lsm[2][1:]]
        lsc=[lsc[0][1:],lsc[1][1:],lsc[2][1:]]
        lmm=[lmm[0][1:],lmm[1][1:],lmm[2][1:]]
        lmc=[lmc[0][1:],lmc[1][1:],lmc[2][1:]]
        ssm=[ssm[0][1:],ssm[1][1:],ssm[2][1:]]
        ssc=[ssc[0][1:],ssc[1][1:],ssc[2][1:]]
        smm=[smm[0][1:],smm[1][1:],smm[2][1:]]
        smc=[smc[0][1:],smc[1][1:],smc[2][1:]]

        return render_template ('chart.html',lsm=lsm,lsc=lsc,ssm=ssm,ssc=ssc,lmm=lmm,lmc=lmc,smm=smm,smc=smc)
    else:
        return render_template("chart.html")






#测试模块
@app.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        # 客户端在login页面发起的POST请求
        username = request.form["username"]
        password = request.form["password"]
        ipaddr   = request.form["ipaddr"]
        database = request.form["database"]

        db = db_login(username, password, ipaddr, database)

        if db == None:
            return render_template("login_fail.html")
        else:
            session['username'] = username
            session['password'] = password
            session['ipaddr'] = ipaddr
            session['database'] = database

            return redirect(url_for('table'))
    else :
        # 客户端GET 请求login页面时
        return render_template("login.html")

# 请求url为host/table的页面返回结果
@app.route("/table", methods=(["GET", "POST"]))
def table():
    # 出于简单考虑，每次请求都需要连接数据库，可以尝试使用其它context保存数据库连接
    if 'username' in session:
        db = db_login(session['username'], session['password'], 
                        session['ipaddr'], session['database'])
    else:
        return redirect(url_for('login'))
    
    tabs = db_showtable(db)

    db_close(db)
    if request.method == "POST":
        if 'clear' in request.form:
            return render_template("table.html", rows = '', dbname=session['database'])
        elif 'search' in request.form:
            return render_template("table.html", rows = tabs, dbname=session['database'])

    else:
        return render_template("table.html", rows = tabs, dbname=session['database'])



#返回不存在页面的处理
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":

    app.run(host = "0.0.0.0", debug=True)