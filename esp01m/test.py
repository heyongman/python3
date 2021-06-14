import time

cron = '120,180'.replace('  ', ' ').strip().split(' ')
cron = [eval(x) for x in cron]
cron.sort()
if cron[0] < 10 or cron[-1] > 24*60:
    print("定时范围超出限制")
else:
    with open('cron', 'w') as f:
        f.write(' '.join([str(x) for x in cron])+'\n')