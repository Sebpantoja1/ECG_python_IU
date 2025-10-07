# ECG Cardioversor Desktop - Python Application

<div align="center">

![ECG Preview](https://via.placeholder.com/600x200/0f0f0f/00ff88?text=ECG+Real-Time+Monitor)

**Sistema profesional de adquisición ECG con cardioversor simulado**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

</div>

---

## 📋 Descripción General

Este proyecto es una **aplicación profesional de escritorio** desarrollada en Python para la adquisición, procesamiento, visualización y control de señales ECG en tiempo real. Diseñada para sistemas médicos y de investigación, incluye simulación completa de cardioversor con pulsos programables.

### 🔬 **Características Médicas**
- **Adquisición ECG** a 2000 Hz con precisión de 12 bits
- **Multiplexor 4:1** para derivaciones estándar (Lead I, II, III, aVF)
- **Algoritmos de detección** Pan-Tompkins y Simple optimizados
- **Cardioversor simulado** con pulsos de 15ms/25ms configurables
- **Filtros médicos** estándar (pasa-banda, notch 50/60Hz, anti-aliasing)

### 🖥️ **Interfaz Profesional**
- **Papel milimetrado** médico estándar (1mm/5mm)
- **Velocidades estándar** 25mm/s y 50mm/s
- **Ganancia configurable** 5/10/20 mm/mV
- **Temas claro/oscuro** con cambio en tiempo real
- **Logs integrados** y monitoreo de estado

---

## 🏗️ Arquitectura del Sistema

### **Hardware Requerido**
El sistema funciona con un **ESP32** que ejecuta el firmware refactorizado que incluye:
- **Boost converter** para generar 30V de salida
- **Multiplexor analógico** 4:1 controlado digitalmente  
- **ADC de 12 bits** a 2000 Hz de muestreo
- **Comunicación UART** a 115200 baud con protocolo de paquetes

### **Software Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ESP32 Board   │────│  Python Desktop │────│   Data Export   │
│                 │    │   Application   │    │                 │
│ • ADC Sampling  │    │ • Real-time GUI │    │ • CSV/JSON      │
│ • MUX Control   │    │ • Signal Proc   │    │ • Session Logs  │
│ • Serial Comm   │    │ • Cardioversor  │    │ • Metadata      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📁 Estructura del Proyecto

```
ecg_app/
├── app.py                      # 🚀 Punto de entrada principal
├── bootstrap.py               # 📦 Generador automático del proyecto
├── core/
│   ├── serial_manager.py       # 📡 Comunicación ESP32 + autodetección
│   ├── data_buffers.py         # 🔄 Buffers circulares optimizados
│   └── logger.py               # 📝 Sistema de logging (futuro)
├── gui/
│   ├── main_window.py          # 🖼️ Ventana principal PyQt6
│   └── widgets/
│       ├── plotter.py          # 📊 Visualización médica tiempo real
│       └── control_panel.py    # 🎛️ Panel serie y controles
├── algorithms/                 # 🧮 Módulos de procesamiento (futuro)
│   ├── pan_tompkins.py        # 🫀 Algoritmo Pan-Tompkins
│   ├── simple_detector.py     # 📈 Detector simple alternativo
│   └── filters.py             # 🎚️ Filtros médicos avanzados
├── cardioversor/              # ⚡ Lógica de cardioversión (futuro)
│   ├── controller.py          # 🎯 Estados y control de seguridad
│   └── pulse_generator.py     # ⚡ Pulsos 15ms/25ms configurables
├── db/                        # 🗄️ Persistencia SQLite (futuro)
│   ├── database.py            # 💾 Esquema y migraciones
│   └── dao.py                 # 📋 CRUD sesiones y eventos
└── export/                    # 📤 Exportación de datos (futuro)
    └── exporters.py           # 📊 CSV/JSON con metadatos
```

---

## ⚙️ Instalación y Configuración

### **Requisitos del Sistema**
- **Python 3.10+** (Windows/Linux/macOS)
- **Puerto serie** disponible (COM8 por defecto en Windows)
- **ESP32** con firmware ECG cargado

### **Instalación Rápida**

#### Opción 1: Bootstrap Automático
```bash
# Descargar y ejecutar bootstrap
python bootstrap.py

# Instalar dependencias
pip install pyqt6 pyqtgraph pyserial numpy scipy pandas

# Ejecutar aplicación
cd ecg_app
python app.py
```

#### Opción 2: Instalación Manual
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/ecg-cardioversor.git
cd ecg-cardioversor

# Crear entorno virtual (recomendado)
python -m venv ecg_env
source ecg_env/bin/activate  # Linux/macOS
# o
ecg_env\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

### **Configuración del Hardware**
```python
# En core/serial_manager.py - personalizar si es necesario
DEFAULT_BAUD = 115200           # Velocidad serie
DEFAULT_PREF_PORT = "COM8"      # Puerto preferido Windows
ESP_KEYWORDS = [                # Detectores automáticos
    "USB-SERIAL", "CP210", "CH340", "FTDI",
    "SILICON LABS", "ESP32", "CDC"
]
```

---

## 🚀 Ejemplos de Uso

### **1. Uso Básico - Primera Conexión**

```python
# La aplicación se inicia con tema oscuro por defecto
python app.py

# En la GUI:
# 1. Panel Serie → "Actualizar Puertos" para ver dispositivos
# 2. Seleccionar puerto o dejar COM8 (autodetectado)
# 3. "Conectar" → La app detecta automáticamente el ESP32
# 4. Verificar estado: "Conectado a COM8 @ 115200 bps"
```

**Logs esperados:**
```
Conectado a COM8 @ 115200 bps
Estado MUX restaurado tras reconexión
>> START
Tema: oscuro
```

### **2. Control del Multiplexor (Derivaciones ECG)**

```python
# Comandos enviados automáticamente por la GUI:
serial_mgr.send_mux_command("START")      # Modo automático
serial_mgr.send_mux_command("STOP")       # Detener
serial_mgr.send_mux_command("STATE_0")    # Lead I manual
serial_mgr.send_mux_command("STATE_1")    # Lead II manual
serial_mgr.send_mux_command("STATE_2")    # Lead III manual
serial_mgr.send_mux_command("STATE_3")    # aVF manual
serial_mgr.send_mux_command("DELAY_5000") # 5 segundos entre cambios
```

**Estados del MUX:**
| Comando | Derivación | Pin A | Pin B | Uso Clínico |
|---------|------------|-------|-------|-------------|
| STATE_0 | Lead I     | 0     | 0     | Actividad horizontal |
| STATE_1 | Lead II    | 0     | 1     | Ritmo principal |
| STATE_2 | Lead III   | 1     | 0     | Plano frontal |
| STATE_3 | aVF        | 1     | 1     | Eje eléctrico inferior |

### **3. Visualización en Tiempo Real**

```python
# Control de plotter médico
plot.window_s = 8.0           # 8 segundos visibles
plot.mm_per_s = 25            # 25 mm/s (velocidad estándar)
plot.mm_per_mV = 10           # 10 mm/mV (ganancia estándar)

# Cambio de velocidad y ganancia desde GUI:
# Velocidad: 25 mm/s → ECG normal
# Velocidad: 50 mm/s → Análisis detallado de complejos QRS
# Ganancia: 5 mm/mV → Señales de alta amplitud
# Ganancia: 20 mm/mV → Señales débiles o análisis fino
```

### **4. Gestión de Reconexión**

```python
# Escenario: ESP32 se reinicia o desconecta
# La app detecta pérdida de conexión y cambia estado a "Desconectado"

# Usuario presiona "Reconectar":
# 1. Autodetecta puerto disponible
# 2. Reconecta a 115200 baud
# 3. Restaura automáticamente último estado del MUX
serial_mgr.restore_mux_state()  # Automático tras reconexión

# Logs de reconexión exitosa:
# "Conectado a COM8 @ 115200 bps"
# "Estado MUX restaurado tras reconexión"
# ">> STATE_1"  (si estaba en Lead II antes)
```

### **5. Cambio de Tema Visual**

```python
# Desde menú "Tema" o botones del panel:
main_window.apply_theme("dark")   # Tema oscuro médico
# - Fondo: #121212 (gris oscuro)
# - Plot: #0f0f0f con cuadrícula roja/gris
# - Señal: #00FF88 (verde médico)

main_window.apply_theme("light")  # Tema claro
# - Fondo: blanco estándar
# - Plot: blanco con cuadrícula estándar
# - Mantiene colores médicos apropiados
```

---

## 📋 Comandos y Protocolos

### **Protocolo Serie ESP32 ↔ PC**

#### **Datos ADC (ESP32 → PC)**
```
Formato: 4 bytes por muestra
[0xAA] [LSB] [MSB] [CHECKSUM]

Ejemplo:
0xAA 0x4C 0x07 0xEB
→ Valor: 0x074C = 1868 (ADC 12-bit)
→ Voltaje: 1868/4095 * 3300 = 1505.5 mV
→ Checksum: 0xAA ^ 0x4C ^ 0x07 = 0xEB ✓
```

#### **Comandos (PC → ESP32)**
```bash
# Control del multiplexor
START\n           # Iniciar secuencia automática
STOP\n            # Detener multiplexor
STATE_0\n         # Seleccionar Lead I (manual)
STATE_1\n         # Seleccionar Lead II (manual)  
STATE_2\n         # Seleccionar Lead III (manual)
STATE_3\n         # Seleccionar aVF (manual)
DELAY_5000\n      # Configurar delay 5000ms
STATUS\n          # Consultar estado actual

# Comandos de cardioversor (futuro)
CV_ARM\n          # Armar cardioversor
CV_CHARGE\n       # Cargar capacitor
CV_FIRE_15\n      # Descargar pulso 15ms
CV_FIRE_25\n      # Descargar pulso 25ms  
CV_DISARM\n       # Desarmar inmediato
```

### **API Python - Ejemplos de Código**

#### **Conexión y Configuración**
```python
from core.serial_manager import SerialManager

# Crear manager con configuración personalizada
serial_mgr = SerialManager(
    preferred_port="COM3",    # Puerto específico
    baud=115200,              # Velocidad estándar
    logger=print              # Función de logging
)

# Conectar con autodetección
try:
    port = serial_mgr.connect()
    print(f"Conectado a: {port}")
except RuntimeError as e:
    print(f"Error: {e}")

# Verificar conexión
if serial_mgr.connected:
    print("✓ ESP32 conectado y listo")
```

#### **Lectura de Datos en Tiempo Real**
```python
from queue import Empty
import time

# Leer muestras del buffer
def read_ecg_samples(serial_mgr, duration_seconds=10):
    samples = []
    start_time = time.time()
    
    while (time.time() - start_time) < duration_seconds:
        try:
            # Obtener muestra (valor ADC 12-bit)
            raw_value = serial_mgr.rx_queue.get_nowait()
            
            # Convertir a milivoltios
            voltage_mv = (raw_value / 4095.0) * 3300.0
            
            samples.append({
                'timestamp': time.time(),
                'raw': raw_value,
                'mv': voltage_mv
            })
            
        except Empty:
            time.sleep(0.001)  # Evitar saturar CPU
    
    return samples

# Uso
ecg_data = read_ecg_samples(serial_mgr, duration_seconds=5)
print(f"Capturadas {len(ecg_data)} muestras en 5 segundos")
```

#### **Control Avanzado del Multiplexor**
```python
import time

def ecg_full_sequence(serial_mgr, delay_per_lead=10):
    """Secuencia completa de derivaciones ECG"""
    
    leads = [
        ("Lead I", "STATE_0"),
        ("Lead II", "STATE_1"), 
        ("Lead III", "STATE_2"),
        ("aVF", "STATE_3")
    ]
    
    for lead_name, command in leads:
        print(f"Cambiando a {lead_name}...")
        serial_mgr.send_mux_command(command)
        
        # Esperar estabilización de la señal
        time.sleep(2)
        
        # Capturar datos de esta derivación
        lead_data = read_ecg_samples(serial_mgr, delay_per_lead)
        print(f"  → {len(lead_data)} muestras capturadas")
        
        # Procesar o guardar datos aquí
        # save_lead_data(lead_name, lead_data)
    
    print("Secuencia completa finalizada")

# Ejecutar secuencia automática
ecg_full_sequence(serial_mgr, delay_per_lead=15)
```

---

## 🔧 Configuración Avanzada

### **Personalización de Filtros**
```python
# algorithms/filters.py (en desarrollo)
class ECGFilters:
    def __init__(self, sample_rate=2000):
        self.fs = sample_rate
        
    def bandpass_filter(self, data, low_freq=0.5, high_freq=40):
        """Filtro pasa-banda médico estándar"""
        nyquist = self.fs / 2
        low = low_freq / nyquist
        high = high_freq / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        return signal.filtfilt(b, a, data)
    
    def notch_filter(self, data, freq=50, quality=30):
        """Filtro notch para eliminar interferencia de red"""
        nyquist = self.fs / 2
        freq_norm = freq / nyquist
        b, a = signal.iirnotch(freq_norm, quality)
        return signal.filtfilt(b, a, data)
```

### **Calibración del Sistema**
```python
# utils/calibration.py (futuro)
class ECGCalibration:
    def __init__(self):
        self.adc_max = 4095          # 12-bit ADC
        self.vref = 3300             # 3.3V reference (mV)
        self.gain_hw = 1.0           # Hardware gain factor
        
    def adc_to_mv(self, adc_value):
        """Convertir valor ADC a milivoltios"""
        return (adc_value / self.adc_max) * self.vref / self.gain_hw
    
    def mv_to_mm(self, mv, mm_per_mv=10):
        """Convertir mV a mm en papel milimetrado"""
        return mv * mm_per_mv
    
    def time_to_mm(self, seconds, mm_per_s=25):
        """Convertir tiempo a mm horizontales"""
        return seconds * mm_per_s
```

---

## 🚨 Solución de Problemas

### **Problemas Comunes**

#### **Error: "No se encontraron puertos serie"**
```bash
# Verificar dispositivos conectados
python -c "
from serial.tools import list_ports
ports = list_ports.comports()
for p in ports:
    print(f'{p.device}: {p.description}')
"

# Solución:
# 1. Verificar cable USB ESP32
# 2. Instalar drivers CP210x/CH340 si es necesario
# 3. Cambiar puerto en la GUI o código
```

#### **Error: "Datos corruptos o checksum incorrecto"**
```python
# Verificar protocolo y baudrate
serial_mgr = SerialManager(baud=115200)  # Asegurar 115200

# Revisar logs para detectar patrones:
# - "RX error: ..." → Problema de conexión
# - Paquetes con checksum malo → Interferencia eléctrica
# - Buffer lleno → Reducir frecuencia o aumentar buffer
```

#### **GUI se congela o lag en el plot**
```python
# Reducir carga de procesamiento
def optimize_performance():
    # 1. Reducir frecuencia del timer de GUI
    self.timer.start(50)  # 50ms instead of 33ms
    
    # 2. Limitar muestras procesadas por ciclo
    fetched = 0
    while not q.empty() and fetched < 1000:  # Limit to 1000
        # ... procesar muestras
    
    # 3. Usar downsampling para visualización
    if len(data) > 5000:
        data = data[::2]  # Show every other sample
```

### **Logs de Depuración**

#### **Activar logging detallado**
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ecg_debug.log'),
        logging.StreamHandler()
    ]
)

