from pyramid.view import view_config

@view_config(route_name='export_to_schoolsoft')
def export_to_schoolsoft_view(request):
    from tempfile import NamedTemporaryFile
    import xlwt
    from datetime import datetime
    from pyramid_sqlalchemy import Session
    from ..models import NewComerModel
    from pyramid.response import FileResponse

    with NamedTemporaryFile(delete=True) as f:
        
        wb = xlwt.Workbook()
        ws = wb.add_sheet('臺北市{}{}新生EXCEL檔'.format(
            request.registry.settings['section_name'],
            request.registry.settings['school_name']
        ))
        ws.write(0, 0, '說明1:', xlwt.easyxf('align: horiz center'))
        ws.write_merge(0, 0, 1, 7, '如果您已幫新生編好班級與學號，則請在”新生學號”與”新生班級”欄位填入資料，則系統會自動幫您將學生做報到已註冊並填入學號與班級', xlwt.easyxf('align: horiz center'))
        ws.write(1, 0, '說明2:', xlwt.easyxf('align: horiz center'))

        # 總共 38 個欄位
        end_column = 38

        # 先寫入各欄位說明
        column_description = [
            '就讀學校',
            '編號',
            '姓名',
            '身份證字號',
            '性別',
            '戶籍電話(請輸入一組號碼，不能輸入中文字)',
            '緊急連絡人電話(請輸入一組號碼，不能輸入中文字)',
            '聯絡電話(宅)(請輸入一組號碼，不能輸入中文字)',
            '出生年月日(1000205)',
            '出生地(請填入完整的縣市名稱)',
            '戶籍地址-郵遞區號',
            '戶籍地址-縣市(請填入完整的縣市名稱)',
            '戶籍地址-鄉鎮市(請填入完整的名稱)',
            '戶籍地址-村里(請填入完整的名稱)',
            '戶籍地址-鄰(請填入半形數字)',
            '戶籍地址-住址(包含路巷段號樓等)',
            '通訊地址-郵遞區號',
            '通訊地址-縣市(請填入完整的縣市名稱)',
            '通訊地址-鄉鎮市(請填入完整的名稱)',
            '通訊地址-村里(請填入完整的名稱)',
            '通訊地址-鄰(請填入半形數字)',
            '通訊地址-住址(包含路巷段號樓等)',
            '遷入日期(1000205)',
            '父親姓名',
            '母親姓名',
            '聯絡電話(父)(請輸入一組號碼，不能輸入中文字)',
            '聯絡電話(母)(請輸入一組號碼，不能輸入中文字)',
            '手機號碼(父)(請輸入一組號碼，不能輸入中文字)',
            '手機號碼(母)(請輸入一組號碼，不能輸入中文字)',
            '監護人姓名',
            '與監護人關係',
            '監護人身份證字號',
            '監護人手機(請輸入一組號碼，不能輸入中文字)',
            '新生學號(需以數字填寫)',
            '新生班級(需以數字填寫)',
            '新生座號(需以數字填寫)',
            '學籍設籍日期(1000205)',
            '學生本人領有殘障手冊',
        ]
        for i in range(end_column):
            ws.write(2, i, column_description[i], xlwt.easyxf('align: horiz center'))

        now = datetime.now()

        # 從第四行開始是資料起始點 (cell 是從 0 開始計署，所以第四行其 index 為 3)
        row_counter = 3

        # 只撈出已報到的學生
        for each_newcomer in Session.query(NewComerModel).filter_by(status=1):
            birthday = str(int(each_newcomer.birthday.strftime('%Y')) - 1911) + each_newcomer.birthday.strftime('%m%d')
            move_in_date = str(int(each_newcomer.move_in_date.strftime('%Y')) - 1911) + each_newcomer.move_in_date.strftime('%m%d')

            # 就讀學校
            ws.write(row_counter, 0, '臺北市{}{}'.format(
                request.registry.settings['section_name'],
                request.registry.settings['school_name']
            ))

            # 編號，直接將 row_counter - 2 即可當作編號
            ws.write(row_counter, 1, row_counter - 2)

            # 姓名
            ws.write(row_counter, 2, each_newcomer.name)

            # 身分證字號
            ws.write(row_counter, 3, each_newcomer.id_number)

            # 性別
            ws.write(row_counter, 4, each_newcomer.gender)

            # 聯絡電話（宅）
            ws.write(row_counter, 7, each_newcomer.home_tel)

            # 出生年月日
            ws.write(row_counter, 8, birthday)

            # 戶籍地址-縣市(請填入完整的縣市名稱)
            ws.write(row_counter, 11, '臺北市')

            # 戶籍地址-鄉鎮市(請填入完整的名稱)
            ws.write(row_counter, 12, request.registry.settings['section_name'])

            # 戶籍地址-村里(請填入完整的名稱)
            ws.write(row_counter, 13, each_newcomer.village)
            
            # 戶籍地址-鄰(請填入半形數字)
            ws.write(row_counter, 14, str(int(each_newcomer.neighborhood)))
            
            # 戶籍地址-住址(包含路巷段號樓等)
            ws.write(row_counter, 15, each_newcomer.address)
            
            # 通訊地址-住址(包含路巷段號樓等)
            ws.write(row_counter, 21, each_newcomer.contact_address)
            
            # 遷入日期
            ws.write(row_counter, 22, move_in_date)
            
            # 手機號碼(父)(請輸入一組號碼，不能輸入中文字)
            ws.write(row_counter, 27, each_newcomer.dad_tel)

            # 手機號碼(母)(請輸入一組號碼，不能輸入中文字)
            ws.write(row_counter, 28, each_newcomer.mom_tel)
            
            # 新生學號(需以數字填寫)
            ws.write(row_counter, 33, each_newcomer.school_number)

            # 新生班級(需以數字填寫)
            ws.write(row_counter, 34, each_newcomer.klass)

            # 新生座號(需以數字填寫)
            ws.write(row_counter, 35, each_newcomer.class_number)

            row_counter += 1

        wb.save(f.name)
        response = FileResponse(f.name)
        response.content_disposition = 'attachment; filename="schoolsoft.xls"'
        
        return response

