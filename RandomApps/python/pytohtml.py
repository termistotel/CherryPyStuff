def inputMatrix(m,n, vektori = False):

    if vektori:
        border = "border-right: 2px solid black; border-left: 2px solid black; border-top: none; border-bottom: none;"

    else:
        border = "border: none;"

    tmp = ""            
    tmp+= """
    <div class="container">
        <div style="border-left: 2px solid black; border-right: 2px solid black; display: inline-block">
        """

    for i in range(m):
        for j in range(n):
            tmp+= """
            <input type="text" name="%s" style="width: 30px; height: 30px; %s text-align: center"/>""" % (i, border)# 1 px dotted grey"/>""" % i

        tmp+= "<br>\n"


    tmp+="""
        </div>
    """

    tmp+="""
        
        <div class="row">
            <input type="submit" value="Unesi Vektore">
        </div>
    </div>
    """

    return tmp

def outputMatrix(a, vektori = False):
    m,n = a.shape

    if vektori:
        border = "border-right: 2px solid black; border-left: 2px solid black; border-top: none; border-bottom: none;"
    else:
        border = "border: none:"

    tmp = ""            
    tmp+= """
    <div class="container">
        <div style="border-left: 2px solid black; border-right: 2px solid black; display: inline-block">
        """

    for i in range(m):
        for j in range(n):
            tmp+= """
            <label style="width: 30px; height: 30px; %s text-align: center"> %s </label>""" % (border, "{0:.1f}".format(a[i,j]))# 1 px dotted grey"/>""" % i

        tmp+= "<br>\n"


    tmp+="""
        </div>
    """

    tmp+="""
    </div>
    """

    return tmp

def textMat(a, tekst, vektori = False):
    m,n = a.shape

    if vektori:
        border = "border-right: 2px solid black; border-left: 2px solid black; border-top: none; border-bottom: none;"
    else:
        border = "border: none:"

    tmp = ""            
    tmp+= """
    <div class="container">"""


    tmp += """
        <div class="row">
             <h3><span class="label label-default"> %s </span></h1>
        </div>""" % tekst

    tmp+= """
        <div style="border-left: 2px solid black; border-right: 2px solid black; display: inline-block">
        """


    for i in range(m):
        for j in range(n):
            tmp+= """
            <label style="width: 30px; height: 30px; %s text-align: center"> %s </label>""" % (border, "{0:.1f}".format(a[i,j]))# 1 px dotted grey"/>""" % i

        tmp+= "<br>\n"


    tmp+="""
        </div>
    """

    tmp+="""
    </div>
    """

    return tmp