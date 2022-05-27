DIR = 'data/districts/'
SHP = DIR + '2022-Windsor_Voter_Districts.shp'
DBF = DIR + '2022-Windsor_Voter_Districts.dbf'
ARGS = list((None, SHP, DBF))

from lxml import etree
from pykml.factory import KML_ElementMaker as KML
import shapefile
import sys

def create_reader(args):
    shp_fname = args[1]
    dbf_fname = args[2]

    shp_file = open(shp_fname, 'rb')
    dbf_file = open(dbf_fname, 'rb')
    
    reader = shapefile.Reader(shp=shp_file, dbf=dbf_file)
    return reader

def create_kml_root():
    doc = KML.kml()
    return etree.SubElement(doc, 'Document')
    
def main(args):        
    reader = create_reader(args)
    doc = create_kml_root()    
    
    for shapeRec in reader.shapeRecords():
        name = shapeRec.record[1]

        points = shapeRec.shape.points
            
        doc.append(KML.Placemark(
            KML.name(name),
            KML.LineString(
                KML.coordinates(
                    ' '.join([str(item).strip('[]').replace(' ', '') for item in points])))))

    et = etree.ElementTree(doc)
    et.write('output.kml', pretty_print=True)
            
    return 0

main(ARGS)