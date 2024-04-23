import numpy as np 
import obtencion as ob 
import matplotlib.pyplot as plt 
import pandas as pd

chi_min = 0.01
chi_max = 10
deltan = 0.01

def todolist1():
	global chi_min, chi_max, deltan

	data1 = {'MAp':3., 'mphi':0.1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
	data2 = {'MAp':3., 'mphi':1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
	data3 = {'MAp':3., 'mphi':20,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
	data4 = {'MAp':0.1, 'mphi':1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
	data5 = {'MAp':1, 'mphi':1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
	data6 = {'MAp':20, 'mphi':1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
	datos1 = []
	datos2 = []
	datos3 = []
	datos4 = []
	datos5 = []
	datos6 = []

	k = 0
	for i in np.arange(chi_min,chi_max,deltan):
		data1['Mchi1'] = i
		data2['Mchi1'] = i
		data3['Mchi1'] = i
		data4['Mchi1'] = i
		data5['Mchi1'] = i
		data6['Mchi1'] = i
		rangos = [0.1*i,1*i,2*i,4*i]

		for j in rangos: 
			data1['MAp'] = j
			data2['MAp'] = j 
			data3['MAp'] = j
			data4['mphi'] = j
			data5['mphi'] = j 
			data6['mphi'] = j
			ob1 = ob.DensidadReliquia(data1)
			ob2 = ob.DensidadReliquia(data2)
			ob3 = ob.DensidadReliquia(data3)
			ob4 = ob.DensidadReliquia(data4)
			ob5 = ob.DensidadReliquia(data5)
			ob6 = ob.DensidadReliquia(data6)
			
			datos1.append(ob1.get_datos())
			datos2.append(ob2.get_datos())
			datos3.append(ob3.get_datos())
			datos4.append(ob4.get_datos())
			datos5.append(ob5.get_datos())
			datos6.append(ob6.get_datos())
			#print("Data 1")
			#print(data1)
			#print("Data 2")
			#print(data2)
			#print("Data 3")
		k+=1
		if(k%10 == 0): 
			print(k)
	info1 = pd.DataFrame(datos1)
	info2 = pd.DataFrame(datos2)
	info3 = pd.DataFrame(datos3)
	info4 = pd.DataFrame(datos4)
	info5 = pd.DataFrame(datos5)
	info6 = pd.DataFrame(datos6)
	info1.to_csv('doc/info1.csv')
	info2.to_csv('doc/info2.csv')
	info3.to_csv('doc/info3.csv')
	info4.to_csv('doc/info4.csv')
	info5.to_csv('doc/info5.csv')
	info6.to_csv('doc/info6.csv')

if __name__ == '__main__':
	print("Runing")
	todolist1()
