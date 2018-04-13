#!/bin/sh
cd $(cd $(dirname $0);pwd)
cd src/
python setup1.py build_ext --inplace
#python setup2.py build_ext --inplace

mv *.so ../
mv *.c C_files/
