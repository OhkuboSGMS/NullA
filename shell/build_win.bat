@echo off
setlocal
call conda create -n build_nulla python=3.8 -y
call conda activate build_nulla
call pip install -r requirments.txt
call python -m nulla.meta.create_ml_map
call pyinstaller main.spec --noconfirm
call conda deactivate
call conda remove -n build_nulla --all -y

dist\nulla\main.exe
endlocal