@echo off
echo ====================================
echo Installing Phase 2 Dependencies
echo ====================================
echo.
echo This will install:
echo - sentence-transformers (~90MB download first time)
echo - umap-learn
echo - hdbscan
echo - bertopic (optional)
echo.
echo Installing...
pip install sentence-transformers umap-learn hdbscan
echo.
echo Optional: Install BERTopic for topic modeling
set /p INSTALL_BERTOPIC="Install BERTopic? (y/n): "
if /i "%INSTALL_BERTOPIC%"=="y" (
    pip install bertopic
    echo BERTopic installed!
) else (
    echo Skipping BERTopic (can install later)
)
echo.
echo ====================================
echo Installation complete!
echo ====================================
echo.
echo Run: python analyze_advanced.py
pause
