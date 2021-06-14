import machine
import utime
from machine import Pin, RTC, DEEPSLEEP

led = Pin(4, Pin.OUT)
cron_set = False


def blink():
    led.on()
    utime.sleep_ms(100)
    led.off()
    utime.sleep_ms(100)


def start_ap():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.active():
        sta_if.active(False)
    wlan = network.WLAN(network.AP_IF)
    if not wlan.active():
        wlan.active(True)
    print('ap info:', wlan.ifconfig())


def disconnect():
    import network
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)


def do_connect(ssid, password):
    import network
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
    while not wlan.isconnected():
        blink()
    print('sta info:', wlan.ifconfig())


def ntp_time():
    import ntptime
    ntptime.NTP_DELTA = 3155644800
    ntptime.host = 'ntp1.aliyun.com'
    ntptime.settime()


def fire():
    pin13 = Pin(13, Pin.OUT)
    try:
        pin13.on()
        utime.sleep_ms(0.2)
    except Exception as e:
        print(e)
    pin13.off()

    pin15 = Pin(15, Pin.OUT)
    try:
        pin15.on()
        utime.sleep_ms(1700)
    except Exception as e:
        print(e)
    pin15.off()
    print('fired')


def handleGetCron(socket, args):
    import ESP8266WebServer
    if ESP8266WebServer.__fileExist('cron'):
        with open('cron', 'r') as f:
            cron = f.readline()
            ESP8266WebServer.ok(socket, "200", cron)
    else:
        ESP8266WebServer.ok(socket, "200", "")


def handleCron(socket, args):
    import ESP8266WebServer
    try:
        cron = args['cron'].replace('  ', ' ').strip().split(' ')
        cron = [eval(x) for x in cron]
        cron.sort()
        if cron[0] < 10 or cron[-1] > 24*60:
            ESP8266WebServer.err(socket, "400", "Cron Out of range")
        else:
            with open('cron', 'w') as f:
                f.write(' '.join([str(x) for x in cron])+'\n')
            ESP8266WebServer.ok(socket, "200", "Success")
            global cron_set
            cron_set = True
    except Exception as e:
        ESP8266WebServer.err(socket, "500", str(e))


def handleTimeSync(socket, args):
    import ESP8266WebServer
    rtc = RTC()
    try:
        time = args['time'].split(',')
        time = tuple([int(x) for x in time])
        rtc.datetime(time)
        now = rtc.datetime()
        ESP8266WebServer.ok(socket, "200", "Success:\n%d-%d-%d %d:%d:%d" % (now[0], now[1], now[2], now[4], now[5], now[6]))
    except Exception as e:
        ESP8266WebServer.err(socket, "500", str(e))


def handleCmd(socket, args):
    import ESP8266WebServer
    if 'led' in args:
        if args['led'] == 'on':
            led.on()
        elif args['led'] == 'off':
            led.off()
        ESP8266WebServer.ok(socket, "200", "")
    else:
        ESP8266WebServer.err(socket, "400", "Bad Request")


def web_config():
    import ESP8266WebServer
    ESP8266WebServer.begin()
    ESP8266WebServer.onPath("/time", handleTimeSync)
    ESP8266WebServer.onPath("/cron", handleCron)
    ESP8266WebServer.onPath("/cmd", handleCmd)
    ESP8266WebServer.setDocPath("/")
    try:
        global cron_set
        while not cron_set:
            ESP8266WebServer.handleClient()
    except Exception as e:
        print('web_config', e)
    utime.sleep_ms(100)
    ESP8266WebServer.close()
    disconnect()
    deep_sleep()


def deep_sleep():
    with open('cron', 'r') as f:
        cron_line = f.readline()
    cron_list = cron_line.split(' ')
    cron_list = [x.strip() for x in cron_list]
    fire_list = []
    t = utime.localtime()
    for cron in cron_list:
        cron_min = eval(cron)
        if t[0] < 2021:
            print('Time sync exception', t)
        now_min = t[3] * 60 + t[4]
        if abs(now_min - cron_min) < 5:
            fire()
            fire_list.append(24*60)
        else:
            diff = cron_min - now_min
            if cron_min < now_min:
                diff += 24 * 60
            fire_list.append(diff)
    sleep_time = min(fire_list)
    print('sleep %d min,curr time:%s' % (sleep_time, str(t)))
    rtc = RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, sleep_time * 69000)
    led.off()
    machine.deepsleep()


if __name__ == '__main__':
    led.on()
    if utime.localtime()[0] < 2021:
        start_ap()
        web_config()
    else:
        utime.sleep(10)
        deep_sleep()
