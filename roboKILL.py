import nengo
import numpy as np
import nengo_spa
import ev3_nengo.ev3link
import bluetooth
import time

if not hasattr(ev3_nengo, 'link'):
    ev3_nengo.link = ev3_nengo.ev3link.EV3Link('10.0.0.3')
link = ev3_nengo.link

print(link.dir('/sys/class/tacho-motor'))

for i in range(0,3):
    link.write('/sys/class/tacho-motor/motor%d/speed_sp' % i, '0')
    link.write('/sys/class/tacho-motor/motor%d/command' % i, 'run-forever')

