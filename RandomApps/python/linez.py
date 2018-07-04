import cherrypy
import numpy as np
import mathExtra as me
from pytohtml import inputMatrix, outputMatrix


# @cherrypy.popargs('brojcek')
class Linez(object):

    head = """
<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">    
        <link rel="stylesheet" href="/static/css/bootstrap.css">
        <script src="/static/js/jquery.js"></script>
        <script src="/static/js/popper.js"></script>
        <script src="/static/js/bootstrap.js"></script>
    </head>

"""
    end = """
</html>"""


    @cherrypy.expose
    def index(self):
        body = """
    <body>
        <form method="get" action="matrix">
            <div class="container">
                """

        body += """
                <div class="col-4 input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text" id="">Dimenzija vektora i broj vektora</span>
                    </div>

                    <input type="text" class="form-control" name="n">
                    <input type="text" class="form-control" name="m">
                
                    <div class="row">
                        <input type="submit" value="Unesi matricu">
                    </div>
                </div>  
        """ 

        body+= """
            </div>
        </form>
    </body>"""
        return [self.head, body, "\n</html>"]


    @cherrypy.expose
    def matrix(self, n=0, m=0):
        body = """
    <body>
        <form method="get" action="nezavisnost">"""

        body += inputMatrix(int(n),int(m), vektori=True)

        body+= """
        </form>
    </body>"""

        return [self.head, body, self.end]


    @cherrypy.expose
    def nezavisnost(self, **dictInput):
        tmpmat = me.dictToMatrix(dictInput)
        if type(tmpmat)==type("test"):
            return tmpmat

        lin, mat = me.testLinez(tmpmat)
        body = """
    <body>"""

        body += """
        <div class="container">
             <h3>Jesu li linearno nezavisni: <span class="label label-default"> %s </span></h1>
        </div>""" % lin

        body += outputMatrix(mat)

        body += """
    </body>"""

        return [self.head, body, self.end]
