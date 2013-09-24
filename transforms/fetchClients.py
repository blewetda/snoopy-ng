#!/usr/bin/python
# -*- coding: utf-8 -*-
# glenn@sensepost.com_
# snoopy_ng // 2013
# By using this code you agree to abide by the supplied LICENSE.txt

import sys
import os
from MaltegoTransform import *
import logging
from datetime import datetime
from sqlalchemy import create_engine, MetaData, select, and_
from transformCommon import *
logging.basicConfig(level=logging.DEBUG,filename='/tmp/maltego_logs.txt',format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

def main():
#    print "Content-type: xml\n\n";
#    MaltegoXML_in = sys.stdin.read()
#    logging.debug(MaltegoXML_in)
#    if MaltegoXML_in <> '':
#     m = MaltegoMsg(MaltegoXML_in)

    #Custom query per transform, but apply filter with and_(*filters) from transformCommon.
    #db.echo=True
    filters.append(proxs.c.mac == vends.c.mac)
    s = select([proxs.c.mac,vends.c.vendor, vends.c.vendorLong], and_(*filters))
    logging.debug(s)
    #s = select([proxs.c.mac,vends.c.vendor, vends.c.vendorLong], and_(proxs.c.mac == vends.c.mac, proxs.c.num_probes>1 ) ).distinct()
    r = db.execute(s)
    results = r.fetchall()
    TRX = MaltegoTransform()
    for mac,vendor,vendorLong in results:
        NewEnt=TRX.addEntity("snoopy.Client", "%s\n(%s)" %(vendor,mac[6:]))
        NewEnt.addAdditionalFields("mac","mac address", "strict",mac)
        NewEnt.addAdditionalFields("vendor","vendor", "nostrict", vendor)
        NewEnt.addAdditionalFields("vendorLong","vendorLong", "nostrict", vendorLong)
    TRX.returnOutput()

main()