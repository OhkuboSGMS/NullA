@echo off
setlocal
call conda create -n build_nulla python=3.8 -y
call conda activate build_nulla
call pip install -r requirments.txt
call pyinstaller main.spec --noconfirm
call conda deactivate
call conda remove -n build_nulla --all

dist\main\main.exe
endlocal