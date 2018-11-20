from pyramid_sqlalchemy import BaseObject
from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime

class NewStudentModel(BaseObject):

    __tablename__ = 'new_students'

    # primary key
    id = Column(Integer, primary_key=True)

    # 就學編號
    signup_number = Column(Integer)

    # 學童姓名
    name = Column(String(255))

    # 戶長姓名
    parent_name = Column(String(255))

    # 學童身份證號
    id_number = Column(String(255), unique=True)

    # 戶長身份證號
    parent_id_number = Column(String(255))

    # 出生日期
    birthday = Column(Date)

    # 遷入日期
    move_in_date = Column(Date)

    # 性別
    gender = Column(String(10))

    # 里
    village = Column(String(255))
    
    # 鄰
    neighborhood = Column(String(255))

    # 戶籍地址
    address = Column(String(255))

    # 備註
    note = Column(String(255))

    # 以下是額外紀錄的欄位

    # 狀態，0 是未報到， 1 是已報到， 2 是到他校報到， 3 是出國
    status = Column(Integer, default=0)
    
    # 家裡電話
    home_tel = Column(String(255))

    # 父親電話
    dad_tel = Column(String(255))

    # 母親電話
    mom_tel = Column(String(255))

    # 其他聯絡電話
    other_tel = Column(String(255))

    # 通訊地址
    contact_address = Column(String(255))

    # 大頭照的檔案名稱
    picture_name = Column(String(255))

    # 下面三個欄位都是為了相容校務系統而故意設為 String，省得型別還要轉來轉去
    
    # 學號
    school_number = Column(String(255))

    # 班級
    klass = Column(String(255))

    # 座號
    class_number = Column(String(255))

    # 最後更新時間
    last_update = Column(DateTime, default=datetime.now, onupdate=datetime.now)
