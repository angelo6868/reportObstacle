"""
该模块用于实现分页的功能
"""
import math


class Pagination(object):
    # current_page,11,user_list,10
    def __init__(self,dataTotalNum,currentPage,numbersPerPage,pageNum):
        """
        :param dataTotalNum: 数据总的内容条数
        :param currentPage: 当前显示的页码
        :param numbersPerPage: 每页显示的内容条数
        :param pageNum: 页面显示的页码数量
        """
        self.data_total_num = int(dataTotalNum)
        print("总数据为",self.data_total_num)
        self.current_page = int(currentPage)
        print("当前显示页数为",self.current_page)
        self.numbers_per_page = int(numbersPerPage)
        self.page_num = int(pageNum)

    def start(self):
        return (self.current_page-1)*self.numbers_per_page

    def end(self):
        return self.current_page*self.numbers_per_page

    @property
    def total_pages(self):
        """
        self.data_total_num:数据总条数
        self.numbers_per_page：每页显示的数据条数
        :return: 返回页码的总数
        """
        a, b = divmod(self.data_total_num,self.numbers_per_page)
        if b > 0:
            return a+1
        return a

    def page_numbers(self):
        """
        self.total_pages:页码总数
        :return: 函数返回页面要显示的页码范围
        """
        print("self.total_pages",self.total_pages)
        if self.total_pages <= self.page_num:
            return list(range(1,self.total_pages+1))
        elif self.current_page < (math.ceil(self.page_num/2))+1:
            return list(range(1,self.page_num+1))
        elif self.current_page < self.total_pages - (math.ceil(self.page_num/2))+1:
            return list(range(self.current_page - int(self.page_num/2),self.current_page + math.ceil(self.page_num/2)))
        elif self.current_page >= self.total_pages - (math.ceil(self.page_num/2))+1:
            return list(range(self.total_pages - self.page_num+1,self.total_pages+1))

    def pageStr(self):
        """

        :return: 返回分页所需的样式，以及页码数据，需要加上bootstrap.css插件
        """
        page_list = []
        first_page = '<li><a href="/user2.html/?p=1">首页</a></li>'
        page_list.append(first_page)
        if self.current_page <= 1:
            page_prv_str = '<li><a href="#">上一页</a></li>'
        else:
            page_prv_str = '<li><a href="/user2.html/?p=%s">上一页</a></li>' % (self.current_page - 1,)
        page_list.append(page_prv_str)
        for i in self.page_numbers():
            if self.current_page == i:
                pager_num_str = '<li class="active"><a href="/user2.html/?p=%s">%s</a></li>' % (i, i)
            else:
                pager_num_str = '<li><a href="/user2.html/?p=%s">%s</a></li>'%(i,i)
            page_list.append(pager_num_str)
        if self.current_page >= self.total_pages:
            page_next_str = '<li><a href="#">下一页</a></li>'
        else:
            page_next_str = '<li><a href="/user2.html/?p=%s">下一页</a></li>' % (self.current_page + 1,)
        page_list.append(page_next_str)
        last_page = '<li><a href="/user2.html/?p=%s">尾页</a></li>'%self.total_pages
        page_list.append(last_page)
        print(page_list)
        return "".join(page_list)