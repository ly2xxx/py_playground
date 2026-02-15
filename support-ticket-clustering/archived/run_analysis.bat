@echo off
echo Setting up environment...
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set NUMEXPR_NUM_THREADS=1

echo Running analysis...
python analyze_tickets.py

pause
