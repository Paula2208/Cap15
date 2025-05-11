# Capítulo 15

## Requisitos

- Python 3.8 o superior.
- Librería PyGame Zero

## Instalación y Ejecución

1. Clona el repositorio o descarga los archivos del proyecto.
```bash
   git clone <>
```

2. Asegúrate de tener Python y PyGame Zero (PgZero) instalados:

```bash
   pip install pgzero
```

3. Ejecuta el archivo principal del juego:

```bash
   pgzrun main.py
```

## Crear un entorno virtual

1. Tener instalado python

```bash
python3 --version
```

2. Crear un repositorio para el proyecto e ingresar a este:

```bash
mkdir project && cd project
```

3. Crear un entorno virtual para python

```bash
python3 -m venv env
```

4. Activar el entorno virtual
```bash
source env/bin/activate
```
Una vez iniciado, debe verse algo así:

```bash
(env) tu-usuario@tu-mac project %
```

5. Continuar con el desarrollo del proyecto y la instalación de librerías

6. Guardar las dependencias en un archivo para replicarlo en otros entornos

```bash
pip freeze > requirements.txt
```

7. Desactivar el entorno virtual

```bash
deactivate
```


Para que Visual Studio Code utilice automáticamente tu entorno virtual:

1. Abre el proyecto en VS Code.

2. Presiona Cmd + Shift + P y busca *"Python: Select Interpreter"*.

3. Selecciona el intérprete que apunta a tu entorno virtual (debería verse algo como ./env/bin/python).