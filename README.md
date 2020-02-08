# Todoism - Todo伊森

千里之行始于足下, 快用 Todoism 定下你每天的目标, 然后去完成吧! 你的成长由 Todoism 来见证!

## Installation

创建并激活虚拟环境, 然后安装本项目的依赖项.

推荐使用`Pipenv`:
```
$ pipenv install --dev
$ pipenv shell
```

或者使用 `venv/virtualenv` + `pip`:
```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt  # use `pip3` for Python3 on Linux & macOS
```

接着初始化数据库
```
$ flask initdb
```

最后启动Flask, 快去 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) 看看吧!

```
$ flask run
* Running on http://127.0.0.1:5000/
```