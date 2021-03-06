#!/usr/bin/python
#  -*- coding: utf-8 -*-
import math
import swisseph
from datetime import *
import pytz
from pytz import timezone
from init_names import *
from icalendar import Calendar
from icalendar import Event
import sys

def compute_zero(func,x0=0):
  if func(x0)==0:
    return x0

def sexastr2deci(str):
  if (str[0]=='-'):
    sgn = -1.0
    dms = str[1:].split(':')
  else:
    sgn = 1.0
    dms = str.split(':')
 
  decival = 0
  for i in range(0,len(dms)):
    decival = decival + float(dms[i])/(60.0**i)

  return decival*sgn


def print_lat_lon(latstr,lonstr):
  if(latstr[0]=='-'):
    lat_suffix='S'
  else:
    lat_suffix='N'

  lat_data=latstr.split(':')
  while len(lat_data)<3:
    lat_data.append(0)
  formatted_string = '%s°%s\'%s\'\'%s' %(lat_data[0],lat_data[1],lat_data[2],lat_suffix)
  
  if (lonstr[0]=='-'):
    lon_suffix='W'
  else:
    lon_suffix='E'

  lon_data=lonstr.split(':')
  while len(lon_data)<3:
    lat_data.append(0)
  formatted_string = '%s,%s°%s\'%s\'\'%s' %(formatted_string,lon_data[0],lon_data[1],lon_data[2],lon_suffix)

  return formatted_string

def print_end_time(end_time, day_night_length, sunrise_time, script):
  if end_time/24.0>day_night_length:
    end_time_str = ahoratram[script]
  else:
    end_time_str = time(sunrise_time+end_time).toString('\hspace{2ex}')
  return end_time_str

def get_ekadashi_name(paksha,lmonth,smonth,script):
  if paksha=='shukla':
    if smonth==8:
      pref=guruvayupura[script]+'/'
    elif smonth==9:
      pref=vaikuntha[script]+'/'
    else:
      pref=''

    if lmonth==int(lmonth):
      return '%s%s~%s' % (pref,shukla_ekadashi_names[script][lmonth],ekadashi[script])
    else:
      return '%s%s~%s' % (pref,shukla_ekadashi_names[script][13],ekadashi[script])
  elif paksha=='krishna':
    if lmonth==int(lmonth):
      return '%s~%s' % (krishna_ekadashi_names[script][lmonth],ekadashi[script])
    else:
      return '%s~%s' % (krishna_ekadashi_names[script][13],ekadashi[script])

def get_tithi(jd):
  ldiff=(swisseph.calc_ut(jd,swisseph.MOON)[0]-swisseph.calc_ut(jd,swisseph.SUN)[0])%360
  return int(1+math.floor(ldiff / 12.0))

def get_nakshatram(jd):
  lmoon=(swisseph.calc_ut(jd,swisseph.MOON)[0]-swisseph.get_ayanamsa(jd))%360
  return int(1+math.floor(lmoon / (360.0/27.0)))

def get_chandra_masa(month,chandra_masa_names,script):
  if month==int(month):
    return chandra_masa_names[script][month]
  else:
    return '%s~(%s)' % (chandra_masa_names[script][int(month)+1],adhika[script]) 


def get_angams_for_kalas(jd_sunrise,jd_sunrise_tmrw,jd_sunrise_datmrw,jd_sunset,jd_sunset_tmrw,get_angam_func,kala_type):
  if kala_type == 'sunrise':
    angams = [get_angam_func(jd_sunrise),get_angam_func(jd_sunrise),get_angam_func(jd_sunrise_tmrw),get_angam_func(jd_sunrise_tmrw)]
  if kala_type == 'sunset':
    angams = [get_angam_func(jd_sunset),get_angam_func(jd_sunset),get_angam_func(jd_sunset_tmrw),get_angam_func(jd_sunset_tmrw)]
  elif kala_type == 'pratah' :
    angams = [get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(1.0/5.0)),#pratah1 start
              get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(2.0/5.0)),#pratah1 end 
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(1.0/5.0)),#pratah2 start
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(2.0/5.0))]#pratah2 end
  elif kala_type == 'madhyahna' :
    angams = [get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(2.0/5.0)),#madhyahna1 start
              get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(3.0/5.0)),#madhyahna1 end 
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(2.0/5.0)),#madhyahna2 start
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(3.0/5.0))]#madhyahna2 end
  elif kala_type == 'aparahna' :
    angams = [get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(3.0/5.0)),#aparahna1 start
              get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(4.0/5.0)),#aparahna1 end 
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(3.0/5.0)),#aparahna2 start
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(4.0/5.0))]#aparahna2 end
  elif kala_type == 'saydhna' :
    angams = [get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(4.0/5.0)),#saydhna1 start
              get_angam_func(jd_sunrise+(jd_sunset-jd_sunrise)*(5.0/5.0)),#saydhna1 end 
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(4.0/5.0)),#saydhna2 start
              get_angam_func(jd_sunrise_tmrw+(jd_sunset_tmrw-jd_sunrise_tmrw)*(5.0/5.0))]#saydhna2 end
  elif kala_type == 'madhyaratri' :
    angams = [get_angam_func(jd_sunset+(jd_sunrise_tmrw-jd_sunset)*(2.0/5.0)),#madhyaratri1 start
              get_angam_func(jd_sunset+(jd_sunrise_tmrw-jd_sunset)*(3.0/5.0)),#madhyaratri1 end 
              get_angam_func(jd_sunset_tmrw+(jd_sunrise_datmrw-jd_sunset_tmrw)*(2.0/5.0)),#madhyaratri2 start
              get_angam_func(jd_sunset_tmrw+(jd_sunrise_datmrw-jd_sunset_tmrw)*(3.0/5.0))]#madhyaratri2 end
  elif kala_type == 'pradosha' :
    angams = [get_angam_func(jd_sunset),#pradosha1 start
              get_angam_func(jd_sunset+(jd_sunrise_tmrw-jd_sunset)*(1.0/5.0)),#pradosha1 end 
              get_angam_func(jd_sunset_tmrw),#pradosha2 start
              get_angam_func(jd_sunset_tmrw+(jd_sunrise_datmrw-jd_sunset_tmrw)*(1.0/5.0))]#pradosha2 end
  elif kala_type == 'nishita' :
    angams = [get_angam_func(jd_sunset+(jd_sunrise_tmrw-jd_sunset)*(7.0/15.0)),#nishita1 start
              get_angam_func(jd_sunset+(jd_sunrise_tmrw-jd_sunset)*(8.0/15.0)),#nishita1 end 
              get_angam_func(jd_sunset_tmrw+(jd_sunrise_datmrw-jd_sunset_tmrw)*(7.0/15.0)),#nishita2 start
              get_angam_func(jd_sunset_tmrw+(jd_sunrise_datmrw-jd_sunset_tmrw)*(8.0/15.0))]#nishita2 end
  else:
    #Error!
    '''Error!'''
  return angams

def get_festival_day(festival_angam,angam_sunrise,d,jd_sunrise,jd_sunrise_tmrw,get_angam_func,min_t,kala,priority):
  t_cutoff=(jd_sunrise_tmrw-jd_sunrise)*min_t/60.0 #at least min_t nazhis
  
  if angam_sunrise[d]==(festival_angam-1) or angam_sunrise[d]==festival_angam:
    if angam_sunrise[d]==festival_angam or (angam_sunrise[d]==(festival_angam-1) and angam_sunrise[d+1]==(festival_angam+1)):
      if angam_sunrise[d-1]!=festival_angam:#otherwise yesterday would have already been assigned
        #Return d-1 if angam changes within t_cutoff, else d
        if get_angam_func(jd_sunrise+t_cutoff)!=angam_sunrise[d]:
          return d-1
        else:
          return d
    elif angam_sunrise[d+1]==festival_angam:
      #Return d if angam changes within say t_cutoff, else d-1
      if get_angam_func(jd_sunrise_tmrw+t_cutoff)!=angam_sunrise[d+1]:
        return d
      else:
        return d+1
  return None

