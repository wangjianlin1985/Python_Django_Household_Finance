from django.db import models


class ExpendType(models.Model):
    expendTypeId = models.AutoField(primary_key=True, verbose_name='支出类型id')
    expendTypeName = models.CharField(max_length=20, default='', verbose_name='支出类型名称')

    class Meta:
        db_table = 't_ExpendType'
        verbose_name = '支出类型信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        expendType = {
            'expendTypeId': self.expendTypeId,
            'expendTypeName': self.expendTypeName,
        }
        return expendType

