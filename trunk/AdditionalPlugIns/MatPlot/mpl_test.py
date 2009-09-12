#
# This example is from the original matplotlib distribution.
# Press CTRL-J in the TextEditor window to execute it.
#

from pylab import *

dt = 0.01
t = arange(0,10,dt)
nse = randn(len(t))
r = exp(-t/0.05)

cnse = convolve(nse, r)*dt
cnse = cnse[:len(t)]
s = 0.1*sin(2*pi*t) + cnse

subplot(211)
plot(t,s)
subplot(212)
psd(s, 512, 1/dt)

show()