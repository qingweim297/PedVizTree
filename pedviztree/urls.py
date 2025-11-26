"""bms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from app01.pedVis import json_export
from app01 import views, file, pedVis

urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r'^$', views.login),
                  re_path(r'^germ_list/', views.germplasm_list),  # 种质列表
                  re_path(r'^germplasm_list/', views.germplasm_list),  # 种质列表
                  re_path(r'^add_germ/', views.add_germ),  # 新增种质
                  path('edit/<int:nid>/germ/', views.edit_germplasm),  # 编辑种质
                  re_path(r'^check_germ/', views.check_germplasm),  # 查看种质信息
                  re_path(r'^check_germplasm/', views.check_germplasm),  # 查看种质信息
                  re_path(r'^drop_pub/', views.drop_germplasm),  # 删除种质
                  re_path(r'^Pedigree_list/', views.pedigree_list),  # 谱系列表
                  re_path(r'^pedigree_list/', views.pedigree_list),  # 谱系列表
                  re_path(r'^pedigree_net/', views.pedigree_net),  # 谱系列表
                  # re_path(r'^pedigree_net/', pedVis.json_export),  # kinship cluster network
                  re_path(r'^add_pedigree/', views.add_pedigree),  # 新增家系成员
                  re_path(r'^pedigree_tree/', pedVis.show_network),  # 查看家系谱
                  re_path(r'^drop_pedigree/', views.drop_pedigree),  # 删除家系成员
                  re_path(r'^edit_pedigree/', views.edit_pedigree),  # 编辑家系成员
                  re_path(r'^check_pedigree/', views.check_pedigree),  # 查看家系成员
                  re_path(r'^test_tree_list/', views.test_tree_list),  # 试验林列表
                  re_path(r'^arcmap/', views.arcmap),  # 查看试验林方案
                  re_path(r'^add_plantation/', views.add_plantation),  # 新增试验林个体
                  re_path(r'^drop_plantation/', views.drop_plantation),  # 删除试验林个体
                  path('edit/<int:nid>/plantation/', views.edit_plantation),  # 编辑试验林个体信息
                  re_path(r'^check_plantation/', views.check_plantation),  # 查看试验林个体信息
                  re_path(r'^add_plant_tree/', views.add_test_tree),  # 新增试验林个体年份测量信息
                  re_path(r'^drop_plant_tree/', views.drop_plant_tree),  # 删除试验林个体年份测量信息
                  path('edit/<int:nid>/planttree/', views.edit_test_tree),  # 编辑试验林个体年份测量信息
                  re_path(r'^evaluate_germ/', views.evaluate_line),  # 种质评估
                  re_path(r'^analysis_germ/', views.evaluate_PCA),  # 种质评估
                  re_path(r'^estimate_plantation/', views.BLUP_estimates),  # 育种值评价
                  re_path(r'^login/', views.login),  # 登录动作
                  re_path(r'^signup/', views.register),  # 注册页面
                  re_path(r'^register/', views.register),  # 注册
                  re_path(r'^image_list/', views.show_GermPIC_list),
                  re_path(r'^image_upload/', views.upload_image),
                  re_path(r'^add_image/', views.upload_image),
                  re_path(r'^show_image/', views.show_GermPIC_list),
                  re_path(r'^add_pedigree_sib/', views.add_half_sib),
                  re_path(r'^edit_mode/', views.edit_mode),
                  re_path(r'^edit_mode_edit/', views.edit_mode_edit),
                  path('upload/', views.upload_image),
                  # 第一行用来转到填表单，第二行用来处理上传来的图片
                  path('upload_handle/', views.upload_handle, name='upload_handle'),
                  re_path(r'^drop_image/', views.drop_image),  # 删除种质图片
                  path('image_edit/<int:nid>/germ_image/', views.edit_image),  # 编辑种质图片
                  path('file_list/', file.file_list),
                  re_path(r'excel_to_net/', pedVis.excel_upload),
                  re_path(r'excel_to_network/', pedVis.excel_upload),
                  re_path(r'net_excel/', pedVis.draw_network_excel),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
