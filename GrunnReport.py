__author__="Rgs78"
import BP
import cPickle
import time
import imp
import sys
# Déclarer le chemin d'accès aux modules Python supplémentaires
Path = BP.BankPerfectPluginPath()
Path = Path[1:Path.rfind("\\")+1]
sys.path.append(Path + "PyPack")
sys.path.append(Path + "PyMods")
# Charger les modules standards de python non inclus dans BP
import copy
import os
import webbrowser
import codecs
# Charger les modules spécifiques au plugin
from fDate import *
from fNum import *
from GUI import *
from PrefsForm import *
from AccountsListsForm import *

tstart=time.time()
#==============================================================================#
# Variables                                                                    #
#==============================================================================#
# récupération des paramètres de la dernière session
CC = CreateComponent
P, params = pref(CC, application)
version = params['version']

w=[0,0,0,0,0,0,0,0,0,0]
cells=[]
s_names=['S0_off.png','S1_on.png','S2_off.png','S3_off.png']
margin = 10
dH = 0; dV = 20
account_count=BP.AccountCount()
cols=[]
extra=[]
headers=[]
filters=[]
formats=[]
widths=[]
mts=8
last_sort=0
lists={}
group_logo = Path + "groups\\_pas de logo_.png"
acc_list=[]

html_line = '<tr%s></tr>'
html_col_str = '<td>%s</td>'
html_col_flt = '<td class="right">%s</td>'
html_page = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>Export BankPerfect</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<link rel="shortcut icon" href="http://nsm08.casimages.com/img/2013/04/17//13041709480713001411096898.png">
<style>
div, td, th {font: normal 11px arial; padding: 5px; margin: 1px; border: 1px solid #ccc}
h1 {font: bold 19px arial; border-bottom: 1px solid #000; padding: 0 0 5px 0; margin: 5px 0 5px 0}
td.right {text-align: right}
tr.odd td {background-color: #eee}
div, th {font-weight: bold; text-align: center}
.infos {border: 1px solid #777; padding: 10px; margin: 10px}
.infos td {border: 0; text-align: right; padding: 2px; font-weight: bold}
</style>
</head>
<body>

<table class="infos">
    <tr>
        <td>Nombre de lignes:</td>
        <td>%d</td>
    </tr>
    <tr>
        <td>Opérations pointées:</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>Opérations rapprochées:</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>A venir:</td>
        <td>%s</td>
    </tr>
    <tr>
        <td>Solde:</td>
        <td>%s</td>
    </tr>
</table>

<table width="100%%">
<tr>
{table_headers}
</tr>
{table_lines}
</table>

</body>
</html>
"""




#==============================================================================#
# Fonctions                                                                    #
#==============================================================================#

#-------------------------------------------------------------------------------
# section comptes
#Liste des comptes triés selon les réglages manuels de l'utilisateur
display_accounts = BPEval("get_accounts").split(";")
#Dictionnaire qui renvoie l'index réel d'un compte en fonction de sa position dans la liste classée
UID_ok = (BP_version()>='7.4.0.352')
accounts_uid_from_id = {-1: -1}
accounts_id_from_uid = {-1: -1}
real_accounts = {}
real_index = {}
display_index = {}
accounts_positions = {}
for i, name in enumerate(display_accounts):
    p = name.find("=")
    if p == -1: continue
    index = int(name[:p], 10)
    name = name[p+1:]
    display_accounts[i] = name
    accounts_positions[index] = i
    display_index[name] = i
    real_accounts[i] = index
    real_index[name] = index
    if UID_ok:
        UID = BP.GetURL("get_account_uid_from_id:%s" % index)
        accounts_uid_from_id[index] = UID
        accounts_id_from_uid[UID] = index

ID_YES = 6
categs = {-1: ("", "")}

current_parent = ""
for i, categ in enumerate(BP.CategName):
    p = categ.find("=")
    name = categ[p+1:]
    id = int(categ[:p], 10)
    if name.startswith(" "):
        name = name.strip()
        categs[id] = (current_parent, name)
    else:
        current_parent = name
        categs[id] = (name, "")

## chargement des données
#def load_PrefAccounts(Sender=None):
#    s = BP.GetURL("load_script_data:RgsRecherchePref")
#    if s != '':
#        s = cPickle.loads(s)
#        Grid.visible = False
#        for i in range (len(s)):
#            try: C[i].Checked = s[i]
#            except: pass
#        Grid.visible = True

## enregistrement des données
#def save_PrefAccounts(Sender=None):
#    s = [c.Checked for c in C]
#    s = cPickle.dumps(s)
#    BP.GetURL("save_script_data:RgsRecherchePref:" + s)
#    b_save_accounts.Picture.LoadFromFile(Path + "Icons\\Save_accounts2.png"); b_save_accounts.Repaint(); time.sleep(0.3)
#    b_save_accounts.Picture.LoadFromFile(Path + "Icons\\Save_accounts.png"); b_save_accounts.Repaint(); time.sleep(0.3)

# chargement du choix de colonnes
def load_PrefCols(Sender=None):
    global extra, nstd, nsup
    extra={}
    s = BP.GetURL("load_script_data:RgsRechColsPref")

    if params.get('cols','')=='':
        cols = [[make(CC,"TCheckBox", g3, Width = 160, Caption = "Compte"),False,True,'x',''],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Date"),False,True,'d',(01,01,1600)],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Mode"),True,False,'s','Dépôt de chèque'],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Tiers"),True,False,'x',''],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Détail"),True,False,'x',''],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Catégorie"),True,False,'x',''],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Sous-Catégorie"),True,False,'x',''],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Montant"),True,True,'f','999 999,99'],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Pointage"),True,False,'s','P'],
                [make(CC,"TCheckBox", g3, Width = 160, Caption = "Solde"),False,False,'f',"9 999 999,99"]]
        n=['','#freeicon']
        n+=[c[0].Caption for c in cols]
        for c in cols:
            c[0].Checked = True
            if c[2] :
                c[0].Enabled = False
                c[0].Font.Style = ["fsBold"]
        for acc in range(account_count):
            for line in range(BP.OperationCount[acc]):
                keys = BP.GetURL("extra_get:%s;%s" % (acc, line)).split(';')
                for key in keys:
                    if not key in n : extra[key]=1
        for key in extra.keys():
            cols.append([make(CC,"TCheckBox", g4, Width = 160, Caption = key),True,False,'x',''])
        nstd=10
        nsup=len(cols)-nstd
    else:
        cols = params['cols']
        nstd=10
        nsup=len(cols)-nstd
        for c in cols[nstd:]:
            extra[c[0][0]]=1
        for c in cols[:nstd] :
            chk,enb=c[0][1],c[0][2]
            c[0]=make(CC,"TCheckBox", g3, Width = 160, Caption = c[0][0])
            c[0].Checked = chk
            c[0].Enabled = enb
        for c in cols[nstd:] :
            chk,enb=c[0][1],c[0][2]
            c[0]=make(CC,"TCheckBox", g4, Width = 160, Caption = c[0][0])
            c[0].Checked = chk
            c[0].Enabled = enb
        n=['','#freeicon']
#        n+=[c[0].Caption for c in cols]
        new_extra = {}
        for acc in range(account_count):
            for line in range(BP.OperationCount[acc]):
                keys = BP.GetURL("extra_get:%s;%s" % (acc, line)).split(';')
                for key in keys:
                    if not key in n : new_extra[key]=1
        for key in new_extra.keys():
            if not key in extra.keys() : cols.append([make(CC,"TCheckBox", g4, Width = 160, Caption = key),True,False,'x',''])
        for i in range(len(cols)-1,nstd,-1) :
            if cols[i][0].Caption not in new_extra.keys():
                cols[i][0].visible = False
                cols.pop(i)
        extra = new_extra
        nstd=10
        nsup=len(cols)-nstd
    return cols


def export_html(Sender=None):
    if len(fcells) == 0:
        BP.MsgBox("Il n'y a aucune ligne à exporter", 64)
    else:
        # creation des en-têtes de table
        t_h = ''
        for h in cols:
            if h[0].Checked:
                t_h += '<th>%s</th>' %(h[0].Caption)
        #lignes de données - format
        t_l = '<tr%s><td>%s</td><td>%s</td>'
        for i in range(2,len(formats)):
            if formats[i]=='f':
                t_l+='<td class="right">%s</td>'
            elif formats[i] in 'sx':
                t_l+='<td>%s</td>'
        t_l+='</tr>'
        #lignes de données - données
        lines = []
        totals = {0: 0, 1: 0, 2: 0}
        odd = 0
        for ligne in fcells:
            l = copy(ligne)
            odd = not odd
            if odd: css = ' class="odd"'
            else: css = ""
            idx = [h[0].Caption for h in cols if h[0].Checked].index('Pointage')
            mark=0
            if l[idx]=='P': mark=1
            elif l[idx]=='R': mark=2
            idx = [h[0].Caption for h in cols if h[0].Checked].index('Montant')
            amount = l[idx]
            if mark in totals: totals[mark] += amount
            else: totals[mark] = amount
            for i in range(len(l)):
                if l[i]=='':l[i]='&nbsp;'
                elif isinstance(l[i],float): l[i]=fmt_float(l[i]).replace(' ','&nbsp;')
            c = [css, l[0], tup_to_str(l[1])]
            c+= l[2:]
            c = tuple(c)
            line = t_l % c
            lines.append(line)
        page = html_page %(len(lines), fmt_float(totals[1]), fmt_float(totals[2]), fmt_float(totals[0]), fmt_float(totals[0] + totals[1] + totals[2]))
        page = page.replace("{table_headers}", t_h)
        page = page.replace("{table_lines}", "\n".join(lines))
        bp_export_folder = BPEval("bp_export_folder")
        filename = "export.html"
        open(bp_export_folder + filename, "w").write(page)
        if BP.MsgBox("Le fichier %s a été créé dans le répertoire %s.\nSouhaitez-vous l'ouvrir ?" %(filename, bp_export_folder), MB_YESNO + MB_ICONINFORMATION) == ID_YES:
            BP.ShellExecute("open", bp_export_folder + filename, "", 1)
        
def export(Acc):
    if len(fcells) == 0:
        BP.MsgBox("Il n'y a aucune ligne à exporter", 64)
    else:
        #largeurs de colonnes
        w_line = ''
        for i,l in enumerate(w): w_line += 'F;W%d %d %d\n' %(i+1,i+1,l/5)
        #formats
        f_line = ''
        for i,f in enumerate(formats):
            if f=='d':   f_line += 'F;P19;FG0G;C%d\n' %(i+1)
            elif f=='f': f_line += 'F;P37;FF2G;C%d\n' %(i+1)
            else:        f_line += 'F;P0;FG0G;C%d\n' %(i+1)
        #en-têtes  
        '''C;K"Compte"
        F;P19;FG0C;X2
        C;K"Date"
        C;X3;K"Mode"
        C;X4;K"Tiers"
        C;X5;K"DNBetails"
        C;X6;K"CatNBegorie"
        F;P37;FF2C;X7
        C;K"Sous-catNBegorie"
        F;P37;FF2C;X8
        C;K"Montant"
        C;X9;K"Pointage"
        C;X10;K"Solde"'''
        h_line = ''
        i=0
        for h in cols:
            if h[0].Checked:
                h_line += 'C;X%d;K"%s"\n' %(i+1,h[0].Caption)
                i+=1
        #lignes de données - format
        tpl_line = '''C;Y%d;X1;K"%s"\nC;X2;K%d'''
        for i in range(2,len(formats)):
            tpl_line+='\n'
            if formats[i]=='f':
                tpl_line+='C;X%s;K' % (i+1); tpl_line+='''%.4f'''
            elif formats[i] in 'sx':
                tpl_line+='C;X%s;K' % (i+1); tpl_line+='''"%s"'''
        #lignes de données - données
        y = 2
        lines = []
        for l in fcells:
            c = [y, l[0], to_delphi_date(l[1])]
            c+= l[2:]
            c = tuple(c)
            line = tpl_line % c
            y += 1
            lines.append(line)
        #constitution du fichier
        template_path = BP.BankPerfectPluginPath().split("|")[1].replace(".py", ".slk")
        tpl = open(template_path, "r").read()
        tpl = tpl.replace("{count}", str(len(lines)).replace("{count-1}", str(len(lines)-1)))
        tpl = tpl.replace('{widths}',w_line)
        tpl = tpl.replace('{formats}',f_line)
        tpl = tpl.replace('{headers}',h_line)
        lines = "\n".join(lines)
        tpl = tpl.replace("{lines}", lines)
        bp_export_folder = BPEval("bp_export_folder")
        filename = "myGrunnReport.slk"
        open(bp_export_folder + filename, "w").write(tpl)
        if BP.MsgBox("Le fichier %s a été créé dans le répertoire %s.\nSouhaitez-vous l'ouvrir ?" %(filename, bp_export_folder), MB_YESNO + MB_ICONINFORMATION) == ID_YES:
            BP.ShellExecute("open", bp_export_folder + filename, "", 1)

Acc = BP.AccountCurrent()

def draw(S, ACol, ARow, R, State):
    if len(fcells)==0 : return
    Grid.FixedRows=1
    cv = S.Canvas
    header = headers[ACol]
    if "gdSelected" in State: cv.Brush.Color = 0x00dec5b9
    elif ARow > 0 and ARow % 2 == 0: cv.Brush.Color = 0x00f5f5f5
    align = R.Left + 5
    if ARow == 0:
        s = header
        cv.Font.Style = ["fsBold"]
    else:
        if formats[ACol]=='d':
            s = tup_to_str(fcells[ARow - 1][ACol])
        elif formats[ACol]=='f':
            s = fmt_float(fcells[ARow - 1][ACol])
        else:    
            s = fcells[ARow - 1][ACol]
        if header == "Montant" or header == "Solde":
            align = R.Right-cv.TextWidth(s)-5
            if '-' in s : cv.Font.Color = 0x000000CC
            else: cv.Font.Color = 0x00008800
    cv.TextRect(R, align, R.Top + 5, s)
    cv.Brush.Style = 1

# mise à jour des listes de comptes préférées
def maj_listes(Sender=None):
    global acc_list
    FormLists.show(lists)
    if Cvalue(bm_list_C)!='': acc_list = lists[Cvalue(bm_list_C)][0]
    filter_grid()


def def_cols():
    global cols, extra, E, headers, filters, formats, widths
    cols = load_PrefCols()
    E=[]
    for i in range(0,len(cols)):
        if len(E)<=i :
            E.append(make(CC,"TEdit", g1, Width=0))
            E[i].OnChange=filter_grid
    headers=[c[0].Caption for c in cols if c[0].Checked]
    filters=[c[1] for c in cols if c[0].Checked]
    formats=[c[3] for c in cols if c[0].Checked]
    widths =[c[4] for c in cols if c[0].Checked]
    g3.Height = g4.Height = (max(nstd,len(cols)-nstd)+2)*20
    f2.Height = g3.Height+margin*7+POK.Height

def fill_grid(S=None):
    global cells, headers, filters, formats, widths
    cells = []
    headers=[c[0].Caption for c in cols if c[0].Checked]
    filters=[c[1] for c in cols if c[0].Checked]
    formats=[c[3] for c in cols if c[0].Checked]
    widths =[c[4] for c in cols if c[0].Checked]
    for Acc in range(account_count):
        solde = 0
        for i in range(BP.OperationCount[Acc]):
            categ = BP.OperationCateg[Acc][i]
            categ = categs[categ]
            mark = BP.OperationMark[Acc][i]
            mark = ('', 'P', 'R')[mark]
            montant = BP.OperationAmount[Acc][i]
            suppl = BP.GetURL("extra_get:%s;%s" % (Acc, i)).split(';')
            solde += montant
            line = [BP.AccountName[Acc], str_to_tup(BP.OperationDate[Acc][i])]
            if cols[2][0].Checked : line.append(BP.OperationMode[Acc][i])
            if cols[3][0].Checked : line.append(BP.Operationthirdparty[Acc][i])
            if cols[4][0].Checked : line.append(BP.OperationDetails[Acc][i])
            if cols[5][0].Checked : line.append(categ[0])
            if cols[6][0].Checked : line.append(categ[1])
            line.append(montant)
            if cols[8][0].Checked : line.append(mark)
            if cols[9][0].Checked : line.append(solde)
            for j in range(len(extra.keys())):
                if cols[10+j][0].Checked:
                    if cols[10+j][0].Caption in suppl:
                        line.append(BP.GetURL("extra_get:%s;%s;%s" % (Acc, i,cols[10+j][0].Caption)))
                    else:
                        line.append('')
            cells.append(line)
    Grid.ColCount = len(line)
    filter_grid()

def filter_grid(Sender=None):
    global fcells,mts,acc_list#,group_logo
    acc_list = []
    if bm_list_C.ItemIndex!=-1 :
        for UId in lists[Cvalue(bm_list_C)][0]:
            acc_list.append(UId)
#            selected_accounts.append(int(BP.GetURL("get_account_id_from_uid:%s" % UId)))
#        group_logo = lists_logos[bm_list_C.Items[bm_list_C.ItemIndex]]
#        if bm_list_C.ItemIndex!=-1: bm_logo.picture.LoadFromFile(group_logo)
    bm_list_C.Hint = '\n'.join([acc for acc in display_accounts if accounts_uid_from_id[real_index[acc]] in acc_list])

    temp = []
    fcells = []
    D2.Visible = D0.Checked
    dd=from_delphi_date(D1.Date)
    df=from_delphi_date(D2.Date)
    somme = 0
    mts = -1
    if 'Montant' in headers:  mts = headers.index('Montant')
    for c in cells:
        if accounts_uid_from_id[real_index[c[0]]] in acc_list: temp.append(c)

    for c in temp:
        OK = True            
        if D0.Checked:
            if c[1]<dd or c[1]>df : OK = False
        else:
            if c[1]<dd : OK = False
        if OK:
            for i in range(0,Grid.Colcount):
                if formats[i] in 'sx':
                    if len(E[i].Text)>0 and E[i].Text[0]=='/':
                        s=E[i].Text[1:].lower()
                        if s=='':
                            if c[i]!='': OK = False
                        elif not s in c[i].lower()and c[i]!='': OK = False
                    elif len(E[i].Text)>0 and E[i].Text[0]=='*':
                        s=E[i].Text[1:].lower()
                        if s=='':
                            if c[i]=='': OK = False
                        elif c[i]=='' or s in c[i].lower(): OK = False
                    elif len(E[i].Text)>0 and E[i].Text[0]=='-':
                        s=E[i].Text[1:].lower()
                        if s=='':
                            if c[i]!='': OK = False
                        elif s in c[i].lower(): OK = False
                    elif not E[i].Text.lower() in c[i].lower(): OK = False
                elif formats[i]=='f':
                    ops = ["<=",">=","<>","<",">","="]
                    found = False
                    for op in ops:                        
                        if len(E[i].Text)>=len(op):
                            limit = str_to_float(E[i].Text[len(op):])
                            op2 = op
                            if op == "=": op2 = "=="
                            if not found and E[i].Text.startswith(op):
                                found = True
                                if not eval("%f %s %f" % (c[i],op2,limit)):
                                    OK=False
                    if not found and E[i].Text!="":
                        if not E[i].Text in fmt_float(c[i]) : OK=False
        if OK:
            fcells.append(c)
            if mts!=-1: somme += c[mts]
    total.Caption = fmt_float(somme)
    Grid.RowCount = len(fcells)+1
    Grid.Repaint()
#    trace('cols')

def keycmp_asc(a,b):
    return cmp((a,b),(b,a))
def keycmp_desc(a,b):
    return cmp((b,a),(a,b))
def sortGrid(c):
    global fcells, last_sort, sens
    temp = [(f[c],f) for f in fcells]
    if c==last_sort: sens=[keycmp_asc,keycmp_desc][sens==keycmp_asc]
    else: sens=keycmp_asc
    if sens == keycmp_asc: sort_btn.Picture.LoadFromFile(Path + "icons\\tria.png")
    else:                  sort_btn.Picture.LoadFromFile(Path + "icons\\trid.png")
    temp.sort(sens)
    fcells = [f[1] for f in temp]
    last_sort=c
    Grid.Repaint()

def Grid_clic(Sender,button,b,x,y):
    '''traitement d'un clic dans la grille'''
    #clic gauche sur un titre
    if button == 'mbLeft' and y<Grid.DefaultRowHeight:
        #recherche de la colonne cliquée
        c=0; s=0
        while s<x and c<Grid.ColCount:
            s+=w[c]+1
            c+=1
        sort_btn.Left=sum(w[:c])-sort_btn.Width-5+c; sort_btn.Repaint()
        sortGrid(c-1)
        
def col_size():
    global w
    c=Grid.ColCount
    w=[0]*c
    for i in range(Grid.ColCount):
        if formats[i] in 'sf':
            w[i]=Grid.Canvas.TextWidth(widths[i])+10
            c-=1
        elif formats[i] == 'd':
            w[i]=Grid.Canvas.TextWidth('01-01-2000')+25
            c-=1
        else:
            w[i]=0
    elevator=25
    default=1
    if c !=0: default=(Grid.Width-elevator-sum(w)-(Grid.ColCount-c))/c-1
    for i in range(Grid.ColCount):
        if w[i]==0: w[i] = default
    Grid.Repaint()

def ResizeForm(Sender=None):
    global w, dH
    cW = f1.ClientWidth
    cH = f1.ClientHeight/1.0001

    f1_panel.Width=cW-2;f1_panel.Height=cH
    bm.Left = cW-bm.Width-margin/2; bm.Top = margin-4
    bm_list_C.Left = bm.Left-bm_list_C.Width-margin/2; bm_list_C.Top = bm.Top
    bm_label.Left = bm_list_C.Left-bm_label.Width-margin/2; bm_label.Top = bm_list_C.Top+4

    g1.SetBounds(5,bm.top+bm.Height,cW-margin,g1.Height)

    Grid.Left=g1.Left; Grid.Top=g1.Top+g1.Height+5; Grid.Width=g1.Width; 
    col_size()
    sort_btn.Left=sum(w[:last_sort+1])-sort_btn.Width-5
    for i in range(Grid.ColCount): Grid.ColWidths[i]=w[i]

    E[0].Left=Grid.Left+1; E[0].Top=g1.Font.Size+15; E[0].Width=w[0]-5
    for i in range(1,Grid.ColCount):
        E[i].Left=E[i-1].Left+E[i-1].Width+2; E[i].Top=E[i-1].Top; E[i].Width=w[i]-1
        if formats[i]=="d": E[i].visible=False
    for i in range(2,Grid.ColCount):
        if not filters[i]:
            E[i].Text=''
            E[i].Visible = False

    D1.Left=w[0]+3 ; D1.Width=w[1]-1; D1.Top=g1.Font.Size+5
    D2.Left=D1.Left; D2.Width=w[1]-1; D2.Top=D1.Top+D1.Height
    D0.Left=D1.Left-D0.Width-1; D0.Top=D2.Top+7

    Cancel.Left=cW-Cancel.Width-margin; Cancel.Top=cH-Cancel.Height-15
    BOK.Left=Cancel.Left-BOK.Width-5; BOK.Top=Cancel.Top
    BHTML.Left=BOK.Left-design.Width-5; BHTML.Top=Cancel.Top
    design.Left = BHTML.Left-design.Width-5; design.Top=Cancel.Top
    Lversion.Left=Cancel.Left; Lversion.Top=Cancel.Top+Cancel.Height;  Lversion.Width=50
    total.Top = Cancel.Top-20; total.left=E[8].Left-Grid.Canvas.TextWidth(total.Caption)*1.7

    Grid.Height=total.Top-Grid.Top

def resize_f2(Sender=None):
    global cols
    cW = f2.ClientWidth
    cH = f2.ClientHeight/1.0001
    f2_panel.Width=cW-2;f2_panel.Height=cH
    g3.Width = g4.Width = (cW-margin*3)/2
    g3.Left=margin; g4.Left=g3.Width+margin*2
    cols[0][0].Left = margin; cols[0][0].Top = margin*2
    for i in range(1,nstd):
        cols[i][0].Left = margin; cols[i][0].Top = cols[i-1][0].Top+20
    if nsup>0:
        cols[nstd][0].Left = margin; cols[nstd][0].Top = margin*2
        for i in range(1,nsup):
            cols[nstd+i][0].Left = margin; cols[nstd+i][0].Top = cols[nstd+i-1][0].Top+20
       
    POK.Left =  cW-POK.Width-margin; POK.Top=cH-POK.Height 

def Exit(Sender):
    global f1
    f1.ModalResult = 2
    params['position']=[f1.Left,f1.Top,f1.Width,f1.Height]
    for c in cols : c[0]=c[0].Caption, c[0].Checked, c[0].Enabled
    params['cols']=cols
    params['lists']=lists
    params['list']=bm_list_C.itemIndex
    set_params(params)


def fOK(Sender):
    global f1
    f1.ModalResult = 1
    return

def PValid(Sender):
    fill_grid()
    ResizeForm(None)
    f2.ModalResult = 1

def perso(Sender):
    f2.ShowModal()
#-------------------------------------------------------------------------------
# formulaire principal
f1 = CreateComponent("TForm", None)
f1.SetProps(Width=900, Height=600, Caption="GrunnReport")
f1_panel = make(CC,"TPanel", f1, BorderStyle = "bsNone")
make(CC,"TImage", f1_panel, Width=1700, Height=1400, Picture=Path + "icons\\Ciel.png")
#----grille
Grid = CreateComponent("TDrawGrid", f1)
Grid.SetProps(Parent=f1, Left=20, Top=150, Width=800, Height=347, ScrollBars="ssBoth", FixedRows=1, FixedCols=0, RowCount=2, FixedColor=clBtnFace, OnDrawCell=draw, OnMouseUp=Grid_clic, Options=["goHorzLine", "goVertLine", "goDrawFocusSelected", "goRowSelect", "goThumbTracking","goFixedHorzLine","goColSizing","goFixedVertLine"])
sort_btn=make(CC,"TImage", Grid, Top=5, Width=15, Height=15, Picture=Path + "icons\\tria.png")
sort_btn.Enabled=False


#----groupe filtrage
g1 = make(CC,"TGroupBox", f1_panel, Caption=" Filtrage ", FontStyle=["fsBold","fsItalic"], FontSize=9, Left=30, Top=25, Width=175, Height=65, ShowHint=1, Hint="""abc  : non vide et contient 'abc'\n*      : non vide\n*abc: non vide ET sans 'abc'\n/      : vide\n/abc: vide OU contient 'abc'\n-abc: vide OU sans 'abc'""")
make(CC,"TImage", g1, Left = 0, Top = Grid.Canvas.TextHeight('A')/1.5, Width=1700, Height=100, Picture=Path + "Icons\\fond_filtre.png")
D1 = make(CC,"TDateTimePicker", g1, Left=30, Top=15, Width=95, Date=time.mktime(time.localtime()) / 86400 + 25569)
D0 = make(CC,"TCheckBox", g1, Width=10)
D2 = make(CC,"TDateTimePicker", g1, Left=30, Top=13, Width=95, Date=time.mktime(time.localtime()) / 86400 + 25569)
# choix du groupe de comptes
bm = make(CC,"MyButton", f1_panel, Left = 15, Top = 0, Width=26, Height=26, OnClick=maj_listes, ShowHint=True, Hint='Gérer les groupes de comptes', Picture=Path + "Icons\\bookmark.png")
bm_label  = make(CC, "TLabel", f1_panel, Caption="Sélection des comptes ", Left = 50, Top = 5, FontSize=9, FontStyle=["fsBold", "fsItalic"])
bm_list_C = make(CC, "TComboBox", f1_panel, Left = 200, Top = 2, Width=120, FontSize = 9, OnClick=filter_grid, ShowHint=True, Hint='' , Style="csDropDownList")
#----total des montants affichés
total = make(CC,"TLabel",f1_panel,Caption = "", Width = 10, FontStyle = ["fsBold"], FontSize = 11)
#----bouton de sélection des colonnes à afficher
design = make(CC,'MyButton',f1_panel, Width=55, Height=55, OnClick=perso, ShowHint=1, Hint="Personnalisation des colonnes", Picture=Path + "icons\\design.png")
#----bouton de sortie
Cancel = make(CC,'MyButton',f1_panel, Width=55, Height=55, OnClick=Exit, ShowHint=1, Hint="Exit", Picture=Path + "icons\\fin.png")
#----bouton de validation
BOK = make(CC,'MyButton',f1_panel, Width=55, Height=55, OnClick=export, ShowHint=1, Hint="Export vers tableur", Picture=Path + "icons\\export.png")
BHTML = make(CC,'MyButton',f1_panel, Width=55, Height=55, OnClick=export_html, ShowHint=1, Hint="Export HTML", Picture=Path + "icons\\html.png")
Lversion = make(CC,"TLabel",f1_panel,Caption = " v%s "%version, FontStyle = ["fsItalic"])

# formulaire de gestion des groupes de comptes
FormLists = AccountsListsForm(CC, bm_list_C)

#-------------------------------------------------------------------------------
# formulaire de personnalisation des colonnes
f2 = CreateComponent("TForm", None)
f2.SetProps(Position="poMainFormCenter", Width=500, Height=600, Caption="Choix des colonnes à afficher")
f2_panel = make(CC,"TPanel", f2, BorderStyle = "bsNone")
make(CC,"TImage", f2_panel, Width=1700, Height=1400, Picture=Path + "icons\\Ciel.png")
g3 = make(CC,"TGroupBox", f2_panel, Caption=" Champs standards ", FontStyle=["fsBold","fsItalic"], FontSize=9, Left=15, Top=25, Width=175, Height=220)
g4 = make(CC,"TGroupBox", f2_panel, Caption=" Champs supplémentaires ", FontStyle=["fsBold","fsItalic"], FontSize=9, Top=25, Width=175, Height=220)
#----bouton de validation
POK = make(CC,"TImage", f2_panel, Width=50, Height=50, OnClick=PValid, ShowHint=1, Hint="Validation", Picture=Path + "icons\\OK_on.png")
#POK = make(CC,"MyButton", f2_panel, Width=50, Height=50, OnClick=PValid, ShowHint=1, Hint="Validation", Picture=Path + "icons\\OK_on.png")
#----cases à cocher
def_cols()
# initialisation des froupes de comtpes
lists = params.get('lists',{})
group = params.get('list',-1)
klist = lists.keys()
klist.sort()
bm_list_C.Items.Text = FormLists.cb_lists.Items.Text = '\n'.join(klist)
bm_list_C.Hint = '\n'.join([acc for acc in display_accounts if accounts_uid_from_id[real_index[acc]] in acc_list])
if lists!={}:
    if group>len(klist) or group==-1: group=0
    bm_list_C.ItemIndex = FormLists.cb_lists.ItemIndex = group
    acc_list = lists[klist[group]]
else:
    BP.MsgBox("Aucun groupe de comptes n'a été trouvé\nConfigurez un groupe de comptes", 0)
    err_group = True
if bm_list_C.ItemIndex!=-1:
    try: bm_logo.picture.LoadFromFile(lists_logos[bm_list_C.Items[bm_list_C.ItemIndex]])
    except: pass


DateMin = [2000,1,1]
DateMax = str_to_tup("") #date du jour
D1.Date=to_delphi_date(DateMin)
D2.Date = to_delphi_date(DateMax)
D0.Checked = True
sens=keycmp_asc
D1.OnChange = D2.OnChange = D0.OnClick = filter_grid
fill_grid()
f1.OnResize=ResizeForm
f2.OnResize=resize_f2

if len(params.get('position',[]))==4:
    f1.Left,f1.Top,f1.Width,f1.Height = params['position']
else:
    f1.Position = "poMainFormCenter"

ResizeForm(None)

f1.ShowModal()
