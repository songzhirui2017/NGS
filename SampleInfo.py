# coding: utf-8
# Coder: Song Zhirui
# Email: songzhiruifly@hotmail.com
# Date: 2018-06-13
# Info: Get Mapping & QC info 

import sys
import os
import numpy
from collections import OrderedDict


#参数检查
if len(sys.argv) != 3:
    print("Check your args!")
    sys.exit(0)
else:
    shell_name, map_info, qc_info = sys.argv


if not os.path.exists(map_info):
    print("There is no mapping summary info!")
    sys.exit(0)


#summary dict
info_dict = OrderedDict()
qc_dict = OrderedDict()

#读取qc summary
with open(qc_info) as ii:
    for i in ii:
        ilist = i.rstrip().split("\t")
        sample, lib, lane, rreads, rdata = ilist[:5]

        if sample not in info_dict.keys():
            if rreads.isdigit():
                info_dict[sample] = [lib, [int(rreads)], [int(rdata)]]
            else:
                info_dict[sample] = [lib, rreads, rdata]
        else:
            if rreads.isdigit():
                info_dict[sample][0] = lib
                info_dict[sample][1].append(int(rreads))
                info_dict[sample][2].append(int(rdata))
            else:
                info_dict[sample] = [lib, rreads, rdata]

    
    for sample in info_dict.keys():
        if sample == "Sample name":
            qc_dict[sample] = info_dict[sample]
        else:
            qc_dict[sample] = [info_dict[sample][0], sum(info_dict[sample][1]), sum(info_dict[sample][2])]

#读取mapping summary
with open(map_info) as ii:
    info_list = []
    for i in ii:
        ilist = i.strip().split("\t")
        info_list.append(ilist)

    info_array = numpy.array(info_list)
    new_info = numpy.transpose(info_array)

#合并mapping summary & qc summary
for sample, raw in qc_dict.items():
    if sample == "Sample name":
        sample = "Sample"

    for info in new_info:
        if sample == info[0]:
            raw.extend(list(info)[1:])
            INFO = "\t".join([sample] + [str(i) for i in raw]) #+ "\n"
            print(INFO)
    





