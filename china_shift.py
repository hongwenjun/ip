# load dynamic C library for map shift
from ctypes import *
shift = cdll.LoadLibrary('./china_shift.so')

class Location(Structure):
    _fields_ = [
        ('lon', c_double),
        ('lat', c_double)]

shift.transformFromWGSToGCJ.argtypes = [Location]
shift.transformFromWGSToGCJ.restype = Location
shift.transformFromGCJToWGS.argtypes = [Location]
shift.transformFromGCJToWGS.restype = Location

shift.bd_encrypt.argtypes = [Location]
shift.bd_encrypt.restype = Location
shift.bd_decrypt.argtypes = [Location]
shift.bd_decrypt.restype = Location

def test_china_shift():
	# Location gps = { 119.465265, 29.1934702}; 
	# 地球WGS-84 转 火星GCJ-02 转 百度BD-09
	
	loc = Location(lon = 119.465265, lat = 29.1934702)
	print("地球WGS-84:",loc.lat, loc.lon)
	
	loc = shift.transformFromWGSToGCJ(loc)
	print("火星GCJ-02:",loc.lat, loc.lon)
	
	loc = shift.bd_encrypt(loc)
	print("百度 BD-09:",loc.lat, loc.lon)
	
	# 百度BD-09 转 火星GCJ-02 转 地球WGS-84
	loc = Location(lon = 119.476936, lat = 29.196518 )
	print("百度 BD-09:",loc.lat, loc.lon)
	
	loc = shift.bd_decrypt(loc)
	print("火星GCJ-02:",loc.lat, loc.lon)
	
	loc = shift.transformFromGCJToWGS(loc)
	print("地球WGS-84:",loc.lat, loc.lon)

if __name__ == '__main__':
	test_china_shift()

