import re
import requests

print(requests.get('https://maps.app.goo.gl/bcHmerv1BTfVewt56'))
print(requests.get('https://maps.app.goo.gl/bchmerv1btfvewt56'))
print('https://maps.app.goo.gl/bcHmerv1BTfVewt56' == 'https://maps.app.goo.gl/bchmerv1btfvewt56')