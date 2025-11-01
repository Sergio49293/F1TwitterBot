from VueltaClase import *


def scatter_vueltas_multipiloto(vueltas_objetos):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for obj in vueltas_objetos:
        laps = obj.vueltas_piloto
        lap_times = laps["LapTime"].dt.total_seconds()
        lap_numbers = range(len(lap_times))
        ax.scatter(lap_numbers, lap_times, c=obj.color, label=obj.piloto, s=20, alpha=0.8)

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
    nombre_archivo = f"{carpeta}/Scatter_{año}_{sesion.replace(' ', '_')}({nombres_pilotos}).png"
    plt.savefig(nombre_archivo, dpi=250, bbox_inches="tight")
    plt.close()
    
    print(f"Gráfico guardado en {nombre_archivo}")


def comparar_telemetrias_varias(vueltas):
    # ======= CONFIGURACIÓN DE FIGURA =======
    fig, ax = plt.subplots(6, 1, figsize=(15, 20))
    plt.subplots_adjust(hspace=0.5, top=0.93, bottom=0.05, left=0.05, right=0.95)

    # ======= REFERENCIA: vuelta más rápida =======
    ref = min(vueltas, key=lambda v: v.tiempo_s)

    # ======= DISTANCIA Y MARGEN =======
    dist_max = min(v.telemetria['Distance'].max() for v in vueltas) * 1.03
    distancia_comun = np.linspace(0, dist_max, 2000)

    # ======= TIEMPO DE REFERENCIA =======
    t_ref = np.interp(
        distancia_comun,
        ref.telemetria['Distance'],
        ref.telemetria['Time'].dt.total_seconds()
    )

    # ======= ETIQUETAS DE LOS EJES =======
    etiquetas = {
        'Speed': 'Velocidad [km/h]',
        'Throttle': 'Acelerador [%]',
        'Brake': 'Freno [%]',
        'nGear': 'Marcha',
        'RPM': 'RPM'
    }

    # ======= DIBUJAR DIFERENCIA Y TELEMETRÍAS =======
    for v in vueltas:
        color = v.color
        t = np.interp(
            distancia_comun,
            v.telemetria['Distance'],
            v.telemetria['Time'].dt.total_seconds()
        )
        diff = t - t_ref

        # Primera gráfica: diferencias
        ax[0].plot(distancia_comun, diff, label=v.piloto, color=color, linestyle='-')

        # Resto: variables de telemetría
        for i, data in enumerate(['Speed', 'Throttle', 'Brake', 'nGear', 'RPM']):
            ax[i+1].plot(v.telemetria['Distance'], v.telemetria[data],
                         label=v.piloto, color=color, linestyle='-')

    # ======= AJUSTES VISUALES =======
    ax[0].axhline(0, color='black', linestyle='dashdot')
    ax[0].set_ylabel('Diferencia (s)')
    ax[5].set_xlabel('Distancia [m]')

    for i, data in enumerate(['', 'Speed', 'Throttle', 'Brake', 'nGear', 'RPM']):
        if i > 0:
            ax[i].set_ylabel(etiquetas[data])
        ax[i].set_xlim(0, distancia_comun[-1])
        ax[i].legend(fontsize=8)
        ax[i].set_xticks(np.arange(0, math.ceil(dist_max / 250) * 250 + 1, 250))

    # ======= TÍTULOS AL ESTILO DE LA CLASE =======
    sesion = vueltas[0].nombre_completo_sesion
    año = vueltas[0].año
    circuito = vueltas[0].circuito

    fig.text(0.5, 0.97, f"Comparativa de Telemetrías - {sesion}", ha="center", fontsize=16)

    # Subtítulo con colores de pilotos
    x_base = 0.5
    spacing = 0.05
    total = len(vueltas)
    ancho_total = (total - 1) * spacing
    x_inicio = x_base - ancho_total / 2

    for i, v in enumerate(vueltas):
        x_pos = x_inicio + i * spacing
        fig.text(x_pos, 0.95, v.piloto, color=v.color, ha="center", fontsize=16, fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # ======= GUARDAR =======
    carpeta = f"graficos/{año}/{circuito}"
    os.makedirs(carpeta, exist_ok=True)

    nombres_pilotos = "-".join([v.piloto for v in vueltas])
    nombre_archivo = f"{carpeta}/TelemetriaComparativa_{año}_{circuito}_{vueltas[0].tipo_sesion}({nombres_pilotos}).png"

    fig.savefig(nombre_archivo, dpi=250, bbox_inches="tight")
    plt.close(fig)

    print(f"Gráfico guardado en: {nombre_archivo}")



# ====== EJEMPLO DE USO ======
vuelta_ver = VueltaClase("VER", 2023, "Monaco", "Q")
vuelta_ver.cargar_todo()

vuelta_alo = VueltaClase("ALO", 2023, "Monaco", "Q")
vuelta_alo.cargar_todo()

vuelta_lec = VueltaClase("LEC", 2023, "Monaco", "Q")
vuelta_lec.cargar_todo()

comparar_telemetrias_varias([vuelta_ver, vuelta_alo, vuelta_lec])

