import urllib.parse
import urllib.request
import re
import json

from helper import *

sch_lim = [(5, 131114001, 131114168)]
'''sch_lim = [
    (3, 141114001, 141114172),      # ECE 3
    (5, 131114001, 131114168),      # ECE 5
    (3, 141119001, 141119078),      # MSME 3
    (5, 131119001, 131119071),      # MSME 5
    (7, 121116301, 121116365),      # CHEM 7
    (5, 131113001, 131113135),      # EE 5
    (7, 121113001, 121113115),      # EE 7
]'''
url = 'http://dolphintechnologies.in/manit/accessview.php'
data = {'scholar': '0', 'semester': '0', 'submit': 'Submit'}

with open('pattern.txt') as f:
    pattern = f.read()

res_data = []

for tpl in sch_lim:
    data['semester'] = str(tpl[0])
    for sch_no in range(*tpl[1:]):
        data['scholar'] = str(sch_no)
        post = bytes(urllib.parse.urlencode(data), 'utf-8')
        html_doc = urllib.request.urlopen(url, post).read().decode()
        reg_match = re.match(pattern, html_doc, re.DOTALL)
        if not reg_match:
            continue
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
            continue

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
        print(sch_no)

with open('data.js', 'w') as f:
    f.write('data = ' + json.dumps(res_data))
