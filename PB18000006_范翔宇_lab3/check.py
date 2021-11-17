def delSpace(data):
    return data.strip()


def IDcheck(data):
    print(data)
    if (len(data) != 18):
        return False
    var_id = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']
    for i in range(18):
        flag = 0
        for j in range(11):
            if data[i] == var_id[j]:
                flag = 1
        if flag == 0:
            return False
    return True


def namecheck(data):
    string = "~!@#$%^&*()_+-*/<>,.‘’[]"
    for i in range(len(data)):
        print(data[i])
        for j in string:
            if data[i] == j:
                return False
    return True


def accIDcheck(data):
    if len(data) != 6:
        return False
    var_id = ['1', '0', '9', '8', '7', '6', '5', '4', '3', '2']
    for i in range(6):
        flag = 0
        for j in range(10):
            if data[i] == var_id[j]:
                flag = 1
        if flag == 0:
            return False
    return True


def loanIDcheck(data):
    if (len(data) != 4):
        return False
    var_id = ['1', '0', '9', '8', '7', '6', '5', '4', '3', '2']
    for i in range(4):
        flag = 0
        for j in range(10):
            if data[i] == var_id[j]:
                flag = 1
        if flag == 0:
            return False
    return True


def datecheck(data):
    if (len(data) != 10):
        return False
    datalist = data.split("-")
    if (len(datalist) != 3):
        return False
    # year
    if int(datalist[0]) < 0 or int(datalist[0]) > 9999:
        return False
    # month
    if int(datalist[1]) < 1 or int(datalist[1]) > 12:
        return False
    # day
    if int(datalist[2]) < 1 or int(datalist[2]) > 31:
        return False
    return True


def leapYear(year):
    year = int(year)
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True  # 整百年能被400整除的是闰年
            else:
                return False
        else:
            return True  # 非整百年能被4整除的为闰年
    else:
        return False


def checkYear(year):
    if (len(year) != 4):
        return False
    number = ['1', '0', '9', '8', '7', '6', '5', '4', '3', '2']
    for i in range(4):
        flag = 0
        for j in range(10):
            if year[i] == number[j]:
                flag = 1
        if flag == 0:
            return False
    return True
