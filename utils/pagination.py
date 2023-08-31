import math
from django.core.paginator import Paginator
import os

PER_PAGES = int(os.environ.get('PER_PAGE',6))

def make_pagination_range(
    page_range,
    qt_pages,
    current_page
):
    middle_range = math.ceil(qt_pages/2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    start_range_offset = abs(start_range) if start_range < 0 else 0
    total_pages = len(page_range)
    
    if current_page > total_pages:
        raise PageError

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset 
        
    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)            
        
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'qt_pages': qt_pages,
        'page_range':page_range,
        'current_page': current_page,
        'total_pages':total_pages,
        'start_range':start_range,
        'stop_range':stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range':stop_range < total_pages
    }

def make_pagination(request, queryset, qt_pages = 4, per_page = PER_PAGES):
    try:
        current_page = int(request.GET.get('page',1))
    except ValueError:
        current_page = 1
    paginator = Paginator(queryset, per_page)
    
    pagination_range = make_pagination_range(
        paginator.page_range,
        qt_pages,
        current_page
    )
    page_obj = paginator.get_page(current_page)
    return page_obj,pagination_range
    

class PageError(Exception):
    pass