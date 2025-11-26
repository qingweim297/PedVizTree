from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


# 种质资源信息类
# 种质资源信息类
class germplasm(models.Model):
    id = models.AutoField('序号', primary_key=True)
    germ_id = models.CharField('编号', max_length=10, null=True)
    time = models.DateField('保存时间', max_length=64, null=True)
    provenance = models.CharField('种源', max_length=4, null=True)
    longitude = models.DecimalField('经度', max_digits=5, decimal_places=2, null=True)
    latitude = models.DecimalField('纬度', max_digits=5, decimal_places=2, null=True)
    average_altitude = models.DecimalField('平均海拔', max_digits=5, decimal_places=1, null=True)
    annual_average_temperature = models.DecimalField('年平均气温', max_digits=3, decimal_places=1, null=True)
    annual_precipitation = models.DecimalField('年降水量', max_digits=5, decimal_places=1, null=True)
    average_annual_sunshine_duration = models.DecimalField('年均日照时数', max_digits=5, decimal_places=1, null=True)
    frost_free_period = models.DecimalField('无霜期', max_digits=3, decimal_places=0, null=True)
    relative_humidity = models.DecimalField('相对湿度', max_digits=3, decimal_places=1, null=True)
    total_height = models.DecimalField('树高', max_digits=3, decimal_places=1, null=True)
    diameter_at_breast_height = models.DecimalField('胸径', max_digits=4, decimal_places=1, null=True)
    cone_type = models.CharField('球果类型', max_length=4, null=True)
    cone_bract_scale_shape = models.CharField('苞鳞形状', max_length=2, null=True)
    the_split_of_bracts_and_scales_in_immature_cones = models.CharField('张裂程度', max_length=2, null=True)
    cone_length = models.DecimalField('球果长度', max_digits=3, decimal_places=1, null=True)
    cone_width = models.DecimalField('球果宽度', max_digits=3, decimal_places=1, null=True)
    cone_volume = models.DecimalField('球果体积', max_digits=4, decimal_places=2, null=True)
    cone_shape_coefficient = models.DecimalField('果形系数', max_digits=3, decimal_places=1, null=True)
    bract_scale_length = models.DecimalField('苞鳞长度', max_digits=4, decimal_places=2, null=True)
    bract_scale_width = models.DecimalField('苞鳞宽度', max_digits=4, decimal_places=2, null=True)
    bract_scale_length_width_ratio = models.DecimalField('苞鳞长宽比', max_digits=3, decimal_places=2, null=True)
    new_leaf_white_powder = models.CharField('新叶白粉', max_length=3, null=True)
    old_leaf_white_powder = models.CharField('老叶白粉', max_length=3, null=True)
    leaf_color = models.CharField('颜色', max_length=4, null=True)
    serration_density = models.DecimalField('锯齿密度', max_digits=4, decimal_places=2, null=True)
    needle_hardness = models.CharField('针叶硬度', max_length=1, null=True)
    leaf_length = models.DecimalField('针叶长度', max_digits=4, decimal_places=2, null=True)
    leaf_width = models.DecimalField('针叶宽度', max_digits=3, decimal_places=2, null=True)
    leaf_index = models.DecimalField('叶形指数', max_digits=4, decimal_places=2, null=True)
    volume_of_wood = models.DecimalField('材积', max_digits=4, decimal_places=3, null=True)
    wet_weight_of_wood = models.DecimalField('木材湿重', max_digits=5, decimal_places=3, null=True)
    dry_weight_of_wood = models.DecimalField('木材干重', max_digits=4, decimal_places=3, null=True)
    water_absorption_of_wood = models.DecimalField('木材吸水率', max_digits=4, decimal_places=3, null=True)
    wood_density = models.DecimalField('木材密度', max_digits=4, decimal_places=3, null=True)
    thousand_seed_weight = models.DecimalField('千粒重', max_digits=4, decimal_places=2, null=True)
    rate_of_emergence = models.DecimalField('出苗率', max_digits=4, decimal_places=2, null=True)


# 种质图像单独的类
class GermImage(models.Model):
    file_id = models.CharField('序号', max_length=64)
    germ_id = models.CharField('种质编号', max_length=64)
    germ_image = models.ImageField(upload_to='photos', max_length=100, blank=True, null=True, verbose_name='种质图像')


