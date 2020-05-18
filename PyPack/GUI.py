
# coding = iso-8859-15
__author__ = "Rgs78"


#==============================================================================#
# section Importation des modules Python                                                           #
#==============================================================================#

import BP
import imp
import sys
import time
# D�clarer le chemin d'acc�s aux modules Python suppl�mentaires
Path = BP.BankPerfectPluginPath()
Path = Path[1:Path.rfind("\\") + 1]
sys.path.append(Path + "PyPack")
# Charger les modules standards de python non inclus dans BP
import os
import webbrowser
from copy import copy
# Charger les modules sp�cifiques au plugin
#fDate = imp.load_source("", Path + "fDate.py")

application = 'GrunnReport'
#-------------------------------------------------------------------------------
# formulaire "pr�f�rences"
#-------------------------------------------------------------------------------

# Charge le fichier d�sign� par Path
def loadfile(path):
    f = open(path, "r")
    rec = f.read().split("\n")
    return rec


defaults={
    'Position':"poMainFormCenter",
    'FontStyle':[], 'FontSize':8, 'FontName':'Tahoma', 'FontColor':0x00000000,
    }

def make(CC,Type,Parent,**kwargs):
    if Type!='MyButton': o = CC(Type, Parent)
    else:
        o = CC('TButton', Parent)
        img = make(CC, 'TImage', o, Enabled=False, **kwargs)
    o.Parent = Parent
    attr = dir(o)

    defs = [kw for kw in defaults if not kw in kwargs]
    for kw in defs:
        if 'Font'in kw and 'Font' in attr:
            o.Font.__setattr__(kw[4:],defaults[kw])
        if kw in attr :
            if   kw=='Picture' : o.Picture.LoadFromFile(defaults[kw])
            else: o.__setattr__(kw,defaults[kw])

    for kw in kwargs:
        if 'Font'in kw and 'Font' in attr:
            o.Font.__setattr__(kw[4:],kwargs[kw])
        if kw in attr :
            if   kw=='Picture' : o.Picture.LoadFromFile(kwargs[kw])
            else: o.__setattr__(kw,kwargs[kw])

    if "OnClick" in attr and o.OnClick != None: o.Cursor = -21
    if Type=='MyButton':
        Width = o.Width
        Height = o.Height
        img.Left=(Width-img.Picture.Width)/2;img.Top=(Height-img.Picture.Height)/2

    return o

#K = [4096,256,16,1]
#defaults_args = {'Left':1, 'Top':1, 'Width':1, 'Height':20, 'MinWidth':1, 'MinHeight':1, 'Position':'poMainFormCenter', 'Anchors':['akLeft','akTop'],
#            'OnClick':None, 'Color':0x00ffffff, 'Caption':"",
#            'FontStyle':[], 'FontSize':8, 'FontName':'Tahoma', 'FontColor':0x00000000,
#            'Picture':None, 'Cursor':0,
#            'BorderStyle':0, 'Enabled':True,
#            'ShowHint':1, 'Hint':"",
#            'ModalResult':0, 'onResize':None,
#            'Date':time.mktime(time.localtime()) / 86400 + 25569}
#def make(CC, Type, Parent,**kwargs):
#    if type(CC)==str: CC=eval(CC)
#    defaults=copy(defaults_args); defaults.update(kwargs)
#    if Type!='MyButton':
#        o = CC(Type, Parent)
#    else:
#        o = CC('TButton', Parent)
#        o.Parent = Parent
#        o.Width=defaults['Width']
#        o.Height=defaults['Height']
#        Picture=defaults['Picture']
#        f = open(Picture,'rb')
#        f.read(16);h,l = f.read(4),f.read(4)
#        Width = sum([ord(h[i])*K[i] for i in range(4)])
#        Height = sum([ord(l[i])*K[i] for i in range(4)])
#        img = make(CC, 'TImage',o, Width=Width, Height=Height, Picture=Picture, Enabled=False)
##        img=CC('TImage',o)
##        img.Parent=o
##        img.Width=Width
##        img.Height=Height
##        img.Picture.LoadFromFile(Picture)
##        img.Enabled=False
#        img.Left=(o.Width-Width)/2;img.Top=(o.Height-Height)/2
#    o.Parent = Parent
#    attr=dir(o)
#    if 'Font' in attr:
#        for (key,value) in [arg for arg in defaults.items() if 'Font'in arg[0]]:
#            o.Font.__setattr__(key[4:],value)
#    for arg in [arg for arg in attr if arg in defaults.keys()]:
#        if arg!='Picture':
#            o.__setattr__(arg, defaults[arg])
#        else: o.Picture.LoadFromFile(defaults['Picture'])
#    if [arg for arg in kwargs.keys() if arg.startswith('On')]!=[]:o.Cursor=-21
#    return o



