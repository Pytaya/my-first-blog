#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: xiaobin
@license: none 
@contact: 854325981@qq.com
@software: PyCharm
@file: simple_and_filter_tag.py
@time: 2018/7/9/0009 7:09
"""

from django import template
from django.utils.html import strip_tags  #去掉所有html标签
import markdown

register = template.Library()  # 也不能用其他变量名

# 下面的是filter  ----这个可以做为模板语言中 if的条件,缺陷是只能两个参数


@register.filter
def if_first(num):
    a,b = divmod(int(num), 2)
    if b == 0:
        return True
    else:
        return False


@register.filter
def markdown_change(content):
    content = strip_tags(content)  # 在转换为markdown之前去掉所有html标签，防止xss攻击
    content = markdown.markdown(
        content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc', ],
        safe_mode=True)
    return content

@register.filter
def only_text(content, counts=100):
    counts = int(counts)
    content = markdown.markdown(
        content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc', ],
        safe_mode=True)
    content = strip_tags(content)[0:counts]  # 在转换为markdown之前去掉所有html标签，防止xss攻击
    return content

@register.filter
def cut_pre_content(all_data, counts=20):
    counts = int(counts)
    if len(all_data) > counts:
        ret_data = "{}...".format(all_data[0: counts])
    else:
        ret_data = all_data
    return ret_data
