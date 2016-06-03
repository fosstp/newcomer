授權
----
GNU GPL v2

安裝
----

為避免影響系統環境，建議使用 virtualenv / pyven 建立獨立執行的環境，
以下範例以 Debian 為操作環境

1. 安裝 virtualenv 套件

aptitude update && aptitude install python-virtualenv

2. 安裝 python3 套件

aptitude install python3 python3-dev build-essential

3. 建立 virtualenv

mkdir ~/venv
virtualenv -p python3 ~/venv/newcomer

4. 拉下 git repo

mkdir ~/git && cd ~/git
git clone https://github.com/fosstp/newcomer

5. 進入 virtualenv

source ~/venv/newcomer/bin/activate

6. 安裝系統需要的程式套件

cd ~/git/newcomer
python setup.py develop

7. 更改設定檔

cd ~/git/newcomer
cp production.ini.sample production.ini

更改 production.ini
7.1 一般來說資料庫跑 sqlite3 就很夠了，所以可以啟用 sqlite3 backend。比方以下範例是指定資料庫檔案位置在 /foo/bar/database.db:

sqlalchemy.url = sqlite:////foo/bar/database.db

7.2 設定學校名稱

school_name = 您的學校名稱

8. 初始化資料庫

cd ~/git/newcomer
python create_db.py production.ini

9. 啟動網站

cd ~/git/newcomer
pserve production.ini

10. 打開瀏覽器瀏覽 http://localhost:6543
