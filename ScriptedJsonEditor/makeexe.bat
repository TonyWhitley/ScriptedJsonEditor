setlocal
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"

if exist env\scripts (
	set path=%path%;env\Scripts
	pyinstaller ^
	  --onefile ^
	  --distpath . ^
	  "%~dp0\ScriptedJsonEditor.py "
	pause
	)
REM fails to get pypiwin32 on AppVeyor ####  if not exist env\scripts	pip install -r requirements.txt

