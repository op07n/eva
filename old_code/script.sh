#!/bin/bash
echo Batch Analisys Starts...
date

#find /Volumes/16GB/grabaciones/tenerife/smr/11/1*/* -name *.gps | xargs -I{} ./AstTool_0300.py -f{} -d1 -b
#find ../../Asterix/SMR/06/16/* -name *.gps | xargs -I{} ./AstTool_0400.py -f{} -d1 -b

#find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/04/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
#find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/13/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
# find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/14/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
# find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/15/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
# find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/16/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
# find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/17/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/25/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/26/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/27/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/28/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
find /Volumes/16GB/grabaciones/tenerife/smr/2015/03/29/* -name *.gps | xargs -I{} ./eva.py -f{} -l1 -b -d -i 
echo Batch Analisys Ends...
date


