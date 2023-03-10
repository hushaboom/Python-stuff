#!/usr/bin/python3

from subprocess import check_output, run
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from time import sleep
import os

def coreTemp():
     
     outp = []
     retStr = str()
     outstr = "sensors | grep 'Core'"
     outA = check_output(outstr,shell=True).decode().strip().split('\n')
     for i in outA:
          outp.append(i)
     for i in outp:
          retStr += ' '.join(i.split()[:3])+'\n'
     return retStr

def sysInfo():
     
     outstr = 'ps -exo pid,cmd,%mem,%cpu --sort=-%cpu | head'
     outp = check_output(outstr, shell=True).decode()
     return outp

def cpuCounter():

        n = 0
        cpu = check_output(['lscpu']).decode('utf-8').split('CPU(s)')[1].strip(' /nb:On-line')
        count = (0,int(cpu))
        return count

def freqOut(cpuRange=(0,0)):
    
    freqs = {}

    for i in range(cpuRange[0], cpuRange[1]):
        strn = '/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq'%i
        fn = float(check_output(["cat", strn]).decode('utf-8').strip(' /nb'))
        freqs['CPU%d'%i] = fn/1000

    return freqs

def memGrab():
        
    p = check_output(["free"]).decode('utf-8').split('Mem:')[1].split('Swap:')[0].strip().split()
    pout = p[1:3]
    pout.append(p[4])

    used,free,cache = pout[0],pout[1],pout[2]
    strn = ' Used: %.2f' % ((float(used)/float(p[0]))*100)
    stfree = ' Free: %.2f' % (float(free)/float(p[0])*100)
    cacfree = 'Cache: %.2f' % ((float(cache)/float(p[0]))*100)
    return strn,stfree,cacfree,(pout[0],pout[1],pout[2])

def utc():
          
     up = check_output(['uptime']).decode().strip().split()
     nowTime = str(up[0])[:-3]
     upTime = str(up[2])
     avgLoad = ' '.join(up[-3:])
     outp = 'Time: %s  Up: %s  Load Avg: %s'%(nowTime,upTime,avgLoad)
     return outp

def hdd():

     outhdd = []

     strn = 'iostat -p sda | head'
     stats = check_output(strn, shell=True).decode().split('\n')
     outKernel = stats[0].replace('\t', '')
     outLoad = '%.2f'%(float(stats[3].strip().split()[0]))
     
     for i in stats[6:-1]:
          outhdd.append(' '.join(i.strip().split()))
     
     hddstr = '\n'.join(outhdd)
     return outKernel,outLoad,hddstr,stats

def freqMax():
     strn = 'lscpu | grep "CPU max MHz" | tail'
     outp = float(check_output(strn,shell=True).decode().strip().split(':')[1].strip())
     return int(outp)

def driveStr ():
     dHold = []
     ldHold = []
     drHold = []

     for i in hdd()[3][1:]:
          dHold.append([i.split()])

     for i in dHold:
          if len(i[0]) == 7:
               i = i[0][1:]
               ldHold.append(i)
          if len(i[0]) == 6:
               ldHold.append([e.strip() for e in i[0]])
          if len(i[0]) == 8:
               drHold.append([e.strip() for e in i[0]])
          else:
               pass

     ldStr = str()
     drStr = str()

     for i in ldHold:
          ldStr += '{0:<8} {1:<8} {2:<8} {3:<8} {4:<8} {5:<8}\n'.format(*i)

     for i in (drHold[0], drHold[1], drHold[-1]):
          drStr += '{0:<8} {1:<8} {2:<10} {3:<10} {5:<10} {6:<10}\n'.format(*i)

     return ldStr,drStr

def dumpMem():
     rstr = 'sysctl vm.drop_caches=1'
     os.environ ['DISPLAY'] = ':0'
     os.environ ['XAUTHORITY'] = '/home/your_user/.Xauthority'
     run(rstr, shell=True)