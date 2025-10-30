from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import pandas as pd
import numpy as np
import os
import math

class VueltaClase():
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True,color_scheme='fastf1')
    def __init__(self,piloto,año,circuito,sesion,n__vuelta=None):
        #Datos que tiene que introducirlos el usuario
        self.piloto = piloto
        self.año = año
        self.circuito = circuito
        self.tipo_sesion = sesion
        self.n_vuelta = n__vuelta   
        
        
        self.color = None
        
        self.sesion = None #EVENTO
        self.vuelta = None
        
        
        self.telemetria = None
        self.tiempo = 0
        #Tiempo de sectores
        self.tiempo_sector1= None
        self.tiempo_sector2 = None
        self.tiempo_sector3 = None
        
        #Compuesto, stint, neumatico
        self.compuesto = None
        self.vida_neumatico = None
        self.stint = None
        
        #Velocidades punta
        self.vel_FL= None
        self.velI1 = None
        self.velI2 = None
        self.velST = None
        
        self.vuelta_txt = self.n_vuelta if self.n_vuelta is not None else "R"
        
    def cargar_todo(self):
        self.cargar_sesion()    
        self.cargar_color()
        self.cargar_nombre_evento()
        self.cargar_datos_circuito()
        
        self.cargar_vueltas_sesion()
        self.cargar_vuelta_esp()
        self.cargar_telemetria()
        self.cargar_sectores()
        self.cargar_vels_punta()
        self.compuesto_stint_vida_etc()
        self.cargar_otros_attr()
       
       
    def cargar_sesion(self):
        self.sesion = fastf1.get_session(self.año,self.circuito,self.tipo_sesion)
        self.sesion.load()
        
    def cargar_color(self):
        self.equipo = fastf1.plotting.get_team_name_by_driver(self.piloto,self.sesion)#short = True para acortar
        self.color = fastf1.plotting.get_team_color(self.equipo, self.sesion)
    
    def cargar_nombre_evento(self):
        self.nombre_evento = self.sesion.event["EventName"]
        self.nombre_completo_sesion =  f"{self.nombre_evento} - {self.tipo_sesion}"
    
    
    def cargar_vueltas_sesion(self):
        self.vueltas_piloto = self.sesion.laps.pick_drivers(self.piloto)
             
    def cargar_vuelta_esp(self):
        if self.n_vuelta !=None:
            self.vuelta = self.sesion.laps.pick_drivers(self.piloto).iloc[self.n_vuelta+1] 
        else: 
            self.vuelta = self.sesion.laps.pick_drivers(self.piloto).pick_fastest()             
    
    def cargar_telemetria(self):
        self.telemetria = self.vuelta.get_telemetry()     
        
    def cargar_datos_circuito(self):
        self.info_circuito = self.sesion.get_circuit_info()
        self.curvas_dist = self.info_circuito.corners['Distance'].values
  
    def cargar_sectores(self):
        # Tiempos de sectores de la vuelta actual
        self.tiempo_sector1 = self.vuelta['Sector1Time']
        self.tiempo_sector2 = self.vuelta['Sector2Time']
        self.tiempo_sector3 = self.vuelta['Sector3Time']
    
    def compuesto_stint_vida_etc(self):
        self.compuesto = self.vuelta['Compound']
        self.vueltas_neum = self.vuelta['TyreLife']
        self.neum_nuevo = self.vuelta[['FreshTyre']]
        self.stint = self.vuelta['Stint']

    def cargar_vels_punta(self):
        self.vel_FL = self.vuelta['SpeedFL']
        self.vel_I1 = self.vuelta['SpeedI1']
        self.vel_I2 = self.vuelta['SpeedI2']
        self.vel_ST = self.vuelta['SpeedST']
  
    def cargar_otros_attr(self):
        self.hora_comienzo = self.vuelta['LapStartTime']
        self.status_pista = self.vuelta['TrackStatus']
        self.posicion = self.vuelta['Position']
        self.deleted = self.vuelta['Deleted']
        self.accurate = self.vuelta['IsAccurate']
    
    
    
    #PARTE DE GENERAR GRAFICOS    
    def titulo_tamanio_grafico_tel(self):
        #Tamaño del grafico, subplots...
        self.fig, self.ax = plt.subplots(5, 1, figsize=(15, 20))
        plt.subplots_adjust(hspace=0.5, top=0.93, bottom=0.05,left=0.05,right=0.95)

        #Titulo con colores
        self.fig.text(0.5, 0.97, f'Telemetria {self.nombre_completo_sesion} Vuelta {self.vuelta_txt}:', ha='center', fontsize=16)
        self.fig.text(0.5, 0.95, self.piloto, color = self.color, ha='center', fontsize=16, fontweight='bold')
  
    def graficar_telemetria(self):
        
        #Obtener los datos máximos y mínimos para el gráfico
        metros = (self.telemetria['Distance']).max()
        metros = math.ceil(metros / 100) * 100
        
        # Diccionario con etiquetas
        etiquetas = {
            'Speed': 'Velocidad [km/h]',
            'Throttle': 'Acelerador [%]',
            'Brake': 'Freno [%]',
            'nGear': 'Marcha',
            'RPM': 'RPM'
        }

        for i, data in enumerate(['Speed','Throttle','Brake','nGear','RPM']):
            self.ax[i].plot(self.telemetria['Distance'], self.telemetria[data], label=self.piloto, color=self.color, linestyle='-')
            self.ax[i].set_xticks(np.arange(0, metros+250, 250))
            self.ax[i].set_ylabel(etiquetas[data])

        self.ax[4].set_xlabel('Distancia [m]')
        plt.tight_layout(rect=[0, 0, 1, 0.95])  
 
    def guardar_telemetria(self):
        #Crear carpeta específica por año y GP
        carpeta = f"graficos/{self.año}/{self.circuito}"
        os.makedirs(carpeta, exist_ok=True)
        
        # Nombre de archivo con piloto y vuelta
        nombre_archivo = f"{carpeta}/Telemetria_{self.año}_{self.circuito}_{self.tipo_sesion}({self.piloto})-vuelta{self.vuelta_txt}.png"
        
        # Guardar figura
        self.fig.savefig(nombre_archivo, dpi=250, bbox_inches='tight')
        plt.close(self.fig)
        
        print(f"Grafico guardado en: {nombre_archivo}")
    
    def generar_png_telemetria(self):   
        self.titulo_tamanio_grafico_tel()
        self.graficar_telemetria()
        self.guardar_telemetria()
        
#El valor de sesion(Race, Qualy, FP) sera el que ponga luego en el grafico o otras cosas por eso 
#Hay que comprobar que el valor introducido para sesion sea Race y convertirlo si es r o R o algo asi


#COMPROBAR SI LO DEL ILOC+1 FUNCIONA Y COMO FUNCIONA PICKLAPS
#PROBAR SI PILOTO["TEAM"] DEVUELVE EL EQUIPO SINO HACERLO CON LA VUELTA, PERO NO SE DEBERIA CARGAR UNA VUELTA PARA ESO 
#PROBAR CON PICK_TEAM SINO
