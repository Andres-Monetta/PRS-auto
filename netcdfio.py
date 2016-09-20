#!/usr/bin/python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import netCDF4
import numpy
import datetime

def ncdump(nc_fid, verb=True):
    '''
    http://schubert.atmos.colostate.edu/~cslocum/netcdf_example.html
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print "\t\ttype:", repr(nc_fid.variables[key].dtype)
            for ncattr in nc_fid.variables[key].ncattrs():
                print '\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr))
        except KeyError:
            print "\t\tWARNING: %s does not contain variable attributes" % key
    # def print_ncattr

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print "NetCDF Global Attributes:"
        for nc_attr in nc_attrs:
            print '\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions

    # Dimension shape information.
    if verb:
        print "NetCDF dimension information:"
        for dim in nc_dims:
            print "\tName:", dim 
            print "\t\tsize:", len(nc_fid.dimensions[dim])
            print_ncattr(dim)

    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print "NetCDF variable information:"
        for var in nc_vars:
            if var not in nc_dims:
                print '\tName:', var
                print "\t\tdimensions:", nc_fid.variables[var].dimensions
                print "\t\tsize:", nc_fid.variables[var].size
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

# def ncdump

#########################################
#########################################
#########################################

def netcdf2png(url):

  file = netCDF4.Dataset(url,'r')

  # examine the variables
  print file.variables.keys()
  # print file.variables['z']

  lon        = file.variables['lon'][:]
  lat        = file.variables['lat'][:]
  time       = file.variables['time'][:]
  dataWidth  = file.variables['dataWidth'][:]
  lineRes    = file.variables['lineRes'][:]

  lon_u      = file.variables['lon'].units
  lat_u      = file.variables['lat'].units
  time_u     = file.variables['time'].units
  # dataWidth_u = file.variables['dataWidth'].units
  lineRes_u  = file.variables['lineRes'].units

  print lon
  print lon_u
  print lat
  print lat_u
  print time
  print time_u
  print dataWidth
  # print dataWidth_u
  print lineRes
  print lineRes_u

  print lon.size
  print lon.shape

  print lat_u.size
  print lat.shape

  # # sample every 10th point of the 'z' variable
  # topo = file.variables['z'][::10,::10]

  # # make image
  # plt.figure(figsize=(10,10))
  # plt.imshow(topo,origin='lower') 
  # plt.title(file.title)
  # plt.savefig('./imagen/image.png', bbox_inches=0)

  file.close()

# def netcdf2png

#########################################
#########################################
#########################################
#################################### Main

# http://stackoverflow.com/questions/8864599/convert-netcdf-to-image
# http://stackoverflow.com/questions/8864599/convert-netcdf-to-image
# http://www.unidata.ucar.edu/software/netcdf/software.html
# https://code.google.com/archive/p/netcdf4-python/wikis/UbuntuInstall.wiki
# http://www.hydro.washington.edu/~jhamman/hydro-logic/blog/2013/10/12/plot-netcdf-data/

# http://matplotlib.org/basemap/users/examples.html
# http://stackoverflow.com/questions/33523589/python-overlaying-netcdf-data-on-a-basemap-contourf
# http://basemaptutorial.readthedocs.io/en/latest/backgrounds.html
# http://www.idlcoyote.com/map_tips/badmercator.html

archivo = './imagen/goes13.2016.015.140733.BAND_04.nc'

# Dataset is the class behavior to open the file
# and create an instance of the ncCDF4 class
nc_fid = netCDF4.Dataset(archivo, 'r')
                                        
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

lats = nc_fid.variables['lat'][:]  # extract/copy the data
lons = nc_fid.variables['lon'][:]
data = nc_fid.variables['data'][:]
lineRes = nc_fid.variables['lineRes'][:]
elemRes = nc_fid.variables['elemRes'][:]

nc_fid.close()

lon_0 = lons.mean()
lat_0 = lats.mean()

print lineRes
print elemRes

#                low left                  upper right
print "Lats: " + str(lats[-1][-1]) + "," + str(lats[0][0])
print "Lons: " + str(lons[0][0])   + "," + str(lons[-1][-1])

# create polar stereographic Basemap instance.
# voy a usar las coordenadas que se ven en el ncview
# Lats:  -40.2073 -27.7527
# Longs: -66.8611 -48.9735
m = Basemap(projection='merc',lon_0=lon_0,lat_0=lat_0,\
            llcrnrlat=-40.2073,urcrnrlat=-27.7527,\
            llcrnrlon=-66.8611,urcrnrlon=-48.9735,\
            resolution='l')

img = data[0]

re_lons = numpy.reshape(lons,(1,165240))[0]
re_lats = numpy.reshape(lats,(1,165240))[0]

print numpy.sort(re_lons)
print numpy.sort(re_lats)

# transform to nx x ny regularly spaced 4km native projection grid
nx = int((m.xmax-m.xmin)/4000.) + 1
ny = int((m.ymax-m.ymin)/4000.) + 1

print nx
print ny
re_img = numpy.reshape(img,(1,165240))[0]

topodat = m.transform_scalar(re_img,\
                             numpy.sort(re_lons),\
                             numpy.sort(re_lats),\
                             648,\
                             255)

# cm le define el esquema de colores
m.imshow(topodat, cm.GMT_haxby, origin='upper')

m.drawcoastlines()
m.drawstates()
m.drawcountries()

plt.axis('off')
plt.savefig(archivo+str(datetime.datetime.now())+'.png', bbox_inches=0, dpi=200)
# plt.show()
