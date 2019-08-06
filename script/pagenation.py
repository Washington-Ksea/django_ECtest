"""pagenation"""
import math

pagenate_by = 2
page_range = 3

def get_pagenation(obj_count, target_page, pagenate_by = pagenate_by):
    """
    args:
        obj_count: 表示する対象の全クエリ数
        target_page: 現在の移動予定のページ数
        pagenate_by: 1ページに表示する数
    return:
        display_obj_index: 最後に表示する対象のインデックス
        display_obj_num: 1ページに表示可能な数
    """
    display_obj_index = pagenate_by
    display_obj_num = pagenate_by

    if target_page is None:
        #page is 1, 2, 3 ...
        display_obj_index = pagenate_by
        
    elif target_page.isdecimal():
        target_page = int(target_page)
    
        if target_page == 0:
            if pagenate_by <= obj_count:
                display_obj_index = pagenate_by
            else:
                display_obj_index = obj_count
                display_obj_num = obj_count

        elif target_page * pagenate_by <= obj_count:
            #表示予定のインデックスが表示対象の数より小さい
            display_obj_index = target_page * pagenate_by

        else:
            display_obj_index = obj_count
            display_obj_num = obj_count % pagenate_by
    
    return display_obj_index, display_obj_num

def get_page_range(obj_count, target_page, pagenate_by=pagenate_by, page_range = page_range):
    """
    args:
        obj_count: 表示する対象の全クエリ数
        target_page: 現在の移動予定のページ数
        pagenate_by: 1ページに表示する数
        page_range: ページ遷移のため表示する範囲
    return:
        page_info
            :page_range: もし、target_page 5, page_range 3なら、  2, 3, 4, 5, 6, 7, 8
            制限として、obj_countの範囲かつ、1以上
    """
    page_info = {
        'has_previous': None,
        'previous_page_number': None,
        'has_next': None,
        'next_page_number': None,
        'page_range': []
    }

    if target_page is None:
        target_page = 1
    elif target_page.isdecimal():
        target_page = int(target_page)
    
    if target_page not in [1, 0]:
        page_info['has_previous'] = True
        page_info['previous_page_number'] = target_page - 1
    
    last_page = math.ceil(obj_count / pagenate_by)
    if target_page < last_page:
        page_info['has_next'] = True
        page_info['next_page_number'] = target_page + 1
    
    page_info['page_range'] = [page for page in range(target_page - page_range, target_page + page_range + 1) if page >= 1 and page <= last_page]
    print(page_info)
    return page_info

