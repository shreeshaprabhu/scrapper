import urllib.parse
import urllib.request
import re
import json
import threading

from helper import *

# scholar number range and POST details
''' sch_lim = [(5, 131114001, 131114168)] '''
sch_lim = [
    (3, 141114001, 141114172),      # ECE 3
    (5, 131114001, 131114168),      # ECE 5
    (7, 121114001, 121114149),      # ECE 7
    (3, 141119001, 141119078),      # MSME 3
    (5, 131119001, 131119071),      # MSME 5
    (3, 141117001, 141117093),      # CHEM 3
    (5, 131117001, 131117070),      # CHEM 5
    (7, 121116301, 121116365),      # CHEM 7
    (5, 131113001, 131113135),      # EE 5
    (7, 121113001, 121113115),      # EE 7
    (5, 131116001, 131116111),      # ME 5 (I)
    (5, 131116201, 131116303),      # ME 5 (II)
]
url = 'http://dolphintechnologies.in/manit/accessview.php'

# Maximum number of thread
THREAD_LIMIT = 20


# initialization method
def prepare():
    # regex pattern for extracting data from HTML
    with open('pattern.txt') as f:
        pattern = f.read()
    global dfa
    dfa = re.compile(pattern, re.DOTALL)

    # data.min.json for storing processed data
    with open('data.min.json', 'a') as f:
        pass
    global res_data
    with open('data.min.json') as f:
        read_data = f.read()
    if read_data:
        res_data = json.loads(read_data)
        print(len(res_data))
    else:
        res_data = []

    # mark already read results by Scholar number
    global read_sch_no
    read_sch_no = set()
    for res in res_data:
        read_sch_no.add(int(res['sch_no']))


# method to dump data into json files
def finish():
    # indented json
    with open('data.pretty.json', 'w') as f:
        f.write(json.dumps(res_data, indent=4))
    # json
    with open('data.min.json', 'w') as f:
        f.write(json.dumps(res_data))
    # json
    with open('data.js', 'w') as f:
        f.write('data = ' + json.dumps(res_data))


# a method that retrieves and processes result of one student
def fetch_result(sem, sch_no):
    print(sch_no)
    data = {'scholar': str(sch_no), 'semester': str(sem), 'submit': 'Submit'}
    post = bytes(urllib.parse.urlencode(data), 'utf-8')

    try:
        html_doc = urllib.request.urlopen(url, post).read().decode()
    except:
        print('Failed to connect', sch_no)
        return

    reg_match = dfa.match(html_doc)
    if not reg_match:
        return

    rg = reg_match.group
    course = get_course(rg(2))
    semester = get_sem(rg(4))
    branch = get_branch(rg(6))
    month_year = get_month_year(rg(8))
    name = get_name(rg(10))
    status = get_status(rg(12))
    sch_no = get_sch_no(rg(14))
    sub_code = get_sub_code(rg(18))
    sub_name = get_sub_name(rg(20))
    credit = get_credit(rg(22))
    credit_earned = get_credit_earned(rg(24))
    grade_points = get_pointer(rg(26))
    grade = get_grade(rg(28))
    sgpa = get_sgpa(rg(30))
    cgpa = get_cgpa(rg(32))
    result = get_result(rg(34))

    res = {
        'course': course,
        'semester': semester,
        'branch': branch,
        'month_year': month_year,
        'name': name,
        'status': status,
        'sch_no': sch_no,
        'subjects': [],
        'sgpa': sgpa,
        'cgpa': cgpa,
        'result': result
    }

    l = len(sub_code)
    if not l == len(sub_name) == len(credit) == len(credit_earned) == len(grade_points) == len(grade):
        return

    for i in range(l):
        sub = {
            'code': sub_code[i],
            'name': sub_name[i],
            'credit': credit[i],
            'credit_earned': credit_earned[i],
            'grade_points': grade_points[i],
            'grade': grade[i]
        }
        res['subjects'].append(sub)

    res_data.append(res)
    print('*', sch_no)


def main():
    prepare()

    try:
        for tpl in sch_lim:
            for sch_no in range(*tpl[1:]):
                if sch_no in read_sch_no:
                    continue
                # fetch_result(tpl[0], sch_no)
                while threading.active_count() >= THREAD_LIMIT:
                    pass
                threading.Thread(target=fetch_result, args=(tpl[0], sch_no), name='ResultFetcher').start()
        while threading.active_count() > 1:
            done = True
            for thread in threading.enumerate():
                if thread.name == 'ResultFetcher':
                    done = False
            if done:
                break
    finally:
        finish()

if __name__ == '__main__':
    main()
