import os
import syslog
from settings import PROG_NAME
def log_cef(message_name, message_description, items=[]):
    FACILITY = syslog.LOG_LOCAL4
    syslog.openlog(PROG_NAME, 0, FACILITY)
    label_string = ''
    for row in items:
        for key, value in row.items():
            label_string = label_string.join("%s=%s " %(key, value))
            
    cefmsg = 'CEF:0|Mozilla|%s|1.0|%s|%s|5|%s dhost=%s'% (PROG_NAME, message_name, message_description, label_string, os.uname()[1])
    syslog.syslog(syslog.LOG_INFO, cefmsg)
    syslog.closelog()
