@echo off
chcp 65001 > nul
title uv 설치

echo ========================================
echo        uv 설치를 시작합니다.
echo ========================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"

echo.
echo ========================================
echo 설치 작업이 종료되었습니다.
echo.
echo 오류가 있으면 이 화면을 닫지 말고
echo 강사에게 보여주세요.
echo ========================================
echo.

pause