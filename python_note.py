import re

li = ['#asdasd','@1241as','gaasgasv']

for i in li:
    m = re.match(r'^[^#@].*$', i)
    if m:
        print(i)