def get_angam_float(jd, arc_len, w):
  lmoon=(swisseph.calc_ut(jd,swisseph.MOON)[0]-swisseph.get_ayanamsa(jd))%360
  lsun=(swisseph.calc_ut(jd,swisseph.SUN)[0]-swisseph.get_ayanamsa(jd))%360
  ldiff=(lmoon*w[0]+lsun*w[1])%360
  return (ldiff/arc_len)

def get_angam_data_string(angam_names, arc_len, jd_sunrise, jd_sunrise_tmrw, 
  t_sunrise, longitude_moon, longitude_sun, longitude_moon_tmrw, 
  longitude_sun_tmrw, w, script):

  daily_motion_moon = (longitude_moon_tmrw-longitude_moon)%360
  daily_motion_sun = (longitude_sun_tmrw-longitude_sun)%360

  num_angas = int(360.0/arc_len)
  angam = [0]*3
  angam_str = ['']*3
  angam_end_str = ['']*3
  angam_end = [0]*3
  angam_remaining = [0]*3

  #Compute karanam details
  angam[0] = int(1+math.floor((longitude_moon*w[0]+longitude_sun*w[1])%360 / arc_len))
  angam_tmrw = int(1+math.floor((longitude_moon_tmrw*w[0]+longitude_sun_tmrw*w[1])%360 / arc_len))

  # There cannot be more than 3 angams (max=3 for karanams) in a day, 
  # because of total arc ~ 12 deg and arclen per angam
  for i in range(0,3):
    if ((angam_tmrw-angam[0])%num_angas > i) or (i==0): #i=0 must be considered, because the angam may not change till the next sunrise
      #multiple change
      angam[i]=((angam[0]+(i-1))%num_angas)+1
      angam_str[i] = angam_names[angam[i]]
      angam_remaining[i] = arc_len*(i+1)-(((longitude_moon*w[0]+
        longitude_sun*w[1])%360)%arc_len)
      angam_end[i] = angam_remaining[i]/(daily_motion_moon*w[0]+
        daily_motion_sun*w[1])*24.0
      angam_end_str[i] = print_end_time(angam_end[i],jd_sunrise_tmrw-jd_sunrise,t_sunrise,script)
    else:
      angam_str[i] = ''
      angam_end_str[i] = ''
      
    if (angam_end_str[i] == ahoratram[script] and i!=0):
      #needs correction, owing to the fact that we compute longitude every 24h,
      #rather than at next sunrise the second/third angam cannot be 'all day'!
      #Its ending will reflect in tomorrow's calendar
      angam_str[i] = ''
      angam_end_str[i] = ''


  angam_data_string=''
  for i in range(0,3):
    if angam_str[i] != '': 
      if i==2:
        angam_data_string = angam_data_string+'\\\\'
      if (angam_end_str[i] == ahoratram[script]):
        angam_data_string = '%s\\mbox{%s {\\tiny \\RIGHTarrow} %s}'           % (angam_data_string,angam_str[i],angam_end_str[i])
      else:
        angam_data_string = '%s\\mbox{%s {\\tiny \\RIGHTarrow} \\textsf{%s}}' % (angam_data_string,angam_str[i],angam_end_str[i])
    
  return [angam[0],angam_data_string]

class  city:
  '''
  This class enables the construction of a city object
  '''
  def __init__(self,name,latitude,longitude,timezone):
    '''Constructor for city'''
    self.name = name
    self.latstr = latitude
    self.lonstr = longitude
    self.latitude = sexastr2deci(latitude)
    self.longitude = sexastr2deci(longitude)
    self.timezone = timezone

  def getLastDhanurTransit(self, jd_start):
    '''Compute the last transit through dhanus. Especially useful to find
    the sun month on Jan 1'''
    swisseph.set_sid_mode(swisseph.SIDM_LAHIRI) #Force Lahiri Ayanamsha
    for d in range(-25,0):
      jd = jd_start + d
      [y,m,d,t] = swisseph.revjul(jd)
    
      jd_sunrise=swisseph.rise_trans(jd_start=jd,body=swisseph.SUN,lon=self.longitude,
        lat=self.latitude,rsmi=swisseph.CALC_RISE|swisseph.BIT_DISC_CENTER)[1][0]
      jd_sunrise_tmrw=swisseph.rise_trans(jd_start=jd+1,body=swisseph.SUN,
        lon=self.longitude,lat=self.latitude,rsmi=swisseph.CALC_RISE|swisseph.BIT_DISC_CENTER)[1][0]
      jd_sunset =swisseph.rise_trans(jd_start=jd,body=swisseph.SUN,lon=self.longitude,
        lat=self.latitude,rsmi=swisseph.CALC_SET|swisseph.BIT_DISC_CENTER)[1][0]
    
      longitude_sun_rise=swisseph.calc_ut(jd_sunrise,swisseph.SUN)[0]-swisseph.get_ayanamsa(jd_sunrise)
      longitude_sun_set=swisseph.calc_ut(jd_sunset,swisseph.SUN)[0]-swisseph.get_ayanamsa(jd_sunset)
      solar_month_rise = int(1+math.floor(((longitude_sun_rise)%360)/30.0))
      solar_month = int(1+math.floor(((longitude_sun_set)%360)/30.0))
      longitude_sun_tmrw=swisseph.calc_ut(jd_sunrise+1,swisseph.SUN)[0]-swisseph.get_ayanamsa(jd_sunrise+1)
      solar_month_tmrw = int(1+math.floor(((longitude_sun_tmrw)%360)/30.0))
  
      if solar_month_rise!=solar_month_tmrw:
        if solar_month!=solar_month_tmrw:
          return jd+1
        else:
          return jd

class  time:
  '''This  class is a time class with methods for printing, conversion etc.'''
  def  __init__(self,t):
    self.t = t

  def  toString(self,default_suffix='',format='hh:mm'):
    t = self.t
    if t>=24:
      t = t-24
      suffix = '(+1)'
    else:
      suffix = default_suffix

    hour = math.floor(t)
    t = t - hour
    minute = math.floor(t*60.0)
    t = t-minute
    second = round(t*60)  

    if format == 'hh:mm':
      return '%02d:%02d%s' % (hour,minute,suffix)
    elif format == 'hh:mm:ss':
      return '%02d:%02d:%02d%s' % (hour,minute,second,suffix)
    else:
      '''Thrown an exception, for unknown format'''
      
class  divas:
  '''This class will store all the details of a particular day of a year'''

  def  __init__(self,city,jd):
    ''' '''
    [y,m,dt,t] = swisseph.revjul(jd)
    local_time = pytz.timezone(tz).localize(datetime(y, m, dt, 6, 0, 0))
    #checking @ 6am local - can we do any better?
    tz_off=(datetime.utcoffset(local_time).days*86400+datetime.utcoffset(local_time).seconds)/3600.0 
    #compute offset from UTC


    self.city = city
    self.year = y
    self.month = m
    self.date  = dt

    self.jd_sunrise  = swisseph.rise_trans(jd_start=jd,body=swisseph.SUN,
       lon=self.city.longitude,lat=self.city.latitude,
      rsmi=swisseph.CALC_RISE|swisseph.BIT_DISC_CENTER)[1][0]  
    self.jd_sunset  = swisseph.rise_trans(jd_start=jd,body=swisseph.SUN,
       lon=self.city.longitude,lat=self.city.latitude,
      rsmi=swisseph.CALC_SET|swisseph.BIT_DISC_CENTER)[1][0]  
    self.jd_moonrise  = swisseph.rise_trans(jd_start=jd_sunrise,body=swisseph.MOON,
       lon=self.city.longitude,lat=self.city.latitude,
      rsmi=swisseph.CALC_RISE|swisseph.BIT_DISC_CENTER)[1][0]  
    self.jd_moonset  = swisseph.rise_trans(jd_start=jd_sunset,body=swisseph.MOON,
       lon=self.city.longitude,lat=self.city.latitude,
      rsmi=swisseph.CALC_SET|swisseph.BIT_DISC_CENTER)[1][0]  

    self.t_sunrise   = (self.jd_sunrise -jd)*24.0 + tz_off
    self.t_sunset    = (self.jd_sunset  -jd)*24.0 + tz_off
    self.t_moonrise  = (self.jd_moonrise-jd)*24.0 + tz_off
    self.t_moonset   = (self.jd_moonset -jd)*24.0 + tz_off


  def compute_kala(self):
     '''Computes all the kalas, including rahukalam, yamagandam etc.'''


