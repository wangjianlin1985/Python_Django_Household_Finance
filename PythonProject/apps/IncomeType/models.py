from django.db import models


class IncomeType(models.Model):
    typeId = models.AutoField(primary_key=True, verbose_name='分类id')
    typeName = models.CharField(max_length=20, default='', verbose_name='分类名称')

    class Meta:
        db_table = 't_IncomeType'
        verbose_name = '收入分类信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        incomeType = {
            'typeId': self.typeId,
            'typeName': self.typeName,
        }
        return incomeType

