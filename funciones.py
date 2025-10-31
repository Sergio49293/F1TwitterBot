from VueltaClase import*

def scatter_vueltas_multipiloto(vueltas_objetos):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for obj in vueltas_objetos:
        laps = obj.vueltas_piloto
        lap_times = laps["LapTime"].dt.total_seconds()
        lap_numbers = range(len(lap_times))

        ax.scatter(lap_numbers, lap_times, c=obj.color, label=obj.piloto,s=20,alpha=0.8)

    nombres_pilotos = "-".join([obj.piloto for obj in vueltas_objetos])
    sesion = vueltas_objetos[0].nombre_completo_sesion
    año = vueltas_objetos[0].año
    circuito = vueltas_objetos[0].circuito
    

    ax.set_xlabel("Número de vuelta")
    ax.set_ylabel("Tiempo de vuelta (segundos)")
    ax.set_title(f"Tiempos de vuelta - {sesion} ({nombres_pilotos})")
    ax.grid(True)
    ax.legend()

    carpeta = f"graficos/{año}/{circuito}"
    os.makedirs(carpeta, exist_ok=True)
    nombre_archivo = f"{carpeta}/Scatter_{año}_{sesion}({nombres_pilotos}).png"
    plt.savefig(nombre_archivo, dpi=250, bbox_inches="tight")
    plt.close()
    
    print(f"Grafico guardado en {nombre_archivo}")
'''
#EJEMPLO DE EJECUCION
vueltaalo = VueltaClase("VER", 2023, "Monaco", "R")
vueltaalo.cargar_todo()

vueltaver = VueltaClase("ALO", 2023, "Monaco", "R")
vueltaver.cargar_todo()

scatter_vueltas_multipiloto([vueltaalo, vueltaver])
'''