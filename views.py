import hashlib
import json

import matplotlib
import numpy as np
from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.db.models import Count
from django.forms import ValidationError, model_to_dict  # ② 把model对象转换成dict
from django.http import JsonResponse  # ①通过JsonResponse返回请求
import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import preprocessing
# import statsmodels.api as sm
# import statsmodels.formula.api as smf
from app01 import models
# 种质展示列表
from app01.models import LmsUser
from bms.upload import getNewName
from .models import PedigreeTree
from app01.models import PedigreeMPTT


# Create your views here.


def upload_handle(request):
    # 获取一个文件管理器对象
    file = request.FILES['pic']

    # 保存文件
    new_name = getNewName('GermPIC')  # 具体实现在自己写的uploads.py下
    # 将要保存的地址和文件名称
    where = '%s/photos/%s' % (settings.MEDIA_ROOT, new_name)
    #  分块保存image
    content = file.chunks()
    with open(where, 'wb') as f:
        for i in content:
            f.write(i)
    # 返回的http response
    return HttpResponse('ok')


def germplasm_list(request):
    germplasm = models.germplasm.objects.all()
    return render(request, 'germ_list.html', {'germ_list': germplasm})


def show_GermPIC_list(request):
    GermImage = models.GermImage.objects.all()
    return render(request, 'show_image.html', {'image_list': GermImage})


# 删除种质
def drop_germplasm(request):
    drop_id = request.GET.get('id')
    drop_obj = models.germplasm.objects.get(id=drop_id)
    drop_obj.delete()
    return redirect('/germ_list/')


# 添加谱系成员
def add_pedigree(request):
    if request.method == 'POST':
        new_pedigree_name = request.POST.get('pedigree_name')
        new_pedigree_f = request.POST.get('parent_f')
        new_pedigree_m = request.POST.get('parent_m')
        new_pedigree_id = request.POST.get('germ_id')
        # if len(new_pedigree_id) != 11:
        #     tkinter.messagebox.showinfo('提示', '输入种质资源编号有误')
        #     return HttpResponseRedirect("/add_pedigree/")
        models.pedigree.objects.create(pedigree_name=new_pedigree_name,
                                       parent_f=new_pedigree_f,
                                       parent_m=new_pedigree_m,
                                       germ_id=new_pedigree_id)
        return redirect('/pedigree_list/')
    return render(request, 'pedigree_add.html')


# 删除谱系成员
def drop_pedigree(request):
    drop_id = request.GET.get('id')
    drop_obj = models.pedigree.objects.get(id=drop_id)
    drop_obj.delete()
    return redirect('/pedigree_list/')


# 修改谱系成员
def edit_pedigree(request):
    if request.method == 'POST':
        edit_id = request.GET.get('id')
        edit_obj = models.PedigreeTree.objects.get(id=edit_id)
        new_pedigree_name = request.POST.get('edit_name')
        new_pedigree_sire = request.POST.get('edit_sire')
        new_pedigree_dam = request.POST.get('edit_dam')
        new_pedigree_germ_id = request.POST.get('edit_germ')
        edit_obj.name = new_pedigree_name
        edit_obj.sire = new_pedigree_sire
        edit_obj.dam = new_pedigree_dam
        edit_obj.germ_id = new_pedigree_germ_id
        edit_obj.save()
        return redirect('/pedigree_list/')
    edit_id = request.GET.get('id')
    edit_obj = models.PedigreeTree.objects.get(id=edit_id)
    return render(request, 'pedigree_edit.html', {
        'pedigree': edit_obj,
    })


#  上传图片
def upload_image(request):
    if request.method == 'POST':
        new_id = request.POST.get('file_id')
        new_germ_id = request.POST.get('germ_id')
        new_image = request.FILES.get('photo')
        models.GermImage.objects.create(file_id=new_id, germ_id=new_germ_id, germ_image=new_image)
        return redirect('/show_image/')
        return HttpResponse('上传成功！')
    else:
        return render(request, 'image_upload.html')


