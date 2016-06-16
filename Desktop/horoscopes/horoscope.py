#Untested on mac


from select import select
import sys
from msvcrt import getch, kbhit, putch
from urllib2 import urlopen
import time
import re
from platform import system

def leap(y):
    if y%400==0:
        return True
    elif y%100==0:
        return False
    elif y%4==0:
        return True
    else:
        return False

def check_dob(a):
    n = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if len(a)!=10:
        return -1
    c = 0
    for i in a:
        if i not in n:
            c+=1
    if c!=2:
        return -1
    try:
        m = int(a[0:2])
        d = int(a[3:5])
        y = int(a[6:])
    except:
        return -3
    if m<=0 or d<=0 or y<=0:
        return -1
    t = time.localtime()
    if '0'*(2-len(str(m)))+str(m)+a[2]+'0'*(2-len(str(d)))+str(d)+a[5]+str(y)!=a:
        return -4
    elif d>31:
        return -1
    elif m>12:
        return -1
    elif m>7 and m%2==1 and d==31:
        return -1
    elif m<7 and m%2==0 and d==31:
        return -1
    elif m==2:
        if d==30:
            return -1
        elif d==29:
            if not leap(y):
                return -1
    if y>t.tm_year:
        return -2
    elif y==t.tm_year:
        if m>t.tm_mon:
            return -2
        elif m==t.tm_mon:
            if d>t.tm_mday:
                return -2
            elif d==t.tm_mday:
                return 2
    elif m==t.tm_mon and d==t.tm_mday:
        return 3
    else:
        return 1

def convert(a):
    return a[0:2]+a[3:5]

def sign(dob):
    d = int(dob[:4])
    if d>=120 and d<=218:
        return 'Aquarius'
    elif d>=219 and d<=320:
        return 'Pisces'
    elif d>=321 and d<=419:
        return 'Aries'
    elif d>=420 and d<=520:
        return 'Taurus'
    elif d>=521 and d<=620:
        return 'Gemini'
    elif d>=621 and d<=722:
        return 'Cancer'
    elif d>=723 and d<=822:
        return 'Leo'
    elif d>=823 and d<=922:
        return 'Virgo'
    elif d>=923 and d<=1022:
        return 'Libra'
    elif d>=1023 and d<=1121:
        return 'Scorpio'
    elif d>=1122 and d<=1221:
        return 'Sagittarius'
    else:
        return 'Capricorn'

def fetch(dob, d):
    if d!='daily':
        d+='-horoscope'
    else:
        d+='horoscope-feed'
    try:
        s = urlopen('http://www.findyourfate.com/rss/'+d+'.asp?sign='+sign(dob)).read()
    except:
        return 'Can\'t connect to the page! Maybe the site changed, or maybe the wifi password changed.'
    s = '~~~~~~'.join(s.split('\n'))
    l = re.findall('</title><description>.*</description>', s)[0][21:-14]
    if d[:5]=='daily':
        l = re.findall('</title><description>.*', l)[0][21:]
    l = '\n'.join(l.strip('~~~~~~').split('~~~~~~'))
    return l+'\n\n'

while True:
    print 'Hello!\nHow are you on this fine day?\nWell no need to inconvenience yourself.\nRather, let US tell you how you are.\n\n'
    while True:
        print 'Please enter your DOB in MM/DD/YYYY format'
        a = raw_input()
        c = check_dob(a)
        if c==-1:
            print 'Please enter a valid date.'
        elif c==-2:
            print "Oh! A time traveller! Well we don't really have anything for you right now. Perhaps you'd like to wait till our next update? *snicker*"
        elif c==-3:
            print "Perhaps your date separator is longer than a single character. It shouldn't be."
        elif c==-4:
            print 'Definitely strange! I swear I had the date right!'
        elif c==3:
            print 'Happy birthday, dear user!'
            break
        elif c==2:
            print 'Just born? Wish you a happy life, little one!'
            break
        elif c==1:
            break
    dob=convert(a)
    print '\nYour sign is', sign(dob)
    print '\nYour Yearly horoscope is:\n', fetch(dob, 'yearly')
    print '\nYour monthly horoscope is:\n', fetch(dob, 'monthly')
    print '\nYour weekly horoscope is:\n', fetch(dob, 'weekly')
    print "\nYour today's horoscope is:\n", fetch(dob, 'daily')
    time.sleep(1)
    print 'What? Not your horoscope? Perhaps the date of birth is wrong. Wanna enter another? Or perhaps you\'d rather like to exit?'
    if system()!='Windows':
        print '(enter Y to agree)'
    d = time.localtime().tm_mday
    tim = time.localtime()
    while True:
        tim = time.localtime()
        if system()=='Windows':
            answer=raw_input("Do you want to refresh? If the horoscope hasn't changed, it won't be displayed.(R)\nOr maybe change the dob, or exit?(C for both)")
            if answer.upper()=='R':
                pass
            elif answer.upper()=='C':
                break
        else:
            i, o, e = select([sys.stdin],[],[],500)
            if i.upper()=='Y':
                break
        print 'Here!'
        if tim.tm_mday!=time.localtime().tm_mday:
            print '\n\nGood Morning!!!\n'
            if str(tim.tm_mon)+str(tim.mday)==dob:
                print 'Happy birthday!!!\n'
            if tim.tm_year!=time.localtime().tm_year:
                print "\nHappy new year!! Your horoscope for this year is:"
                print fetch(dob, 'yearly')
            if tim.tm_mon!=time.localtime().tm_mon:
                print "\nHere's your horoscope for the month:"
                print fetch(dob, 'monthly')
            if time.localtime().tm_wday==0:
                print '\nWeekly horoscope delivery!!'
                print fetch(dob, 'weekly')
                d = time.localtime().tm_mday
            if tim.tm_mday!=time.localtime().tm_mday:
                print "\nToday's horoscope says:"
                print fetch(dob, 'daily')
                print 'What? Not your horoscope? Perhaps the date of birth is wrong. Wanna enter another? Or perhaps you\'d rather exit?'
                if system()!='Windows':
                    print '(enter Y to agree)'
    if raw_input('Exit? (Y/N)').lower().strip()=='y':
        break
