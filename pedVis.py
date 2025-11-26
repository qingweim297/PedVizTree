import os
from django.http import JsonResponse
import networkx as nx
import numpy as np
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from app01 import models
from pyvis.network import Network
import json


# get cleaned data of the pedigree excel,delete nan value row
def get_cleaned_member(filename):
    file = pd.read_excel(filename)
    child = file['Ind']
    Sire = file['Sire']
    Dam = file['Dam']
    pedigree_member = pd.concat([child, Sire, Dam], axis=1)
    cleaned_member = pedigree_member.dropna(axis=0, how='any')
    return cleaned_member


# get no repeated member list
def get_member_list(filename):
    cleaned_member = get_cleaned_member(filename)
    progeny_member = cleaned_member['Ind'].unique()
    parent_member = np.concatenate((cleaned_member['Sire'].unique(), cleaned_member['Dam'].unique()), axis=0)
    member_list = np.concatenate((progeny_member, parent_member), axis=0)
    return member_list


# get the [id,sire,dam] list and id:[sire,dam] dict
def get_pedigree_matrix(filename):
    cleaned_member = get_cleaned_member(filename)
    pedigree_id = cleaned_member['Ind'].values
    pedigree_sire = cleaned_member['Sire'].values
    pedigree_dam = cleaned_member['Dam'].values
    pedigree_matrix = np.vstack((pedigree_id, pedigree_sire, pedigree_dam))
    pedigree_matrix = pedigree_matrix.transpose()
    return pedigree_matrix


# Use pyvis and networkx to draw the network of pedigree
def draw_network_excel(request):
    if request.method == 'POST':
        data = request.POST
        uploaded_file = request.post.FILES['file']
        filename = uploaded_file.name
    member_list = get_member_list(filename)
    pedigree_matrix = get_pedigree_matrix(filename)
    G = nx.DiGraph()
    same_parents = []
    baby = []
    family_members = {}
    for row in pedigree_matrix:
        child = row[0]
        parents = row[1:]
        family_members[child] = parents
    # 寻找回交个体
    back_self = []
    for row in pedigree_matrix:
        sire, dam = row[1], row[2]
        for other_row in pedigree_matrix:
            if other_row[0] != row[0]:
                if (other_row[0] == sire and other_row[1] == dam or
                        other_row[0] == sire and other_row[2] == dam or
                        other_row[0] == dam and other_row[1] == sire or
                        other_row[0] == dam and other_row[2] == sire):
                    back_self.append(row[0])
    # 寻找自交个体
    inbred_self = []
    for row in pedigree_matrix:
        if parents[0] != 0 and parents[1] != 0:
            if row[1] == row[2]:
                same_parents.append(row[1])
                inbred_self.append(row[0])
    # add node to pic
    for member in member_list:
        if member not in back_self and member not in inbred_self:
            G.add_node(member, color='grey', value=float(np.sum(pedigree_matrix == member)))  # 杂交、自然野生个体标记为灰色点
        elif member in back_self:
            G.add_node(member, color='blue', value=float(np.sum(pedigree_matrix == member)))  # 回交个体标记为蓝色
        else:
            G.add_node(member, color='yellow', value=float(np.sum(pedigree_matrix == member)))  # 自交个体标记为黄色
    # 添加边(父母关系)
    for child, parents in family_members.items():
        if parents[0] != parents[1]:
            father = parents[0]
            mother = parents[1]
            G.add_edge(father, child, color='orange', label='sire')  # 父本通过有向箭头表示传递关系，橙色为指示色
            G.add_edge(mother, child, color='blue', label='dam')  # 母本蓝色为指示色
        else:
            father = parents[0]
            G.add_edge(father, child, color='green')  # 自交绿色为指示色
    nt = Network(height="1000px", width='100%', directed=True)
    nt.from_nx(G)
    nt.show(r'D:\gms\templates\net_excel.html')
    return render(request, 'net_excel.html')


# def upload_excel_to_net(request):
#     return render(request, 'excel_to_net.html')


