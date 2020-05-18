# To change this template, choose Tools | Templates
# and open the template in the editor.

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

__author__="Bob"
__date__ ="$27 déc. 2013 17:38:41$"
from GUI import *
from fCombo import *

import BP
Path = BP.BankPerfectPluginPath()
Path = Path[1:Path.rfind("\\") + 1]

class AccountsListsForm:
    def __init__(self, CC, linked_combo):
        '''
        Formulaire pour la mise à jour des listes de comptes
        
        paramètres :
            - CC     = fonction CreateComponent
            - linked_combo = liste déroulante du formulaire parent qui contient la liste des groupes de comptes
            
        Avant d'appeler le formulaire, il faut lui passer les variables en appelant la fonction .prepare 
        Les variables sont :
            - lists       = liste des groupes de comptes + logo = {list1:[[Uid1, Uid2, ...], "logo1"], list2:[[...],"logo2"], ...}
            - lists_logos = logos associés aux listes de comptes
        
        la liste de linked_combo est mise à jour
        à la fermeture, linked_combo est positionné sur la même valeur que la liste déroulante du formulaire "AccountsLists"
        '''
        self.linked_combo = linked_combo
        self.lists = {}
        self.display_accounts = BP.GetURL("get_accounts").split(";")
        self.group_logo = Path + "groups\\_pas de logo_.png"

        self.init_accounts()

        self.form = CC("TForm", None)
        self.form.SetProps(Width=420, Height=350, Caption = "Mise à jour des listes de comptes")
        self.form.OnClose=self.update
        self.back = make(CC,"TImage", self.form, Left = 0, Top = 0, Picture=Path + "Icons\\ciel.png")
        self.ll0 = make(CC, "TLabel", self.form, FontSize = 10, FontStyle = ["fsBold","fsItalic"], Caption="Afficher la liste :  ")
        self.ll1 = make(CC, "TLabel", self.form, FontSize = 10, FontStyle = ["fsBold","fsItalic"], Caption="Enregistrer sous le nom :  ")
        self.cb_lists = make(CC, "TComboBox", self.form, OnClick=self.init_lists)
        self.cb_lists.Style="csDropDownList"
        self.list0 = make(CC,"TListBox", self.form, FontSize = 10); self.list0.OnClick = self.swap
        self.list1 = make(CC,"TListBox", self.form, FontSize = 10); self.list1.OnClick = self.swap
        self.picker = make(CC,"MyButton", self.form, Width=54, Height=44, OnClick=self.pick_logo, ShowHint=1, Hint="Choisir une icône pour ce groupe ", Picture=Path + "groups\\_pas de logo_.png")
        self.new_list = make(CC, "TEdit", self.form)
        self.new_list.OnChange=self.resize_lists
        self.ok_list = make(CC, "TImage", self.form, Width=24, Height=24, OnClick=self.set_list, Picture=Path + "icons\\ok3.png")
        self.ko_list = make(CC, "TImage", self.form, Width=24, Height=24, OnClick=self.del_list, Picture=Path + "icons\\ko3.png")
        self.form.OnResize=self.resize_lists

        self.set_list()

    def init_accounts(self):
        self.real_index = {}
        display_index = {}
        for i, name in enumerate(self.display_accounts):
            p = name.find("=")
            if p == -1: continue
            index = int(name[:p], 10)
            name = name[p+1:]
            self.display_accounts[i] = name
            self.real_index[name] = index

    def show(self,lists):
        self.lists = lists
        self.klist = self.lists.keys()
        self.klist.sort()
        if self.cb_lists.Items.ToList!=self.klist:
            self.cb_lists.Items.Text='\n'.join(self.klist)
            self.cb_lists.ItemIndex=0
            self.init_lists()
        else:
            self.init_lists()
        current = Cvalue(self.linked_combo)
