from unittest import TestCase
from utils.pagination import make_pagination_range

class PaginationTest(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        # current page = 1 - qty page = 2 - middle page = 2
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qty_pages=4,
            current_page=1
        )
        self.assertIn([1,2,3,4], pagination)

    def test_first_range_is_static_if_current_page_is_than_middle_page(self):
        # current page = 1 - qty page = 2 - middle page = 2
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertIn([1,2,3,4], pagination)
        # current page = 2 - qty page = 2 - middle page = 2
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qty_pages=4,
            current_page=2,
        )
        self.assertIn([1,2,3,4], pagination)
        # current page = 3 - qty page = 2 - middle page = 2
        # Here range should change
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qty_pages=4,
            current_page=3
        )
        self.assertIn([2,3,4,5], pagination)
        # current page = 4 - qty page = 2 - middle page = 2
        pagination = make_pagination_range(
            page_range= list(range(1,21)),
            qty_pages=4,
            current_page=4
        )
        self.assertIn([3,4,5,6], pagination)