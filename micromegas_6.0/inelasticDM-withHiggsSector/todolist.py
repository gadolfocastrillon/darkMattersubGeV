import numpy as np 


chi_min = 0.01
chi_max = 0.02
deltan = 0.01

data1 = {'MAp':3., 'mphi':0.1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
data2 = {'MAp':3., 'mphi':1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
data3 = {'MAp':3., 'mphi':20,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}


for i in np.arange(chi_min,chi_max,deltan):
	rangos = [0.1*i,1*i,2*i,4*i]
	for j in rangos: 
		data1['MAp'] = j
		data2['MAp'] = j 
		data3['MAp'] = j
		print("Data 1")
		print(data1)
		print("Data 2")
		print(data2)
		print("Data 3")
		print(data3)
	
