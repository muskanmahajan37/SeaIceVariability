"""
Scripts calculates correlations of SIV/SIT with the AO
 
Notes
-----
    Source : http://www.esrl.noaa.gov/psd/data/gridded/data.
             ncep.reanalysis.derived.html
    Reference : Wu et al. [2006] and Overland et al. [2012]
    Author : Zachary Labe
    Date   : 7 October 2016
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import datetime
import scipy.stats as sts
import read_SeaIceThick_PIOMAS as CT
import read_SeaIceConc_PIOMAS as CC
import calc_PiomasArea as CA
from calc_SIV import sivGrid
from mpl_toolkits.basemap import Basemap

### Define directories
directorydata = '/home/zlabe/Documents/Research/SeaIceVariability/Data/'  
directorydata2 = '/home/zlabe/Surtsey/seaice_obs/PIOMAS/'  
directoryfigure = '/home/zlabe/Desktop/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print '\n' '----Plot NCEP - %s----' % titletime 

### Alott time series
year1 = 1979
year1AD = 1980
year2 = 2015
years = np.arange(year1,year2+1,1)
years2 = np.arange(year1AD,year2+1,1)
months = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',r'Aug',
          r'Sep',r'Oct',r'Nov',r'Dec']
          
### Read in data
seasons = ['JFM','AMJ','JAS','OND']  

ao = np.empty((4,len(years)-1))
sit = np.empty((4,len(years)))
siv = np.empty((4,len(years)))
for i in xrange(len(seasons)):
    filename1 = 'AO_%s_%s%s.txt' % (seasons[i],year1AD,year2)
    filename2 = 'sit_%s_%s%s.txt' % (seasons[i],year1,year2)
    filename3 = 'siv_%s_%s%s.txt' % (seasons[i],year1,year2)
    
    ao[i,:] = np.genfromtxt(directorydata + filename1)
    sit[i,:] = np.genfromtxt(directorydata + filename2)
    siv[i,:] = np.genfromtxt(directorydata + filename3)
    
    print 'Reading data file %s!' % seasons[i]

varx = ao[0,:]
vary = sit[0,1:]    
slope,intercept,r,p_value,std_err = sts.stats.linregress(varx,vary) 

plt.figure()
plt.plot(sit[0])
plt.plot(ao[0])

### Plot figure
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

fig = plt.figure()
ax = plt.subplot(111)

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([]) 
        
ax = plt.subplot(221)

### Adjust axes spines
adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

timex = np.arange(len(years2))
slope_w,intercept_w,r_w,p_value,std_err = sts.stats.linregress(timex,ao[0]) 
line_w = slope_w*timex + intercept_w

plt.plot(ao[0],marker='o',markersize=4,zorder=2,linewidth=2,
         color='steelblue')
plt.plot(siv[0,1:],zorder=2,linewidth=2,color='darkorange')
plt.plot(timex,line_w,zorder=1,linewidth=1.3,color='r')

plt.axvline(np.where(years2 == 2007)[0],color='k',linestyle='--')
plt.axvline(np.where(years2 == 2012)[0],color='k',linestyle='--')
         
plt.xticks(np.arange(0,year2-year1AD+3,5),
           map(str,np.arange(year1AD,year2+3,5)),fontsize=6)
plt.xlim([0,year2-year1+2])

plt.yticks(np.arange(-3,4,1),map(str,np.arange(-3,4,1)),fontsize=6)
plt.ylim([-3,3])

plt.text(-0.1,-3.1,r'\textbf{SIV}',fontsize=11,color='darkorange')
plt.text(-1.3,2.7,r'\textbf{JFM}',fontsize=20,color='darkgrey')

ax = plt.subplot(222)

### Adjust axes spines
adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

timex = np.arange(len(years2))
slope_sp,intercept_sp,r_sp,p_value,std_err = sts.stats.linregress(timex,ao[1]) 
line_sp = slope_sp*timex + intercept_sp

plt.plot(ao[1],marker='o',markersize=4,zorder=2,linewidth=2,
         color='steelblue')
plt.plot(siv[1,1:],zorder=2,linewidth=2,color='darkorange')
plt.plot(timex,line_sp,zorder=1,linewidth=1.3,color='r')

plt.axvline(np.where(years2 == 2007)[0],color='k',linestyle='--')
plt.axvline(np.where(years2 == 2012)[0],color='k',linestyle='--')
         
plt.xticks(np.arange(0,year2-year1AD+3,5),
           map(str,np.arange(year1AD,year2+3,5)),fontsize=6)
plt.xlim([0,year2-year1+2])

plt.yticks(np.arange(-3,4,1),map(str,np.arange(-3,4,1)),fontsize=6)
plt.ylim([-3,3])

plt.text(-0.1,-3.1,r'\textbf{SIV}',fontsize=11,color='darkorange')
plt.text(-1.3,2.7,r'\textbf{AMJ}',fontsize=20,color='darkgrey')

ax = plt.subplot(223)

### Adjust axes spines
adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

timex = np.arange(len(years2))
slope_su,intercept_su,r_su,p_value,std_err = sts.stats.linregress(timex,ao[2]) 
line_su = slope_su*timex + intercept_su

plt.plot(ao[2],marker='o',markersize=4,zorder=2,linewidth=2,
         color='steelblue')
plt.plot(siv[2,1:],zorder=2,linewidth=2,color='darkorange')
plt.plot(timex,line_su,zorder=1,linewidth=1.3,color='r')

plt.axvline(np.where(years2 == 2007)[0],color='k',linestyle='--')
plt.axvline(np.where(years2 == 2012)[0],color='k',linestyle='--')
         
plt.xticks(np.arange(0,year2-year1AD+3,5),
           map(str,np.arange(year1AD,year2+3,5)),fontsize=6)
plt.xlim([0,year2-year1+2])

plt.yticks(np.arange(-3,4,1),map(str,np.arange(-3,4,1)),fontsize=6)
plt.ylim([-3,3])

plt.text(-0.1,-3.1,r'\textbf{SIV}',fontsize=11,color='darkorange')
plt.text(-1.3,2.7,r'\textbf{JAS}',fontsize=20,color='darkgrey')       

ax = plt.subplot(224)

### Adjust axes spines
adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')

timex = np.arange(len(years2))
slope_f,intercept_f,r_f,p_value,std_err = sts.stats.linregress(timex,ao[3]) 
line_f = slope_f*timex + intercept_f

plt.plot(ao[3],marker='o',markersize=4,zorder=2,linewidth=2,
         color='steelblue')
plt.plot(siv[3,1:],zorder=2,linewidth=2,color='darkorange')
plt.plot(timex,line_f,zorder=1,linewidth=1.3,color='r')

plt.axvline(np.where(years2 == 2007)[0],color='k',linestyle='--')
plt.axvline(np.where(years2 == 2012)[0],color='k',linestyle='--')
         
plt.xticks(np.arange(0,year2-year1AD+3,5),
           map(str,np.arange(year1AD,year2+3,5)),fontsize=6)
plt.xlim([0,year2-year1+2])

plt.yticks(np.arange(-3,4,1),map(str,np.arange(-3,4,1)),fontsize=6)
plt.ylim([-3,3])

plt.text(-0.1,-3.1,r'\textbf{SIV}',fontsize=11,color='darkorange')
plt.text(-1.3,2.7,r'\textbf{OND}',fontsize=20,color='darkgrey')


fig.subplots_adjust(hspace=0.4)
plt.savefig(directoryfigure + 'ao_siv_timeseries.png',dpi=300)

###########################################################################
###########################################################################
###########################################################################
### Call functions
lats,lons,sit = CT.readPiomas(directorydata2,years,0.15)
lats,lons,sic = CC.readPiomas(directorydata2,years,0.01)
area = CA.readPiomasArea(directorydata2)
sivgr = sivGrid(sit,sic,area,False)

sivgr_w = np.nanmean(sivgr[1:,0:3,:,:],axis=1)
ad_w = ao[0]
sivgr_sp = np.nanmean(sivgr[1:,3:6,:,:],axis=1)
ad_sp = ao[1]
sivgr_su = np.nanmean(sivgr[1:,6:9,:,:],axis=1)
ad_su = ao[2]
sivgr_f = np.nanmean(sivgr[1:,9:12,:,:],axis=1)
ad_f = ao[3]

def corr(sivgrq,adq):
    varx = sivgrq
    vary = adq
    corr = np.empty((sivgrq.shape[1],sivgrq.shape[2]))
    for i in xrange(sivgrq.shape[1]):
        for j in xrange(sivgrq.shape[2]):
            corr[i,j] = sts.stats.pearsonr(varx[:,i,j],vary)[0]
        
    corr[np.where(corr == 1.)] = np.nan
    return corr
    
corr_w = corr(sivgr_w,ad_w)
corr_sp = corr(sivgr_sp,ad_sp)
corr_su = corr(sivgr_su,ad_su)
corr_f = corr(sivgr_f,ad_f)


### Plot figure
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

fig = plt.figure()
ax = plt.subplot(221)

m = Basemap(projection='npstere',boundinglat=66,lon_0=270,
            resolution='l',round =True)
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='k',linewidth=0.2)
parallels = np.arange(50,90,10)
meridians = np.arange(-180,180,30)
#m.drawparallels(parallels,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
#m.drawmeridians(meridians,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
m.drawlsmask(land_color='darkgrey',ocean_color='mintcream')

# Make the plot continuous
barlim = np.arange(-1,1.1,.5)
values = np.arange(-1,1.1,0.1)

cs = m.contourf(lons,lats,corr_w,
                values,extend='both',latlon=True)
cs1 = m.contour(lons,lats,corr_w,
                values,linewidths=0.2,colors='darkgrey',
                linestyles='-',latlon=True)
        
cs.set_cmap('RdBu_r')
ax.annotate(r'\textbf{JFM}', xy=(0, 0), xytext=(-0.23, 0.9),
            xycoords='axes fraction',fontsize=22,color='darkgrey')

###########################################################################
###########################################################################

ax = plt.subplot(222)

m = Basemap(projection='npstere',boundinglat=66,lon_0=270,
            resolution='l',round =True)
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='k',linewidth=0.2)
parallels = np.arange(50,90,10)
meridians = np.arange(-180,180,30)
#m.drawparallels(parallels,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
#m.drawmeridians(meridians,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
m.drawlsmask(land_color='darkgrey',ocean_color='mintcream')

cs = m.contourf(lons,lats,corr_sp,
                values,extend='both',latlon=True)
cs1 = m.contour(lons,lats,corr_sp,
                values,linewidths=0.2,colors='darkgrey',
                linestyles='-',latlon=True)
        
cs.set_cmap('RdBu_r')

ax.annotate(r'\textbf{AMJ}', xy=(0, 0), xytext=(0.8, 0.9),
            xycoords='axes fraction',fontsize=22,color='darkgrey')

###########################################################################
###########################################################################

ax = plt.subplot(223)

m = Basemap(projection='npstere',boundinglat=66,lon_0=270,
            resolution='l',round =True)
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='k',linewidth=0.2)
parallels = np.arange(50,90,10)
meridians = np.arange(-180,180,30)
#m.drawparallels(parallels,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
#m.drawmeridians(meridians,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
m.drawlsmask(land_color='darkgrey',ocean_color='mintcream')

cs = m.contourf(lons,lats,corr_su,
                values,extend='both',latlon=True)
cs1 = m.contour(lons,lats,corr_su,
                values,linewidths=0.2,colors='darkgrey',
                linestyles='-',latlon=True)
        
cs.set_cmap('RdBu_r')
ax.annotate(r'\textbf{JAS}', xy=(0, 0), xytext=(-0.23, 0.9),
            xycoords='axes fraction',fontsize=22,color='darkgrey')

###########################################################################
###########################################################################

ax = plt.subplot(224)

m = Basemap(projection='npstere',boundinglat=66,lon_0=270,
            resolution='l',round =True)
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='k',linewidth=0.2)
parallels = np.arange(50,90,10)
meridians = np.arange(-180,180,30)
#m.drawparallels(parallels,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
#m.drawmeridians(meridians,labels=[False,False,False,False],
#                linewidth=0.3,color='k',fontsize=6)
m.drawlsmask(land_color='darkgrey',ocean_color='mintcream')

cs = m.contourf(lons,lats,corr_f,
                values,latlon=True)
cs1 = m.contour(lons,lats,corr_f,
                values,linewidths=0.2,colors='darkgrey',
                linestyles='-',latlon=True)
        
cs.set_cmap('RdBu_r')

ax.annotate(r'\textbf{OND}', xy=(0, 0), xytext=(0.8, 0.9),
            xycoords='axes fraction',fontsize=22,color='darkgrey')

cbar_ax = fig.add_axes([0.312,0.1,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=True)

cbar.set_label(r'\textbf{Correlation Coefficient}')
cbar.set_ticks(barlim)
cbar.set_ticklabels(map(str,barlim)) 
plt.setp(ax.get_xticklabels(),visible=False)

fig.subplots_adjust(top=0.95)
fig.subplots_adjust(bottom=0.2)
fig.subplots_adjust(wspace=-0.45)

plt.savefig(directoryfigure + 'testcorrs_ao',dpi=300)