#import numpy as np 
import subprocess 
#from scipy.optimize import differential_evolution
#from scipy.stats import chi2
#import matplotlib.pyplot as plt
import pandas as pd 
#import time


class Likelihood: 
	def __init__(self,data_):
		self.data = data_
		self.ruta = 'data.dat'
		self.rutaG = './main data.dat >temporal.dat'
		self.calc()
		self.omega = self.calc_omega()
		self.mchi2 = self.find_mx2()
		self.like_omega = self.l_omega()
		self.log_like = self.gaussian()
		self.diccionario2 = {'Mchi2':self.mchi2, 'Densidad reliquia':self.omega,'loglikelihood':self.log_like}
		self.data.update(self.diccionario2)

	def writer(self,file,dictionary):
		data1=open(file,'w')
		for items in dictionary.items(): 
			data1.write("%s %s\n"%items)
		data1.close()

	def calc(self): 
	    self.writer(self.ruta,self.data) 
	    subprocess.getoutput(self.rutaG)

	def find_command(self,COMMAND):
		const = 0.0 
		dato = subprocess.getoutput(COMMAND)
		if(len(dato)>0):
			const = float(dato)
		else: 
			const = -1 
		return const

	def find_mx2(self):
	    COMMAND_MCHI2 = "grep 'Mchi1' temporal.dat | awk 'BEGIN{FS=\" \"};{print $11}' "
	    return self.find_command(COMMAND_MCHI2)

	def calc_omega(self):
		COMMAND_RQ = "grep 'Omega' temporal.dat | awk 'BEGIN{FS=\"=\"};{print $3}'"
		return self.find_command(COMMAND_RQ)

	def l_omega(self):
		omega_th = self.omega
		omega_ex = 0.12
		delta_omega_pdg = ((0.1*omega_th)**2 + 0.001*2)**0.5
		return (omega_th - omega_ex)**2 / delta_omega_pdg**2

	def gaussian(self): 
		return self.l_omega()

	def __str__(self):
		texto=f'Los resultados son'
		for clave, valor in self.data.items():
			texto += '\n'
			texto+=f"{clave} = {valor}"
		return texto

	def get_gaussian(self):
		return self.log_like

	def get_datos(self):
		return self.data 

if __name__ == '__main__':
	x = [-0.9,1.12,-2,0.01]
	ob1 = Likelihood(diccionario(x))
	#print(ob1)
	obj = [] 
	obj.append(ob1.get_datos())
	print(pd.DataFrame(obj))
	print(ob1.get_gaussian())