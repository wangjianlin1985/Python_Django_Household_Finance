from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Income.models import Income
from apps.IncomeType.models import IncomeType
from apps.PayWay.models import PayWay
from apps.UserInfo.models import UserInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台收入添加
    def get(self,request):
        incomeTypes = IncomeType.objects.all()  # 获取所有收入分类
        payWays = PayWay.objects.all()  # 获取所有支付方式
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'incomeTypes': incomeTypes,
            'payWays': payWays,
            'userInfos': userInfos,
        }

        # 使用模板
        return render(request, 'Income/income_frontAdd.html', context)

    def post(self, request):
        income = Income() # 新建一个收入对象然后获取参数
        income.incomeTypeObj = IncomeType.objects.get(typeId=request.POST.get('income.incomeTypeObj.typeId'))
        income.incomeFrom = request.POST.get('income.incomeFrom')
        income.payWayObj = PayWay.objects.get(payWayId=request.POST.get('income.payWayObj.payWayId'))
        income.payAccount = request.POST.get('income.payAccount')
        income.incomeMoney = float(request.POST.get('income.incomeMoney'))
        income.incomeDate = request.POST.get('income.incomeDate')
        income.userObj = UserInfo.objects.get(user_name=request.POST.get('income.userObj.user_name'))
        income.incomeMemo = request.POST.get('income.incomeMemo')
        income.save() # 保存收入信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class UserFrontAddView(BaseView):  # 前台收入添加
    def get(self,request):
        incomeTypes = IncomeType.objects.all()  # 获取所有收入分类
        payWays = PayWay.objects.all()  # 获取所有支付方式
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'incomeTypes': incomeTypes,
            'payWays': payWays,
            'userInfos': userInfos,
        }

        # 使用模板
        return render(request, 'Income/income_userFrontAdd.html', context)

    def post(self, request):
        income = Income() # 新建一个收入对象然后获取参数
        income.incomeTypeObj = IncomeType.objects.get(typeId=request.POST.get('income.incomeTypeObj.typeId'))
        income.incomeFrom = request.POST.get('income.incomeFrom')
        income.payWayObj = PayWay.objects.get(payWayId=request.POST.get('income.payWayObj.payWayId'))
        income.payAccount = request.POST.get('income.payAccount')
        income.incomeMoney = float(request.POST.get('income.incomeMoney'))
        income.incomeDate = request.POST.get('income.incomeDate')
        income.userObj = UserInfo.objects.get(user_name=request.session['user_name'])
        income.incomeMemo = request.POST.get('income.incomeMemo')
        income.save() # 保存收入信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改收入
    def get(self, request, incomeId):
        context = {'incomeId': incomeId}
        return render(request, 'Income/income_frontModify.html', context)


