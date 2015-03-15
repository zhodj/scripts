#!/usr/bin/python
#-*- coding: utf-8 -*-
import os, sys, string
import poplib
import email

host = ""
username = ""
password = ""

pp = poplib.POP3(host)
pp.set_debuglevel(0)
pp.user(username)
pp.pass_(password)

ret = pp.stat()
print ret

num = ret[0] - 2
print "num:", num

down = pp.retr(num)
print 'lines:', len(down)

context_str = ''
for line in down[1]:
  context_str = context_str + line + '\n'

msg = email.message_from_string(context_str)
subject = msg.get("subject")
h = email.Header.Header(subject)
dh = email.Header.decode_header(h)
subject = dh[0][0]

print "subject:",subject.decode('gb2312');
print "from:",email.utils.parseaddr(msg.get("from"))[1]
print "to:",email.utils.parseaddr(msg.get("to"))[1]


for par in msg.walk():
  if not par.is_multipart():
    name = par.get_param("name")
    if name:
      h = email.Header.Header(name)
      dh = email.Header.decode_header(h)
      fname = dh[0][0]
      print '附近名：',fname.decode('gb2312')
      data = par.get_payload(decode = True)

      try:
        f = open(fname.decode('gb2312'), 'wb')
      except:
        print '附件名有非法字符，自动换一个'
        f = open('aaaa', 'wb')
      f.write(data)
      f.close()
    else:
      print par.get_payload(decode = True)
  print '+'*60

pp.quit()