#def make(CC, Type, Parent,
#            Left=1, Top=1, Width=1, Height=20, MinWidth=1, MinHeight=1, Position='poMainFormCenter', Anchors=['akLeft','akTop'],
#            OnClick=None, Color=0x00ffffff, Caption="",
#            FontStyle=[], FontSize=8, FontName='Tahoma', FontColor=0x00000000,
#            Picture=None, Cursor=0,
#            BorderStyle=None, Enabled=True,
#            ShowHint=1, Hint="",
#            ModalResult=0, onResize=None,
#            Date=time.mktime(time.localtime()) / 86400 + 25569):
#    if type(CC)==str: CC=eval(CC)
#    if Type!='MyButton': o = CC(Type, Parent)
#    else:
#        o = CC('TButton', Parent)
#        img = make(CC, 'TImage',o, Width=Width, Height=Height, Picture=Picture, Enabled=False)
#        f = open(Picture,'rb')
#        f.read(16);h,l = f.read(4),f.read(4)
#        sh = 0
#        for i  in range(len(h)): sh+=ord(h[i])*(16**(len(h)-i-1))
#        sl = 0
#        for i  in range(len(l)): sl+=ord(l[i])*(16**(len(l)-i-1))
#        img.Left=(Width-sl)/2;img.Top=(Height-sh)/2
#    o.Parent = Parent
#    o.SetProps(Parent=Parent, Left=Left, Top=Top, Width=Width, Height=Height,Anchors=Anchors, ShowHint=ShowHint, Hint=Hint, Cursor=Cursor)
#    attr = dir(o)
#    if "ModalResult" in attr: o.ModalResult = ModalResult
#    if "onResize" in attr: o.onResize = onResize
#    if "Enabled" in attr: o.Enabled = Enabled
#    if "OnClick" in attr: o.OnClick = OnClick
#    if "Caption" in attr: o.Caption = Caption
#    if "BorderStyle" in attr and BorderStyle != None: o.BorderStyle = BorderStyle
#    if "Position" in attr: o.Position = Position
#    if "Font" in attr: o.Font.SetProps(Style=FontStyle, Color=FontColor, Size=FontSize, Name=FontName)
#    if "Picture" in attr: o.Picture.LoadFromFile(Picture)
#    if "Constraints" in attr:
#        if MinWidth != 1: o.Constraints.MinWidth = MinWidth
#        else: o.Constraints.MinWidth = o.Width
#        if MinHeight != 1: o.Constraints.MinHeight = MinHeight
#        else: o.Constraints.MinHeight = o.Height
#    if "OnClick" in attr and o.OnClick != None: o.Cursor = -21
#    if "Date" in attr: o.Date = Date
#    
#    return o

def Debug():
    for acc in range(BP.AccountCount()):
        l = ';'.join(BP.Operationthirdparty[acc])
        if ('debug '+ application).lower() in l.lower():
            for i in range(BP.OperationCount[acc]-1,-1,-1):
                if ('debug '+ application).lower() in BP.Operationthirdparty[acc][i].lower():
                    return True, BP.Operationthirdparty[acc][i]
    return False, ''

def trace(s=None):
    if s==None: BP.MsgBox('test',0)
    else: BP.MsgBox(repr(s),0)

# version de BP
def BP_version():
    f=open(BP.BankPerfectExePath()+'\\history.txt','r')
    ok = False
    while not ok:
        l=f.readline()
        n = l.find("Build")
        if n != -1:
            p=l[n:].find(']')
            v=l[n+6:n+p]
            ok = True
    return v

