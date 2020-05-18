#____________________ FONCTIONS DE DATES _______________________________________
import time

def is_leap_year(y):
    return (y % 4 == 0) and (y % 100 != 0 or y % 400 == 0)

def days_of_year(y):
    if is_leap_year(y): return 366
    return 365

def day_table(y):
    if is_leap_year(y): return [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else: return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def str_to_tup(s):
    if s == "": return time.localtime()[:3]
    else:
        d = int(s[:2])
        m = int(s[3:5])
        y = int(s[6:10])
        return y,m,d

def tup_to_str(tup):
    if tup == (0, 0, 0): tup = time.localtime()[:3]
    y, m, d = tup
    d = str(d)
    m = str(m)
    y = str(y)
    if len(d) < 2 : d = "0"+d
    if len(m) < 2 : m = "0"+m
    return "%s-%s-%s" % (d,m,y)

def to_delphi_date(tup):
    if tup == (0, 0, 0): tup = time.localtime()[:3]
    y, m, d = tup
    days = day_table(y)
    if (y >= 1) and (y <= 9999) and (m >= 1) and (m <= 12) and (d >= 1) and (d <= days[m - 1]):
        for i in range(m - 1): d += days[i]
        i = y - 1
        return i * 365 + i / 4 - i / 100 + i / 400 + d - 693594
    return 0

def from_delphi_date(serial):
    serial = int(serial)
    if serial > 39813:
        serial -= 39813
        y = 2009
    else:
        serial -= 1
        y = 1900
    doy = days_of_year(y)
    while serial > doy:
        serial -= doy
        y += 1
        doy = days_of_year(y)

    days = day_table(y)
    m = 1
    days_of_month = days[m - 1]
    while serial > days_of_month:
        serial -= days_of_month
        m += 1
        days_of_month = days[m - 1]
    return y, m, serial

def days_of_month(y, m):
    return day_table(y)[m - 1]

def add_years(date, delta):
    y, m, d = date
    return y + delta, m, d

def add_days(dt, delta):
    y, m, d = dt
    d += delta
    if delta > 0:
        while d > days_of_month(y, m):
            d -= days_of_month(y, m)
            m += 1
            if m == 13: y += 1; m = 1
    else:
        while d < 1:
            m -= 1
            d += days_of_month(y, m)
            if  m == 0: y -= 1; m = 12
    return y, m, d

def add_months(date, delta):
    y, m, d = date
    KeepLast = days_of_month(y, m) == d
    m += delta
    if delta > 0:
        while m > 12: y += 1; m -= 12
    elif delta < 0:
        while m < 1: y -= 1; m += 12;

    LastDay = days_of_month(y, m)
    if KeepLast or d > LastDay: return y, m, LastDay
    else: return y, m, d

def add_to_date(dt, d, u):
    if u == 0: return add_days(dt, d)
    elif u == 1: return add_months(dt, d)
    else: return add_years(dt, d)

def day_of_week(y, m, d):
    #0=Dim, 1=Lun, ..., 6=Sam
    if m >=3: return ((23 * m) / 9 + d + 4 + y + y/4 - y/100 + y/400 - 2) % 7
    return ((23 * m) / 9 + d + 4 + y + (y-1)/4 - (y-1)/100 + (y-1)/400) % 7

def easter_date(Y):
    C = Y / 100
    H = (19 * (Y % 19) + C - (C / 4) - ((8 * C + 13) / 25) + 15) % 30
    I = ((H / 28) * (29 / (H + 1)) * ((21 - (Y % 19)) / 11) - 1) * (H / 28) + H
    R = 28 + I - (((Y / 4 + Y) + I + 2 + (C / 4) - C) % 7)
    if R <= 31: return (Y, 3, R)
    else: return (Y, 4, R - 31)

def non_working_day(dt, include): #include: DSF, D=dim, S=sam, F=Férié
    y, m, d = dt
    dw = day_of_week(y, m, d)
    if "D" in include and dw == 0: return 1
    if "S" in include and dw == 6: return 1
    if "F" in include:
        if (m, d) in [(1, 1), (5, 1), (8, 1), (7, 14), (8, 15), (11, 1), (11, 11), (12, 25)]: return 1
        E = easter_date(y)
        #Lundi de pâques, Jeudi ascension, Lundi de Pentecote
        if (y, m, d) in [add_days(E, 1), add_days(E, 39), add_days(E, 50)]: return 1
    return 0

def next_working_date(dt, include):
    while non_working_day(dt, include): dt = add_days(dt, 1)
    return dt

def previous_working_date(dt, include):
    while non_working_day(dt, include): dt = add_days(dt, -1)
    return dt

def IsDate(dt):
    try:
        y, m, d = dt
        if (m == 2) and (y % 4 == 0) and ( (y % 100 != 0) or (y % 400 == 0) ): Max = 29
        else: Max = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
        return m > 0 and m < 13 and d > 0 and d <= Max
    except:
        return 0
