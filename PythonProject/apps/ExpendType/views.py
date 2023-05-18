from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.ExpendType.models import ExpendType
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台支出类型添加
    def get(self,request):

        # 使用模板
        return render(request, 'ExpendType/expendType_frontAdd.html')

    def post(self, request):
        expendType = ExpendType() # 新建一个支出类型对象然后获取参数
        expendType.expendTypeName = request.POST.get('expendType.expendTypeName')
        expendType.save() # 保存支出类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改支出类型
    def get(self, request, expendTypeId):
        context = {'expendTypeId': expendTypeId}
        return render(request, 'ExpendType/expendType_frontModify.html', context)


class FrontListView(BaseView):  # 前台支出类型查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        expendTypes = ExpendType.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(expendTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        expendTypes_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'expendTypes_page': expendTypes_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ExpendType/expendType_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示支出类型详情页
    def get(self, request, expendTypeId):
        # 查询需要显示的支出类型对象
        expendType = ExpendType.objects.get(expendTypeId=expendTypeId)
        context = {
            'expendType': expendType
        }
        # 渲染模板显示
        return render(request, 'ExpendType/expendType_frontshow.html', context)


class ListAllView(View): # 前台查询所有支出类型
    def get(self,request):
        expendTypes = ExpendType.objects.all()
        expendTypeList = []
        for expendType in expendTypes:
            expendTypeObj = {
                'expendTypeId': expendType.expendTypeId,
                'expendTypeName': expendType.expendTypeName,
            }
            expendTypeList.append(expendTypeObj)
        return JsonResponse(expendTypeList, safe=False)


class UpdateView(BaseView):  # Ajax方式支出类型更新
    def get(self, request, expendTypeId):
        # GET方式请求查询支出类型对象并返回支出类型json格式
        expendType = ExpendType.objects.get(expendTypeId=expendTypeId)
        return JsonResponse(expendType.getJsonObj())

    def post(self, request, expendTypeId):
        # POST方式提交支出类型修改信息更新到数据库
        expendType = ExpendType.objects.get(expendTypeId=expendTypeId)
        expendType.expendTypeName = request.POST.get('expendType.expendTypeName')
        expendType.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台支出类型添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'ExpendType/expendType_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        expendType = ExpendType() # 新建一个支出类型对象然后获取参数
        expendType.expendTypeName = request.POST.get('expendType.expendTypeName')
        expendType.save() # 保存支出类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新支出类型
    def get(self, request, expendTypeId):
        context = {'expendTypeId': expendTypeId}
        return render(request, 'ExpendType/expendType_modify.html', context)


class ListView(BaseView):  # 后台支出类型列表
    def get(self, request):
        # 使用模板
        return render(request, 'ExpendType/expendType_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        expendTypes = ExpendType.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(expendTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        expendTypes_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        expendTypeList = []
        for expendType in expendTypes_page:
            expendType = expendType.getJsonObj()
            expendTypeList.append(expendType)
        # 构造模板页面需要的参数
        expendType_res = {
            'rows': expendTypeList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(expendType_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除支出类型信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        expendTypeIds = self.getStrParam(request, 'expendTypeIds')
        expendTypeIds = expendTypeIds.split(',')
        count = 0
        try:
            for expendTypeId in expendTypeIds:
                ExpendType.objects.get(expendTypeId=expendTypeId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出支出类型信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        expendTypes = ExpendType.objects.all()
        #将查询结果集转换成列表
        expendTypeList = []
        for expendType in expendTypes:
            expendType = expendType.getJsonObj()
            expendTypeList.append(expendType)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(expendTypeList)
        # 设置要导入到excel的列
        columns_map = {
            'expendTypeId': '支出类型id',
            'expendTypeName': '支出类型名称',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'expendTypes.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="expendTypes.xlsx"'
        return response

