授權
----
GNU GPL v2

安裝
----

為避免影響系統環境，建議使用 virtualenv / pyven 建立獨立執行的環境，
以下範例以 Debian 為操作環境


1. 安裝 python3 相關套件

apt install python3 python3-dev python3-venv build-essential


2. 拉下 git repo

mkdir ~/git && cd ~/git
git clone https://github.com/fossnio/tp_enroll.git

3. 建立 venv 環境

cd tp_enroll
python3 -m venv .venv

4. 進入 virtualenv

source .venv/bin/activate

5. 安裝系統需要的程式套件

pip install pip setuptools pipenv -U
pipenv sync

6. 更改設定檔

cp production.ini.sample production.ini

7. 更改 production.ini

一般來說資料庫跑 sqlite3 就很夠了，所以可以啟用 sqlite3 backend。比方以下範例是指定資料庫檔案位置在 /foo/bar/database.db:

sqlalchemy.url = sqlite:////foo/bar/database.db

設定學校名稱

school_name = 濱江國民小學

設定學校所在的行政區

section_name = 中山區

8. 初始化資料庫

python create_db.py production.ini

9. 啟動網站

pserve production.ini

10. 打開瀏覽器瀏覽 http://localhost:6543
