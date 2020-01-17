# shp_to_postgis
Tool to create a new table and insert features from a bunch of shapefiles in a folder matching a given prefix.


Update script settings to match your environment


Settings:

data_folder :    path to folder where files are in

host        :    database ip or database url

database    :    database name to connect

usr         :    database user

pw          :    database user password

schema      :    schema to create new table, should already exist

prefix      :    prefix pattern to find shapefiles in a folder

table       :    table name to create in database



Modify as you wish.
