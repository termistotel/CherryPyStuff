import dill as pickle
import cherrypy

homeLocation = '/home/alion/Projekti/cherrypyTest'

rootConfig = {'/': {'log.screen': False,
              'log.access_file': homeLocation+'/logs/access_file.log',
              'log.error_file': homeLocation+'/logs/error_file.log',
              'tools.sessions.on': True,
              'tools.sessions.storage_class': cherrypy.lib.sessions.MemcachedSession
              # 'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
              # 'tools.sessions.storage_path': "/some/directory"
                }
             }

tst = lambda x: x

class Root(object):

    @cherrypy.expose
    def index(self):
        return "<h1>Hello! How are you?"

    @cherrypy.expose
    def set(self):
        cookie = cherrypy.response.cookie
        cookie['cookieName'] = 'cookieValue'
        cookie['cookieName']['path'] = '/'
        cookie['cookieName']['max-age'] = 3600
        cookie['cookieName']['version'] = 1
        return "<html><body>Hello, I just sent you a cookie</body></html>"

    @cherrypy.expose
    def read(self):
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
    def count(self):
        if 'count' not in cherrypy.session:
            cherrypy.session['count'] = 0
        cherrypy.session['count'] += 1
        cherrypy.session['testica'] = tst
        #print(cherrypy.lib.sessions.MemcachedSession)
        return "<h1> Naspamao si stranicu %s puta" % (cherrypy.session['count'])


if __name__ == '__main__':
   cherrypy.quickstart(Root(), '/', rootConfig)
