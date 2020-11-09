<div align="center" style="margin-bottom: 10px;">
    <a href="https://twitter.com/intent/follow?screen_name=kennbroorg">
	<img alt="follow on Twitter" src="https://img.shields.io/twitter/follow/kennbroorg.svg?label=follow%20&style=for-the-badge&logo=twitter&labelColor=abcdef&color=1da1f2">
    </a>
</div>

<div align="center" style="margin-bottom: 10px;">
    <img alt="Python" src="https://img.shields.io/badge/python-3.7-informational.svg?style=for-the-badge">
    <img alt="Flask" src="https://img.shields.io/badge/interface-flask-yellowgreen.svg?style=for-the-badge">
    <img alt="Node" src="https://img.shields.io/badge/node-12.x-brightgreen.svg?style=for-the-badge">
    <img alt="Angular" src="https://img.shields.io/badge/web%20framwork-angular%207-red.svg?style=for-the-badge">
</div>

<div align="center">
    <a href="https://gitlab.com/kennbroorg/shit-bucket/fecalface/-/blob/master/README.es.md">
	<img alt="README English" src="https://img.shields.io/badge/README-English-orange.svg?style=for-the-badge">
    </a>
</div>

---

<div align="center">   

[Description](#description)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Installation](#installation)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Website][website]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Issues][issues]

</div>

---

<!--
Website References
-->
[website]:https://kennbroorg.gitlab.io/shit-bucket/fecalface-page
[issues]:https://gitlab.com/kennbroorg/shit-bucket/fecalface/-/issues

<h1 align="center">FecalFace</h1>

<div align="center">
    <img alt="Logo" src="frontend/src/assets/images/FecalFace-simetric-logo-trans.png"> 
</div>

---

<h2 id="description">Descripción</h2>
Fecalface nace del concepto "Balde de caca" donde la idea es tratar de pudrir los datos que tienen acerca de nosotros.
Especificamente, el proyecto se relaciona con la detección y reconocimiento de rostros.
La motivación de este proyecto es que las empresas que colectan nuestras caras no podrán identificarnos o relacionarnos con nuestros avatars.

Este proyecto (PoC por ahora) involucra : 

- Deteción de caras en avatars de nuestras RRSS
- Identificación con nuestras cuentas
- Ataque al avatar para protegerlo
- Detección posterior al ataque sin identificación
- Disponibilizar la imagen protegida para su descarga

**This project is part of Shit Bucket tools**

###  ¿ Qué hace el proyecto ? 
Colecta el avatar de las RRSS (Instagram por ahora), tratando de determinar la posición del rostro si existe y luego atacándolo para hacer que una comparación final entre la cara original y la atacada no sean relacionables por una IA, pero para el ojo humano sigan siendo similares y reconocibles.

###  ¿ Qué no hace el proyecto ?
Este proyecto no hará que nuestras caras sean confundidas con la de un oso panda. Y en este momento el proyecto no funciona con avatars con más de una cara.

###  Procedo de ataque
El proceso de ataque hace un uso intensivo de procesamiento, tardando entre 5 y 7 minutos. Tenga paciencia o compre GPUs.
>La aclaración de arriba es importante y también está en el disclaimer

## Website
Visite el [website][website] del proyecto.

<h2 id="installation">Instalación</h2>

## Instalación Fácil (Unicamente Python)

Ir a nuestro [website][website]. Descargar el archivo ZIP y descomprimirlo.
```
unzip latest.zip
cd Fecalface-pack
pip install -r requirements.txt
cd backend
python app.py -e prod
```
Y, finalmente, [browsealo](#browse).

## Instalación completa (para DEV)

### Clonar el repositorio

```shell
git clone https://gitlab.com/kennbroorg/iKy.git
```

### Instalar el backend

#### Python 

Usted debe instalar las librerías que están en requirements.txt

```shell
python3 -m pip install -r requirements.txt
```

### Instar el frontend

#### Node

Primero que nada, se debe instalar [nodejs](https://nodejs.org/en/).


#### Dependencias

Dentro del directorio **frontend** se debe instalar las dependencias

```shell
cd frontend
npm install
```

## Encendiendo Fecalface

### Encendiendo el backend

Encender el backend en una terminal, dentro del directorio **backend**

```shell
python3 app.py
```

### Encendiendo el frontend

Finalmente, para encender el frontend, ejecutar el siguiente comando dentro del directorio **frontend**

```shell
npm start
```

<h3 id="browser">Browser</h3>

Abrir el browser en esta [url](http://127.0.0.1:9001) 

<h2 id="issues">Issues</h2>

Si experimenta algún problema o tiene alguna sugerencia, no dude en crear un issue. 

<div align="center">   

[<img alt="Create an issue" src="https://kennbroorg.gitlab.io/shit-bucket/fecalface-page/images/OpenIssueButton.png" height="60px">](https://gitlab.com/kennbroorg/shit-bucket/fecalface/-/issues)

</div>

## Aviso Legal

Todo aquel que contribuya o haya contribuído con el proyecto, incluyéndome, no somos responsables por el uso de la herramienta (Ni el uso legal ni el uso ilegal, ni el "otro" uso). 

Tenga en cuenta que este software fue inicialmente escrito para con fines educativos (para educarnos a nosotros mismos), y ahora el objetivo es colaborar con la comunidad haciendo software libre de calidad, y si bien la calidad no es excelente (a veces ni siquiera buena) nos esforzamos en perseguir la excelencia.

El proceso de ataque hace un uso intensivo de procesamiento, tardando entre 5 y 7 minutos. Tenga paciencia o compre GPUs

No reembolsamos su dinero si no está satisfecho.

Espero que disfrute la utilización de la herramienta tanto como nosotros disfrutamos hacerla. El esfuerzo fue y es enorme (Tiempo, conocimiento, codificación, pruebas, revisiones, etc) pero lo haríamos de nuevo.

No use la herramienta si no puede leer claramente las instrucciones y/o el presente Aviso Legal.

Por cierto, para quienes insistan en acordarse de mi madre, ella murió hace muchos años pero la amo como si estuviera aquí mismo.