class panchangam:
  '''This class enables the construction of a panchangam'''

  def __init__(self,city,year=2012,script='deva'):
    '''Constructor for the panchangam.'''
    self.city = city
    self.year = year
    self.script = script

    self.jd_start = swisseph.julday(year,1,1,0)
    self.eventSep = '\\diam '

    swisseph.set_sid_mode(swisseph.SIDM_LAHIRI) #Force Lahiri Ayanamsha

  def computeAngams(self):
    '''Compute the entire panchangam'''
    #INITIALISE VARIABLES
    self.jd_sunrise=[None]*368
    self.jd_sunset=[None]*368
    self.jd_moonrise=[None]*368
    self.jd_moonset=[None]*368
    longitude_moon_sunrise=[None]*368
    longitude_sun_sunrise=[None]*368
    longitude_sun_sunset=[None]*368
    self.solar_month=[None]*368
    self.solar_month_sunrise=[None]*368
    self.lunar_month=[None]*368
    self.month_data=[None]*368
    self.tithi_data_string=[None]*368
    self.tithi_sunrise=[None]*368
    self.nakshatram_data_string=[None]*368
    self.nakshatram_sunrise=[None]*368
    self.karanam_data_string=[None]*368
    self.karanam_sunrise=[None]*368
    self.yogam_data_string=[None]*368
    self.yogam_sunrise=[None]*368
    self.weekday=[None]*368
    self.sunrise=[None]*368
    self.sunset=[None]*368
    self.sangava=[None]*368
    self.rahu=[None]*368
    self.yama=[None]*368
    self.festival_day_list={}
    self.festivals=['']*368
    
    self.weekday_start=swisseph.day_of_week(self.jd_start)+1
    #swisseph has Mon = 0, non-intuitively!
  
    solar_month_day = self.jd_start-self.city.getLastDhanurTransit(self.jd_start)

    month_start_after_sunset = 0

    ##################################################
    #Compute all parameters -- latitude/longitude etc#
    ##################################################
  
    for d in range(-1,367):
      jd = self.jd_start-1+d
      [y,m,dt,t] = swisseph.revjul(jd)
      weekday = (self.weekday_start -1 + d)%7 
    
      local_time = pytz.timezone(self.city.timezone).localize(datetime(y, m, dt, 6, 0, 0))
      #checking @ 6am local - can we do any better?
      tz_off=(datetime.utcoffset(local_time).days*86400+datetime.utcoffset(local_time).seconds)/3600.0 
      #compute offset from UTC
  
      self.jd_sunrise[d+1]=swisseph.rise_trans(jd_start=jd+1,body=swisseph.SUN,
        lon=self.city.longitude,lat=self.city.latitude,rsmi=swisseph.CALC_RISE|swisseph.BIT_DISC_CENTER)[1][0]
      self.jd_sunset[d+1]=swisseph.rise_trans(jd_start=self.jd_sunrise[d+1],body=swisseph.SUN,
        lon=self.city.longitude,lat=self.city.latitude,rsmi= swisseph.CALC_SET|swisseph.BIT_DISC_CENTER)[1][0]
      self.jd_moonrise[d+1]=swisseph.rise_trans(jd_start=jd+1,body=swisseph.MOON,
        lon=self.city.longitude,lat=self.city.latitude,rsmi=swisseph.CALC_RISE|swisseph.BIT_DISC_CENTER)[1][0]
      self.jd_moonset[d+1]=swisseph.rise_trans(jd_start=jd+1,body=swisseph.MOON,
        lon=self.city.longitude,lat=self.city.latitude,rsmi= swisseph.CALC_SET|swisseph.BIT_DISC_CENTER)[1][0]
    
      longitude_sun_sunrise[d+1] = swisseph.calc_ut(self.jd_sunrise[d+1],swisseph.SUN )[0]-swisseph.get_ayanamsa(self.jd_sunrise[d+1])
      longitude_moon_sunrise[d+1]= swisseph.calc_ut(self.jd_sunrise[d+1],swisseph.MOON)[0]-swisseph.get_ayanamsa(self.jd_sunrise[d+1])
      longitude_sun_sunset[d+1]  = swisseph.calc_ut(self.jd_sunset[d+1], swisseph.SUN )[0]-swisseph.get_ayanamsa(self.jd_sunset[d+1] )
      
      self.solar_month[d+1] =    int(1+math.floor(((longitude_sun_sunset[d+1])%360)/30.0))
  
      self.solar_month_sunrise[d+1] = int(1+math.floor(((longitude_sun_sunrise[d+1])%360)/30.0))
  
      if(d<=0):
        continue
        #This is just to initialise, since for a lot of calculations, we require comparing with tomorrow's
        #data. This computes the data for day 0, -1.
  
      t_sunrise=(self.jd_sunrise[d]-jd)*24.0+tz_off
      t_sunset=(self.jd_sunset[d]-jd)*24.0+tz_off
      #print '%',jd,self.jd_sunrise[d],self.jd_sunset[d],tz_off
  	
    
      #Solar month calculations
      if month_start_after_sunset==1:
        solar_month_day = 0
        month_start_after_sunset = 0
    
      if self.solar_month[d]!=self.solar_month[d+1]:
        solar_month_day = solar_month_day + 1
        if self.solar_month[d]!=self.solar_month_sunrise[d+1]:
          month_start_after_sunset=1
          [_m,solar_month_end_time] = get_angam_data_string(masa_names[self.script], 30, self.jd_sunrise[d],
            self.jd_sunrise[d+1], t_sunrise, longitude_moon_sunrise[d], longitude_sun_sunrise[d], 
            longitude_moon_sunrise[d+1], longitude_sun_sunrise[d+1], [0,1], self.script)
      elif self.solar_month_sunrise[d]!=self.solar_month[d]:
        #sankrAnti!
        #sun moves into next rAshi before sunset -- check rules!
        solar_month_day = 1
        [_m,solar_month_end_time] = get_angam_data_string(masa_names[self.script], 30, self.jd_sunrise[d],
          self.jd_sunrise[d+1], t_sunrise, longitude_moon_sunrise[d], longitude_sun_sunrise[d],
          longitude_moon_sunrise[d+1], longitude_sun_sunrise[d+1], [0,1], self.script)
      else:
        solar_month_day = solar_month_day + 1
        solar_month_end_time = ''
      
      self.month_data[d] = '\\sunmonth{%s}{%d}{%s}' % (masa_names[self.script][self.solar_month[d]],solar_month_day,solar_month_end_time)
  
      #KARADAYAN NOMBU -- easy to check here
      if solar_month_end_time !='': #month ends today
        if (self.solar_month[d]==12 and solar_month_day==1) or (self.solar_month[d]==11 and solar_month_day!=1):
          self.festival_day_list[karadayan_nombu[self.script]] = [d]
      #KOODARA VALLI -- easy to check here
      if self.solar_month[d]==9 and solar_month_day==27:
        self.festival_day_list[koodaravalli[self.script]]= [d]
  
    
      #Sunrise/sunset and related stuff (like rahu, yama)
      yamagandam_octets  = [5,4,3,2,1,7,6]
      rahukalam_octets = [8,2,7,5,6,4,3]

      length_of_day = t_sunset-t_sunrise

      yamagandam_start = t_sunrise + (1/8.0)*(yamagandam_octets[weekday]-1)*length_of_day
      yamagandam_end = yamagandam_start + (1/8.0)*length_of_day
      rahukalam_start = t_sunrise + (1/8.0)*(rahukalam_octets[weekday]-1)*length_of_day
      rahukalam_end = rahukalam_start + (1/8.0)*length_of_day
      sangava_start = t_sunrise + (1/5.0)*length_of_day
    
      self.sunrise[d]  = time(t_sunrise).toString()
      self.sunset[d]   = time(t_sunset).toString()
      self.sangava[d] = time(sangava_start).toString()
      self.rahu[d] = '%s--%s' % (time(rahukalam_start).toString() ,time(rahukalam_end).toString())
      self.yama[d] = '%s--%s' % (time(yamagandam_start).toString(),time(yamagandam_end).toString())
      
      [self.tithi_sunrise[d],self.tithi_data_string[d]]=get_angam_data_string(tithi_names[self.script], 12, self.jd_sunrise[d],
        self.jd_sunrise[d+1], t_sunrise, longitude_moon_sunrise[d], longitude_sun_sunrise[d], longitude_moon_sunrise[d+1],
        longitude_sun_sunrise[d+1], [1,-1], self.script)
      [self.nakshatram_sunrise[d], self.nakshatram_data_string[d]]=get_angam_data_string(nakshatra_names[self.script], (360.0/27.0),
        self.jd_sunrise[d], self.jd_sunrise[d+1], t_sunrise, longitude_moon_sunrise[d], longitude_sun_sunrise[d], 
        longitude_moon_sunrise[d+1], longitude_sun_sunrise[d+1], [1,0], self.script)
      [self.karanam_sunrise[d],self.karanam_data_string[d]]=get_angam_data_string(karanam_names[self.script], 6, self.jd_sunrise[d],
        self.jd_sunrise[d+1], t_sunrise, longitude_moon_sunrise[d], longitude_sun_sunrise[d], longitude_moon_sunrise[d+1],
        longitude_sun_sunrise[d+1], [1,-1], self.script)
      [self.yogam_sunrise[d],self.yogam_data_string[d]]=get_angam_data_string(yogam_names[self.script], (360.0/27.0), self.jd_sunrise[d],
        self.jd_sunrise[d+1], t_sunrise, longitude_moon_sunrise[d], longitude_sun_sunrise[d], longitude_moon_sunrise[d+1],
        longitude_sun_sunrise[d+1], [1,1], self.script)
 
  def assignLunarMonths(self):
    last_month_change = 1
    last_lunar_month = None
    for d in range(1,367):
      #Assign lunar_month for each day
      if(self.tithi_sunrise[d]==1):
        for i in range(last_month_change,d):
          if (self.solar_month[d]==last_lunar_month):
            self.lunar_month[i] = self.solar_month[d]%12 + 0.5
          else:
            self.lunar_month[i] = self.solar_month[d]
        last_month_change = d 
        last_lunar_month = self.solar_month[d]
      elif(self.tithi_sunrise[d]==2 and self.tithi_sunrise[d-1]==30):
        #prathama tithi was never seen @ sunrise
        for i in range(last_month_change,d):
          if (self.solar_month[d-1]==last_lunar_month):
            self.lunar_month[i] = self.solar_month[d-1]%12 + 0.5
          else:
            self.lunar_month[i] = self.solar_month[d-1]
        last_month_change = d 
        last_lunar_month = self.solar_month[d-1]
  
    for i in range(last_month_change,367):
      self.lunar_month[i]=self.solar_month[last_month_change-1]+1

  def computeFestivals(self):
    for d in range(1,367):
      jd = self.jd_start-1+d
      [y,m,dt,t] = swisseph.revjul(jd)
      weekday = (self.weekday_start -1 + d)%7 
  
      ##################
      #Festival details#
      ##################
  
      ###--- MONTHLY VRATAMS ---###
  
      #EKADASHI Vratam
      if self.tithi_sunrise[d]==11 or self.tithi_sunrise[d]==12: #One of two consecutive tithis must appear @ sunrise!
        #check for shukla ekadashi
        if (self.tithi_sunrise[d]==11 and self.tithi_sunrise[d+1]==11): 
          self.festivals[d+1]=sarva[self.script]+'~'+get_ekadashi_name(paksha='shukla',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)#lunar_month[d] or [d+1]?
          if self.lunar_month[d+1]==4:
            self.festivals[d+1]+=self.eventSep+chaturmasya_start[self.script]
          if self.lunar_month[d+1]==8:
            self.festivals[d+1]+=self.eventSep+chaturmasya_end[self.script]
        elif (self.tithi_sunrise[d]==11 and self.tithi_sunrise[d+1]!=11): 
          #Check dashami end time to decide for whether this is sarva/smartha
          tithi_arunodayam = get_tithi(self.jd_sunrise[d]-(1/15.0)*(self.jd_sunrise[d]-self.jd_sunrise[d-1])) #Two muhurtams is 1/15 of day-length
          if tithi_arunodayam==10:
            self.festivals[d]=smartha[self.script]+'~'+get_ekadashi_name(paksha='shukla',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
            self.festivals[d+1]=vaishnava[self.script]+'~'+get_ekadashi_name(paksha='shukla',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
            if self.lunar_month[d]==4:
              self.festivals[d]+=self.eventSep+chaturmasya_start[self.script]
            if self.lunar_month[d]==8:
              self.festivals[d]+=self.eventSep+chaturmasya_end[self.script]
          else:
            self.festivals[d]=sarva[self.script]+'~'+get_ekadashi_name(paksha='shukla',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
            if self.lunar_month[d]==4:
              self.festivals[d]+=self.eventSep+chaturmasya_start[self.script]
            if self.lunar_month[d]==8:
              self.festivals[d]+=self.eventSep+chaturmasya_end[self.script]
        elif (self.tithi_sunrise[d-1]!=11 and self.tithi_sunrise[d]==12):
          self.festivals[d]=sarva[self.script]+'~'+get_ekadashi_name(paksha='shukla',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
          if self.lunar_month[d]==4:
            self.festivals[d]+=self.eventSep+chaturmasya_start[self.script]
          if self.lunar_month[d]==8:
            self.festivals[d]+=self.eventSep+chaturmasya_end[self.script]
   
      if self.tithi_sunrise[d]==26 or self.tithi_sunrise[d]==27: #One of two consecutive tithis must appear @ sunrise!
        #check for krishna ekadashi
        if (self.tithi_sunrise[d]==26 and self.tithi_sunrise[d+1]==26): 
          self.festivals[d+1]=sarva[self.script]+'~'+get_ekadashi_name(paksha='krishna',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)#lunar_month[d] or [d+1]?
        elif (self.tithi_sunrise[d]==26 and self.tithi_sunrise[d+1]!=26): 
          #Check dashami end time to decide for whether this is sarva/smartha
          tithi_arunodayam = get_tithi(self.jd_sunrise[d]-(1/15.0)*(self.jd_sunrise[d]-self.jd_sunrise[d-1])) #Two muhurtams is 1/15 of day-length
          if tithi_arunodayam==25:
            self.festivals[d]=smartha[self.script]+'~'+get_ekadashi_name(paksha='krishna',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
            self.festivals[d+1]=vaishnava[self.script]+'~'+get_ekadashi_name(paksha='krishna',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
          else:
            self.festivals[d]=sarva[self.script]+'~'+get_ekadashi_name(paksha='krishna',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
        elif (self.tithi_sunrise[d-1]!=26 and self.tithi_sunrise[d]==27):
          self.festivals[d]=sarva[self.script]+'~'+get_ekadashi_name(paksha='krishna',lmonth=self.lunar_month[d],smonth=self.solar_month[d],script=self.script)
  
      #PRADOSHA Vratam
      if self.tithi_sunrise[d]==12 or self.tithi_sunrise[d]==13:
        tithi_sunset = get_tithi(self.jd_sunset[d])
        tithi_sunset_tmrw = get_tithi(self.jd_sunset[d+1])
        if tithi_sunset<=13 and tithi_sunset_tmrw!=13:
          self.festivals[d]=pradosham[self.script]
        elif tithi_sunset_tmrw==13:
          self.festivals[d+1]=pradosham[self.script]
  
      if self.tithi_sunrise[d]==27 or self.tithi_sunrise[d]==28:
        tithi_sunset = get_tithi(self.jd_sunset[d])
        tithi_sunset_tmrw = get_tithi(self.jd_sunset[d+1])
        if tithi_sunset<=28 and tithi_sunset_tmrw!=28:
          self.festivals[d]=pradosham[self.script]
        elif tithi_sunset_tmrw==28:
          self.festivals[d+1]=pradosham[self.script]

      #SANKATAHARA chaturthi
      if self.tithi_sunrise[d]==18 or self.tithi_sunrise[d]==19:
        ldiff_moonrise_yest=(swisseph.calc_ut(self.jd_moonrise[d-1],swisseph.MOON)[0]-swisseph.calc_ut(self.jd_moonrise[d-1],swisseph.SUN)[0])%360
        ldiff_moonrise=(swisseph.calc_ut(self.jd_moonrise[d],swisseph.MOON)[0]-swisseph.calc_ut(self.jd_moonrise[d],swisseph.SUN)[0])%360
        ldiff_moonrise_tmrw=(swisseph.calc_ut(self.jd_moonrise[d+1],swisseph.MOON)[0]-swisseph.calc_ut(self.jd_moonrise[d+1],swisseph.SUN)[0])%360
        tithi_moonrise_yest = int(1+math.floor(ldiff_moonrise_yest/12.0))
        tithi_moonrise = int(1+math.floor(ldiff_moonrise/12.0))
        tithi_moonrise_tmrw = int(1+math.floor(ldiff_moonrise_tmrw/12.0))
  
        if tithi_moonrise==19:
          if tithi_moonrise_yest!=19:#otherwise yesterday would have already been assigned
            self.festivals[d]=chaturthi[self.script] 
            if self.lunar_month[d]==5:#shravana krishna chaturthi
              self.festivals[d]=maha[self.script]+self.festivals[d]
        elif tithi_moonrise_tmrw==19:
            self.festivals[d+1]=chaturthi[self.script] 
            if self.lunar_month[d]==5: #self.lunar_month[d] and[d+1] are same, so checking [d] is enough
              self.festivals[d+1]=maha[self.script]+self.festivals[d+1]
  
      #SHASHTHI Vratam
      if self.tithi_sunrise[d]==5 or self.tithi_sunrise[d]==6:
        if self.tithi_sunrise[d]==6 or (self.tithi_sunrise[d]==5 and self.tithi_sunrise[d+1]==7):
          if self.tithi_sunrise[d-1]!=6:#otherwise yesterday would have already been assigned
            self.festivals[d]=shashthi[self.script] 
            if self.lunar_month[d]==8:#kArtika krishna shashthi
              self.festivals[d]=skanda[self.script]+self.festivals[d]
        elif self.tithi_sunrise[d+1]==6:
            self.festivals[d+1]=shashthi[self.script] 
            if self.lunar_month[d]==8: #self.lunar_month[d] and[d+1] are same, so checking [d] is enough
              self.festivals[d+1]=skanda[self.script]+self.festivals[d+1]
  
      ###--- OTHER (MAJOR) FESTIVALS ---###
      #type of month | month number | type of angam (tithi|nakshatram) | angam number | min_t cut off for considering prev day (without sunrise_angam) as festival date
      festival_rules={
              gauri_tritiya[self.script]:['lunar_month', 1,'tithi',      3, 0,'sunrise',  'purvaviddha'],
             matsya_jayanti[self.script]:['lunar_month', 1,'tithi',      3, 0,'aparahna', 'purvaviddha'],
                 ramanavami[self.script]:['lunar_month', 1,'tithi',      9, 0,'madhyahna','purvaviddha'],
            akshaya_tritiya[self.script]:['lunar_month', 2,'tithi',      3, 0,'sunrise',  'purvaviddha'],
              ganga_saptami[self.script]:['lunar_month', 2,'tithi',      7, 0,'madhyahna','purvaviddha'],
           nrisimha_jayanti[self.script]:['lunar_month', 2,'tithi',     14, 0,'sunset',   'purvaviddha'],
        parashurama_jayanti[self.script]:['lunar_month', 2,'tithi',      3, 0,'madhyahna','purvaviddha'],
           shankara_jayanti[self.script]:['lunar_month', 2,'tithi',      5, 0,'sunrise',  'purvaviddha'],
              kurma_jayanti[self.script]:['lunar_month', 4,'tithi',     15, 0,'saydhna',  'purvaviddha'],
           bahula_chaturthi[self.script]:['lunar_month', 5,'tithi',     19, 0,'saydhna',  'purvaviddha'],
          hayagriva_jayanti[self.script]:['lunar_month', 5,'tithi',     15, 0,'sunrise',  'purvaviddha'],
                janmashtami[self.script]:['lunar_month', 5,'tithi',     23, 0,'nishita',  'paraviddha' ],
             yajur_upakarma[self.script]:['lunar_month', 5,'tithi',     15, 0,'sunrise',  'purvaviddha'],
         ananta_chaturdashi[self.script]:['lunar_month', 6,'tithi',     14, 0,'sunrise',  'purvaviddha'],
          mahalaya_amavasya[self.script]:['lunar_month', 6,'tithi',     30, 0,'sunrise',  'purvaviddha'],
           mahalaya_paksham[self.script]:['lunar_month', 6,'tithi',     16, 0,'sunrise',  'purvaviddha'],
                radhashtami[self.script]:['lunar_month', 6,'tithi',      8, 0,'sunrise',  'purvaviddha'],
             rishi_panchami[self.script]:['lunar_month', 6,'tithi',      5, 0,'sunrise',  'purvaviddha'],
      uma_maheshvara_vratam[self.script]:['lunar_month', 6,'tithi'     ,15, 0,'sunrise',  'purvaviddha'],
             vamana_jayanti[self.script]:['lunar_month', 6,'tithi',     12, 0,'sunrise',  'purvaviddha'],
              varahajayanti[self.script]:['lunar_month', 6,'tithi',      3, 0,'madhyahna','purvaviddha'],
                 vchaturthi[self.script]:['lunar_month', 6,'tithi',      4, 0,'madhyahna','purvaviddha'],
             buddha_jayanti[self.script]:['lunar_month', 7,'tithi',     15, 0,'sunset',   'purvaviddha'],
                   dipavali[self.script]:['lunar_month', 7,'tithi',     29, 0,'sunrise',  'purvaviddha'],
                durgashtami[self.script]:['lunar_month', 7,'tithi',      8, 0,'sunrise',  'purvaviddha'],
           govatsa_dvadashi[self.script]:['lunar_month', 7,'tithi',     27, 0,'madhyahna','purvaviddha'],
             lalitapanchami[self.script]:['lunar_month', 7,'tithi',      5, 0,'sunrise',  'purvaviddha'],
                 mahanavami[self.script]:['lunar_month', 7,'tithi',      9, 0,'sunrise',  'purvaviddha'],
              vijayadashami[self.script]:['lunar_month', 7,'tithi',     10, 0,'sunrise',  'purvaviddha'],
                 gopashtami[self.script]:['lunar_month', 8,'tithi',      8, 0,'madhyahna','purvaviddha'],
               tripurotsava[self.script]:['lunar_month', 8,'tithi',     15, 0,'pradosha', 'purvaviddha'],
              tulasi_vivaha[self.script]:['lunar_month', 8,'tithi',     12, 0,'madhyahna','purvaviddha'],
         dattatreya_jayanti[self.script]:['lunar_month', 9,'tithi',     15, 0,'pradosha', 'purvaviddha'],
            bahula_panchami[self.script]:['lunar_month',10,'tithi',     20, 0,'sunrise',  'purvaviddha'],
           bhishma_dvadashi[self.script]:['lunar_month',11,'tithi',     12, 0,'sunrise',  'purvaviddha'],
              bhishmashtami[self.script]:['lunar_month',11,'tithi',      8, 0,'madhyahna','purvaviddha'],
              ratha_saptami[self.script]:['lunar_month',11,'tithi',      7, 0,'sunrise',  'purvaviddha'],
                 shivaratri[self.script]:['lunar_month',11,'tithi',     29, 0,'nishita',  'paraviddha' ],
             holika_purnima[self.script]:['lunar_month',12,'tithi',     15, 0,'pradosha', 'purvaviddha'],
                rg_upakarma[self.script]:['lunar_month', 5,'nakshatram',22, 0,'sunrise',  'purvaviddha'],
               maha_kartiki[self.script]:['lunar_month', 8,'nakshatram', 3, 0,'pradosha', 'purvaviddha'],
             chitra_purnima[self.script]:['solar_month', 1,'tithi',     15, 0,'sunrise',  'purvaviddha'],
            hanumat_jayanti[self.script]:['solar_month', 9,'tithi',     30, 0,'sunrise',  'purvaviddha'],
               adi_krittika[self.script]:['solar_month', 4,'nakshatram', 3, 0,'sunrise',  'purvaviddha'],
               goda_jayanti[self.script]:['solar_month', 4,'nakshatram',11, 0,'sunrise',  'purvaviddha'],
              sama_upakarma[self.script]:['solar_month', 5,'nakshatram',13, 0,'sunrise',  'purvaviddha'],
            ardra_darshanam[self.script]:['solar_month', 9,'nakshatram', 6, 0,'sunrise',  'purvaviddha'],
           phalguni_uttaram[self.script]:['solar_month',12,'nakshatram',12, 4,'sunrise',  'purvaviddha']}
      
      #debugFestivals=True 
      debugFestivals=False 
      for x in iter(festival_rules.keys()):
        [month_type, month_num, angam_type, angam_num, t_min, kala, priority]=festival_rules[x]
        if (month_type=='lunar_month' and self.lunar_month[d]==month_num) or (month_type=='solar_month' and self.solar_month[d]==month_num):
          if angam_type=='tithi':
            angam_sunrise=self.tithi_sunrise
            get_angam_func=get_tithi
          elif angam_type=='nakshatram':
            angam_sunrise=self.nakshatram_sunrise
            get_angam_func=get_nakshatram
          else:
            print 'Error; unknown string in rule: %s' % (angam_type)    
            return

          fday=None
          if angam_sunrise[d]==angam_num-1 or angam_sunrise[d]==angam_num:
            angams = get_angams_for_kalas(self.jd_sunrise[d],self.jd_sunrise[d+1],self.jd_sunrise[d+2],self.jd_sunset[d],self.jd_sunset[d+1],get_angam_func,kala)
            if debugFestivals is True:
              print '%',x,': ',festival_rules[x]
              print "%angams today & tmrw:",angams
            if priority == 'paraviddha':
              if angams[0]==angam_num or angams[1]==angam_num:
                fday=d
              if angams[2]==angam_num or angams[3]==angam_num:
                fday=d+1
              if fday is None:
                sys.stderr.write('Could not assign paraviddha day for %s! Please check for unusual cases.\n' % x)
            elif priority == 'purvaviddha':
              angams_yest = get_angams_for_kalas(self.jd_sunrise[d-1],self.jd_sunrise[d],self.jd_sunrise[d+1],self.jd_sunset[d-1],self.jd_sunset[d],get_angam_func,kala)
              if debugFestivals is True:
                print "%angams yest & today:",angams_yest
              if angams[0]==angam_num or angams[1]==angam_num:
                if self.festival_day_list.has_key(x):
                  #Check if yesterday was assigned already to this purvaviddha festival!
                  if self.festival_day_list[x].count(d-1)==0:
                    fday=d
                else:
                  fday=d
              elif angams[2]==angam_num or angams[3]==angam_num:
                fday=d+1
              if fday is None:
                '''This means that the correct angam did not touch the kalam on either day!'''
                #sys.stderr.write('Could not assign purvaviddha day for %s! Please check for unusual cases.\n' % x)
                if angams[2]==angam_num+1 or angams[3]==angam_num+1:
                  #Need to assign a day to the festival here since the angam did not touch kalam on either day
                  #BUT ONLY IF YESTERDAY WASN'T ALREADY ASSIGNED, THIS BEING PURVAVIDDHA
                  #Perhaps just need better checking of conditions instead of this fix
                  if self.festival_day_list.has_key(x):
                    if self.festival_day_list[x].count(d-1)==0:
                      fday=d
                  else:
                    fday=d

          if fday is not None:
            if debugFestivals is True:
              print '%',d,':', x, fday
            if self.festival_day_list.has_key(x):
              if self.festival_day_list[x][0]!=fday:
                #Second occurrence of a festival within a Gregorian calendar year
                self.festival_day_list[x]=[self.festival_day_list[x][0],fday]
            else:
              self.festival_day_list[x]=[fday]

      #NAVARATRI START
      if self.lunar_month[d]==7 and self.lunar_month[d-1]==6:
        self.festival_day_list[navaratri_start[self.script]]=[d]
  
      #PONGAL/AYANAM
      if self.solar_month[d]==10 and self.solar_month[d-1]==9:
        self.festival_day_list[uttarayanam[self.script]]=[d]
  
      if self.solar_month[d]==4 and self.solar_month[d-1]==3:
        self.festival_day_list[dakshinayanam[self.script]]=[d]
  
      samvatsara_id = (self.year - 1568)%60 + 1; #distance from prabhava
      new_yr=mesha_sankranti[self.script]+'~('+year_names[self.script][(samvatsara_id%60)+1]+'-'+samvatsara[self.script]+')'

      if self.solar_month[d]==1 and self.solar_month[d-1]==12:
        self.festival_day_list[new_yr]=[d]
  
      if self.lunar_month[d]==1 and self.lunar_month[d-1]!=1:
        self.festival_day_list[yugadi[self.script]]=[d]
  
    #Add saved festivals
    if self.festival_day_list[tripurotsava[self.script]]!=self.festival_day_list[maha_kartiki[self.script]]:
      del self.festival_day_list[maha_kartiki[self.script]]

    self.festival_day_list[gayatri_japam[self.script]]=[self.festival_day_list[yajur_upakarma[self.script]][0]+1]
    self.festival_day_list[varalakshmi_vratam[self.script]]=[self.festival_day_list[yajur_upakarma[self.script]][0]-((self.weekday_start-1+self.festival_day_list[yajur_upakarma[self.script]][0]-5)%7)]
  
    for x in iter(self.festival_day_list.keys()):
      for j in range(0,len(self.festival_day_list[x])):
        if self.festivals[self.festival_day_list[x][j]]!='':
          self.festivals[self.festival_day_list[x][j]]+=self.eventSep
        self.festivals[self.festival_day_list[x][j]]+=x
  
  def computeSolarEclipses(self):
    swisseph.set_topo(lon=self.city.longitude,lat=self.city.latitude,alt=0.0) #Set location
    jd = self.jd_start
    while 1:
      next_eclipse_sol=swisseph.sol_eclipse_when_loc(julday=jd,lon=self.city.longitude,lat=self.city.latitude)
      [y,m,dt,t] = swisseph.revjul(next_eclipse_sol[1][0])
      local_time = pytz.timezone(self.city.timezone).localize(datetime(y, m, dt, 6, 0, 0))
      #checking @ 6am local - can we do any better?
      tz_off=(datetime.utcoffset(local_time).days*86400+datetime.utcoffset(local_time).seconds)/3600.0 
      #compute offset from UTC
      jd=next_eclipse_sol[1][0]+(tz_off/24.0)
      jd_eclipse_solar_start=next_eclipse_sol[1][1]+(tz_off/24.0)
      jd_eclipse_solar_end=next_eclipse_sol[1][4]+(tz_off/24.0)
      eclipse_y=swisseph.revjul(jd-1)[0]# -1 is to not miss an eclipse that occurs after sunset on 31-Dec!
      if eclipse_y!=self.year:
        break
      else:
        #print '%%', fday, (jd_eclipse_solar_start), (jd_eclipse_solar_end), (self.jd_sunrise[fday])
        #print '%%', swisseph.revjul(jd_eclipse_solar_start), swisseph.revjul(jd_eclipse_solar_end), swisseph.revjul(self.jd_sunrise[fday])
        fday=int(math.floor(jd)-math.floor(self.jd_start)+1)
        if (jd<(self.jd_sunrise[fday]+tz_off/24.0)):
          fday-=1
        #print '%%', fday, (jd_eclipse_solar_start), (jd_eclipse_solar_end), (self.jd_sunrise[fday])
        #print '%%', swisseph.revjul(jd_eclipse_solar_start), swisseph.revjul(jd_eclipse_solar_end), swisseph.revjul(self.jd_sunrise[fday])
        eclipse_solar_start = swisseph.revjul(jd_eclipse_solar_start)[3]
        eclipse_solar_end   = swisseph.revjul(jd_eclipse_solar_end)[3]
        if (jd_eclipse_solar_start-(tz_off/24.0))==0.0 or (jd_eclipse_solar_end-(tz_off/24.0))==0.0:# or jd_eclipse_end<self.jd_sunrise[fday] or jd_eclipse_start>self.jd_sunset[fday]:
          jd=jd+20 #Move towards the next eclipse... at least the next new moon (>=25 days away)
          continue
        if eclipse_solar_end < eclipse_solar_start:
          eclipse_solar_end+=24
        sunrise_eclipse_day = swisseph.revjul(self.jd_sunrise[fday])[3]
        sunset_eclipse_day = swisseph.revjul(self.jd_sunset[fday])[3]
        jd_sunrise_eclipse_day = self.jd_sunrise[fday]
        jd_sunset_eclipse_day = self.jd_sunset[fday]
        if jd_eclipse_solar_start<jd_sunrise_eclipse_day:
          eclipse_solar_start=sunrise_eclipse_day
        if jd_eclipse_solar_end>jd_sunset_eclipse_day:
          eclipse_solar_end=sunset_eclipse_day
        solar_eclipse_str = surya_grahanam[self.script]+'~\\textsf{'+time(eclipse_solar_start).toString()+'}{\\RIGHTarrow}\\textsf{'+time(eclipse_solar_end).toString()+'}'
        if self.festivals[fday]!='':
          self.festivals[fday]+=self.eventSep
        self.festivals[fday]+=solar_eclipse_str
      jd=jd+20

  def computeLunarEclipses(self):
    swisseph.set_topo(lon=self.city.longitude,lat=self.city.latitude,alt=0.0) #Set location
    jd = self.jd_start
    while 1:
      next_eclipse_lun=swisseph.lun_eclipse_when(jd)
      [y,m,dt,t] = swisseph.revjul(next_eclipse_lun[1][0])
      local_time = pytz.timezone(self.city.timezone).localize(datetime(y, m, dt, 6, 0, 0))
      #checking @ 6am local - can we do any better? This is crucial, since DST changes before 6 am
      tz_off=(datetime.utcoffset(local_time).days*86400+datetime.utcoffset(local_time).seconds)/3600.0 
      #compute offset from UTC
      jd=next_eclipse_lun[1][0]+(tz_off/24.0)
      jd_eclipse_lunar_start=next_eclipse_lun[1][2]+(tz_off/24.0)
      jd_eclipse_lunar_end=next_eclipse_lun[1][3]+(tz_off/24.0)
      eclipse_y=swisseph.revjul(jd-1)[0]# -1 is to not miss an eclipse that occurs after sunset on 31-Dec!
      if eclipse_y!=self.year:
        break
      else:
        eclipse_lunar_start = swisseph.revjul(jd_eclipse_lunar_start)[3]
        eclipse_lunar_end   = swisseph.revjul(jd_eclipse_lunar_end)[3]
        if (jd_eclipse_lunar_start-(tz_off/24.0))==0.0 or (jd_eclipse_lunar_end-(tz_off/24.0))==0.0:
          jd=jd+20 #Move towards the next eclipse... at least the next full moon (>=25 days away)
          continue
        fday=int(math.floor(jd_eclipse_lunar_start)-math.floor(self.jd_start)+1)
        #print '%%',jd,fday,self.jd_sunrise[fday],self.jd_sunrise[fday-1]
        if (jd<(self.jd_sunrise[fday]+tz_off/24.0)):
          fday-=1
        if eclipse_lunar_start<swisseph.revjul(self.jd_sunrise[fday+1]+tz_off/24.0)[3]:
          eclipse_lunar_start+=24
        #print '%%',jd,fday,self.jd_sunrise[fday],self.jd_sunrise[fday-1],eclipse_lunar_start, eclipse_lunar_end
        jd_moonrise_eclipse_day=swisseph.rise_trans(jd_start=self.jd_sunrise[fday],body=swisseph.MOON,
          lon=self.city.longitude,lat=self.city.latitude,rsmi=swisseph.CALC_RISE|swisseph.BIT_DISC_CENTER)[1][0]+(tz_off/24.0)
        jd_moonset_eclipse_day=swisseph.rise_trans(jd_start=jd_moonrise_eclipse_day,body=swisseph.MOON,
          lon=self.city.longitude,lat=self.city.latitude,rsmi=swisseph.CALC_SET|swisseph.BIT_DISC_CENTER)[1][0]+(tz_off/24.0)
        #if jd_eclipse_lunar_start<(self.jd_sunrise[fday]+(tz_off/24.0)):
        if eclipse_lunar_end < eclipse_lunar_start:
          eclipse_lunar_end+=24
        #print '%%', (jd_eclipse_lunar_start), (jd_eclipse_lunar_end), (jd_moonrise_eclipse_day), (jd_moonset_eclipse_day)
        #print '%%', swisseph.revjul(jd_eclipse_lunar_start), swisseph.revjul(jd_eclipse_lunar_end), swisseph.revjul(jd_moonrise_eclipse_day), swisseph.revjul(jd_moonset_eclipse_day)
        if jd_eclipse_lunar_end<jd_moonrise_eclipse_day or jd_eclipse_lunar_start>jd_moonset_eclipse_day:
          jd=jd+20 #Move towards the next eclipse... at least the next full moon (>=25 days away)
          continue
        moonrise_eclipse_day = swisseph.revjul(jd_moonrise_eclipse_day)[3]
        moonset_eclipse_day = swisseph.revjul(jd_moonset_eclipse_day)[3]
        if jd_eclipse_lunar_start<jd_moonrise_eclipse_day:
          eclipse_lunar_start=moonrise_eclipse_day
        if jd_eclipse_lunar_end>jd_moonset_eclipse_day:
          eclipse_lunar_end=moonset_eclipse_day
        lunar_eclipse_str = chandra_grahanam[self.script]+'~\\textsf{'+time(eclipse_lunar_start).toString()+'}{\\RIGHTarrow}\\textsf{'+time(eclipse_lunar_end).toString()+'}'
        if self.festivals[fday]!='':
          self.festivals[fday]+=self.eventSep
        self.festivals[fday]+=lunar_eclipse_str
      jd=jd+20

  def writeTeX(self,template_file):
    '''Write out the panchangam TeX using a specified template'''
    daycol = {0:'blue',1:'blue',2:'blue',3:'blue',4:'blue',5:'blue',6:'blue'}
    month = {1:'JANUARY', 2:'FEBRUARY', 3:'MARCH', 4:'APRIL', 5:'MAY', 6:'JUNE', 7:'JULY', 8:'AUGUST', 9:'SEPTEMBER', 10:'OCTOBER', 11: 'NOVEMBER', 12:'DECEMBER'}
    MON = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11: 'November', 12:'December'}
    WDAY = {0:'Sun',1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'}

    template_lines=template_file.readlines()
    for i in range(0,len(template_lines)-3):
      print template_lines[i][:-1]

    samvatsara_id = (self.year - 1568)%60 + 1; #distance from prabhava
    samvatsara_names = '%s–%s' % (year_names[self.script][samvatsara_id], 
      year_names[self.script][(samvatsara_id%60)+1])
     
    print '\\mbox{}'
    print '{\\font\\x="Candara" at 60 pt\\x %d\\\\[0.5cm]}' % self.year
    print '\\mbox{\\font\\x="Sanskrit 2003:script=deva" at 48 pt\\x %s}\\\\[0.5cm]' % samvatsara_names
    print '{\\font\\x="Candara" at 48 pt\\x \\uppercase{%s}\\\\[0.2cm]}' % self.city.name
    print '{\\font\\x="Candara" at 16 pt\\x {%s}\\\\[0.5cm]}' % print_lat_lon(self.city.latstr, self.city.lonstr)
    print '\hrule'

    print '\\newpage'
    #print '\\centerline{\\LARGE {{%s}}}\\mbox{}\\\\[2cm]' % list_of_festivals[self.script]
    print '\\centerline{\\LARGE {{%s}}}' % list_of_festivals[self.script]
    print '\\begin{center}'
    print '\\begin{minipage}[t]{0.3\\linewidth}'
    print '\\begin{center}'
    print '\\begin{tabular}{>{\\sffamily}r>{\\sffamily}r>{\\sffamily}cp{6cm}}'

    mlast=1
    for d in range(1,367):
      jd = self.jd_start-1+d
      [y,m,dt,t] = swisseph.revjul(jd)
      weekday = (self.weekday_start -1 + d)%7 
   
      if self.festivals[d]!='':
        if m!=mlast:
          mlast=m
          #print '\\hline\\\\'
          print '\\\\'
          if m==5 or m==9:
            print '\\end{tabular}'
            print '\\end{center}'
            print '\\end{minipage}\hspace{1cm}%'
            print '\\begin{minipage}[t]{0.3\\linewidth}'
            print '\\begin{center}'
            print '\\begin{tabular}{>{\\sffamily}r>{\\sffamily}l>{\\sffamily}cp{6cm}}'
          
        print '%s & %s & %s & {\\raggedright %s} \\\\' % (MON[m],dt,WDAY[weekday],self.festivals[d].replace(self.eventSep,'\\\\'))
 
      if m==12 and dt==31:
        break

    print '\\end{tabular}'
    print '\\end{center}'
    print '\\end{minipage}'
    print '\\end{center}'
    print '\\clearpage'

    for d in range(1,367):
      jd = self.jd_start-1+d
      [y,m,dt,t] = swisseph.revjul(jd)
      weekday = (self.weekday_start -1 + d)%7 

      if dt==1:
        if m>1:
          if weekday!=0: #Space till Sunday
            for i in range(weekday,6):
              print "{}  &"
            print "\\\\ \hline"
          print '\end{tabular}'
          print '\n\n'
  
        #Begin tabular
        print '\\begin{tabular}{|c|c|c|c|c|c|c|}'
        print '\multicolumn{7}{c}{\Large \\bfseries \sffamily %s %s}\\\\[3mm]' % (month[m],y)
        print '\hline'
        print '\\textbf{\\textsf{SUN}} & \\textbf{\\textsf{MON}} & \\textbf{\\textsf{TUE}} & \\textbf{\\textsf{WED}} & \\textbf{\\textsf{THU}} & \\textbf{\\textsf{FRI}} & \\textbf{\\textsf{SAT}} \\\\ \hline'
        #print '\\textbf{भानु} & \\textbf{इन्दु} & \\textbf{भौम} & \\textbf{बुध} & \\textbf{गुरु} & \\textbf{भृगु} & \\textbf{स्थिर} \\\\ \hline'
    
        #Blanks for previous weekdays
        for i in range(0,weekday):
          print "{}  &"

      print '\caldata{\\textcolor{%s}{%s}}{%s{%s}}{\\sundata{%s}{%s}{%s}}{\\tnyk{%s}{%s}{%s}{%s}}{\\rahuyama{%s}{%s}}{%s} ' % (daycol[weekday],
      dt,self.month_data[d],get_chandra_masa(self.lunar_month[d],chandra_masa_names,self.script),self.sunrise[d],self.sunset[d],self.sangava[d],self.tithi_data_string[d],self.nakshatram_data_string[d],self.yogam_data_string[d],self.karanam_data_string[d],self.rahu[d],self.yama[d],self.festivals[d])
  
      if weekday==6:
        print "\\\\ \hline"
      else:
        print "&"
  
      if m==12 and dt==31:
        break
  
      # For debugging specific dates
      #if m==4 and dt==10:
      #  break
  
    for i in range(weekday+1,6):
      print "{}  &"
    if weekday!=6:
      print "\\\\ \hline"
    print '\end{tabular}'
    print '\n\n'
  
    print template_lines[-2][:-1]
    print template_lines[-1][:-1]


  def computeIcsCalendar(self):
    self.ics_calendar = Calendar()
    for d in range(1,367):
      jd = self.jd_start-1+d
      [y,m,dt,t] = swisseph.revjul(jd)
  
      weekday = (self.weekday_start -1 + d)%7 

      if self.festivals[d] != '':
        summary_text=unicode(self.festivals[d],"UTF-8")
        summary_text=summary_text.replace('C','Ch').replace('c','ch')
        #this will work whether we have one or more events on the same day
        for stext in summary_text.split(self.eventSep):
          if not stext.find('graha') == -1:
            #It's a grahanam, with a start and end time
            event = Event()
            [stext,t1,arrow,t2]=summary_text.split('\\')
            event.add('summary',stext.replace('~',' ').strip())
            #we know that t1 is something like 'textsf{14:44}{'
            #so we know that positions of min and hour
            event.add('dtstart',datetime(y,m,dt,int(t1[7:9]),int(t1[10:12]),tzinfo=pytz.timezone(self.city.timezone)))
            event.add('dtend',datetime(y,m,dt,int(t2[7:9]),int(t2[10:12]),tzinfo=pytz.timezone(self.city.timezone)))
            self.ics_calendar.add_component(event)
          else:
            event = Event()
            event.add('summary',stext.replace('~',' '))
            event.add('dtstart',datetime(y,m,dt,tzinfo=pytz.timezone(self.city.timezone)))
            event.add('dtend',datetime(y,m,dt,tzinfo=pytz.timezone(self.city.timezone)))
            event['X-MICROSOFT-CDO-ALLDAYEVENT'] = 'TRUE'
            #event.add('dtend',datetime(y,m,dt,tzinfo=pytz.timezone(self.city.timezone))+timedelta(days=1))
            #though ugly, the above seems the only way to create an all day event
            self.ics_calendar.add_component(event)

      if m==12 and dt==31:
        break

  def writeIcsCalendar(self,fname):
    if fname is None:
      fname = '%s-%4d.ics' % (self.city.name,self.year)
    ics_calendar_file = open(fname,'w')
    ics_calendar_file.write(self.ics_calendar.to_ical())
    ics_calendar_file.close()

  def writeDebugLog(self):
    log_file=open('cal_log_%4d.txt' % self.year,'w')
    for d in range(1,367):
      jd = self.jd_start-1+d
      [y,m,dt,t] = swisseph.revjul(jd)
      longitude_sun_sunset  = swisseph.calc_ut(self.jd_sunset[d], swisseph.SUN )[0]-swisseph.get_ayanamsa(self.jd_sunset[d])
      log_data = '%02d-%02d-%4d\t[%3d]\tsun_rashi=%8.3f\ttithi=%8.3f\tsolar_month\
        =%2d\tlunar_month=%4.1f\n' % (dt,m,y,d,(longitude_sun_sunset%360)/30.0,
        get_angam_float(self.jd_sunrise[d],12.0,[1,-1]),self.solar_month[d],self.lunar_month[d])
      log_file.write(log_data)
