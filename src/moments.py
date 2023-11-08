#
# moments
#
#import numpy as np
import math

class MOMENTS:
	def __init__( self ):
		self.values = []	#an array of random variables
		self.values2 = []	#an array of squares of random variables
		self.values3 = []	#an array of cubes of random variables
		self.values4 = []	#an array of (random variable)^4
		
		self.size = 0.0		# size of the valuesX lists
		
		self.avg = 0.0		# average
		self.var = 0.0		# variance
		self.std = 0.0		# standard deviation
		self.stdErr = 0.0	# standard error
		self.skew = 0.0		# skewness
		self.kurt = 0.0		# kurtosis
		
	def PushBack(self, x):
		self.values.append(x)
		self.values2.append(x**2)
		self.values3.append(x**3)
		self.values4.append(x**4)
		
	def Calculate(self):
		self.size = len(self.values) # all valuesX lists should have same length
		x_avg = sum(self.values)/self.size
		x2_avg = sum(self.values2)/self.size
		x3_avg = sum(self.values3)/self.size
		x4_avg = sum(self.values4)/self.size
		
		self.avg = x_avg
		self.var = x2_avg - x_avg**2
		self.std = math.sqrt(self.var)
		self.stdErr = self.std/math.sqrt(self.size)
		self.skew = (x3_avg - 3.0*x_avg*self.var - x_avg**3)/(self.std**3)
		self.kurt = (x4_avg - 4.0*x3_avg*x_avg + 6.0*x2_avg*x_avg**2 - 3.0*x_avg**4)/(self.var**2) - 3.0
