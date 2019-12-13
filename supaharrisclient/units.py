import numpy
import astropy.units as u


def arcmin2parsec(arcmin, distance_kpc):
    """ """
    radian = (arcmin*u.arcmin).to(u.rad)
    parsec = numpy.tan(radian) * distance_kpc*1000
    return parsec


def parsec2arcmin(parsec, distance_kpc):
    """ """
    radian = numpy.arctan2(parsec, distance_kpc*1000)
    arcmin = (radian*u.rad).to(u.arcmin).value
    return arcmin
