#!/usr/bin/env python
# coding:utf-8

import os
import sys

# current_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.path.abspath("/Users/he/proj/XX-Net/code/default/launcher")
# helper_path = os.path.join(current_path, os.pardir, os.pardir, os.pardir, 'data', 'launcher', 'helper')

if __name__ == "__main__":
    python_path = os.path.abspath(os.path.join(current_path, os.pardir, 'python27', '1.0'))
    noarch_lib = os.path.abspath(os.path.join(python_path, 'lib', 'noarch'))
    sys.path.append(noarch_lib)
    osx_lib = os.path.join(python_path, 'lib', 'darwin')
    sys.path.append(osx_lib)
    extra_lib = "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC"
    sys.path.append(extra_lib)

# import config
# import module_init
import subprocess
import webbrowser

# from xlog import getLogger
# xlog = getLogger("launcher")

import AppKit
import SystemConfiguration
from PyObjCTools import AppHelper


class MacTrayObject(AppKit.NSObject):
    def __init__(self):
        pass

    def applicationDidFinishLaunching_(self, notification):
        # setupHelper()
        # loadConfig()
        self.setupUI()
        self.registerObserver()

    def setupUI(self):
        self.statusbar = AppKit.NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(
            AppKit.NSSquareStatusItemLength)  # NSSquareStatusItemLength #NSVariableStatusItemLength

        # Set initial image icon
        icon_path = os.path.join(current_path, "web_ui", "favicon-mac.ico")
        image = AppKit.NSImage.alloc().initByReferencingFile_(icon_path.decode('utf-8'))
        image.setScalesWhenResized_(True)
        image.setSize_((15, 15))
        self.statusitem.setImage_(image)

        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        self.statusitem.setToolTip_("XX-Net")

        # Get current selected mode
        proxyState = getProxyState(currentService)

        # Build a very simple menu
        self.menu = AppKit.NSMenu.alloc().initWithTitle_('XX-Net')

        menuitem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Disable GAEProxy', 'disableProxy:', '')
        # 设置为选中状态
        menuitem.setState_(AppKit.NSOnState)
        # if proxyState == 'disable':
        #     menuitem.setState_(AppKit.NSOnState)
        self.menu.addItem_(menuitem)
        # self.disableGaeProxyMenuItem = menuitem

        # Default event
        menuitem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'windowWillClose:', '')
        self.menu.addItem_(menuitem)
        # Bind it to the status item
        self.statusitem.setMenu_(self.menu)

        # Hide dock icon
        AppKit.NSApp.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)

    def updateStatusBarMenu(self):
        self.currentServiceMenuItem.setTitle_(getCurrentServiceMenuItemTitle())

        # Remove Tick before All Menu Items
        self.autoGaeProxyMenuItem.setState_(AppKit.NSOffState)
        self.globalGaeProxyMenuItem.setState_(AppKit.NSOffState)
        self.globalXTunnelMenuItem.setState_(AppKit.NSOffState)
        self.globalSmartRouterMenuItem.setState_(AppKit.NSOffState)
        self.disableGaeProxyMenuItem.setState_(AppKit.NSOffState)

        # Get current selected mode
        proxyState = getProxyState(currentService)

        # Update Tick before Menu Item
        if proxyState == 'pac':
            self.autoGaeProxyMenuItem.setState_(AppKit.NSOnState)
        elif proxyState == 'gae':
            self.globalGaeProxyMenuItem.setState_(AppKit.NSOnState)
        elif proxyState == 'x_tunnel':
            self.globalXTunnelMenuItem.setState_(AppKit.NSOnState)
        elif proxyState == 'smart_router':
            self.globalSmartRouterMenuItem.setState_(AppKit.NSOnState)
        elif proxyState == 'disable':
            self.disableGaeProxyMenuItem.setState_(AppKit.NSOnState)

        # Trigger autovalidation
        self.menu.update()

    def validateMenuItem_(self, menuItem):
        return currentService or (menuItem != self.autoGaeProxyMenuItem and
                                  menuItem != self.globalGaeProxyMenuItem and
                                  menuItem != self.globalXTunnelMenuItem and
                                  menuItem != self.globalSmartRouterMenuItem and
                                  menuItem != self.disableGaeProxyMenuItem)

    def presentAlert_withTitle_(self, msg, title):
        self.performSelectorOnMainThread_withObject_waitUntilDone_('presentAlertWithInfo:', [title, msg], True)
        return self.alertReturn

    def presentAlertWithInfo_(self, info):
        alert = AppKit.NSAlert.alloc().init()
        alert.setMessageText_(info[0])
        alert.setInformativeText_(info[1])
        alert.addButtonWithTitle_("OK")
        alert.addButtonWithTitle_("Cancel")
        self.alertReturn = alert.runModal() == AppKit.NSAlertFirstButtonReturn

    def registerObserver(self):
        nc = AppKit.NSWorkspace.sharedWorkspace().notificationCenter()
        nc.addObserver_selector_name_object_(self, 'windowWillClose:', AppKit.NSWorkspaceWillPowerOffNotification, None)

    def windowWillClose_(self, notification):
        executeResult = subprocess.check_output(['networksetup', '-listallnetworkservices'])
        services = executeResult.split('\n')
        services = filter(lambda service: service and service.find('*') == -1 and getProxyState(service) != 'disable',
                          services)  # Remove disabled services and empty lines

        if len(services) > 0:
            print('helperDisableAutoProxy')
        os._exit(0)
        AppKit.NSApp.terminate_(self)

    def disableProxy_(self, _):
        print("disableProxy_")


