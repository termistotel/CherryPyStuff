import cherrypy
import numpy as np
import mathExtra as me
import pytohtml as pyth

import os


class Matsvd(object):	
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
                """

        body += """
        <div class="container">
            <h2>Input a matrix</h2>
            <form method="get" action="matrix">
                <div class="input-group col-6 mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text" id="">Dimenzija vektora i broj vektora</span>
                    </div>

                    <input type="text" class="form-control" name="n">
                    <input type="text" class="form-control" name="m">
                </div>
                <input type="submit" value="Submit matrix"> 
            </form>  
        </div>

        <div class="container">
            <br><h2>Or upload a picture</h2>
            <form action="picturesvd" method="post" enctype="multipart/form-data">
                <div class="input-group mb-3 col-10">
                    <div class="input-group-prepend">
                        <span class="input-group-text">Threshold: </span>
                        <input type="text" class="form-control" name="threshold" placheholder="0.1">
                    </div>
                    <div class="input-group-prepend">
                        <span class="input-group-text">filename: </span>
                    </div>
                    <input type="file" class="form-control" name="picfile">
                </div>
                <input type="submit" value="Submit picture"/>
            </form>
        </div>
        """ 

        body+= """
    </body>"""
        return [self.head, body, self.end]


    @cherrypy.expose
    def matrix(self, n=0, m=0):
        body = """
    <body>
        <form method="get" action="svd">"""

        body += pyth.inputMatrix(int(n),int(m), vektori=False)

        body+= """
        </form>
    </body>"""
        return [self.head, body, self.end]


    @cherrypy.expose
    def svd(self, **dictInput):
        body = """
    <body>"""

        matrica = me.dictToMatrix(dictInput)
        if type(matrica)==type("test"):
            return matrica

        U, sigma, V = me.svdecomposition(matrica)

        sigma = np.diag(sigma)
       
        body += pyth.textMat(matrica, "Originalna matrica: ")
        body += pyth.textMat(U.dot(sigma).dot(V.T), "Rekonstruirana matrica: ")

        body += pyth.textMat(sigma, "Sigma: ")
        body += pyth.textMat(U, "U: ")
        body += pyth.textMat(V, "V: ")

        body += """
    </body>"""
        return [self.head, body, self.end]

    @cherrypy.expose
    def picturesvd(self, threshold=0.01, picfile=None):
        if not picfile.file:
            return "Nema slike"

        body = """
    <body>"""

        try:
            float(threshold)
        except:
            threshold=0.01


        # Ucitavanje matplotliba i opencv-a sto traje beskonacno
        import matplotlib as mpl
        mpl.use('Agg')  # ovo koristi kao backend jer nije pokrenut xserver
        import matplotlib.pyplot as plt
        import cv2


        # Ucitavanje unesenog fajla kao sliku
        npimg = np.fromstring(picfile.file.read(), np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR )
        img = np.sum(img/(3.0), axis=2, dtype="float64")

        # SVD
        U, sigma, V = me.svdecomposition(img)

        # Grafovi prije rezanja
        plt.rc('text', usetex=True)
        fig = plt.Figure()
        fig, axes = plt.subplots(1,2)
        fig.set_figheight(5)
        fig.set_figwidth(12)
        fig.set_dpi(100)
        fig.suptitle("Singular Values - sve")

        axes[0].plot(sigma)
        axes[0].set_title("Normalan graf")

        axes[1].loglog(sigma, 'r')
        axes[1].set_title("log-log graf")

        for i in axes:
            i.set_xlabel("n", fontsize=20)
            i.set_ylabel('$\sigma$', fontsize=20)


        # Uzmi samo sigme koje su iznad thresholda
        maxdim = min(sigma.shape)

        sigma = sigma[sigma>float(threshold)]
        U = U[:, :sigma.shape[0]]
        V = V[:, :sigma.shape[0]]

        # Grafovi poslije rezanja
        fig2 = plt.Figure()
        fig2, axes = plt.subplots(1,2)
        fig2.set_figheight(5)
        fig2.set_figwidth(12)
        fig2.set_dpi(100)
        fig2.suptitle("Singular Values - iznad thresholda")

        axes[0].plot(sigma)
        axes[0].set_title("Normalan graf")

        axes[1].loglog(sigma, 'r')
        axes[1].set_title("log-log graf")

        for i in axes:
            i.set_xlabel("n", fontsize=20)
            i.set_ylabel('$\sigma$', fontsize=20)

        newdim = min(sigma.shape)

        recons = U.dot(np.diag(sigma)).dot(V.T)
        recons = np.clip(recons, 0, 255)

        cv2.imwrite('static/img/originalna.png', img)
        cv2.imwrite('static/img/rekonstruirana.png', recons)
        fig.savefig("static/img/grafovi1.png", bbox_inches='tight')
        fig2.savefig("static/img/grafovi2.png", bbox_inches='tight')

        body += """
        <div class="container">
            <h3>Pic shape: %s </h3><br>
            <h3>Threshold: %s </h3>
            <h3>Old dimension: %s </h3>
            <h3>New dimension: %s </h3>
            <h3>Dimensions reduced: %s </h3>
        </div>

        """ % (img.shape, threshold, maxdim, newdim, maxdim-newdim)

        body += """
        <div class="container-fluid">
        """

        body += """
            <div class="row">
                <div class="col-6">
                    <h4 class="label label-default" style="text-align: center">Originalna slika</h4>
                    <img class="img-fluid" src="/static/img/originalna.png" />
                </div>
        """

        body += """
                <div class="col-6">
                    <h4 class="label label-default" style="text-align: center">Rekonstruirana slika</h4>
                    <img class="img-fluid" src="/static/img/rekonstruirana.png" />
                </div>
            </div>
        """

        body += """
                <div class="col-12">
                    <img class="img-fluid" src="/static/img/grafovi1.png" />
                </div>
            </div>
        """

        body += """
                <div class="col-12">
                    <img class="img-fluid" src="/static/img/grafovi2.png" />
                </div>
            </div>
        """

        body += """
        </div>
        """

        body += """
    </body>"""
        return [self.head, body, self.end]