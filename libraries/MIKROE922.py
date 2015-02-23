"""
 MikroE-922 - v0.0
 Copyright 2015 Erik Fargas
 A library for PyBBIO to interface with MCP3204 chip
 ADC 12-bits via SPI
"""

from bbio import *

class MIKROE922:
        def __init__(self, spi_channel=0):
                self.spi_channel = spi_channel
                self.conn = SPI(0, spi_channel)
                self.conn.max_speed_hz = 1000000 # 1MHz
 
        def __del__( self ):
                self.close
 
        def close(self):
                if self.conn != None:
                        SPI(self.spi_channel).end()
                        self.conn = None
 
        def bitstring(self, n):
                s = bin(n)[2:]
                return '0'*(8-len(s)) + s
 
        def read(self, adc_channel=0):
                # build command
                cmd  = 128 # start bit
                cmd +=  64 # single end / diff
                if adc_channel % 2 == 1:
                        cmd += 8
                if (adc_channel/2) % 2 == 1:
                        cmd += 16
                if (adc_channel/4) % 2 == 1:
                        cmd += 32
 
                # send & receive data
                reply_bytes = self.conn.transfer(0,[cmd, 0, 0, 0])
 
                #
                reply_bitstring = ''.join(self.bitstring(n) for n in reply_bytes)
                # print reply_bitstring
 
                # see also... http://akizukidenshi.com/download/MCP3204.pdf (page.20)
                reply = reply_bitstring[5:17]
                return int(reply, 2)
 
if __name__ == '__main__':
        ADC = MIKROE922(0)
        SPI(ADC.spi_channel).begin()
        SPI(ADC.spi_channel).setMaxFreq(0,ADC.conn.max_speed_hz)

 
        count = 0
        a0 = 0
        a1 = 0
        a2 = 0
        a3 = 0
 
        while True:
                count += 1
                a0 += ADC.read(0)
                a1 += ADC.read(1)
                a2 += ADC.read(2)
                a3 += ADC.read(3)
 
                if count == 10:
                        print "ch0=%04d, ch1=%04d, ch2=%04d, ch3=%04d" % (a0/10, a1/10, a2/10, a3/10)
                        count = 0
                        a0 = 0
                        a1 = 0
                        a2 = 0
                        a3 = 0