def getCurrentServiceMenuItemTitle():
    if currentService:
        return 'Connection: %s' % currentService
    else:
        return 'Connection: None'


def getProxyState(service):
    if not service:
        return

    # Check if auto proxy is enabled
    executeResult = subprocess.check_output(['networksetup', '-getautoproxyurl', service])
    if (executeResult.find('http://127.0.0.1:8086/proxy.pac\nEnabled: Yes') != -1):
        return "pac"

    # Check if global proxy is enabled
    executeResult = subprocess.check_output(['networksetup', '-getwebproxy', service])
    if (executeResult.find('Enabled: Yes\nServer: 127.0.0.1\nPort: 8087') != -1):
        return "gae"

    # Check if global proxy is enabled
    if (executeResult.find('Enabled: Yes\nServer: 127.0.0.1\nPort: 1080') != -1):
        return "x_tunnel"

    if (executeResult.find('Enabled: Yes\nServer: 127.0.0.1\nPort: 8086') != -1):
        return "smart_router"

    return "disable"


# Generate commands for Apple Script
def getEnableAutoProxyCommand(service):
    return "networksetup -setautoproxyurl \\\"%s\\\" \\\"http://127.0.0.1:8086/proxy.pac\\\"" % service


def getDisableAutoProxyCommand(service):
    return "networksetup -setautoproxystate \\\"%s\\\" off" % service


sys_tray = MacTrayObject.alloc().init()
currentService = None


def fetchCurrentService(protocol):
    global currentService
    status = SystemConfiguration.SCDynamicStoreCopyValue(None, "State:/Network/Global/" + protocol)
    if not status:
        currentService = None
        return
    serviceID = status['PrimaryService']
    service = SystemConfiguration.SCDynamicStoreCopyValue(None, "Setup:/Network/Service/" + serviceID)
    if not service:
        currentService = None
        return
    currentService = service['UserDefinedName']

@AppKit.objc.callbackFor(AppKit.CFNotificationCenterAddObserver)
def networkChanged(center, observer, name, object, userInfo):
    fetchCurrentService('IPv4')
    # loadConfig()
    sys_tray.updateStatusBarMenu()


# Note: the following code can't run in class
def serve_forever():
    app = AppKit.NSApplication.sharedApplication()
    app.setDelegate_(sys_tray)

    # Listen for network change
    nc = AppKit.CFNotificationCenterGetDarwinNotifyCenter()
    AppKit.CFNotificationCenterAddObserver(nc, None, networkChanged, "com.apple.system.config.network_change", None, AppKit.CFNotificationSuspensionBehaviorDeliverImmediately)

    # fetchCurrentService('IPv4')
    AppHelper.runEventLoop()


def main():
    serve_forever()


if __name__ == '__main__':
    main()
