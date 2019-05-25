@echo off
sort allows.te /O temp.te
@<"temp.te">"temp2.te" (for /f "delims=" %%i in ('more') do @if not defined %%i (echo %%i& set %%i=*))
del allows.te
del temp.te
rename temp2.te allows.te