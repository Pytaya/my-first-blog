# -*- coding: utf-8 -*-

import markdown2

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()  # 自定义filter时必须加上

@register.filter(is_safe=True)  # 注册template filter
@stringfilter  #希望字符串作为参数
def djangomarkdown(value):
    return mark_safe(markdown2.markdown(force_text(value),
                                        extras=["code-friendly"]
                                        )
                     )
    