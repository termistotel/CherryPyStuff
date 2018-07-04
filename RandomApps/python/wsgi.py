import cherrypy
import main

import os

homeLocation = '/home/anna/webStranica/RandomApps'
os.chdir(homeLocation)

# rootConfig = {
#     '/flavicon.ico': {
#         'tools.staticfile.on': True
#         # 'tools.staticfile.filename': "/path/to/myfavicon.ico"
#     },
#     '/': {
#         'log.screen': False,
#         'log.access_file': homeLocation+'/logs/access_file.log',
#         'log.error_file': homeLocation+'/logs/error_file.log',
#         # 'tools.sessions.on': True,
#         # 'tools.sessions.storage_class': cherrypy.lib.sessions.MemcachedSession
#         # 'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
#         # 'tools.sessions.storage_path': "/some/directory"
#     },
#     '/static': {
#         'tools.staticdir.on': True,
#         'tools.staticdir.dir': homeLocation+"/static"
#     }
# }

# class Root(object):
#     @cherrypy.expose
#     def index(self):
#     	return "Testica"


def application(environ, start_response):
    cherrypy.tree.mount(main.Root(homeLocation), script_name='/', config=main.rootConfig(homeLocation))
    return cherrypy.tree(environ, start_response)