@view_config(route_name='export_to_enroll')
def export_to_enroll_view(request):
    import io
    from pyramid_sqlalchemy import Session
    from ..models import NewComerModel
    from pyramid.response import FileIter

    f = io.BytesIO()

    f.write('就學編號,姓名,身份證號,聯絡電話,報到否(0/1)\r\n'.encode('cp950', 'replace'))
    
    for each_newcomer in Session.query(NewComerModel).filter(NewComerModel.signup_number!=None):
        if each_newcomer.status == 1:
            f.write('{0},{1},{2},,{3}\r\n'.format(
                each_newcomer.signup_number, each_newcomer.name, each_newcomer.id_number, 1
            ).encode('cp950', 'replace'))
        else:
            f.write('{0},{1},{2},,{3}\r\n'.format(
                each_newcomer.signup_number, each_newcomer.name, each_newcomer.id_number, 0
            ).encode('cp950', 'replace'))

    f.flush()
    f.seek(0)

    response = request.response
    response.app_iter = FileIter(f)
    response.content_type = 'application/octet-stream'
    response.content_disposition = 'attachment; filename="enroll.csv"'
    
    return response

@view_config(route_name='export_to_moe')
def export_to_moe_view(request):
    import io, re
    from tempfile import NamedTemporaryFile
    import xlwt
    from pyramid_sqlalchemy import Session
    from ..models import NewComerModel
    from pyramid.response import FileResponse

    with NamedTemporaryFile(delete=True) as f:
        
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet1')
        ws.write(0, 0, '姓名')
        ws.write(0, 1, '身分證號')

        regex = re.compile(r'^[A-Z]\d{9}$') # 比對是否為身分證號
        
        counter = 1
        for each_newcomer in Session.query(NewComerModel).filter(NewComerModel.status==1):
            if regex.match(each_newcomer.id_number):
                ws.write(counter, 0, each_newcomer.name)
                ws.write(counter, 1, each_newcomer.id_number)
                counter += 1

        wb.save(f.name)

        f.flush()
        f.seek(0)

        response = FileResponse(f.name)
        response.content_type = 'application/octet-stream'
        response.content_disposition = 'attachment; filename="moe.xls"'
        
        return response

@view_config(route_name='export_to_ecard')
def export_to_ecard_view(request):
    import os, glob
    from pkg_resources import resource_filename
    from zipfile import ZipFile
    from tempfile import NamedTemporaryFile
    from pyramid.response import FileResponse

    with NamedTemporaryFile(delete=True) as f:

        os.chdir(resource_filename('newcomer', 'static/pictures'))

        with ZipFile(f.name, 'w') as z:
            for i in glob.glob('*'):
                z.write(i)

        f.flush()
        f.seek(0)

        response = FileResponse(f.name)
        response.content_type = 'application/octet-stream'
        response.content_disposition = 'attachment; filename="ecard.zip"'

        return response
