
import re

st = '22.3333, 33.22222'
one = re.search(r'\d+\.\d+', st).group(0)
two = re.findall(r'\d+\.\d+', st)[-1]
print(one)
print(two)