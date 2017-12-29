setlocal
path=%path%;C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64;env\Scripts

if exist env\scripts (
	pyinstaller ^
	  --onefile ^
	  --distpath . ^
	  "%~dp0\ScriptedJsonEditor.py "
	pause
	) else (
	rem No virtualenv
	)
REM fails to get pypiwin32 on AppVeyor ####  if not exist env\scripts 	pip install -r requirements.txt