# Los logs incluirán:
# - Conexiones/desconexiones serie
# - Comandos MUX enviados/recibidos  
# - Estadísticas de buffers y colas
# - Errores de checksum y timeouts
```

#### **Monitoreo en Tiempo Real**
```python
# Panel de estadísticas (futuro)
def show_performance_stats():
    print(f"Buffer RX: {serial_mgr.rx_queue.qsize()}/20000")
    print(f"Buffer TX: {serial_mgr.tx_queue.qsize()}/2000") 
    print(f"Samples/sec: {calculate_sample_rate()}")
    print(f"Packet errors: {error_count}")
    print(f"Connected: {serial_mgr.connected}")
```

---

## 🔮 Roadmap y Desarrollo Futuro

### **Fase 2 - Algoritmos y Filtros** (En progreso)
- [ ] Pan-Tompkins optimizado sin lag
- [ ] Algoritmo simple con parámetros configurables  
- [ ] Filtros médicos en tiempo real
- [ ] Panel de configuración de algoritmos

### **Fase 3 - Cardioversor Completo**
- [ ] Estados: Armado → Carga → Descarga → Desarme
- [ ] Pulsos configurables 15ms/25ms
- [ ] Doble confirmación de seguridad
- [ ] Marcadores visuales en plot
- [ ] Comunicación real con ESP32

### **Fase 4 - Base de Datos y Exportación**
- [ ] SQLite para sesiones y eventos
- [ ] Export CSV/JSON con metadatos
- [ ] Reportes PDF automáticos
- [ ] Análisis estadístico de sesiones

### **Fase 5 - Interfaz Web (FastAPI)**
- [ ] API REST para control remoto
- [ ] WebSocket para datos en tiempo real
- [ ] Dashboard web con Plotly/Dash
- [ ] Acceso multi-usuario

---

## 🤝 Contribución

### **Cómo Contribuir**
1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### **Áreas de Contribución**
- **Algoritmos médicos**: Pan-Tompkins, detección de arritmias
- **Interfaz de usuario**: Mejoras UX/UI, nuevos temas
- **Hardware**: Soporte para otros microcontroladores
- **Documentación**: Tutoriales, ejemplos, traducciones
- **Testing**: Pruebas unitarias, integración

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 🙏 Agradecimientos

- **PyQt6** por el framework GUI robusto
- **pyqtgraph** por visualización de alto rendimiento  
- **Comunidad ESP32** por documentación y soporte
- **Algoritmo Pan-Tompkins** por detección confiable de QRS

---

## 📞 Contacto y Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/ecg-cardioversor/issues)
- **Email**: tu-email@dominio.com
- **Wiki**: [Documentación Completa](https://github.com/tu-usuario/ecg-cardioversor/wiki)

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub**

**Desarrollado con ❤️ para la comunidad médica y de investigación**

</div>