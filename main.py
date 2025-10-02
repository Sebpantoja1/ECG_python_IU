import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Agrega la carpeta actual al path para importar módulos locales
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from backend.signal_processor import ECGFilters
from backend.serial_handler import SerialReader
from backend.plot_visualizer import setup_plot, update_plot
from .backend import config

def main():
    print("=== 📊 MONITOR ECG CON VISUALIZACIÓN ===")
    print(f"Puerto: {config.SERIAL_PORT} | Baud Rate: {config.BAUD_RATE}")
    print(f"Debug Mode: {'✅' if config.DEBUG_MODE else '❌'} | Raw Data: {'✅' if config.RAW_DATA_MODE else '❌'}")
    print(f"Filtros: {'🟢 ACTIVOS' if config.ENABLE_FILTERS else '🔴 INACTIVOS'}")
    print(f"Límites Y: {'📏 FIJOS' if config.FIXED_Y_LIMITS else '📏 ADAPTATIVOS'}")
    print(f"Frecuencia de muestreo: {config.SAMPLE_RATE} Hz")
    print()
    
    ecg_filters = ECGFilters(config.SAMPLE_RATE)
    serial_reader = SerialReader(config.SERIAL_PORT, config.BAUD_RATE, ecg_filters)
    
    fig, ax1, ax2, line_raw, line_filtered, peaks_line, status_text, filter_text = setup_plot()
    
    try:
        serial_reader.start()
        
        ani = animation.FuncAnimation(fig, update_plot, fargs=(serial_reader,), interval=config.REFRESH_INTERVAL, 
                                      blit=False, cache_frame_data=False)
        
        def on_close(event):
            serial_reader.stop()
            plt.close('all')
        
        fig.canvas.mpl_connect('close_event', on_close)
        
        print("🖼️  Abriendo ventana de visualización...")
        plt.show()
        
    except KeyboardInterrupt:
        print("\n🛑 Cerrando aplicación...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        serial_reader.stop()
        print("👋 Aplicación cerrada")

if __name__ == "__main__":
    main()