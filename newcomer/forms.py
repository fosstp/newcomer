from datetime import datetime
from pyramid_wtforms import Form, FileField, HiddenField, IntegerField, StringField, DateField, SelectField, BooleanField
from pyramid_wtforms.validators import FileRequired, InputRequired, DataRequired

class UploadForm(Form):
    file = FileField('檔案', [FileRequired()])

class NewComerForm(Form):
    id = HiddenField()
    signup_number    = StringField('就學編號（手動新增者免填）')
    name             = StringField('學童姓名', [InputRequired('必填')])
    parent_name      = StringField('戶長姓名', [InputRequired('必填')])
    id_number        = StringField('學童身份證號', [InputRequired('必填')])
    parent_id_number = StringField('戶長身份證號', [InputRequired('必填')])
    birthday         = DateField('出生日期', [InputRequired('必填')], default=datetime.now)
    move_in_date     = DateField('遷入日期', [InputRequired('必填')], default=datetime.now)
    gender           = StringField('性別', [InputRequired('必填')])
    village          = StringField('里（比如：成功里）', [InputRequired('必填')])
    neighborhood     = StringField('鄰（比如：11）', [InputRequired('必填')])
    address          = StringField('戶籍地址（比如：樂群二路266巷99號）', [InputRequired('必填')])
    note             = StringField('備註')
    status           = SelectField('狀態', [InputRequired('必填')],
                           choices=[('0', '未報到'), ('1', '已報到'), ('2', '他校報到'), ('3', '出國')])
    home_tel         = StringField('家裡電話')
    dad_tel          = StringField('父親電話')
    mom_tel          = StringField('母親電話')
    other_tel        = StringField('其他聯絡電話 (請自行填入需紀錄之資料)')
    contact_address  = StringField('通訊地址（若同戶籍地址可填"同上"）', [InputRequired('必填')])
    picture          = FileField('大頭照')
    is_checked       = BooleanField('已確認資料正確', [DataRequired('請確認資料正確')])
