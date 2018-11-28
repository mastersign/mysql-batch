@ECHO OFF
PUSHD "%~dp0.."

ECHO.Print Version...
CALL python mysql_batch.py -v
IF ERRORLEVEL 1 GOTO:ERR

ECHO.
ECHO.Dry Run...
CALL python mysql_batch.py -c test\config.ini .\test local -d
IF ERRORLEVEL 1 GOTO:ERR

ECHO.
ECHO.Run...
CALL python mysql_batch.py -c test\config.ini .\test local
IF ERRORLEVEL 1 GOTO:ERR

:END
POPD
ECHO.
ECHO.OK
ECHO.
GOTO:EOF

:ERR
POPD
ECHO.
ECHO.TEST FAILED!
ECHO.
EXIT /B 1
