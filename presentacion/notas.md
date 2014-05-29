# Notas presentación

## Diapositivas

#### 2 - Portada 

Buenos días, mi nombre es José Tomás Tocino, soy alumno de Ingeniería Informática y voy a presentar mi proyecto titulado _"SiteUp, plataforma de monitorización de servicios de internet"._

#### 3 - Índice

Éste es el índice que voy a seguir durante la presentación. En primer lugar haré una pequeña introducción explicando el contexto y las motivaciones del proyecto. Seguidamente se explicará la planificación que se ha seguido. Luego haré una descripción de todas las partes que componen el proyecto. Tras ello, haré un repaso de los detalles más importante del desarrollo del proyecto, veremos cuáles son las conclusiones a las que se ha llegado al terminar el proyecto y la difusión que se ha obtenido, y finalmente se hará uan demostración práctica de la funcionalidad del proyecto.

#### 5 - Introducción, contexto

En la actualidad, las nuevas tecnologías son una parte integral de la sociedad. Todos los ámbitos de nuestra vida diaria, desde las relaciones sociales hasta pedir cita para el médico pasan por las nuevas tecnologías en general, e internet en particular. Las comunicaciones en casi todos los casos se realizan a través de la red de redes.

Debido a esta omnipresencia de las tecnologías han ido surgiendo nuevos modelos de negocio basados al 100% en las nuevas tecnologías de la información. Por ejemplo, facebook o twitter son empresas totalmente digitales, sin un producto físico, pero que ya cotizan en bolsas con operaciones de miles de millones de dólares. 

Ahora bien, ¿qué ocurre si fallan las infraestructuras o los servicios en los que se basan estas empresas? Pues que pueden llegar a darse pérdidas incluso económicas. De hecho, Amazon estuvo 40 minutos fuera de línea y en ese periodo llegó a perder 4.8 millones de dólares.

Es por ello que queda manifiesta la importancia de la fiabilidad de estos servicios, y para asegurarse de esa disponibilidad es importante contar con sistemas de monitorización como el que se presenta en este proyecto.

#### 6 - Introducción, motivación personal

Además de este contexto social que he presentado, la idea del proyecto surgió por una situación personal que ocurrió en octubre de 2013. Formé parte de un proceso de selección de personal en Google Irlanda, y las comunicaciones se hicieron a través del correo electrónico personal. El dominio de este correo electrónico estaba gestionado por una empresa de alojamiento que en un momento dado borró accidentalmente los registros DNS y dio lugar a que se perdieran correos electrónicos importantes. Si hubiese tenido algún sistema de monitorización de las DNS esto se podría haber detectado.

#### 7 - Introducción, objetivos

Con la idea en mente de desarrollar un sistema de monitorización se definieron los siguientes objetivos principales:

* Adquirir una base de conocimientos sobre monitorización, estudiando las alternativas que ya existían.
* Crear un módulo capaz de lanzar varios tipos de chequeos.
* Construir alrededor del módulo de chequeos una plataforma web con la que los usuarios puedan crear y gestionar sus chequeos.
* Y finalmente desarrollar un sistema de notificaciones a través de correo electrónico y a través de notificaciones mediante una aplicación Android.

Estos son los objetivos principales que se propusieron para el proyecto. 

#### 8 - Introducción, objetivos transversales

Además, se establecieron varios objetivos transversales como: _(mencionar los puntos)._

#### Planificación GANTT

La planificación que se hizo inicialmente al final se ha seguido con bastante rigor y los plazos han sido los establecidos.

#### 13 - Descripción

De esta descripción se extrae que hay dos productos principales: __PASAR DIAPO__.

#### 16 - Plataforma web/gestión de chequeos/DEF. CHEQUEO

Antes de continuar es importante conocer cuál es la pieza principal del sistema, que son los chequeos. _(tras definición pasar diapo con EJEMPLOS)_.

#### 18 - Plataforma web/detalles de los chequeos

La periodicidad define la frecuencia con la que se debe lanzar ese chequeo. El máximo es de 1 vez por minuto, de forma que en una hora el chequeo se comprueba hasta 60 veces. Esto nos permite tener una gran cantidad de información sobre el servicio vigilado.


## Demostración

* Presentar pantalla inicial, enlace de GET STARTED, enlaces del header 
* Crear usuario, Prueba2
* Presentar pantalla del dashboard
* Presentar perfil de usuario, comentar lo del daily report
* Crear grupo: webs externas
* Crear PingCheck a UCA.es, explicar campos del formulario
* Crear PortCheck a ftp.mozilla.org:22, explicar campos del formulario
* Activar/desactivar el pingcheck
* Activar/desactivar el grupo completo
* Crear otro grupo: personal
* Presentar http://josetomastocino.com/personal
* Crear HttpCheck a http://josetomastocino.com/personal, cadena "Prueba", explicar campos del formulario, SENSIBILIDAD 1
* Crear DNSCheck, josetomastocino.com, A, 78.47.140.228, explicar campos del formulario
* Móvil, abrir AirDroid
* Navegador, ir a web.airdroid.com
* Móvil, abrir SiteUp Client, hacer login
* Presentar listado de chequeos
* Pulsar en el detalle de un chequeo y explicar que la web va bien en el móvil.
* Volver al escritorio, ssh omegote@maquinita, modificar /srv/josetomastocino.com/www/personal
* Mientras, explicar el proceso de cambio de estado, explicar que el cambio a "UP" es instantáneo. Explicar que la sensibilidad antes era global.
* Al recibir la notificación, enseñar pantalla móvil y gmail.
* Volver a la terminal y restaurar el fichero. Recordar que el cambio a "UP" es instantáneo.
* Entrar en el detalle del chequeo, explicar los campos. Explicar la información de eventos. Explicar opciones de exportación.
* Pasar al pingcheck, explicar las gráficas, resúmenes, etc.
