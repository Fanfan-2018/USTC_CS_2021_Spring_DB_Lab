本系统数据库使用mysql（需要安装pymysql库）
后端使用python+flask（需要安装flask库）
前端使用html+jquery+highcharts（直接使用cdn，可以不用安装相关依赖）

使用前请先用本项目的sql文件将数据库录入mysql数据库中。
并在db.py文件dbfunc函数（文件第41行）修改数据库信息为需要连接的数据库。

安装好必要依赖之后，执行
python main.py

打开浏览器，输入localhost:5000/ 即可访问该项目：

进入主页界面。