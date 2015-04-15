import stix.core.stix_package
import capnp
import time
from lxml import etree


capnp.remove_import_hook()
stix_capnp = capnp.load('stix.capnp')


with open('ma_report.bin', 'rb') as fh:
    start_time = time.time()
    for i in range(1000):
        fh.seek(0)
        stix_package = stix_capnp.STIXPackage.read(fh)
        stix_package.to_dict()
    print time.time() - start_time

with open('maa.xml', 'r') as fh:
    start_time = time.time()
    for i in range(1000):
        fh.seek(0)
        doc = etree.parse(fh)
        parsed_package = stix.core.stix_package.STIXPackage.from_xml(doc)
        parsed_package.to_dict()

print time.time() - start_time