#def get_params():
#    global params
#    IniFile = Path + "%s.ini"%application
#    f=loadfile(IniFile)
#    params = {}
#    for line in f:
#        if line.find("=") != -1:
#            params[line.split("=")[0]] = (line.split("=")[1])
#    return params
#
#def set_params(Sender=None,year=None,month=None,duree=None,quadrillage=None,graph=None,dataset=-1):
#    IniFile = Path + "%s.ini"%application
#    file=open(IniFile,"r")
#    #BP.MsgBox(repr(IniFile),0)
#    lines = file.readlines()
#    for i, line in enumerate(lines):
#        if '=' in line:
#            # fichiers images des ic�nes de lignes
#            #for j in range (len(i_code)):
#            #    if i_code[j]==line.split("=")[0] :
#            #        lines[i]=i_code[j]+'='+params[i_code[j]][0]+'|'+params[i_code[j]][1]+"\n"
#            if line.split("=")[0]=='year':
#                lines[i] = 'year=%s\n' % year
#            if line.split("=")[0]=='month':
#                lines[i] = 'month=%s\n' % month
#            if line.split("=")[0]=='duree':
#                lines[i] = 'duree=%s\n' % duree
#            if line.split("=")[0]=='quadrillage':
#                lines[i] = 'quadrillage=%s\n' % quadrillage
#            if line.split("=")[0]=='graph':
#                lines[i] = 'graph=%s\n' % graph
#            if line.split("=")[0]=='dataset':
#                lines[i] = 'dataset=%s\n' % dataset
#    file=open(IniFile,"w")
#    file.writelines(lines)
#    #BP.MsgBox(repr(lines),0)
#    file.close()
#    P.ModalResult = 1
#    return lines
#
#
#def pref(CreateComponent, app):
#    global P, Pr1, Pr2, application
#    application = app
#    CC = CreateComponent
#
#    def pExit(Sender):
#        P.ModalResult = 2
#        return
#
#    def browse(Sender):
#        Path = BP.OpenDialog("Choisissez le fichier image", "", "*.png", "fichier image(*.png)|*.png")
#        if Path != '':
#            Sender.Picture.LoadFromFile(Path)
#            name = Path.split('\\')[-1]
#            dst = '\\'.join(BP.BankPerfectExePath().split('\\')[:-1])+'\\icons'
#            shutil.copyfile(Path,'%s/%s.png'%(dst,params[Sender.name][0]))
#
#    def default(Sender):
#        src = ('\\'.join(BP.BankPerfectPluginPath().split('\\')[:-1])+'\\icons\\icons')[1:]
#        dst = '\\'.join(BP.BankPerfectExePath().split('\\')[:-1])+'\\icons'
#        if not os.path.isdir(dst): os.mkdir(dst)
#        # recopier les fichiers du r�pertoire source vers le r�pertoire icons de BP
#        names = os.listdir(src)
#        for name in names :
#            shutil.copyfile('%s/%s'%(src,name),'%s/%s'%(dst,name))
#        for i,P in enumerate(Pi):
#            P.Picture.LoadFromFile(dst + "\\%s.png" % i_file[i])
#
#
#    def message_prive(sSender):
#        webbrowser.open("http://www.chelly.net/phpbb/ucp.php?i=pm&mode=compose&u=9774")
#
#    def donate(Sender):
#        webbrowser.open("https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=36E2ATWEW5ZAA ")
#
#
#    params = get_params()
#    #Pi=[];Pi_l=[];i_code = []; i_file = []; i_label = []
#    #keys = params.keys(); keys.sort()
#    #for key in keys:
#    #    if key[:3]=='Att':
#    #        i_code.append(key)
#    #        i_file.append(params[key][0])
#    #        i_label.append(params[key][1])
#    L = 300
#    H = 330  #+len(i_code)*20
#    P = make(CC, "TForm", None, Caption = None, Width=L, Height=H)
#    PTitre = make(CC, "TLabel", P, Left=20, Top=15, Caption="Recherche ", FontStyle=["fsBold","fsItalic"], FontSize = 12)
#    make(CC, "TBevel",P,Top = PTitre.Top+30, Left = 2,Height = 2,Width = L-20)
#    PT2 = make(CC, "TLabel", P, Left=10, Top=PTitre.Top+40, Caption="Param�tres :", FontStyle = ["fsBold"], FontSize = 10)
#    # groupe 'Int�gration � BP -----------------------------------------------------
#    #Pg1 = make(CC, "TGroupBox", P, Caption="Ic�nes de lignes * ", Left=10, Top=PT2.Top+20, Width=L-40, Height=00 , FontStyle = ["fsItalic"]) #Height=len(i_code)*20+30
#    #icons_path = '\\'.join(BP.BankPerfectExePath().split('\\')[:-1])+'\\icons'
#    #for i in range(len(i_code)):
#    #    Pi.append(make(CC, "TImage", Pg1, Left = 15, Top = 20+20*i, Width = 16, Height = 16, OnClick = browse, Picture = icons_path + "\\%s.png" % i_file[i]))
#    #    Pi[i].Name = i_code[i]
#    #    Pi_l.append(make(CC, "TLabel", Pg1, Left = 40, Top = 20+20*i, Width=150, Caption =i_label[i]))
#    #Pi2 = make(CC, "TImage", Pg1, Left = 200, Top = 20, Width=32, Height=47, OnClick= default, ShowHint=True, Hint='Restauration des ic�nes originales', Picture = Path + "icons\\standard_icon.png")
#    #Pi3 = make(CC, "TImage", Pg1, Left = 200, Top = 70, Width=32, Height=47, OnClick= set_freeicon, ShowHint=True, Hint='Mise en place des ic�nes sur les lignes anciennes', Picture = Path + "icons\\check-list.png")
#    #PLm = make(CC, "TLabel", P, Left=20, Top=Pg1.Top+Pg1.Height+5, Caption="* au red�marrage de BP ", FontStyle = ["fsItalic"], FontColor = 0x00555555)
#    # groupe 'pr�f�rences' ---------------------------------------------------------
#    Pg2 = make(CC, "TGroupBox", P, Caption="Pr�f�rences", Left=10, Top=PT2.Top+20, Width=L-40, Height=70, FontStyle = ["fsItalic"])
#    #Pr1 = CC("TRadioButton", Pg2)
#    #Pr1.SetProps(Parent=Pg2, Left=10, Top=30, Width=200, Caption="[1/n] tiers de l'op�ration")
##    Pr1 = make(CC, "TRadioButton", Pg2, Left=10, Top=20, Width=200, Caption="[1/n] tiers de l'op�ration")
##    Pr2 = make(CC, "TRadioButton", Pg2, Left=10, Top=40, Width=200, Caption="tiers de l'op�ration [1/n]")
##    Pr1.visible = True
##    Pr1.Checked = (params['Tag']=='AVANT')
##    Pr2.Checked = (params['Tag']=='APRES')
#    # boutons ----------------------------------------------------------------------
##    PKO = make(CC, "TImage", P, Left = L-100, Top = Pg2.Top+Pg2.Height+10, Width=30, Height=30, OnClick= pExit, Picture = Path + "icons\\KO2.png")
#    POK = make(CC, "TImage", P, Left = L-60, Top = Pg2.Top+Pg2.Height+10, Width=30, Height=30, OnClick=set_params, Picture = Path + "\\icons\\OK2.png")
#    # signature --------------------------------------------------------------------
#    make(CC, "TBevel",P,Top = POK.Top+POK.Height+10, Left = 2,Height = 2,Width = L-20)
#    Pimage = make(CC, "TImage", P, Left = L-75, Top = POK.Top+POK.Height+55, Width=60, Height=60, Anchors=["akRight"],OnClick=message_prive, Picture = Path + "\\icons\\rgs78.png")
#    PRgs78 = make(CC, "TLabel",P, Caption = "Rgs78", Left=L-65,Top=H-60,FontStyle=["fsBold"], FontColor = 0x00008800)
#    PLZ = make(CC, "TLabel", P, Left=20, Top=Pimage.Top+Pimage.Height/2-55, Caption="Vous pouvez remonter des bugs ou\ndemander des �volutions ici        =>")
#    Pdonate = make(CC, "TImage", P, Left = 70, Top = H-70, Width=71, Height=20,OnClick=donate, Picture = Path + "\\icons\\donate.png")
#    # \params_panel
#    #-------------------------------------------------------------------------------
#    #Pref = make("TImage", ff_panel, Left = margin, Top = ff.Height-32-3, Width=32, Height=32, Anchors=["akLeft", "akBottom"], OnClick=ParamsCall, Picture=Path + "icons\\preferences.png")
#    #-------------------------------------------------------------------------------
#    return P, params

    