class GermImageModelForm(forms.ModelForm):
    class Meta:
        model = models.GermImage
        fields = ["file_id", "germ_id", "germ_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


#   删除图片
def drop_image(request):
    drop_id = request.GET.get('file_id')
    drop_obj = models.GermImage.objects.get(file_id=drop_id)
    drop_obj.delete()
    return redirect('/show_image/')


#   编辑图片
def edit_image(request, nid):
    if request.method == "GET":
        row_object = models.GermImage.objects.filter(file_id=nid).first()
        edit_image_form = GermImageModelForm(instance=row_object)
        return render(request, 'image_edit.html', {'edit_image_form': edit_image_form})
    row_object = models.GermImage.objects.filter(file_id=nid).first()
    edit_image_form = GermImageModelForm(data=request.POST, instance=row_object)
    if edit_image_form.is_valid():
        edit_image_form.save()
        return redirect('/image_list/')
    return render(request, 'image_edit.html', {'edit_image_form': edit_image_form})


# 书籍列表
def evaluate_germ(request):
    return render(request, 'evaluate_germ.html')


# 添加书籍
# def add_book(request):
#     if request.method == 'POST':
#         new_book_name = request.POST.get('name')
#         new_book_ISBN = request.POST.get('ISBN')
#         new_book_translator = request.POST.get('translator')
#         new_book_date = request.POST.get('date')
#         germplasm_id = request.POST.get('germplasm_id')
#         models.Book.objects.create(name=new_book_name, germplasm_id=germplasm_id, ISBN=new_book_ISBN,
#                                    translator=new_book_translator, date=new_book_date)
#         return redirect('/evaluate_germ/')
#     res = models.germplasm.objects.all()
#     return render(request, 'book_add.html', {'germplasm_list': res})


# 删除书籍
# def drop_book(request):
#     drop_id = request.GET.get('id')
#     drop_obj = models.Book.objects.get(id=drop_id)
#     drop_obj.delete()
#     return redirect('/evaluate_germ/')
#

# 编辑书籍
# def edit_book(request):
#     if request.method == 'POST':
#         new_book_name = request.POST.get('name')
#         new_book_ISBN = request.POST.get('ISBN')
#         new_book_translator = request.POST.get('translator')
#         new_book_date = request.POST.get('date')
#         new_germplasm_id = request.POST.get('germplasm_id')
#         edit_id = request.GET.get('id')
#         edit_obj = models.Book.objects.get(id=edit_id)
#         edit_obj.name = new_book_name
#         edit_obj.ISBN = new_book_ISBN
#         edit_obj.translator = new_book_translator
#         edit_obj.date = new_book_date
#         edit_obj.germplasm_id = new_germplasm_id
#         edit_obj.save()
#         return redirect('/evaluate_germ/')
#     edit_id = request.GET.get('id')
#     edit_obj = models.Book.objects.get(id=edit_id)
#     all_germplasm = models.germplasm.objects.all()
#     return render(request, 'evaluate_germ.html', {'book': edit_obj, 'germplasm_list': all_germplasm})


# 密码加密

def setPassword(password):
    """
    加密密码，算法单次md5
    :param apssword: 传入的密码
    :return: 加密后的密码
    """
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)


# 登录
def login(request):
    if request.method == 'POST' and request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        e = LmsUser.objects.filter(email=email).first()
        if e:
            now_password = setPassword(password)
            db_password = e.password
            if now_password == db_password:
                # return render(request, "germ_list.html")
                response = HttpResponseRedirect('/germ_list/')
                response.set_cookie("username", e.username)
                return response

    return render(request, "login.html")


# 注册
def register(request):
    if request.method == "POST" and request.POST:
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        mobile = data.get("mobile")
        LmsUser.objects.create(
            username=username,
            email=email,
            password=setPassword(password),
            # password=password,
            mobile=mobile,
        )
        return HttpResponseRedirect('/login/')
    return render(request, "register.html")


