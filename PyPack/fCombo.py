#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# fonction qui retroune la valeur choisie d'une combobox
def Cvalue(c):
    if c.ItemIndex == -1: return ""
    v = c.Items[c.ItemIndex]
    return v

# fonction qui retourne le nombre de valeurs dans une ComboBox
def Nvalue(c):
    if c.Items.Text == "": return 0
    return len(c.Items.ToList())

# fonction qui retourne l'index d'une valeur dans une ComboBox
def Ivalue(c,v):
    if not v in c.Items.Text : return -1
    return c.Items.ToList().index(v)
