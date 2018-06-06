from pyramid.view import view_config

@view_config(route_name='edit', renderer='templates/edit.jinja2', request_method='GET')
def edit_new_student_view_via_get(request):
    from pyramid_sqlalchemy import Session
    from ..models import NewStudentModel
    from ..forms import NewStudentForm
    new_student = Session.query(NewStudentModel).get(int(request.matchdict['id']))
    form = NewStudentForm(obj=new_student)
    return {'form': form, 'picture_name': new_student.picture_name}

@view_config(route_name='edit', renderer='templates/edit.jinja2', request_method='POST')
def edit_new_student_view_via_post(request):
    import shutil, os
    from pkg_resources import resource_filename
    from pyramid.httpexceptions import HTTPFound
    from pyramid_sqlalchemy import Session
    from ..models import NewStudentModel
    from ..forms import NewStudentForm

    form = NewStudentForm(request.POST)
    # 該欄位是文字欄位，可省略不輸入，但我們希望在這情況下塞到資料庫是 NULL，所以這邊強制改成 None
    if form.signup_number.data == '': form.signup_number.data = None
    if form.validate():
        new_student = Session.query(NewStudentModel).get(int(form.id.data))
        form.populate_obj(new_student)
        if form.picture.data:
            # 有上傳大頭照，要存檔，並將資料庫對應的欄位設定
            picture_name = form.id_number.data + os.path.splitext(form.picture.data.filename)[-1]
            with open(resource_filename('tp_enroll', 'static/pictures/{}'.format(picture_name)), 'wb') as output:
                shutil.copyfileobj(form.picture.data.file, output)
            new_student.picture_name = picture_name
        # 鄰的欄位，應該要純數字。如果使用者誤填了鄰，要刪掉多餘的文字
        if new_student.neighborhood.endswith('鄰'):
            new_student.neighborhood = new_student.neighborhood[:-1]
        Session.add(new_student)
        return HTTPFound(location=request.route_path('home'))
    return {'form': form}
