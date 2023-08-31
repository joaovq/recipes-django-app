from unittest import TestCase
from utils.pagination import PageError, make_pagination_range

class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qt_pages =4,
            current_page=1
        )['pagination']  
        self.assertEqual([1,2,3,4], pagination)
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qt_pages =4,
            current_page=4
        )['pagination']   
        self.assertEqual([3,4,5,6], pagination)
        
    def test_make_sure_middle_ranges_are_correct(self):            
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qt_pages =4,
            current_page=10
        )['pagination']   
        self.assertEqual([9,10,11,12], pagination)
        
    def test_make_pagination_range_end_page_selected(self):
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qt_pages =4,
            current_page=20
        )['pagination']   
        self.assertEqual([17,18,19,20], pagination)
        
    def test_make_pagination_range_when_current_page_near_end_page(self):
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qt_pages =4,
            current_page=18
        )['pagination']   
        self.assertEqual([17,18,19,20], pagination)
        
    def test_make_pagination_range_when_current_page_near_end_page(self):
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qt_pages =4,
            current_page=20
        )['pagination']   
        self.assertEqual([17,18,19,20], pagination) 
        
    def test_with_current_page_greater_than_stop_range(self):        
        with self.assertRaises(PageError):
            make_pagination_range(
                page_range= list(range(1,21)),
                qt_pages =4,
                current_page=25
            )['pagination'] 