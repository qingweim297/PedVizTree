import tkinter.messagebox

from django.contrib import messages
from django.http import HttpResponseRedirect
from tkinter import *

from django.shortcuts import render

from models import *

def alter_pedigree(request):
    if request.method == 'POST':
        germ_id = request.POST.get('germ_id')
        if len(germ_id) != 11:
            tkinter.messagebox.showinfo('提示','输入种质资源编号有误')
            mainloop()
            return HttpResponseRedirect("/add_pedigree/")
    return render(request, 'pedigree_add.html')
