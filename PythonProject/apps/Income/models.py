from django.db import models
from apps.IncomeType.models import IncomeType
from apps.PayWay.models import PayWay
from apps.UserInfo.models import UserInfo


class Income(models.Model):
    incomeId = models.AutoField(primary_key=True, verbose_name='收入id')
    incomeTypeObj = models.ForeignKey(IncomeType,  db_column='incomeTypeObj', on_delete=models.PROTECT, verbose_name='收入类型')
    incomeFrom = models.CharField(max_length=50, default='', verbose_name='收入来源')
    payWayObj = models.ForeignKey(PayWay,  db_column='payWayObj', on_delete=models.PROTECT, verbose_name='支付方式')
    payAccount = models.CharField(max_length=20, default='', verbose_name='支付账号')
    incomeMoney = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='收入金额')
    incomeDate = models.CharField(max_length=20, default='', verbose_name='收入日期')
    userObj = models.ForeignKey(UserInfo,  db_column='userObj', on_delete=models.PROTECT, verbose_name='收入用户')
    incomeMemo = models.CharField(max_length=800, default='', verbose_name='收入备注')

    class Meta:
        db_table = 't_Income'
        verbose_name = '收入信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        income = {
            'incomeId': self.incomeId,
            'incomeTypeObj': self.incomeTypeObj.typeName,
            'incomeTypeObjPri': self.incomeTypeObj.typeId,
            'incomeFrom': self.incomeFrom,
            'payWayObj': self.payWayObj.payWayName,
            'payWayObjPri': self.payWayObj.payWayId,
            'payAccount': self.payAccount,
            'incomeMoney': self.incomeMoney,
            'incomeDate': self.incomeDate,
            'userObj': self.userObj.name,
            'userObjPri': self.userObj.user_name,
            'incomeMemo': self.incomeMemo,
        }
        return income

