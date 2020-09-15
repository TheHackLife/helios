![Test Image 1](https://i.imgur.com/AUZMd9M.png)

Helios RGB Bar por [TheHackLife](https://www.youtube.com/channel/UCOCYnTfY7izcASanFVHL3Aw?view_as=subscriber)

## Instalación
Descargar los firmware y herramientas en la sección [Releases](https://github.com/TheHackLife/helios/releases)
 
Abrir el programa **HELIOS Updater.exe**  
Conectar cualquier placa basada en esp8266 (wemos, nodemcu, etc...)  
Seleccionar el firmware correspondiente *("Controlador.bin" para el hub, "led.bin" para el tubo)*  
El programa subira el firmware automaticamente, ante cualquier problema revisar el archivo *log.txt*  
Controlar las luces a travez del hub conectando se a la red wifi **HELIOS BAR** ó a traves del sitio web *https://helios.bar*  

**Nota:** Para controlar sus tubos leds a traves del sitio web *https://helios.bar* deberá antes conectarse a la red **HELIOS BAR** y una vez configurada su red wifi, obtendrá su HubID *(Nunca revele su HubID, de otra forma cualquiera podría manejar sus lamparas)*, si lo necesita, el HubID puede cambiarse.
 
## API
**HELIOS** Posee una API desde la cual podrá controlar sus luces desde la plataforma que usted desee

#### GET Endpoint
**GET http://cloud.helios.bar:9000/get**  
**uid**: id de tu hub" *(Obligatoria)*  
**json** si incluye esta variable, obtendra sus luces en formato json  

## Respuesta
```javaScript
{
   "bulbs": [
      [
          "6807145", //chip id del tubo
          "070109",  //color base (modo 0)
          "000000",  //color g1 (modo 1)
          "68157f",  //color g2 (modo 1)
          "1",       //Tamaño arcoiris
          "29",      //Velocidad Arcoiris
          "colorf", //modo Audio ritmico
          "5",      //velocidad flash
          "100"     //ip de luz (este valor debe ser usado para enviar comandos a esta luz)
       ],
       [etc...]
   ]
}

```

#### SET Endpoint
**GET http://cloud.helios.bar:9000/set**  

**ip**: ip de lampara ó "all" *(Obligatoria)*  
**uid**: id de tu hub" *(Obligatoria)*  
**change**: 0-6 para cambiar entre modos preestablecidos  
**base**: color en HEX *(Para modo "Color solido" o 0)*  
**g1**: color en HEX *(Para modo "Gradient" o 1)*  
**g2**: color en HEX *(Para modo "Gradient" o 1)*  
**audioMode**: white, flash ó color *(Para modo "Audio Ritmico" o 2)*  
**flashSpeed**: 5-40 *(Para modo "Audio Ritmico" o 2)*  
**rainbowSize**: 5-40 *(Para modo "Aroiris" o 3)*  
**rainbowSpeed**: 5-200 *(Para modo "Aroiris" o 3)*  

## Ejemplos
```javaScript
//Obtenemos un json con todas nuestras luces disponibles
$.get("http://cloud.helios.bar/get?uid=QCGH4456511&json=1");

//Cambiamos la lampara a modo 0 (Color solido)
$.get("http://cloud.helios.bar/set?id=100&uid=QCGH4456511&change=0");

//Cambiamos el color a rojo
$.get("http://cloud.helios.bar/set?id=100&uid=QCGH4456511&base=#7f0000");

//Cambiamos la lampara a modo 1 (Degradado)
$.get("http://cloud.helios.bar/set?id=100&uid=QCGH4456511&change=1");

//Hacemos un degradado entre Rojo y Celeste
$.get("http://cloud.helios.bar/set?id=100&uid=QCGH4456511&g1=#7f0000");
$.get("http://cloud.helios.bar/set?id=100&uid=QCGH4456511&g2=#007b7f");

```

## Apps dentro del sitio
Crear apps dentro del sitio web *https://helios.bar* puede resultar atractivo si no se tiene un entorno donde poder correr la API tradicional

El lenguaje es javaScript y puede hacerlo  mediante los endpoints de la API pública, aunque hemos pre-programado ciertas funciones que pueden ayudarle

### Funciones pre-programadas
#### rainbow _(string HEX1, string HEX1, int STEPS)_
Crea un array con tantos valores como **STEPS** desde un color **HEX1** a otro color **HEX2**

#### change _(String IP, String HEX, function Callback)_
Cambia el color de la lampara establecida mediante **IP** a el color **HEX** establecido *(Solo funciona con modo "base" o 0)*

#### gradient _(String IP, String HEX1, String HEX2, function Callback)_
Crea un degradado en la lampara establecida mediante **IP** desde el color **HEX1** establecido a el color **HEX2** *(Solo funciona con modo "Degradado" o 1)*

#### type _(String IP, String Mode, function Callback)_
Cambia el "audioMode" *(Solo funciona con modo "Audio Ritmico" o 2)*

#### speed _(String IP, int Speed, function Callback)_
Cambia el "flashSpeed" *(Solo funciona con modo "Audio Ritmico" o 2)*

#### size _(String IP, int Speed, function Callback)_
Cambia el tamaño de los colores del Arcoiris *(Solo funciona con modo "Arcoiris" o 3)*

#### speedi _(String IP, int Size, function Callback)_
Cambia el tamaño de los colores del Arcoiris *(Solo funciona con modo "Arcoiris" o 3)*

## Ejemplos
```javaScript
//Ponemos las lamparas en modo 0 (color base)
change("all", 0, function(){
  //Creamos un array de un color a otro, con 20 colores intermedios
  colours = rainbow("#ff00f6", "#1200ff", 20);
  //Creamos un bucle para enviar cada color
  for(i=0;i < colours.length; i++) {
    //Para no enviar todos juntos, lo hacemos en un timeout con un retraso de 100ms cada color
     setTimeout(function(col){
        color("all", col);
     }, 100*i, colours[i].replace("#", ""));
  }
});
```

## License

Hecho por [TheHackLife](https://www.youtube.com/channel/UCOCYnTfY7izcASanFVHL3Aw?view_as=subscriber)  
Helios es un programa gratuito y no ofrece ninguna garantía, fué creado como resultado de un nuevo desafío y con fines educativos, si detecta algún error en Helios puede abrir un Issue aquí, si le gusta Helios puede colaborar con su desarrollo o hacer una [donación](https://www.youtube.com/channel/UCOCYnTfY7izcASanFVHL3Aw?view_as=subscriber)  
MIT License

2020
