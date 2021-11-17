import pymysql


def db_login(user, passwd, server_addr, dbname):
    try:
        db = pymysql.connect(server_addr, user, passwd, dbname)
    except Exception as e:
        db = None

    return db


def db_showtable(db):
    cursor = db.cursor()

    cursor.execute("show tables")
    tabs = cursor.fetchall()

    res = list()

    for tab in tabs:
        cursor.execute("select count(*) from " + tab[0])
        row_cnt = cursor.fetchone()

        res.append((tab[0], row_cnt[0]))

    cursor.close()

    return res


def db_close(db):
    if db is not None:
        db.close()


## 封装SQL语句函数
def dbfunc(sql, m='r'):
    db = None
    try:
        db = pymysql.connect(host="localhost", user="root",
                             password="", db="lab3", port=3306)

    except Exception as e:
        db = None
        print(e)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        if m == 'r':
            data = cursor.fetchall()
        elif m == 'w':
            db.commit()
            data = cursor.rowcount
    except:
        data = False
        db.rollback()
    db.close()
    return data


def dbcount(startdate, enddate):
    # loan
    sql = "select bank,sum(money) as totalmoney,count(distinct cusID) as totalcus from loanstat " \
          + "where paytime <= '" + enddate + "' and paytime >= '" + startdate + "' group by bank"
    # print(sql)
    data_loan = dbfunc(sql)

    # save
    sql = "select bank,sum(money) as totalmoney,count(distinct cusID) as totalcus from savestat " \
          + "where settime <= '" + enddate + "' and settime >= '" + startdate + "' group by bank"
    data_save = dbfunc(sql)

    return data_loan, data_save


if __name__ == "__main__":
    db = db_login("root", "", "127.0.0.1", "lab3")

    tabs = db_showtable(db)

    db_close(db)
