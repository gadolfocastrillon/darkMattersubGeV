import subprocess
import pandas as pd

class DensidadReliquia:
	def __init__(self,data_):
		self.data = data_ 
		self.ruta = 'data.dat'
		self.rutaG = './main data.dat >temporal.dat'
		self.calc() 
		self.omega = self.calc_omega()
		self.mchi2 = self.find_mx2()
		self.diccionario2 = {'Mchi2':self.mchi2, 'Densidad_reliquia':self.omega}

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

	def __str__(self):
		texto=f'Los resultados son'
		for clave, valor in self.data.items():
			texto += '\n'
			texto+=f"{clave} = {valor}"
		return texto

	def get_datos(self):
		diccionario1 = self.data.copy()
		diccionario1.update(self.diccionario2)
		return diccionario1

if __name__ == '__main__':
	data1 = {'MAp':3., 'mphi':0.1,'Mchi1':0.1,'angle':1e-3,'gX':0.1,'epsilon':1e-4,'ff':1e-1}
	ob1 = DensidadReliquia(data1)
	obj = [] 
	obj.append(ob1.get_datos())
	print(obj)