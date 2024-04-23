import pandas as pd
import funcion_l as lik
from scipy.optimize import differential_evolution
import numpy as np
import time

#masa = 10**x_[0]
#data['MAp'] = 4*masa
#data['Mchi1'] = masa
#data['gX'] = x_[1]
#data['epsilon'] = 10**x_[2]
#data['ff'] = x_[3]

def diccionario(x_):
	data = {'MAp':3., 'mphi':1,'Mchi1':0.1,'angle':1e-3,'gX':0.1182,'epsilon':0.1,'ff':0.10}
	data['MAp'] = 10**x_[0] #Logaritmico
	data['mphi'] = 10**x_[1] #Logaritmico
	data['Mchi1'] = 10**x_[2] #Logaritmico
	#data['Mchi1'] = x_[2] #Lineal
	data['gX'] = 10**x_[3] #Logaritmico
	data['epsilon'] = 10**x_[4] #Logaritmico
	data['ff'] = 10**x_[5] #lineal
	return data

def de_scan(bounds,nombre_ = 'datos.csv'):
	x = [] 
	def objective(x_):
		ob = lik.Likelihood(diccionario(x_))
		datos = ob.get_datos()
		#print(datos)
		x.append(datos)
		#print(x)
		if (len(x)%100 == 0): 
			print(len(x),end='\r')
		return ob.get_gaussian()

	differential_evolution(objective, bounds,
                           strategy='best1bin', maxiter=None,
                           popsize=50, tol=0.01, mutation=(0.7, 1.99999), recombination=0.15,
                           polish=False, seed=seed)
	try:
		df = pd.DataFrame(x)
		print("Los elementos del dataframe son:")
		df.to_csv(nombre_, index=False, header=True)
		print(df.head())
		print("El tamaño de los datos es:",len(df))
		print("Datos almacenados con exito")
	except:
		print("Los datos del dataframe no han podido ser almacenados")

	return np.array(x),len(x)

if __name__ == '__main__': 
	#Rango espacio de parámetros
	gX_min = -4
	gX_max = 0.4
	epsilon_min = -6
	epsilon_max = 0
	Mchi1_min = -3
	Mchi1_max = 2
	MAp_min = -3
	MAp_max = 2
	Mphi_min = -3
	Mphi_max = 2
	ff_min = -4
	ff_max = 0.4
	seed = 16
	bounds = [(MAp_min,MAp_max),(Mphi_min,Mphi_max),(Mchi1_min,Mchi1_max),(gX_min,gX_max),(epsilon_min,epsilon_max),(ff_min,ff_max)]
	#bounds = [(Mchi1_min,Mchi1_max),(gX_min,gX_max),(epsilon_min,epsilon_max),(ff_min,ff_max)]
	np.random.seed(seed)
	print("Running de_scan") 
	tO = time.time()
	x,call = de_scan(bounds,nombre_='datos_varios_varA-1.csv')
	de_time = time.time() - tO 
	de_time = de_time/60
	print("Tiempo de ejecución: ", de_time, " minutos")
	print("Cantidad de datos generados: ", call)
	print("Finalizado")