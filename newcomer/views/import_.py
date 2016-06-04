from pyramid.view import view_config

@view_config(route_name='import_via_hro', renderer='templates/import_via_hro.jinja2', request_method='GET')
def import_via_hro_view_via_get(request):
    from ..forms import UploadForm
    return {'form': UploadForm()}

@view_config(route_name='import_via_hro', renderer='templates/import_via_hro.jinja2', request_method='POST')
def import_via_hro_view_via_post(request):
    from datetime import datetime
    from pyramid.httpexceptions import HTTPFound
    from pyramid_sqlalchemy import Session
    from ..forms import UploadForm
    from ..models import NewComerModel

    form = UploadForm(request.POST)
    if form.validate():
        file_content = form.file.data.file.read().decode('cp950')
        content_lines = file_content.split('\r\n')
        for each_line in content_lines:
            splitted_line = each_line.split(',')
            if not splitted_line[0].isdigit(): continue
            if len(splitted_line) != 15: continue
            new_comer = NewComerModel()
            new_comer.signup_number    = int(splitted_line[0])
            new_comer.name             = splitted_line[1]
            new_comer.parent_name      = splitted_line[2]
            new_comer.id_number        = splitted_line[3]
            new_comer.parent_id_number = splitted_line[4]
            new_comer.birthday         = datetime.strptime(splitted_line[5], '%Y/%m/%d')
            new_comer.move_in_date     = datetime.strptime(splitted_line[6], '%Y/%m/%d')
            new_comer.gender           = splitted_line[7]
            new_comer.village          = splitted_line[9]
            new_comer.neighborhood     = splitted_line[10]
            new_comer.address          = splitted_line[11]
            new_comer.note             = splitted_line[14].strip()
            Session.add(new_comer)
        return HTTPFound(location=request.route_path('home'))
    else:
        return {'form': form}

@view_config(route_name='import_via_schoolsoft', renderer='templates/import_via_schoolsoft.jinja2', request_method='GET')
def import_via_schoolsoft_view_via_get(request):
    from ..forms import UploadForm
    return {'form': UploadForm()}

@view_config(route_name='import_via_schoolsoft', renderer='templates/import_via_schoolsoft.jinja2', request_method='POST')
def import_via_schoolsoft_view_via_post(request):
    import shutil, os
    from tempfile import NamedTemporaryFile
    import xlrd
    import sqlalchemy
    from pkg_resources import resource_filename
    from pyramid.httpexceptions import HTTPFound
    from pyramid_sqlalchemy import Session
    from ..models import NewComerModel
    from ..forms import UploadForm

    form = UploadForm(request.POST)

    if form.validate():
        with NamedTemporaryFile(delete=True) as f:
            shutil.copyfileobj(form.file.data.file, f)
            f.flush()
            f.seek(0)
            workbook = xlrd.open_workbook(f.name)
            table = workbook.sheet_by_index(0)
            start_row = 3
            end_column = 38
            changed_list = []
            for i in range(3, table.nrows):
                try:
                    new_comer = Session.query(NewComerModel).filter_by(id_number=table.cell(i, 3).value).one()
                    new_comer.school_number = table.cell(i, 33).value
                    new_comer.klass         = table.cell(i, 34).value
                    new_comer.class_number  = table.cell(i, 35).value

                    # 改大頭照檔名
                    if new_comer.picture_name:
                        basename, extname = new_comer.picture_name.split('.')
                        newname = '.'.join([new_comer.school_number, extname])
                        pictures_dir_root = resource_filename('newcomer', 'static/pictures')
                        src_file = os.path.join(pictures_dir_root, new_comer.picture_name)
                        dst_file = os.path.join(pictures_dir_root, newname)
                        shutil.move(src_file, dst_file)
                        new_comer.picture_name = newname

                    changed_list.append(new_comer)
                except sqlalchemy.orm.exc.NoResultFound:
                    pass
            if changed_list:
                Session.add_all(changed_list)
            return HTTPFound(location=request.route_path('home'))
    else:
        return {'form': form}