#        if self.linked_combo.ItemIndex!=-1: current = Cvalue(self.linked_combo)
#        else: current=""
#        self.cb_lists.ItemIndex = Ivalue(self.cb_lists,current)
        self.cb_lists.ItemIndex = self.cb_lists.Items.Text.split('\n').index(current)        
        self.form.ShowModal()
        self.linked_combo.Hint = self.cb_lists.Items.Text

    def update(self,Sender,x):
        if self.cb_lists.ItemINdex!=-1:
            self.linked_combo.ItemIndex = Ivalue(self.linked_combo,Cvalue(self.cb_lists))
        

    def swap(self,Sender):
        idx = Sender.ItemIndex
        if idx!=-1:
            if Sender == self.list0:
                self.list1.Items.Add(self.list0.Items[idx])
                l = self.list1.Items.ToList()
                l.sort()
                self.list1.Items.Text='\n'.join(l)
                self.list0.Items.Delete(idx)
            else:
                self.list0.Items.Add(self.list1.Items[idx])
                l = self.list0.Items.ToList()
                l.sort()
                self.list0.Items.Text='\n'.join(l)
                self.list1.Items.Delete(idx)

    def pick_logo(self,Sender=None):
        self.group_logo = BP.OpenDialog("Choisissez un logo", Path + "Groups\\*.png", "*.png", "Fichiers image (*.png)")
        if self.group_logo=='': self.group_logo = Path + "groups\\_pas de logo_.png"
        self.picker.ToTuple()[0].Picture.LoadFromFile(self.group_logo)

    def init_lists(self,Sender=None):
        self.list0.Items.Text=''
        self.list1.Items.Text=''
        if self.cb_lists.ItemIndex!=-1:
            name = Cvalue(self.cb_lists) 
            current_list = self.lists[name][0]
            self.new_list.Text=name
            self.group_logo = self.lists[name][1] #self.lists.get(name,Path + "groups\\_pas de logo_.png")
            self.picker.ToTuple()[0].Picture.LoadFromFile(self.group_logo)
        else:
            current_list=[]
            self.new_list.Text=''
            self.group_logo = Path + "groups\\_pas de logo_.png"
        for idx in self.display_accounts:
            UId = BP.GetURL("get_account_uid_from_id:%s" % self.real_index[idx])
            if UId in current_list:
                self.list1.Items.Add(idx)
            else:
                self.list0.Items.Add(idx)

    def set_list(self,Sender=None):
        self.new_list.color = 0x0080ffff; self.new_list.Repaint()
        name = self.new_list.Text
        # si le nom existe déjà: effacer
        if name in self.lists.keys(): self.lists.pop(name)
        # mettre le contenu de la liste 1 dans le dictionnaire 'lists'
        self.lists[name]=[[BP.GetURL("get_account_uid_from_id:%s" % self.real_index[acc]) for acc in self.list1.Items.Text.split('\n')[:-1]], self.group_logo]
        self.klist = self.lists.keys()
        self.klist.sort()
        self.cb_lists.Items.Text = '\n'.join(self.klist); self.cb_lists.ItemIndex = self.cb_lists.Items.Text.split('\n').index(name)
        self.init_lists(Sender)
        if self.linked_combo.ItemIndex!=-1: name_list = self.linked_combo.Items[self.linked_combo.ItemIndex]
        else: name_list='~~'
        self.linked_combo.Items.Text = '\n'.join(self.klist)
        if name_list in self.linked_combo.Items.Text:
           self.linked_combo.ItemIndex = self.linked_combo.Items.Text.split('\n').index(name_list)
        else:
           self.linked_combo.ItemIndex = -1
        time.sleep(0.3); self.new_list.color = 0x00ffffff; self.new_list.Repaint()

    def del_list(self,Sender):
        list = self.cb_lists.Items[self.cb_lists.ItemIndex]
        self.lists.pop(list)
        self.klist = self.lists.keys()
        self.klist.sort()
        self.cb_lists.Items.Text='\n'.join(self.klist)
        self.init_lists(Sender)
        if self.linked_combo.ItemIndex!=-1: name_list = self.linked_combo.Items[self.linked_combo.ItemIndex]
        else: name_list='~~'
        self.linked_combo.Items.Text = '\n'.join(self.klist)
        if name_list in self.linked_combo.Items.Text:
            self.linked_combo.ItemIndex = self.linked_combo.Items.Text.split('\n').index(name_list)
        else:
            self.linked_combo.ItemIndex = -1

    def resize_lists(self,Sender=None):
        cW = self.form.ClientWidth
        cH = self.form.ClientHeight
        self.back.Width = cW; self.back.Height = cH
        margin = 15

        self.ll0.Top = margin
        self.list0.Left=margin; self.list0.Top=self.ll0.Top+self.ll0.Height+margin/2; self.list0.Width=150; self.list0.Height=200
        self.list1.Left=self.list0.Left+self.list0.Width+margin; self.list1.Top=self.list0.Top; self.list1.Width=150; self.list1.Height=200
        self.ll0.Left = self.list1.Left-self.ll0.Width
        self.cb_lists.Left = self.list1.Left; self.cb_lists.Top = margin-4; self.cb_lists.Width = self.list1.Width

        self.ll1.Top = self.list1.Top+self.list1.Height+margin/2; self.ll1.Left = self.list1.Left-self.ll1.Width
        self.new_list.Left = self.list1.Left; self.new_list.Top = self.ll1.Top-4; self.new_list.Width=self.list1.Width
        self.ok_list.Left = self.new_list.Left+self.new_list.Width+margin/2; self.ok_list.Top = self.new_list.Top-2
        self.ok_list.visible = self.new_list.Text!=''
        self.ko_list.Left = self.cb_lists.Left+self.cb_lists.Width+margin/2; self.ko_list.Top = self.cb_lists.Top-2
        self.ko_list.visible = self.cb_lists.ItemIndex!=-1
        self.picker.Left = self.list1.Left+self.list1.Width+margin/2
        self.picker.Top = self.list1.Top


if __name__ == "__main__":
    print "Hello World"
