def get_course(s: str):
    s = s.strip()
    return s


def get_sem(s: str):
    sem = s.strip()
    return sem


def get_branch(s: str):
    br = s.strip()
    return br


def get_month_year(s: str):
    my = s.strip().upper()
    return my


def get_name(s: str):
    n = s.strip()
    return n


def get_status(s: str):
    st = s.strip()
    return st


def get_sch_no(s: str):
    sch_no = s.strip()
    return sch_no


def get_sub_code(s: str):
    s = s.strip().split('<br />')
    sub_arr = []
    for sc in s:
        sc = sc.strip()
        if sc:
            sub_arr.append(sc)
    return sub_arr


def get_sub_name(s: str):
    s = s.strip().split('<br />')
    sub_arr = []
    for sn in s:
        sn = sn.strip()
        if sn:
            sub_arr.append(sn)
    return sub_arr


def get_credit(s: str):
    s = s.strip().split('<br /><div align=\'center\'>')
    cr_arr = []
    for cr in s:
        cr = cr.strip()
        if cr:
            cr_arr.append((cr.split('<br />'))[0])
    return cr_arr


def get_credit_earned(s: str):
    s = s.strip().split('<br />')
    cr_arr = []
    for cr in s:
        cr = cr.strip()
        if cr:
            cr_arr.append(cr)
    return cr_arr


def get_pointer(s: str):
    s = s.strip().split('<br />')
    pnt_arr = []
    for pnt in s:
        pnt = pnt.strip()
        if pnt:
            pnt_arr.append(pnt)
    return pnt_arr


def get_grade(s: str):
    s = s.strip().split('<br />')
    grd_arr = []
    for grd in s:
        grd = grd.strip()
        if grd:
            grd_arr.append(grd)
    return grd_arr


def get_sgpa(s: str):
    s = s.strip()
    return s


def get_cgpa(s: str):
    s = (s.strip().split())[0]
    return s


def get_result(s: str):
    s = s.strip()
    return s
