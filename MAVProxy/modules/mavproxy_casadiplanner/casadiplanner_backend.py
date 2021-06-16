import casadi
import numpy
import scipy.io as sio
import time

class CasadiPlannerBackend:
	
	def __init__(self, init_sol_fname, func_fname):

		self.maxU    = numpy.deg2rad(8)
		self.maxRoll = numpy.deg2rad(40)
		self.xInit = (0,0)
		self.phiInit = numpy.deg2rad(45)

		

		self.init_sol = sio.loadmat(init_sol_fname)
		self.func = casadi.Function.load(func_fname)

		print("maxU %f maxRoll %f xInit %f %f phiInit %f" % (self.maxU, self.maxRoll, self.xInit[0], self.xInit[1], self.phiInit))


	def plan(self):  #current_position, est_thermal_position, roll, heading):
		
		start = time.time()    
		result = self.func(self.maxRoll, self.maxU, self.xInit, self.phiInit, self.init_sol['U'], self.init_sol['X'])

		print('Time taken: {}'.format(time.time() - start))
		
		return result

