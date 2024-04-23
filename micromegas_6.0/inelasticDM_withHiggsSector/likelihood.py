import numpy as np 
import subprocess 
from scipy.optimize import differential_evolution
from scipy.stats import chi2
import matplotlib.pyplot as plt 
import pandas as pd 
import time


sltns = 0 
min_chi_sq = 0. 
alpha = 0.05 
critical_chi_sq = chi2.isf(alpha,2) 

#Ligaduras del sistema
'''
Los parámetros del modelo son: 
Map: Masa del fotón oscuro
mphi: Masa del Higgs oscuro
Mchi1: Masa de chi, candidato a materia oscura 
cabi: Ángulo de mezcla. 
aS: Constante parecida a la electromagnetica.
epsilon: Interacción foton con SM. 
'''
'''
Ligaduras del sistema 
epsilon y cabi son pequeños menores a sqrt(4pi)
Mphi**2 menor o igual a (1/(4*sqrt(pi)aS*)*Map**2
Mchi1 < mphi < Map
'''
'''
MAp = 4mphi
Mchi1 = 1 #GeV
cabi = 1e-5 
aS = 0.1
La idea es variar los valores de epsilon y Map
'''
#Vamos a usar la escala logaritmica.
epsilon_min = -6
epsilon_max = -1
Mchi1_min = -2
Mchi1_max = 1 

seed = 16

def writer(file,dictionary):
    data1=open(file,'w')
    for items in dictionary.items(): 
        data1.write("%s %s\n"%items)
    data1.close()

def eje(COMMAND): 
    const = 0.0 
    dato = subprocess.getoutput(COMMAND)
    if(len(dato)>0):
        const = float(dato)
    else: 
        const = -1 
    return const

def calc(x_): 
    ruta = 'data.dat'
    rutaG = './main data.dat >temporal.dat'
    #COMMAND_RQ = "grep 'Omega' temporal.dat | awk 'BEGIN{FS=\"=\"};{print $3}'"
    COMMAND_RQ = "grep 'Omega' temporal.dat | awk 'BEGIN{FS=\"=\"};{print $3}'"
    #COMMAND_CS = "grep 'proton  SI' temporal.dat | awk '{print $3}'"
    data = {'MAp':3., 'mphi':1,'Mchi1':0.1,'angle':1e-5,'gX':0.1182,'epsilon':0.1,'ff':0.10}
    #ligaduras: 
    #x_[0] va a ser la masa de Mchi1
    #Masa de Higgs oscuro igual a 1. 
    #Masa de chi1 será variada.
    #Valor del ángulo igual a 1e-5
    #gX estará determinado por el valor de alphaD
    #El valor de epsilon variará 
    masa = 10**x_[0]
    data['MAp'] = 4*masa
    data['Mchi1'] = masa
    data['gX'] = x_[1]
    data['epsilon'] = 10**x_[2]
    print(data)
    #x_[0] = Mchi, x_[1] = alphaD, x_[2] = epsilon. 
    #print(data)
    writer(ruta,data) 
    subprocess.getoutput(rutaG)
    return eje(COMMAND_RQ)

def l_omega(x_,omega_th_): 
    MAp_ = 10**x_[0]
    epsilon_ = 10**x_[1]
    aS_ = 10**x_[2]
    omega_th = omega_th_
    omega_ex = 0.12
    delta_omega_pdg = ((0.1*omega_th)**2 + 0.001*2)**0.5
    #print(delta_omega_pdg)
    #delta_omega_pdg = 0.012
    #print(omega_th)
    return (omega_th - omega_ex)**2 / delta_omega_pdg**2

def gaussian(x_):
    return l_omega(x_,calc(x_))


def de_scan(bounds,nombre_ = 'datos.csv'):
    x = [] 
    chi_sq = [] 
    #bounds = [(lash_min,lash_max),(mass_min,mass_max)]
     #Ligaduras del modelo. 

    def objective(x_): 
        arreglo = [0]*4
        chi_sq_ = gaussian(x_)
        chi_sq.append(chi_sq_)
        datos = calc(x_)
        arreglo[0:2] = x_
        arreglo[3] = datos
        arreglo[4] = chi_sq_ 
        x.append(arreglo) 
        #print(arreglo) 
        if (len(x)%100 == 0): 
            print(len(x),end='\r')
        return chi_sq_
    
    differential_evolution(objective, bounds,
                           strategy='best1bin', maxiter=None,
                           popsize=100, tol=0.01, mutation=(0.7, 1.99999), recombination=0.15,
                           polish=False, seed=seed)

    try: 
        column_names = ['Mchi1','gX','epsilon','reliq','chi']
        df = pd.DataFrame(np.array(x),columns = column_names)
        print("Los elementos del dataframe son:")
        df.to_csv(nombre_, index=False, header=None)
        print(df.head())
        print("El tamaño de los datos es:",len(df))
        print("Datos almacenados con exito")

    except:
        print("Los datos del dataframe no han podido ser almacenados")

    return np.array(x),len(x)

if __name__ == '__main__':
	#x_[0] = Mchi, x_[1] = alphaD, x_[2] = epsilon.
    #x = [0.1,0.1,1e-3]
    #print(calc(x))

    gX1 = 1.12
    #gX1 = 2.50
    #aD2 = 0.5
    bounds1 = [(Mchi1_min,Mchi1_max),(gX1,gX1),(epsilon_min,epsilon_max)]
    #bounds2 = [(Map_min,Map_max),(epsilon_min,epsilon_max),(aS2,aS2)]
    np.random.seed(seed) 
    print("Running de_scan") 
    tO = time.time()
    x,call = de_scan(bounds1,nombre_='archivo_1_f0.10.csv')
    #x,call = de_scan(bounds2,nombre_='archivo_2.csv')
    de_time = time.time() - tO 
    de_time = de_time/60
    print("Tiempo de ejecución: ", de_time, " minutos")
    print("Cantidad de datos generados: ", call)
    try: 
        np.savetxt("datos_profile.txt", x, delimiter=',')
        print("Archivo guardado con exito")

    except: 
        print("El archivo no ha podido ser almacenado")

    print("Finalizado")