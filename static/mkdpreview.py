#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import cgi
import imp
import signal
from threading import Thread
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

plugins = {}

os.chdir(os.path.dirname(__file__))
signal.signal(signal.SIGINT, signal.SIG_DFL)

port = int(os.getenv("mkdpreview_port") or "8081")

QNetworkProxyFactory.setUseSystemConfiguration(True)
app = QApplication(sys.argv)
webview = QWebView()
def do_eval(js):
  webview.page().mainFrame().evaluateJavaScript(
      "preview(%s)" % json.dumps(unicode(js, 'utf-8')))
QObject.connect(webview, SIGNAL("preview(QString)"), do_eval)

class PreviewHandler(SimpleHTTPRequestHandler):
  def do_POST(self):
    try:
      s = self.rfile.read(int(self.headers.getheader('content-length')))
      p = cgi.parse_qs(s)
      typ = p.has_key("type") and p["type"][0] or "markdown"
      if not plugins.has_key(typ):
        plugins[typ] = imp.load_source("mod_%s" % typ, "plugin/mod_%s.py" % typ)
      data = plugins[typ].preview(unicode(p["data"][0], 'utf-8'))
      webview.emit(SIGNAL("preview(QString)"), data.encode('utf-8'))
      self.wfile.write("OK")
    except:
      e = sys.exc_info()[0]
      print e
      self.wfile.write("Unexpected error: %s" % e)

class WebServer(QThread):
  def __init__(self):
    QThread.__init__(self)
    self.server = HTTPServer(("", port), PreviewHandler)

  def run(self):
    self.server.serve_forever()

server = WebServer()
server.start()

webview.setWindowTitle('Markdown Previewer')
webview.load(QUrl("http://localhost:%d" % port))
webview.show()

sys.exit(app.exec_())

# vim:set et sw=2 ts=2:
