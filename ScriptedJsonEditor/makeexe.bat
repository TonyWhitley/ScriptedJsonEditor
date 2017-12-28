setlocal
set path=%path%;C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64;env\Scripts
pyinstaller ^
  --onefile ^
  --distpath . ^
  "%~dp0\ScriptedJsonEditor.py "
pause
