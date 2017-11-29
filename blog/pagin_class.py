#coding:utf-8
from django.utils import timezone
import sys
class PageClass():
    def __init__(self,app_name,db_table,current_page):
        self.models = sys.modules[app_name +".models"]  # 等同于 import web_app2.models
        self.tabel = getattr(self.models,db_table)  # 等同于web_app2.models.Host
        self.current_page = current_page
    
    def data_DataCount_AllPageCount(self,per_item=5):
        start = (self.current_page - 1) * per_item  # 得到数据库中每页开始的索引
        end = self.current_page * per_item  # 得到数据库中每页最后的索引,不包含
        # all_result = self.tabel.objects.all().order_by('-id')  # 所有数据
        all_result = self.tabel.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        result = all_result[start:end]  # 返回指定范围数据
        count = all_result.count()  # 总数据条数
        temp = divmod(count, per_item)  # temp[0]:商 ；temp[1]:余数
        if temp[1] == 0:  # 计算总页数
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1
        '''
        # 只返回text内容的前30字
        for item in result:
            item.text = item.text[:30]
            item.text = item.text.strip().replace(' ', '').replace('\t', '').replace('\r', '').strip()
        '''
        return result,count,all_page_count
    
    def pageList(self,all_page_count,show_page_cout=5):
        add_cout,b = divmod(show_page_cout, 2)  # 当前页左右页数
        if all_page_count > show_page_cout:  # 所有页数大于要展示的页数
            if self.current_page <= add_cout + b:  # 当前面小于等于想要展示页数的一半
                begin = 1
                end = show_page_cout
            else:  # 当前页大于show_page_cout一半
                if self.current_page + add_cout >= all_page_count:  # 当前页加上一半大于总页数
                    begin = all_page_count - show_page_cout + 1  # 只展示最后那几页
                    end = all_page_count
                else:  # 展示当前页的左右页
                    begin = self.current_page - add_cout
                    end = self.current_page + add_cout
        else:  # 所有页数小于要展示的页数,直接展示所有页数
            begin = 1
            end = all_page_count
        page_list = list(range(begin, end + 1))
        return page_list
    
    def prePage_NexPage(self,all_page_count):
        if self.current_page == 1:
            pre_page = None
        else:
            pre_page = self.current_page - 1
        if self.current_page == all_page_count:
            nex_page = None
        else:
            nex_page = self.current_page + 1
        return pre_page,nex_page