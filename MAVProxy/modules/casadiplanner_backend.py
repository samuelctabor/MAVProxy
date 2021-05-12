import casadi
import numpy
import scipy.io as sio

def plan():  #current_position, est_thermal_position, roll, heading):
    
	
	maxU    = numpy.deg2rad(8)
	maxRoll = numpy.deg2rad(40)
	xInit = (0,0)
	phiInit = numpy.deg2rad(45)

	init_sol = sio.loadmat('/home/samuel/SoaringStudies/OCP/CasADi/InitialSolution.mat')
	func = casadi.Function.load('/home/samuel/SoaringStudies/OCP/CasADi/OptimalSoaringFunc')
	#func = casadi.Function.load('/home/samuel/SoaringStudies/OCP/CasADi/test_func.casadifunc')

	print("maxU %f maxRoll %f xInit %f %f phiInit %f" % (maxU, maxRoll, xInit[0], xInit[1], phiInit))

	result = func(maxRoll, maxU, xInit, phiInit, init_sol['U'], init_sol['X'])

	return result

