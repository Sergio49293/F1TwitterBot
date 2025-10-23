from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import pandas as pd
import numpy as np
import os
import math

class VueltaClase():
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True,color_scheme='fastf1')
    def __init__(self,piloto,año,circuito,sesion,n__vuelta):
        #Datos que tiene que introducirlos el usuario
        self.piloto = piloto
        
        self.año = año
        self.circuito = circuito
        self.tipo_sesion = sesion
    
        self.n_vuelta = n__vuelta   
        
        #Datos a "calcular"
        self.color = None
        
        self.sesion = None #EVENTO
        self.vuelta = None
        self.vuelta_rapida = None
        
        self.telemetria = None
        self.tiempo = 0
        
        self.tiempo_sector1 = 0
        self.tiempo_sector2 = 0
        self.tiempo_sector3 = 0
        
        self.mejor_sec1 = 0
        self.mejor_sec2 = 0
        self.mejor_sec3 = 0
       
    def cargar_sesion(self):
        self.sesion = fastf1.get_session(self.año,self.circuito,self.tipo_sesion)
        self.sesion.load()
        
    def cargar_color(self):
        self.equipo = fastf1.plotting.get_team_name_by_driver(self.piloto,self.sesion)#short = True para acortar
        self.color = fastf1.plotting.get_team_color(self.equipo, self.sesion)
    
    def cargar_nombre_evento(self):
        self.nombre_evento = self.sesion.event["EventName"]
        self.nombre_completo_sesion =  f"{self.nombre_evento} - {self.tipo_sesion}"
        
    def cargar_vuelta(self):
        self.vuelta = self.sesion.laps.pick_drivers(self.piloto).iloc[self.n_vuelta+1]
    
    def cargar_telemetria(self):
        self.telemetria = self.vuelta.get_telemetry()
        
    #Habria que hacer algo con n_vuelta para que funcionase    
    '''def cargar_vuelta_rapida(self):
        self.vuelta_rapida = self.sesion.laps.pick_drivers(self.piloto).pick_fastest()'''
        
    def cargar_datos_circuito(self):
        self.info_circuito = self.sesion.get_circuit_info()
        self.curvas_dist = self.info_circuito.corners['Distance'].values
        
    def titulo_tamanio_grafico_tel(self):
        #Tamaño del grafico, subplots...
        self.fig, self.ax = plt.subplots(5, 1, figsize=(15, 20))
        plt.subplots_adjust(hspace=0.5, top=0.93, bottom=0.05)

        #Titulo con colores
        self.fig.text(0.5, 0.97, f'Telemetria {self.nombre_completo_sesion} Vuelta {self.n_vuelta}:', ha='center', fontsize=16)
        self.fig.text(0.5, 0.95, self.piloto, color = self.color, ha='center', fontsize=16, fontweight='bold')
  
    def graficar_telemetria(self):
        #Obtener los datos máximos y mínimos para el gráfico
        metros = (self.telemetria['Distance']).max()
        metros = math.ceil(metros / 100) * 100
        
        for i, data in enumerate(['Speed','Throttle','Brake','nGear','RPM']):
            self.ax[i].plot(self.telemetria['Distance'], self.telemetria[data], label=self.piloto, color=self.color, linestyle='-')
            self.ax[i].set_xticks(np.arange(0, metros+250, 250))
            self.ax[i].set_ylabel(data)
        self.ax[4].set_xlabel('Distancia [m]')
        plt.tight_layout()
        
        # Crear carpeta específica por año y GP
        carpeta = f"graficos/{self.año}/{self.circuito}"
        os.makedirs(carpeta, exist_ok=True)
        
        # Nombre de archivo con piloto y vuelta
        nombre_archivo = f"{carpeta}/Telemetria_{self.año}_{self.circuito}_{self.tipo_sesion}({self.piloto})-vuelta{self.n_vuelta}.png"
        
        # Guardar figura
        self.fig.savefig(nombre_archivo, dpi=250, bbox_inches='tight')
        plt.close(self.fig)
        
        print(f"Gráfico guardado en: {nombre_archivo}")
    
    def guardar_telemetria(self):
        pass
    
        
        
        
#El valor de sesion(Race, Qualy, FP) sera el que ponga luego en el grafico o otras cosas por eso 
#Hay que comprobar que el valor introducido para sesion sea Race y convertirlo si es r o R o algo asi

vuelta1 = VueltaClase("ALO",2025,"Hungary",'Q',11)
vuelta1.cargar_sesion()
vuelta1.cargar_nombre_evento()
vuelta1.cargar_color()
vuelta1.cargar_datos_circuito()
vuelta1.cargar_vuelta()
vuelta1.cargar_telemetria()
vuelta1.titulo_tamanio_grafico_tel()
vuelta1.graficar_telemetria()


#COMPROBAR SI LO DEL ILOC+1 FUNCIONA Y COMO FUNCIONA PICKLAPS
#PROBAR SI PILOTO["TEAM"] DEVUELVE EL EQUIPO SINO HACERLO CON LA VUELTA, PERO NO SE DEBERIA CARGAR UNA VUELTA PARA ESO 
#PROBAR CON PICK_TEAM SINO