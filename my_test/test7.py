import ping3
import sys

# lon1.brookfree.pw
server = ["fra1.brookfree.pw", "lon1.brookfree.pw"]
delay = []
for s in server:
    try:
        d = ping3.ping(s, timeout=2)
        delay.append(2 if d is None else d)
    except:
        print("error")
        sys.exit(0)

print(delay)
min_server = delay.index(min(delay))
print(min_server)
print("---------------------")

server1 = ['fra1.brookfree.pw:7000', 'lon1.brookfree.pw:7000']
s = 'fra1.brookfree.pw:7000'
s1 = s[0:s.index(":")]
s2 = [s[0:s.index(":")] for s in server1]
print(s2)
