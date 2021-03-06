"""
Function reads NCEP/NCAR reanalysis for a variety of variables according
to the reader for monthly data.
 
Notes
-----
    Source : http://www.esrl.noaa.gov/psd/data/gridded/data.
             ncep.reanalysis.derived.html
    Author : Zachary Labe
    Date   : 27 September 2016
    
Usage
-----
    readNCEP(directory,years,name,height)
"""

def readNCEP(directory,years,name,height):
    """
    Function reads monthly NCEP/NCAR reanalysis data.

    Parameters
    ----------
    directory : string
        working directory for stored PIOMAS files
    years : integers
        years for data files
    name : string
        heights,tas,slp
    height: string
        surface,1000,925,850,700,600,500,400,300,250,200,150,100,70,50,30,
        20,10

    Returns
    -------
    lats : 2d array
        latitudes
    lons : 2d array
        longitudes
    var : 4d array [year,month,lat,lon]
        ncep variable

    Usage
    -----
    lats,lons,var = readNCEP(directory,years,name,height)
    """
    
    print '\n>>> Using readNCEP function!'    
    
    ### Import modules
    import numpy as np
    from netCDF4 import Dataset
    
    if name == 'heights':
        directoryname = directory + 'h/'
        filename = directoryname + 'hgt.mon.mean.nc'
        varname = 'hgt'
        if height == '1000':
            z = 0
        elif height == '925':
            z = 1
        elif height == '850':
            z = 2
        elif height == '700':
            z = 3
        elif height == '600':
            z = 4
        elif height == '500':
            z = 5
        elif height == '400':
            z = 6
        elif height == '300':
            z = 7
        elif height == '250':
            z = 8
        elif height == '200':
            z = 9
        elif height == '150':
            z = 10
        elif height == '100':
            z = 11
        elif height == '70':
            z = 12
        elif height == '50':
            z = 13
        elif height == '30':
            z = 14
        elif height == '20':
            z = 15
        elif height == '10':
            z = 16
        else:
            ValueError('Wrong height value given!')
    elif name == 'tas':
        directoryname = directory + 'tas/'
        filename = directoryname + 'air.mon.mean.nc'
        varname = 'air'
        if height == '1000':
            z = 0
        elif height == '925':
            z = 1
        elif height == '850':
            z = 2
        elif height == '700':
            z = 3
        elif height == '600':
            z = 4
        elif height == '500':
            z = 5
        elif height == '400':
            z = 6
        elif height == '300':
            z = 7
        elif height == '250':
            z = 8
        elif height == '200':
            z = 9
        elif height == '150':
            z = 10
        elif height == '100':
            z = 11
        elif height == '70':
            z = 12
        elif height == '50':
            z = 13
        elif height == '30':
            z = 14
        elif height == '20':
            z = 15
        elif height == '10':
            z = 16
        else:
            ValueError('Wrong height value given!')
            
    elif name == 'slp':
        directoryname = directory + 'slp/'
        filename = directoryname + 'pres.mon.mean.nc'
        varname = 'pres'
        if height != 'surface':
            ValueError('Wrong height value given!')
    else:
        ValueError('Wrong name of variable!')
        
    ### Time dimension
    yearstart = 1948                               # January 1
    yearmin = int(((np.nanmin(years)-yearstart)*12.))
    yearmax = int((np.nanmax(years)-yearstart)*12.)+12
    print 'Slicing years %s-%s!' % (np.nanmin(years),np.nanmax(years))
        
    ### Read netcdf file
    data = Dataset(filename)
    lats = data.variables['lat'][:]
    lons = data.variables['lon'][:]
    if name == 'slp':
        varq = data.variables[varname][yearmin:yearmax,:,:]
    else:
        varq = data.variables[varname][yearmin:yearmax,z,:,:]
    data.close()   
    print 'Finished reading data file!'
    
    ### Reshaping array
    var = np.reshape(varq,(varq.shape[0]/12.,12,
                           lats.shape[0],lons.shape[0]))
        
    print '*Completed: NCEP data read!\n'
    return lats,lons,var
