
# ¡Oh my dog!

Esta es una aplicación web generada como proyecto para la materia Ingeniería de Software 2 correspondiente a las carreras Licenciatura en Sistemas, Licenciatura en Informática y Analista Programador Universitario de la Universidad Nacional de La Plata.

En este proyecto utilizamos virtualenv y pip para manejar las dependencias.

## Instalar una virtual environment

En primer lugar, moverse al directorio en el cual fue clonado el repositorio de Git. 

En Linux
```bash
    python3 -m venv myvenv
```
En Windows

```bash
    py -m venv myvenv
```

## Activar la virtual environment

En Linux
```bash
    source myvenv/bin/activate
```
En Windows

```bash
    .\env\Scripts\activate
```

## Instalar dependencias

En Linux
```bash
    python3 -m pip install -r requirements.txt
```
En Windows

```bash
    py -m pip install -r requirements.txt
```