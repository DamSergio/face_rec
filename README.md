# Face Recognition CLI Tool

## Descripción

Este es un programa CLI (Interfaz de Línea de Comandos) en Python diseñado para organizar automáticamente tus imágenes en carpetas basadas en el reconocimiento facial. El script examina las imágenes en la carpeta actual y las guarda en subcarpetas correspondientes según las personas que aparecen en las fotos.

## Requisitos

Antes de ejecutar el script, asegúrate de tener instalados los siguientes paquetes y herramientas:

- Python 3.x
- `pip` para instalar paquetes de Python
- CMake (para compilar dependencias)
- Visual Studio con el paquete de desarrollo para C++ (en Windows)

### Paquetes de Python

1. `face_recognition`
2. `Pillow` (para el manejo de imágenes)
3. `opencv-python` (opcional, si se usa para la visualización o procesamiento adicional)
4. `tkinter` (para la interfaz gráfica emergente para ingresar nombres)

## Instalación para modificarlo

1. **Instala CMake y Visual Studio** (si estás en Windows):

   - [Instala CMake](https://cmake.org/install/)
   - Asegúrate de que Visual Studio tenga instalado el componente de desarrollo para C++.

2. **Crea y activa un entorno virtual** (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

3. **Instala los paquetes de python**

```bash
pip install -r requirements.txt
```

## Instalacion para uso

1. **Descargar el archivo face_rec.exe**

2. **Añadir el archivo face_rec al path del sistema**

## Uso

1. **Abra el cmd dentro de la carpeta de sus imagenes y escriba el comando**

```bash
face_rec
```
