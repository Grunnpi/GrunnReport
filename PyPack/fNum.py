# To change this template, choose Tools | Templates
# and open the template in the editor.

# fonction qui formate un nombre avant de l'afficher
def fmt_float(value, precision = 2):
    if abs(value) < 0.01: return "0,00"
    mask = "%%.%df" %precision
    ipart, fpart = (mask %value).split(".")
    #Séparateur décimal
    ipart = (" ".join([ipart[::-1][i:i+3] for i in range(0, len(ipart), 3)]))[::-1]
    return ipart + "," + fpart


def str_to_float(s,Def=0):
    s = s.replace("$", "").replace(" ", "").replace("€", "").replace("F", "").replace(",", ".").replace("%", "")
    if "." in s:
        l = s.split(".")
        s = "%s.%s" %( "".join(l[:-1]), l[-1] )
    try:
        f = float(s)
    except:
        try:
            f = eval(s)
        except:
            return Def
    return f

