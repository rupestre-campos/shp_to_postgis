import ogr,osr
import os


#os.environ['SHAPE_ENCODING'] = "utf-8"


data_folder = '/media/rupestre/DADOS/analise_CAR_RLs/car_data'

host = '999.999.999.99'
database = 'gisDB'
usr = 'ccc'
pw = 'mypass'
schema = 'gisdata'

prefix = 'area_imovel'

table = 'area_imovel'

def create_fields(lyr,fields):
    for tup in fields:
        field = ogr.FieldDefn(tup[0], tup[1])
        lyr.CreateField(field)

def find_shps(data_folder,prefix):
    shps = []
    for r,d,f in os.walk(data_folder):
        for arq in f:
            if arq.startswith(prefix) and arq.endswith('.shp'):
                shps.append(os.path.join(r,arq))
    return shps

def get_fields_n_types(shp):
    ds = ogr.Open(shp)
    layer = ds.GetLayer()
    layer_defn = layer.GetLayerDefn()
    fields = []
    for i in range(layer_defn.GetFieldCount()):
        field_name =  layer_defn.GetFieldDefn(i).GetName()
        field_type_code = layer_defn.GetFieldDefn(i).GetType()
        field_type = layer_defn.GetFieldDefn(i).GetFieldTypeName(field_type_code)
        fields.append((field_name,field_type_code))
    return fields

def main():
    conn = "PG: host=%s dbname='%s' user='%s' password='%s' schemas=%s" % (host,database,usr,pw,schema)
    #print(conn)
    shps = find_shps(data_folder,prefix)
    #print(shps)

    fields = get_fields_n_types(shps[0])
    #print(fields)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4674)

    ds = ogr.Open(conn,1)
    layer = ds.CreateLayer(table, srs, ogr.wkbMultiPolygon)
    create_fields(layer,fields)

    layerDefn = layer.GetLayerDefn()
    n = 0
    for shp in shps:
        print(shp)
        in_ds = ogr.Open(shp)
        in_layer = in_ds.GetLayer()
        for feat in in_layer:
            geom = feat.geometry()
            multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
            if geom.GetGeometryType() == ogr.wkbMultiPolygon:
                #print('nome: ' + nome_municip)
                for polygon in geom:
                    multipolygon.AddGeometry(polygon.Buffer(0))
            else:
                multipolygon.AddGeometry(geom.Buffer(0))
            feature = ogr.Feature(layerDefn)
            feature.SetGeometry(multipolygon)
            for field in fields:
                feature.SetField(field[0],feat.GetField(field[0]))
            
            layer.CreateFeature(feature)
            feature = None

        layer.StartTransaction()
        layer.CommitTransaction()
        n += 1
    
    ds = layer = None

if __name__ == "__main__":
    main()