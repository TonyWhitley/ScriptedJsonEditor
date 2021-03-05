@echo off
setlocal

python -V | find "3.8"
if errorlevel 1 goto not38
::python -V
echo pyinstaller only works with versions up to 3.7
pause
goto :eof

:not38
set path=c:\Python36;c:\Python36\scripts;%path%
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"


if exist env\scripts 	set path=%path%;env\Scripts
if not exist env\scripts	python.exe -m venv env && env/Scripts/activate && python -m pip install -r requirements.txt 

pyinstaller ^
  --onefile ^
  --distpath . ^
  --paths env\Lib\site-packages ^
  "%~dp0\ScriptedJsonEditor.py "
pause
REM fails to get pypiwin32 on AppVeyor ####  if not exist env\scripts 	pip install -r requirements.txt

