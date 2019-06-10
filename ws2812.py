NumpyImported=False
try:
    import numpy
    from numpy import sin, cos, pi
    NumpyImported=True
except ImportError:
    pass
"""
T0H: 0.35   -> 2p=0.31  3p=0.47
T0L: 0.80   -> 6p=0.94  5p=0.78
T1H: 0.70   -> 4p=0.625 5p=0.78
T1L: 0.60   -> 4p=0.625 3p=0.47
"""
def write2812_numpy4(spi,data):
    d=numpy.array(data).ravel()
    tx=numpy.zeros(len(d)*4, dtype=numpy.uint8)
    for ibit in range(4):
        tx[3-ibit::4]=((d>>(2*ibit+1))&1)*0x60 + ((d>>(2*ibit+0))&1)*0x06 +  0x88
    spi.xfer(tx.tolist(), int(4/1.25e-6)) #works, on Zero (initially didn't?)

def write2812_pylist4(spi, data):
    tx=[]
    for rgb in data:
        for byte in rgb: 
            for ibit in range(3,-1,-1):
                tx.append(((byte>>(2*ibit+1))&1)*0x60 +
                          ((byte>>(2*ibit+0))&1)*0x06 +
                          0x88)
    spi.xfer(tx, int(4/1.05e-6))

if NumpyImported:
    write2812=write2812_numpy4
else:
    write2812=write2812_pylist4    