class FileModelForm(forms.ModelForm):
    class Meta:
        model = models.ExcelNet
        fields = ["name", "file"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def excel_upload(request):
    if request.method == "GET":
        form = FileModelForm()
        return render(request, 'excel_to_net.html', {'form': form})
    form = FileModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/excel_to_net/')
    print(form.errors)
    return render(request, 'excel_to_net.html', {'form': form})


# get cleaned data of the pedigree excel,delete nan value row
def data_member_list(cleaned_ped):
    progeny_member = cleaned_ped['germ_id'].unique()
    parent_member = np.concatenate((cleaned_ped['Sire'].unique(), cleaned_ped['Dam'].unique()), axis=0)
    all_member = np.concatenate((progeny_member, parent_member), axis=0)
    all_member_except = [a_ for a_ in all_member if a_ == a_]  # get no repeated member list except nan value
    pedigree_id = cleaned_ped['Ind'].values
    pedigree_sire = cleaned_ped['Sire'].values
    pedigree_dam = cleaned_ped['Dam'].values
    pedigree_matrix = np.vstack((pedigree_id, pedigree_sire, pedigree_dam))
    pedigree_matrix = pedigree_matrix.transpose()  # get the [id,sire,dam] list and id:[sire,dam] dict
    return all_member_except, pedigree_matrix


# Use pyvis and networkx to draw the network of pedigree
def draw_network_data(request):
    pedigree_member = pd.DataFrame(list(models.PedigreeTree.objects.all().values('germ_id', 'Sire', 'Dam')))
    cleaned_ped = pedigree_member.dropna(subset=['Sire', 'Dam'], how='all')
    all_member, pedigree_matrix = data_member_list(cleaned_ped)
    G = nx.DiGraph()
    same_parents = []
    family_members = {}
    for row in pedigree_matrix:
        child = row[0]
        parents = row[1:]
        family_members[child] = parents
    # 寻找回交个体
    back_self = []
    for row in pedigree_matrix:
        sire, dam = row[1], row[2]
        for other_row in pedigree_matrix:
            if other_row[0] != row[0] and isinstance(row[1], str) and isinstance(row[2], str):
                if (other_row[0] == sire and other_row[1] == dam or
                        other_row[0] == sire and other_row[2] == dam or
                        other_row[0] == dam and other_row[1] == sire or
                        other_row[0] == dam and other_row[2] == sire):
                    back_self.append(row[0])
    # 寻找自交个体
    inbred_self = []
    for row in pedigree_matrix:
        if row[1] == row[2]:
            same_parents.append(row[1])
            inbred_self.append(row[0])
    #  寻找半同胞个体
    half_self = []
    for row in pedigree_matrix:
        if type(row[1]) == float or type(row[2]) == float:
            half_self.append(row[0])
    # add node to pic
    for member in all_member:
        if member in back_self:
            G.add_node(member, color='blue', value=float(np.sum(pedigree_matrix == member)),
                       title='该个体在交配过程出现了' + str(np.sum(pedigree_matrix == member)) + '次')
        elif member in inbred_self:
            G.add_node(member, color='yellow', value=float(np.sum(pedigree_matrix == member)),
                       title='该个体在交配过程出现了' + str(np.sum(pedigree_matrix == member)) + '次')
        elif member in half_self:
            G.add_node(member, color='red', value=float(np.sum(pedigree_matrix == member)),
                       title='该个体在交配过程出现了' + str(np.sum(pedigree_matrix == member)) + '次')
        else:
            G.add_node(member, color='grey', value=float(np.sum(pedigree_matrix == member)),
                       title='该个体在交配过程出现了' + str(np.sum(pedigree_matrix == member)) + '次')
    # 添加边(父母关系)
    for child, parents in family_members.items():
        if isinstance(parents[0], str) and isinstance(parents[1], str) and parents[0] != parents[1]:
            father = parents[0]
            mother = parents[1]
            G.add_edge(father, child, color='orange', label='sire')
            G.add_edge(mother, child, color='blue', label='dam')
        elif isinstance(parents[0], float) and isinstance(parents[1], str):
            mother = parents[1]
            G.add_edge(mother, child, color='blue', label='dam')
        elif isinstance(parents[0], str) and isinstance(parents[1], float):
            father = parents[0]
            G.add_edge(father, child, color='orange', label='sire')
        else:
            father = parents[0]
            G.add_edge(father, child, color='green')
    nt = Network(height="1000px", width='100%', directed=True)
    nt.from_nx(G)
    nt.show(r'D:\gms\templates\pedigree_vis.html')
    return render(request, 'pedigree_vis.html')


# def upload_excel_to_net(request):
#     return render(request, 'excel_to_net.html')

def show_network(request):
    return render(request, 'nxt_sel1.html')


def json_export(request):
    return render(request,'pedigree_net.html')
#     file_path = os.path.join('static', 'json', 'test_nodes.json')
#     with open(file_path, 'r', encoding='UTF-8') as f:
#         data = json.load(f)
#     return render(request,'pedigree_net.html',{'data':data})
    # return JsonResponse(data)
