import urllib.parse
import urllib.request
import re
from helper import *

url = 'http://dolphintechnologies.in/manit/accessview.php'
data = {'scholar': str(131114112), 'semester': str(5), 'submit': 'Submit'}
post = bytes(urllib.parse.urlencode(data), 'utf-8')
html_doc = urllib.request.urlopen(url, post).read().decode()
with open('pattern3.html') as f:
    pattern = f.read()

reg_match = re.match(pattern, html_doc, re.DOTALL)
rg = reg_match.group

'''g = [2, 4, 6, 8, 10, 12, 14, 18, 20, 22, 24, 26, 28, 30, 32, 34]

for i in g:
    print(reg_match.group(i))'''

print(get_course(rg(2)))
print(get_sem(rg(4)))
print(get_branch(rg(6)))
print(get_month_year(rg(8)))
print(get_name(rg(10)))
print(get_status(rg(12)))
print(get_sch_no(rg(14)))
print()
print(get_sub_code(rg(18)))
print(get_sub_name(rg(20)))
print(get_credit(rg(22)))
print(get_credit_earned(rg(24)))
print(get_pointer(rg(26)))
print(get_grade(rg(28)))
print(get_sgpa(rg(30)))
print(get_cgpa(rg(32)))
print(get_result(rg(34)))