# 全同胞家系的类
class pedigree(models.Model):
    id = models.AutoField('序号', primary_key=True)
    germ_id = models.CharField('种质编号', max_length=64, null=True)
    pedigree_name = models.CharField('家系名称', max_length=64, null=True)
    parent_f = models.CharField('父本', max_length=64, null=True)
    parent_m = models.CharField('母本', max_length=64, null=True)
    # 一个家系可以对应多个种子，一个种子只有一个家系，一对多，在数据库中创建第三张表
    pedigree = models.ForeignKey(to=germplasm, on_delete=models.CASCADE, null=True)


# 家系的类
class half_sib(models.Model):
    id = models.AutoField('序号', primary_key=True)
    germ_id = models.CharField('种质编号', max_length=64)
    pedigree_name = models.CharField('家系名称', max_length=64)
    parent_m = models.CharField('母本', max_length=64)
    # 一个家系可以对应多个种子，一个种子只有一个家系，一对多，在数据库中创建第三张表
    pedigree = models.ForeignKey(to=germplasm, on_delete=models.CASCADE, null=True)


class Sire(models.Model):
    Sire = models.CharField('种质编号', unique=True, max_length=64, null=True)

    def __str__(self):
        return self.Sire


class Dam(models.Model):
    Dam = models.CharField('种质编号', unique=True, max_length=64, null=True)

    def __str__(self):
        return self.Dam


class PedigreeTree(models.Model):
    id = models.AutoField('序号', primary_key=True)
    pedigree_name = models.CharField('家系名称', max_length=64, null=True)
    germ_id = models.CharField(max_length=64, unique=True, verbose_name="种质编号")
    Sire = models.ForeignKey(Sire, to_field='Sire', db_column='Sire',
                             on_delete=models.CASCADE,
                             null=True, blank=True,
                             db_constraint=False,
                             related_name='sireAll',
                             verbose_name="父本")
    Dam = models.ForeignKey(Dam, to_field='Dam', db_column='Dam',
                            on_delete=models.CASCADE,
                            null=True, blank=True,
                            db_constraint=False,
                            related_name='damAll',
                            verbose_name="母本")

    def __str__(self):
        return self.germ_id


# test plantation forest
class Plantation(models.Model):
    p_id = models.CharField('试验林编号', unique= True, max_length=64)
    Fam_num = models.CharField('家系号', max_length=64, null=True)
    Rep = models.CharField('重复', max_length=64)
    Site = models.CharField('场地', max_length=64)
    Block = models.CharField('区组号', max_length=64)
    Plot = models.CharField('地点', max_length=64)
    blk_num = models.CharField('区组编号', max_length=64)

    def __str__(self):
        return self.p_id


# plant tree ind data
class PlantTree(models.Model):
    id = models.AutoField('序号', primary_key=True)
    p_id = models.ForeignKey(Plantation, to_field='p_id', db_column='p_id',
                             on_delete=models.CASCADE,
                             db_constraint=False,
                             verbose_name="试验林编号")
    year = models.IntegerField('保存年份')
    Height = models.CharField('年份树高', max_length=64, null=True)
    dbh = models.CharField('年份胸径', max_length=64, null=True)
    volume_of_wood = models.DecimalField('材积', max_digits=6, decimal_places=5, null=True)

    class Meta:
        unique_together = [('p_id', 'year')]

    def __str__(self):
        return f"{self.p_id}"


# 用户的类
class LmsUser(models.Model):
    id = models.AutoField('序号', primary_key=True)
    username = models.CharField('用户名', max_length=32)
    password = models.CharField('密码', max_length=32)
    email = models.CharField('邮箱', max_length=254)
    mobile = models.BigIntegerField('手机', blank='True')


class ExcelNet(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(max_length=255, upload_to='file', blank=True, null=True)

    def __str__(self):
        return self.name


class PedigreeMPTT(MPTTModel):
    id = models.AutoField('序号', primary_key=True)
    germ_id = models.CharField(max_length=64, unique=True, verbose_name="种质编号")
    Sire = TreeForeignKey(Sire,
                          on_delete=models.PROTECT,
                          null=True, blank=True,
                          db_constraint=False,
                          related_name='child_sire',
                          verbose_name="父本")
    Dam = TreeForeignKey(Dam,
                         on_delete=models.PROTECT,
                         null=True, blank=True,
                         db_constraint=False,
                         related_name='child_dam',
                         verbose_name="母本")

    class MPTTMeta:
        order_insertion_by = ['germ_id']
        parent_attr = 'Sire', 'Dam'

    def __str__(self):
        return self.germ_id

    # if parent filed name is not parent, e.g. depart_parent
