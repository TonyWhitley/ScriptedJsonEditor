setlocal

if exist envPyLint\scripts 	set path=%path%;envPyLint\Scripts
if not exist envPyLint\scripts	pip install -r requirements.txt

pylint --ignore Tests ScriptedJsonEditor.py 
rem --generate-rcfile ^> Xpylintrc