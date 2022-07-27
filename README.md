# NULL-A

Machine Model Inference GUI

## Install 
 ```
 conda create -n nulla python=3.8
 pip install ./ 
 ```

## Run
 `python main.py`

```
usage: nulla [-h] [--source SOURCE] [--model MODEL]

optional arguments:
  -h, --help       show this help message and exit
  --source SOURCE 動画リソースを設定(数字:WEBカメラ,URL:IPカメラ,ファイルパス:ローカル動画)
  --model MODEL Detector名
```


## Build
### Build pyd

Build cython module

`python setup.py build_ext --inplace`

### Build App
 `pyinstaller main.spec`


## Reference

* Cython https://github.com/cython/cython


## TODO
* WEBカメラ,IPカメラ選択可能
* Model 選択可能
* Icon 作成
* requirements整理