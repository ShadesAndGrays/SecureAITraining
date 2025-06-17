@echo off
pushd data
for /d %%D in (besu*) do (
    echo Processing %%D
    pushd "%%D"
    for %%F in (*) do (
        if /I not "%%F"=="key" (
            del /F /Q "%%F"
        )
    )
    for /d %%S in (*) do (
        if /I not "%%S"=="key" (
            rmdir /S /Q "%%S"
        )
    )
    popd
)
popd
echo Done!
pause
