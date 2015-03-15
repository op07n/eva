#!/bin/bash
echo Batch Analisys Starts...
date

#find /Volumes/16GB/grabaciones/tenerife/smr/11/1*/* -name *.gps | xargs -I{} ./AstTool_0300.py -f{} -d1 -b
#find ../../Asterix/SMR/06/16/* -name *.gps | xargs -I{} ./AstTool_0400.py -f{} -d1 -b

#find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/04/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/05/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/06/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/07/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/08/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/09/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/10/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/11/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/12/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 

echo Batch Analisys Ends...
date


