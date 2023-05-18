from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.IncomeType.models import IncomeType
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台收入分类添加
    def get(self,request):

        # 使用模板
        return render(request, 'IncomeType/incomeType_frontAdd.html')

    def post(self, request):
        incomeType = IncomeType() # 新建一个收入分类对象然后获取参数
        incomeType.typeName = request.POST.get('incomeType.typeName')
        incomeType.save() # 保存收入分类信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改收入分类
    def get(self, request, typeId):
        context = {'typeId': typeId}
        return render(request, 'IncomeType/incomeType_frontModify.html', context)


class FrontListView(BaseView):  # 前台收入分类查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        incomeTypes = IncomeType.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(incomeTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        incomeTypes_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'incomeTypes_page': incomeTypes_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'IncomeType/incomeType_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示收入分类详情页
    def get(self, request, typeId):
        # 查询需要显示的收入分类对象
        incomeType = IncomeType.objects.get(typeId=typeId)
        context = {
            'incomeType': incomeType
        }
        # 渲染模板显示
        return render(request, 'IncomeType/incomeType_frontshow.html', context)


class ListAllView(View): # 前台查询所有收入分类
    def get(self,request):
        incomeTypes = IncomeType.objects.all()
        incomeTypeList = []
        for incomeType in incomeTypes:
            incomeTypeObj = {
                'typeId': incomeType.typeId,
                'typeName': incomeType.typeName,
            }
            incomeTypeList.append(incomeTypeObj)
        return JsonResponse(incomeTypeList, safe=False)


class UpdateView(BaseView):  # Ajax方式收入分类更新
    def get(self, request, typeId):
        # GET方式请求查询收入分类对象并返回收入分类json格式
        incomeType = IncomeType.objects.get(typeId=typeId)
        return JsonResponse(incomeType.getJsonObj())

    def post(self, request, typeId):
        # POST方式提交收入分类修改信息更新到数据库
        incomeType = IncomeType.objects.get(typeId=typeId)
        incomeType.typeName = request.POST.get('incomeType.typeName')
        incomeType.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台收入分类添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'IncomeType/incomeType_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        incomeType = IncomeType() # 新建一个收入分类对象然后获取参数
        incomeType.typeName = request.POST.get('incomeType.typeName')
        incomeType.save() # 保存收入分类信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新收入分类
    def get(self, request, typeId):
        context = {'typeId': typeId}
        return render(request, 'IncomeType/incomeType_modify.html', context)


class ListView(BaseView):  # 后台收入分类列表
    def get(self, request):
        # 使用模板
        return render(request, 'IncomeType/incomeType_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        incomeTypes = IncomeType.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(incomeTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        incomeTypes_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        incomeTypeList = []
        for incomeType in incomeTypes_page:
            incomeType = incomeType.getJsonObj()
            incomeTypeList.append(incomeType)
        # 构造模板页面需要的参数
        incomeType_res = {
            'rows': incomeTypeList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(incomeType_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除收入分类信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        typeIds = self.getStrParam(request, 'typeIds')
        typeIds = typeIds.split(',')
        count = 0
        try:
            for typeId in typeIds:
                IncomeType.objects.get(typeId=typeId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出收入分类信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        incomeTypes = IncomeType.objects.all()
        #将查询结果集转换成列表
        incomeTypeList = []
        for incomeType in incomeTypes:
            incomeType = incomeType.getJsonObj()
            incomeTypeList.append(incomeType)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(incomeTypeList)
        # 设置要导入到excel的列
        columns_map = {
            'typeId': '分类id',
            'typeName': '分类名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'incomeTypes.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="incomeTypes.xlsx"'
        return response