class FullSibModelForm(forms.ModelForm):
    class Meta:
        model = models.pedigree
        fields = ["germ_id", "parent_f", "parent_m", "pedigree_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "col-sm-10", "placeholder": field.label}


class HalfSibModelForm(forms.ModelForm):
    class Meta:
        model = models.half_sib
        fields = ["germ_id", "parent_m", "pedigree_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "col-sm-10", "placeholder": field.label}


class PlantModelForm(forms.ModelForm):
    class Meta:
        model = models.Plantation
        fields = ["p_id", "Fam_num", "Rep", "Site", "Block", "Plot", "blk_num"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "col-sm-10", "placeholder": field.label}


def edit_plantation(request, nid):
    if request.method == "GET":
        row_object = models.Plantation.objects.filter(p_id=nid).first()
        form = PlantModelForm(instance=row_object)
        return render(request, 'edit_plantation.html', {'form': form})
    row_object = models.Plantation.objects.filter(p_id=nid).first()
    form = PlantModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/test_tree_list/')
    return render(request, 'edit_plantation.html', {'form': form})


def test_tree_list(request):
    plantation = models.Plantation.objects.all()
    return render(request, 'test_tree.html', {'test_tree_list': plantation})


def add_plantation(request):
    if request.method == "GET":
        form = PlantModelForm()
        return render(request, 'add_plantation.html', {'form': form})
    form = PlantModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/test_tree_list/')
    print(form.errors)
    return render(request, 'add_plantation.html', {'form': form})


# 删除试验林个体
def drop_plantation(request):
    drop_id = request.GET.get('id')
    drop_obj = models.Plantation.objects.get(p_id=drop_id)
    drop_obj.delete()
    return redirect('/test_tree_list/')


#   查看试验林个体信息
def check_plantation(request):
    check_id = request.GET.get('id')
    plant_tree = models.Plantation.objects.get(p_id=check_id)
    Plant_exist = models.PlantTree.objects.filter(p_id=check_id)
    if Plant_exist.exists():
        plant_info = models.PlantTree.objects.filter(p_id=check_id)
        return render(request, 'check_plantation.html', {'plant_tree': plant_tree, 'plant_info': plant_info})
    else:
        return render(request, 'check_plantation.html', {'plant_tree': plant_tree, 'plant_info': None})


# create modelform of plantation tree ind
class TestTreeModelForm(forms.ModelForm):
    class Meta:
        model = models.PlantTree
        fields = ["p_id", "year", "Height", "dbh", "volume_of_wood"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "col-sm-10", "placeholder": field.label}


# edit test plantation tree ind info
def edit_test_tree(request, nid):
    if request.method == "GET":
        row_object = models.PlantTree.objects.filter(p_id=nid).first()
        form = TestTreeModelForm(instance=row_object)
        return render(request, 'edit_plant_tree.html', {'form': form})
    row_object = models.PlantTree.objects.filter(p_id=nid).first()
    form = TestTreeModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/test_tree_list/')
    return render(request, 'edit_plant_tree.html', {'form': form})


def arcmap(request):
    return render(request, 'arcmap.html')


def BLUP_estimates(request):
    return render(request, 'combined_scatter_plot.html')


def perform_breeding_value_analysis(file):
    try:
        # 读取文件
        df = pd.read_csv(file)

        # 选取参与分析的列，包含家系编号、多年份多性状数据
        columns = [
            'Fam_num', 'Ht_2003', 'Ht_2004', 'Ht_2005', 'Ht_2006', 'Ht_2007',
            'Ht_2008', 'Ht_2009', 'Ht_2010', 'Ht_2011'
        ]
        df = df[columns]

        # 处理缺失值
        df = df.dropna()

        # 数据堆叠
        id_vars = ['Fam_num']
        value_vars = [col for col in df.columns if col != 'Fam_num']
        data_stack = pd.melt(df, id_vars=id_vars, value_vars=value_vars,
                             var_name='year_and_trait', value_name='value')

        # 从 year_and_trait 列中提取年份和性状信息
        data_stack['year'] = data_stack['year_and_trait'].str.extract('(\d+)').astype(int)
        data_stack['trait'] = data_stack['year_and_trait'].str.extract('([A-Za-z]+)')

        # 定义并拟合线性混合模型
        # model = smf.mixedlm("value ~ year + trait", data_stack, groups=data_stack["Fam_num"])
        # result = model.fit()

        # 获取育种值（BLUP）
        # blup_estimates = result.random_effects
        # breeding_values = pd.DataFrame({
        #     'Fam_num': list(blup_estimates.keys()),
        #     'breeding_value': [blup_estimates[key][0] for key in blup_estimates]
        # })

        # 将结果转换为字典以便于 JSON 序列化
        # result_dict = breeding_values.to_dict(orient='records')
        # return result_dict
    except Exception as e:
        return {"error": str(e)}


# add test plantation tree ind info
def add_test_tree(request):
    if request.method == "GET":
        form = TestTreeModelForm()
        return render(request, 'add_plant_tree.html', {'form': form})
    form = TestTreeModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/test_tree_list/')
    print(form.errors)
    return render(request, 'add_plant_tree.html', {'form': form})


# 删除试验林个体具体年份信息
def drop_plant_tree(request):
    drop_id = request.GET.get('id')
    plant_trees = models.PlantTree.objects.filter(year=drop_id)
    plant_tree = plant_trees.first()  # 或者使用其他逻辑来处理查询集
    plant_tree.delete()
    return redirect('/test_tree_list/')


def add_half_sib(request):
    if request.method == "GET":
        form = HalfSibModelForm()
        return render(request, "half_sib.html", {"form": form})
    form = HalfSibModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pedigree_list/')
    return render(request, "half_sib.html", {"form": form})


def edit_sib(request, nid):
    if request.method == "GET":
        row_object = models.half_sib.objects.filter(id=nid).first()
        form = HalfSibModelForm(instance=row_object)
        return render(request, 'half_sib.html', {'form': form})
    row_object = models.half_sib.objects.filter(id=nid).first()
    form = HalfSibModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pedigree_list/')
    return render(request, 'half_sib.html', {'form': form})


class GermModelForm(forms.ModelForm):
    class Meta:
        model = models.germplasm
        fields = ["germ_id", "time", "provenance", "longitude", "latitude", "average_altitude",
                  "annual_average_temperature",
                  "annual_precipitation", "average_annual_sunshine_duration", "frost_free_period",
                  "relative_humidity", "total_height", "diameter_at_breast_height", "cone_type",
                  "cone_bract_scale_shape",
                  "the_split_of_bracts_and_scales_in_immature_cones", "cone_length",
                  "cone_width", "cone_volume", "cone_shape_coefficient", "bract_scale_length", "bract_scale_width",
                  "bract_scale_length_width_ratio", "new_leaf_white_powder", "old_leaf_white_powder", "leaf_color",
                  "serration_density", "needle_hardness", "leaf_length", "leaf_width", "leaf_index", "volume_of_wood",
                  "wet_weight_of_wood", "dry_weight_of_wood", "water_absorption_of_wood",
                  "wood_density", "thousand_seed_weight",
                  "rate_of_emergence"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def edit_mode(request):
    germplasm = models.germplasm.objects.all()
    if request.method == "GET":
        form = GermModelForm()
        return render(request, "edit_mode.html", {"germ_list": germplasm})
    form = GermModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/germ_list/')
    return render(request, "edit_mode.html", {"form": form})


def edit_mode_edit(request):
    if request.method == "GET":
        form = GermModelForm()
        return render(request, "edit_mode_edit.html", {"form": form})
    form = GermModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pedigree_list/')
    return render(request, "edit_mode_edit.html", {"form": form})


def edit_germplasm(request, nid):
    if request.method == "GET":
        row_object = models.germplasm.objects.filter(id=nid).first()
        form = GermModelForm(instance=row_object)
        return render(request, 'germ_edit.html', {'form': form})
    row_object = models.germplasm.objects.filter(id=nid).first()
    form = GermModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/germ_list/')
    return render(request, 'germ_edit.html', {'form': form})


def add_germ(request):
    if request.method == "GET":
        form = GermModelForm()
        return render(request, 'add_germ.html', {'form': form})
    form = GermModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/germ_list/')
    print(form.errors)
    return render(request, 'add_germ.html', {'form': form})


#   查看种质信息
def check_germplasm(request):
    check_id = request.GET.get('id')
    germplasm = models.germplasm.objects.get(id=check_id)
    germ_exist = models.GermImage.objects.filter(file_id=check_id)
    if germ_exist.exists():
        germ_image = models.GermImage.objects.get(file_id=check_id)
        return render(request, 'check_germ.html', {'check_germ': germplasm, 'germ_image': germ_image})
    else:
        return render(request, 'check_germ.html', {'check_germ': germplasm, 'germ_image': None})


# 家系的列表
def pedigree_list(request):
    pedigree = models.pedigree.objects.all()
    pedigree_tree = models.PedigreeTree.objects.all()
    return render(request, 'pedigree_list.html', {'pedigree_tree': pedigree_tree})


def recurse_display(data):
    """递归展示"""
    display_list = []
    for item in data:
        display_list.append(item.germ_id)
        children = item.sireAll.all()
        if len(children) > 0:
            display_list.append(recurse_display(children))
    return display_list


def check_pedigree(request):
    check_id = request.GET.get('id')
    ped_tree = models.PedigreeTree.objects.all()
    pedigree_member = models.PedigreeTree.objects.get(id=check_id)
    member_id = pedigree_member.germ_id
    member_sire = pedigree_member.Sire
    member_dam = pedigree_member.Dam
    sire_sire = sire_dam = dam_dam = dam_sire = dam_dam_dam = dam_dam_sire = dam_sire_sire = dam_sire_dam = sire_sire_dam = sire_sire_sire = sire_dam_sire = sire_dam_dam = None
    if member_sire:
        sire_sire = models.PedigreeTree.objects.get(germ_id=member_sire).Sire
        sire_dam = models.PedigreeTree.objects.get(germ_id=member_sire).Dam
    if member_dam:
        dam_dam = models.PedigreeTree.objects.get(germ_id=member_dam).Dam
        dam_sire = models.PedigreeTree.objects.get(germ_id=member_dam).Sire
    if dam_dam:
        dam_dam_dam = models.PedigreeTree.objects.get(germ_id=dam_dam).Dam
        dam_dam_sire = models.PedigreeTree.objects.get(germ_id=dam_dam).Sire
    if dam_sire:
        dam_sire_dam = models.PedigreeTree.objects.get(germ_id=dam_sire).Dam
        dam_sire_sire = models.PedigreeTree.objects.get(germ_id=dam_sire).Sire
    if sire_dam:
        sire_dam_dam = models.PedigreeTree.objects.get(germ_id=sire_dam).Dam
        sire_dam_sire = models.PedigreeTree.objects.get(germ_id=sire_dam).Sire
    if sire_sire:
        sire_sire_dam = models.PedigreeTree.objects.get(germ_id=sire_sire).Dam
        sire_sire_sire = models.PedigreeTree.objects.get(germ_id=sire_sire).Sire
    # data = ''' [{"children": [{"children": [{"children": [{"name":'''+str(sire_sire_sire)+''')}, {"name": '''+str(
    # sire_sire_dam)+''')}], "name": '''+str(sire_sire)+''')}, {"children": [{"name": '''+str(sire_dam_sire)+''')},
    # {"name": '''+str(sire_dam_dam)+''')}],"name": '''+str(sire_dam)+''')}, ], "name": '''+str(member_sire)+''', },
    # {"children": [{"children": [{"name": '''+str(dam_sire_sire)+''')}, {"name": '''+str(dam_sire_dam)+'''}],
    # "name": '''+str(dam_sire)+'''}, {"children": [{"name": '''+str(dam_dam_sire)+'''}, {"name": '''+str(
    # dam_dam_dam)+'''}], "name":'''+ str(dam_dam)+'''}, ], "name": '''+str(member_dam)+''', }, ], "name": '''+str(
    # member_id)+''',}]''' data = json.loads(data)

    return render(request, 'check_pedigree.html', {'member_id': member_id,
                                                   'member_sire': member_sire, 'member_dam': member_dam,
                                                   'sire_sire': sire_sire, 'sire_dam': sire_dam,
                                                   'dam_dam': dam_dam, 'dam_sire': dam_sire,
                                                   'dam_dam_dam': dam_dam_dam, 'dam_dam_sire': dam_dam_sire,
                                                   'dam_sire_sire': dam_sire_sire, 'dam_sire_dam': dam_sire_dam,
                                                   'sire_sire_dam': sire_sire_dam, 'sire_sire_sire': sire_sire_sire,
                                                   'sire_dam_sire': sire_dam_sire, 'sire_dam_dam': sire_dam_dam})


def pedigree_tree(request):
    return render(request, 'nxt_sel1.html')


def pedigree_net(request):
    return render(request, 'cluster_kinship.html')


# #  查看家谱
# def pedigree_tree(request):
#     check_id = request.GET.get('id')
#     pedigree = models.pedigree.objects.get(id=check_id)
#     return render(request, 'pedigree_tree.html', {'pedigree_tree': pedigree})


def Germ_mptt_tree(request):
    germ = PedigreeMPTT.objects.all()
    return render(request, 'mptt.html', {'germ': germ})


def evaluate_line(request):
    germplasm = models.germplasm.objects.filter(total_height__isnull=False)
    cone_count = models.germplasm.objects.filter(cone_type__isnull=False).values('cone_type').annotate(
        count=Count('cone_type')).order_by('count')
    # categories = models.germplasm.objects.filter(cone_type__isnull=False).values_list('cone_type',
    # flat=True).distinct() values = models.germplasm.objects.filter(cone_type__isnull=False).values(
    # 'cone_type').annotate(count=Count('cone_type')).order_by('count').values_list('count', flat=True) 将字典列表转换为所需的格式
    bract_count = models.germplasm.objects.filter(cone_bract_scale_shape__isnull=False).values(
        'cone_bract_scale_shape').annotate(count=Count('cone_bract_scale_shape')).order_by('count')
    split_count = models.germplasm.objects.filter(
        the_split_of_bracts_and_scales_in_immature_cones__isnull=False).values(
        'the_split_of_bracts_and_scales_in_immature_cones').annotate(
        count=Count('the_split_of_bracts_and_scales_in_immature_cones')).order_by('count')
    test_plantation = models.PlantTree.objects.filter()

    return render(request, 'evaluate_germ.html',
                  {'Germ': germplasm,
                   'cone': cone_count,
                   'bract': bract_count,
                   'split': split_count})


def evaluate_PCA(request):
    data = models.germplasm.objects.all().values_list('total_height', 'diameter_at_breast_height',
                                                      'cone_length', 'cone_width', 'cone_shape_coefficient',
                                                      'bract_scale_length', 'bract_scale_width', 'cone_volume',
                                                      'bract_scale_length_width_ratio',
                                                      'leaf_length', 'leaf_width', 'leaf_index',
                                                      'volume_of_wood', 'wet_weight_of_wood', 'dry_weight_of_wood',
                                                      'water_absorption_of_wood', 'wood_density',
                                                      'thousand_seed_weight', 'rate_of_emergence',
                                                      'serration_density', 'needle_hardness')
    rows = ['树高', '胸径', '球果长度', '球果宽度', '果型系数', '苞鳞长度', '苞鳞宽度',
            '球果体积', '苞鳞长宽比', '针叶长度', '针叶宽度', '叶型系数',
            '材积', '木材湿重', '木材干重', '木材吸水率', '木材密度', '千粒重',
            '萌发率', '针叶密度', '针叶硬度']  # X轴标签列表
    # matplotlib.use('Agg')  # 不出现画图的框
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 这两行用来显示汉字
    # plt.rcParams['axes.unicode_minus'] = False
    # sns.set_context({"figure.figsize": (14, 10)})
    # 计算相关性矩阵
    arr = np.array(list(data))
    arr = arr.astype(float)
    arr = np.where(np.isnan(arr), 0, arr)
    correlation_matrix = np.corrcoef(arr.T)  # 直接四舍五入

    heat_matrix = []
    for i in range(len(rows)):
        for j in range(len(rows)):
            value = np.round(correlation_matrix[i, j], 3)
            heat_matrix.append([i, j, value])
    # sns.heatmap(correlation_matrix, annot=True, square=True,
    #             xticklabels=rows,
    #             yticklabels=rows,
    #             fmt=".2f", cmap='coolwarm')
    # title = '相关性热图'
    # plt.title(title, loc='center')
    # # 设置X轴和Y轴的标签
    # sio = BytesIO()
    # plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    # data = base64.encodebytes(sio.getvalue()).decode()
    # src = 'data:image/png;base64,' + str(data)
    # # 记得关闭，不然画出来的图是重复的
    # plt.close()
    df = pd.DataFrame(list(data), columns=rows)

    df = df.dropna(axis=0)
    PCA_data = preprocessing.scale(df)
    covX = np.around(np.corrcoef(PCA_data.T), decimals=3)
    average = np.mean(PCA_data, axis=0)
    m, n = np.shape(PCA_data)
    avgs = np.tile(average, (m, 1))
    data_adjust = PCA_data - avgs
    covX = np.cov(data_adjust.T)
    featValue, featVec = np.linalg.eig(covX)
    featValue = sorted(featValue)[::-1]
    others_sum = np.array(featValue[7:]).sum()
    # prime_v = np.array(featValue)
    # prime_factor = prime_v[prime_v > 1.0]
    # k = len(prime_factor)
    selectVec = np.matrix(featVec.T[:7]).T
    x, y = np.shape(selectVec)
    Cartesian_matrix = []
    for i in range(x):
        for j in range(y):
            row_number = i
            column_number = j
            value = np.round(selectVec[i, j], 3)
            Cartesian_matrix.append([row_number, column_number, value])
    return render(request, 'analysis_germ.html', {'heat_matrix': heat_matrix, 'data': featValue,
                                                  'others': others_sum, 'select': selectVec,
                                                  'matrix': Cartesian_matrix})
