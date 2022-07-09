# Alternate Data Streams
 Extrae los ADS (Alternate Data Streams) de cualquier archivo en windows

## Qué es un Alternate Data Stream:

Los Flujos Alternativos de Datos, Alternate Data Streams o ADS son una característica del sistema de archivos NTFS que permite almacenar metainformación con un fichero, sin necesidad de usar un fichero separado para almacenarla.

* Los ADS es posible mirarlos en Windows con los comandos:
  * CMD: dir /r
  * PowerShell: Get-Item .\file.etc -Stream *
* También es posible crear (si no existe, con notepad) o abrir un ADS y mirar su contenido con los siguientes comandos:
  * CMD: notepad "file.etc:stream_name"
    * Ejemplo: notepad "Alternate-Data-Streams-master.zip:Zone.Identifier"
  * PowerShell: Get-Content .\file.etc -Stream Zone.Identifier

## Ejemplos de Uso:

Ver ADS

```Python
>>> from ADS import ADS
>>> ads = ADS('Alternate-Data-Streams-master.zip')
>>> ads.hasStreams()
True
>>> ads.streams
['Zone.Identifier']
>>> stream = ads.streams[0]
>>> ads.getStreamContent(stream)
b'[ZoneTransfer]\r\nZoneId=3\r\nReferrerUrl=https://github.com/LawlietJH/Alternate-Data-Streams\r\nHostUrl=https://codeload.github.com/LawlietJH/Alternate-Data-Streams/zip/refs/heads/master\r\n'
>>> stream = ads.getStreamContent(stream).decode()
>>> print(stream)
[ZoneTransfer]
ZoneId=3
ReferrerUrl=https://github.com/LawlietJH/Alternate-Data-Streams
HostUrl=https://codeload.github.com/LawlietJH/Alternate-Data-Streams/zip/refs/heads/master
>>> ads.fullFilename(ads.streams[0])
'Alternate-Data-Streams-master.zip:Zone.Identifier'
```

Crear y Eliminar ADS

```Python
>>> text = 'Hola Mundo!\nEste es otro Alternate Data Stream (ADS)'
>>> ads.addStreamFromString('HolaMundo', text.encode())
True
>>> ads.addStreamFromFile('hola mundo.txt')
True
>>> ads.streams
['Zone.Identifier', 'HolaMundo', 'hola mundo.txt']
>>> print(ads.getStreamContent(ads.streams[1]).decode())
Hola Mundo!
Este es otro Alternate Data Stream (ADS)
>>> print(ads.getStreamContent(ads.streams[2]).decode())
Hola Mundo!
>>> ads.deleteStream(ads.streams[2])
True
>>> ads.streams
['Zone.Identifier', 'HolaMundo']
>>> ads.deleteStream(ads.streams[1])
True
>>> ads.streams
['Zone.Identifier']
```

## ¿Qué es el "Zone Identifier"?

También conocido como **_La Marca de la Web_** (_Mark-of-the-Web_ o _MOTW_) es una característica de seguridad introducida originalmente por Internet Explorer para obligar a las páginas web guardadas a ejecutarse en la zona de seguridad de la ubicación desde la que se guardó la página. En el pasado, esto se lograba agregando un comentario HTML en forma de <!-–saved from url=> al comienzo de una página web guardada.

Este mecanismo se extendió más tarde a otros tipos de archivos además de HTML. Esto se logró mediante la creación de un flujo de datos alternativo (ADS) para los archivos descargados. ADS es una característica del sistema de archivos NTFS que se agregó en Windows 3.1. Esta característica permite asociar más de un flujo de datos con un nombre de archivo, usando el formato "nombre de archivo: nombre de flujo".

Al descargar un archivo, Internet Explorer crea un nombre ADS _Zone.Identifier_ y agrega un _ZoneId_ a esta secuencia para indicar de qué zona se origina el archivo. Aunque no es un nombre oficial, muchas personas aún se refieren a esta funcionalidad como **_Mark-of-the-Web_**.

Los siguientes valores de ZoneId pueden usarse en un Zone.Identifier ADS:

0. Computadora local
1. Intranet local
2. Sitios de confianza
3. Internet
4. Sitios restringidos

Hoy en día, todo el software principal en la plataforma de Windows que se ocupa de archivos adjuntos o archivos descargados genera un ADS de Zone.Identifier, incluidos Internet Explorer, Edge, Outlook, Chrome, FireFox, etc. ¿Cómo escriben estos programas estos ADS? Ya sea creando el ADS directamente o mediante la implementación del sistema de la interfaz IAttachmentExecute . El comportamiento de este último se puede controlar a través de la propiedad SaveZoneInformation en el Administrador de archivos adjuntos .

Tenga en cuenta que la implementación de Windows 10 de la interfaz IAttachmentExecute también agregará información de URL a Zone.Identifier ADS.
