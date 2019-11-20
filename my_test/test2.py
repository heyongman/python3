from __future__ import print_function

str0 = '\u201c'
s = '\u4eba\u751f\u82e6\u77ed\uff0cpy\u662f\u5cb8'
s = s.decode('unicode_escape')
print(s)

s1 = '\xc0\xe0\xd2\xd1\xb4\xe6\xd4\xda\xa1\xa3'
s2 = s1.decode('gb2312')
print(s2)
