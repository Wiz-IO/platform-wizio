# Arduino - PlatformIO Simulator for PC

**Simulator !?!?** Arduino source codes is compiled and executed as PC applications

Can be used for **education**, testing and debuging, for working with Comm Ports, Internet, Math ...

Your source codes can work on each Arduino board

OR you can create normal GCC project [read this](https://github.com/Wiz-IO/platform-wizio/wiki/GCC-Project)

**A few words in the beginning**
* **Version: 1.0.3** ( very beta - may be bugs yet )
* **Windows** ( and visual mode )
* Linux - in progress...
* Mac - later
* Raspberry PI is a Linux - this platform can support the board - later
* **Please read** [WIKI](https://github.com/Wiz-IO/platform-wizio/wiki)
* Tested at Windows 7, 8, 10, Ubuntu Linux 

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/arduino-simulator.png) 

VIDEO: 

https://www.youtube.com/watch?v=SKojOHDvfC0 ( DOOM - visual mode )


## The Compiler
* Windows - **MinGW-32** (GCC)
* * How to Install MinGW-32 [VIDEO](https://www.youtube.com/watch?v=sXW2VLrQ3Bs)
* * Add to PATH C:/MinGW/bin;
* Linux - **GCC**
* * How to Install GCC on Ubuntu Linux [VIDEO](https://www.youtube.com/watch?v=cotkJrewAz0)
* * openSSL: sudo apt-get install libssl-dev
* Mac - **GCC**

![Project](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/wizio-linux-ubuntu.png)

## Install Platform 

First install **MinGW-32** or **GCC** on your PC 

**PIO Home** > Platforms > Advanced Installation 

paste link https://github.com/Wiz-IO/platform-wizio.git

**Manual Install / Reinstall / Remove**
* .platformio\platforms\wizio
* .platformio\packages\framework-wizio

## Examples for:
* GSM base AT commands
* Sokets, HTTP/HTTPS
* MQTT to the clouds Amazon, Google, Azure, Eclipse

## Thanks to

* Ivan Kravets - [PlatformIO](https://platformio.org/)
* [comet.bg](https://www.comet.bg/?cid=92)

## Used source codes from

* [Core Arduino](https://github.com/arduino/Arduino)
* [Google Cloud Platform](https://github.com/GoogleCloudPlatform/google-cloud-iot-arduino)
* [Amazon AWS](https://github.com/aws)
* [Microsoft Azure](https://github.com/Azure)
* [Eclipse mosquitto](https://github.com/eclipse/mosquitto)
* [openSSL](https://github.com/openssl/openssl)
* [Esp32](https://github.com/espressif/arduino-esp32)
* [RasPiArduino](https://github.com/me-no-dev/RasPiArduino)
* [Adafruit](https://github.com/adafruit)


## Support links

* https://community.platformio.org
* https://www.comet.bg/?cid=92



>If you want to help / support:   
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)
