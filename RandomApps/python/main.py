import random
import string
import cherrypy
import hashlib
import numpy as np
from linez import Linez
from matsvd import Matsvd

import os

homeLocation = '/home/alion/Projekti/cherrypyTest/RandomApps'


def rootConfig(homeLocation):
    return {
    '/flavicon.ico': {
        'tools.staticfile.on': True
        # 'tools.staticfile.filename': "/path/to/myfavicon.ico"
    },
    '/': {
        'log.screen': False,
        'log.access_file': homeLocation+'/logs/access_file.log',
        'log.error_file': homeLocation+'/logs/error_file.log',
        # 'tools.sessions.on': True,
        # 'tools.sessions.storage_class': cherrypy.lib.sessions.MemcachedSession
        # 'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
        # 'tools.sessions.storage_path': "/some/directory"
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': homeLocation+"/static"
    }
}


USERS = {'jon': 'svejedno'}


class Root(object):
    # def _cp_dispatch(self, vpath):
    #     print(vpath, "kurac")
    #     if len(vpath) == 3:
    #         cherrypy.request.params['artist'] = vpath.pop(0)  # /band name/
    #         vpath.pop(0) # /albums/
    #         cherrypy.request.params['title'] = vpath.pop(0) # /album title/
    #         return self.albums
    #     return self

    def __init__(self, homeLocation):
        self.homeLocation = homeLocation
        self.linez = Linez()
        self.matsvd = Matsvd()

    @cherrypy.expose(['indeks'])
    def index(self):
        # return """
        # <h1>Hello! How are you?</h1> 
        # <a href="admin">Admin </a>
        # """
        f = open("index.html", "r")
        return f

    @cherrypy.expose
    def pwd(self):
        return os.getcwd()

    @cherrypy.expose
    def generate(self, length=9):
        return ''.join(random.sample(string.hexdigits, int(length)))

    @cherrypy.expose
    def setcookie(self):
        cookie = cherrypy.response.cookie
        cookie['cookieName'] = 'cookieValue'
        cookie['cookieName']['path'] = '/'
        cookie['cookieName']['max-age'] = 3600
        cookie['cookieName']['version'] = 1
        return "<html><body>Hello, I just sent you a cookie</body></html>"

    @cherrypy.expose
    def getcookie(self):
        cookie = cherrypy.request.cookie
        res = """<html><body>Hi, you sent me %s cookies.<br />
                Here is a list of cookie names/values:<br />""" % len(cookie)
        for name in cookie.keys():
            res += "name: %s, value: %s<br>" % (name, cookie[name].value)

        # for i in cookie['cookieName']:
        #     print(i)
        #     print(cookie['cookieName'][i])

        return res + "</body></html>"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def jsondecode(self):
        data = cherrypy.request.json
        return str(data)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def jsonencode(self):
        return {'key': 'value'}


# print(encrypt_pwd(b'test'))

if __name__ == '__main__':
   cherrypy.quickstart(Root(homeLocation), '/', rootConfig(homeLocation))