class FrontListView(BaseView):  # 前台收入查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        incomeTypeObj_typeId = self.getIntParam(request, 'incomeTypeObj.typeId')
        incomeFrom = self.getStrParam(request, 'incomeFrom')
        payWayObj_payWayId = self.getIntParam(request, 'payWayObj.payWayId')
        payAccount = self.getStrParam(request, 'payAccount')
        incomeDate = self.getStrParam(request, 'incomeDate')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        # 然后条件组合查询过滤
        incomes = Income.objects.all()
        if incomeTypeObj_typeId != '0':
            incomes = incomes.filter(incomeTypeObj=incomeTypeObj_typeId)
        if incomeFrom != '':
            incomes = incomes.filter(incomeFrom__contains=incomeFrom)
        if payWayObj_payWayId != '0':
            incomes = incomes.filter(payWayObj=payWayObj_payWayId)
        if payAccount != '':
            incomes = incomes.filter(payAccount__contains=payAccount)
        if incomeDate != '':
            incomes = incomes.filter(incomeDate__contains=incomeDate)
        if userObj_user_name != '':
            incomes = incomes.filter(userObj=userObj_user_name)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(incomes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        incomes_page = self.paginator.page(self.currentPage)

        # 获取所有收入分类
        incomeTypes = IncomeType.objects.all()
        # 获取所有支付方式
        payWays = PayWay.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'incomeTypes': incomeTypes,
            'payWays': payWays,
            'userInfos': userInfos,
            'incomes_page': incomes_page,
            'incomeTypeObj_typeId': int(incomeTypeObj_typeId),
            'incomeFrom': incomeFrom,
            'payWayObj_payWayId': int(payWayObj_payWayId),
            'payAccount': payAccount,
            'incomeDate': incomeDate,
            'userObj_user_name': userObj_user_name,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Income/income_frontquery_result.html', context)


class UserFrontListView(BaseView):  # 前台收入查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        incomeTypeObj_typeId = self.getIntParam(request, 'incomeTypeObj.typeId')
        incomeFrom = self.getStrParam(request, 'incomeFrom')
        payWayObj_payWayId = self.getIntParam(request, 'payWayObj.payWayId')
        payAccount = self.getStrParam(request, 'payAccount')
        incomeDate = self.getStrParam(request, 'incomeDate')
        userObj_user_name = request.session['user_name']
        # 然后条件组合查询过滤
        incomes = Income.objects.all()
        if incomeTypeObj_typeId != '0':
            incomes = incomes.filter(incomeTypeObj=incomeTypeObj_typeId)
        if incomeFrom != '':
            incomes = incomes.filter(incomeFrom__contains=incomeFrom)
        if payWayObj_payWayId != '0':
            incomes = incomes.filter(payWayObj=payWayObj_payWayId)
        if payAccount != '':
            incomes = incomes.filter(payAccount__contains=payAccount)
        if incomeDate != '':
            incomes = incomes.filter(incomeDate__contains=incomeDate)
        if userObj_user_name != '':
            incomes = incomes.filter(userObj=userObj_user_name)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(incomes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        incomes_page = self.paginator.page(self.currentPage)

        # 获取所有收入分类
        incomeTypes = IncomeType.objects.all()
        # 获取所有支付方式
        payWays = PayWay.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'incomeTypes': incomeTypes,
            'payWays': payWays,
            'userInfos': userInfos,
            'incomes_page': incomes_page,
            'incomeTypeObj_typeId': int(incomeTypeObj_typeId),
            'incomeFrom': incomeFrom,
            'payWayObj_payWayId': int(payWayObj_payWayId),
            'payAccount': payAccount,
            'incomeDate': incomeDate,
            'userObj_user_name': userObj_user_name,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Income/income_userFrontquery_result.html', context)


class FrontShowView(View):  # 前台显示收入详情页
    def get(self, request, incomeId):
        # 查询需要显示的收入对象
        income = Income.objects.get(incomeId=incomeId)
        context = {
            'income': income
        }
        # 渲染模板显示
        return render(request, 'Income/income_frontshow.html', context)


class ListAllView(View): # 前台查询所有收入
    def get(self,request):
        incomes = Income.objects.all()
        incomeList = []
        for income in incomes:
            incomeObj = {
                'incomeId': income.incomeId,
                'incomeFrom': income.incomeFrom,
            }
            incomeList.append(incomeObj)
        return JsonResponse(incomeList, safe=False)


class UpdateView(BaseView):  # Ajax方式收入更新
    def get(self, request, incomeId):
        # GET方式请求查询收入对象并返回收入json格式
        income = Income.objects.get(incomeId=incomeId)
        return JsonResponse(income.getJsonObj())

    def post(self, request, incomeId):
        # POST方式提交收入修改信息更新到数据库
        income = Income.objects.get(incomeId=incomeId)
        income.incomeTypeObj = IncomeType.objects.get(typeId=request.POST.get('income.incomeTypeObj.typeId'))
        income.incomeFrom = request.POST.get('income.incomeFrom')
        income.payWayObj = PayWay.objects.get(payWayId=request.POST.get('income.payWayObj.payWayId'))
        income.payAccount = request.POST.get('income.payAccount')
        income.incomeMoney = float(request.POST.get('income.incomeMoney'))
        income.incomeDate = request.POST.get('income.incomeDate')
        income.userObj = UserInfo.objects.get(user_name=request.POST.get('income.userObj.user_name'))
        income.incomeMemo = request.POST.get('income.incomeMemo')
        income.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台收入添加
    def get(self,request):
        incomeTypes = IncomeType.objects.all()  # 获取所有收入分类
        payWays = PayWay.objects.all()  # 获取所有支付方式
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'incomeTypes': incomeTypes,
            'payWays': payWays,
            'userInfos': userInfos,
        }

        # 渲染显示模板界面
        return render(request, 'Income/income_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        income = Income() # 新建一个收入对象然后获取参数
        income.incomeTypeObj = IncomeType.objects.get(typeId=request.POST.get('income.incomeTypeObj.typeId'))
        income.incomeFrom = request.POST.get('income.incomeFrom')
        income.payWayObj = PayWay.objects.get(payWayId=request.POST.get('income.payWayObj.payWayId'))
        income.payAccount = request.POST.get('income.payAccount')
        income.incomeMoney = float(request.POST.get('income.incomeMoney'))
        income.incomeDate = request.POST.get('income.incomeDate')
        income.userObj = UserInfo.objects.get(user_name=request.POST.get('income.userObj.user_name'))
        income.incomeMemo = request.POST.get('income.incomeMemo')
        income.save() # 保存收入信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新收入
    def get(self, request, incomeId):
        context = {'incomeId': incomeId}
        return render(request, 'Income/income_modify.html', context)


class ListView(BaseView):  # 后台收入列表
    def get(self, request):
        # 使用模板
        return render(request, 'Income/income_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        incomeTypeObj_typeId = self.getIntParam(request, 'incomeTypeObj.typeId')
        incomeFrom = self.getStrParam(request, 'incomeFrom')
        payWayObj_payWayId = self.getIntParam(request, 'payWayObj.payWayId')
        payAccount = self.getStrParam(request, 'payAccount')
        incomeDate = self.getStrParam(request, 'incomeDate')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        # 然后条件组合查询过滤
        incomes = Income.objects.all()
        if incomeTypeObj_typeId != '0':
            incomes = incomes.filter(incomeTypeObj=incomeTypeObj_typeId)
        if incomeFrom != '':
            incomes = incomes.filter(incomeFrom__contains=incomeFrom)
        if payWayObj_payWayId != '0':
            incomes = incomes.filter(payWayObj=payWayObj_payWayId)
        if payAccount != '':
            incomes = incomes.filter(payAccount__contains=payAccount)
        if incomeDate != '':
            incomes = incomes.filter(incomeDate__contains=incomeDate)
        if userObj_user_name != '':
            incomes = incomes.filter(userObj=userObj_user_name)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(incomes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        incomes_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        incomeList = []
        for income in incomes_page:
            income = income.getJsonObj()
            incomeList.append(income)
        # 构造模板页面需要的参数
        income_res = {
            'rows': incomeList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(income_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除收入信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        incomeIds = self.getStrParam(request, 'incomeIds')
        incomeIds = incomeIds.split(',')
        count = 0
        try:
            for incomeId in incomeIds:
                Income.objects.get(incomeId=incomeId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出收入信息到excel并下载
    def get(self, request):
        # 收集查询参数
        incomeTypeObj_typeId = self.getIntParam(request, 'incomeTypeObj.typeId')
        incomeFrom = self.getStrParam(request, 'incomeFrom')
        payWayObj_payWayId = self.getIntParam(request, 'payWayObj.payWayId')
        payAccount = self.getStrParam(request, 'payAccount')
        incomeDate = self.getStrParam(request, 'incomeDate')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        # 然后条件组合查询过滤
        incomes = Income.objects.all()
        if incomeTypeObj_typeId != '0':
            incomes = incomes.filter(incomeTypeObj=incomeTypeObj_typeId)
        if incomeFrom != '':
            incomes = incomes.filter(incomeFrom__contains=incomeFrom)
        if payWayObj_payWayId != '0':
            incomes = incomes.filter(payWayObj=payWayObj_payWayId)
        if payAccount != '':
            incomes = incomes.filter(payAccount__contains=payAccount)
        if incomeDate != '':
            incomes = incomes.filter(incomeDate__contains=incomeDate)
        if userObj_user_name != '':
            incomes = incomes.filter(userObj=userObj_user_name)
        #将查询结果集转换成列表
        incomeList = []
        for income in incomes:
            income = income.getJsonObj()
            incomeList.append(income)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(incomeList)
        # 设置要导入到excel的列
        columns_map = {
            'incomeId': '收入id',
            'incomeTypeObj': '收入类型',
            'incomeFrom': '收入来源',
            'payWayObj': '支付方式',
            'payAccount': '支付账号',
            'incomeMoney': '收入金额',
            'incomeDate': '收入日期',
            'userObj': '收入用户',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'incomes.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="incomes.xlsx"'
        return response

