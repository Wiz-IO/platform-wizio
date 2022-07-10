## Raspberry Pi Pico RP2040 - PlatformIO ( Pico-SDK & Arduino )

**A few words in the beginning**
* **Due to Raspberry Pi Pico Team's bad attitude towards the project <br>I won't work hard or maybe I won't update fast<br><br>**
* **Version: 1.1.1** The project is a work in progress, there may be bugs...
* [Look here, if there is something new](https://github.com/Wiz-IO/wizio-pico/wiki#last-news) 
* This project is based on [**PICO-SDK**](https://github.com/raspberrypi/pico-sdk)
* **PICO-SDK** _( the file organization has been restructured to be flexible and have a fast compilation )_
* * **default** SDK 1.4.0 ( backup  1.3.1 and 1.2.0 ) 
* * Support and Pico W ( WiFi ) board
* **Frameworks**
* * Baremetal ( pico-sdk, C/C++ ) _baremetal is just a name for pico-sdk here_
* * Arduino ( in progress... )
* **Debug** ( in progress... )
* * [PICOPROBE](https://github.com/Wiz-IO/wizio-pico/wiki/DEBUG#picoprobe) ( Windows for now )
* * CMSIS-DAP [( Windows for now )](https://www.youtube.com/watch?v=SdpsmgRp5Co)
* **Libraries** [FreeRTOS](https://github.com/Wiz-IO/wizio-pico/wiki/COMMON#freertos), FatFS, littlefs ... etc
* Basic **[File System](https://github.com/Wiz-IO/wizio-pico/wiki/COMMON#file-system--vfs--virtual-file-system-)** ( RAM disk, FLASH disk, SD card )
* [**READ WIKI**](https://github.com/Wiz-IO/wizio-pico/wiki/) 
* [Framework code](https://github.com/Wiz-IO/framework-wizio-pico)
* [Baremetal Examples](https://github.com/Wiz-IO/wizio-pico-examples/tree/main/baremetal)
* [Arduino Examples](https://github.com/Wiz-IO/wizio-pico-examples/tree/main/arduino)
* [Video demo - Arduino - TFT ST7789](https://www.youtube.com/watch?v=x8Z4btIwf7M)
* **Systems support**
* * Windows, Linux, Darwin _(if someone is editing the platform they have to take this into account)_


**Notes**
* Please [Re-Install](https://github.com/Wiz-IO/wizio-pico/blob/main/README.md#fast-uninstal--reinstal--do-this-and-install-again) the platform. The project is a work in progress and the platform is installed from here...
* _I am in Home-Office, it's hard for me to test hardwares as SPI, I2C ... etc_

![pico](https://raw.githubusercontent.com/Wiz-IO/LIB/master/pico/a1.jpg)

## Install Platform
_Note: be sure [**git**](https://git-scm.com/downloads) is installed_
* PIO Home > Platforms > Advanced Installation 
* paste https://github.com/Wiz-IO/wizio-pico
* INSTALL

## Uninstall ( fast ) ... Re-Install ( do this and Install again )
* In directory C:\Users\USER_NAME\.platformio\\**platforms**
  * delete folder **wizio-pico** ( builders )
* In directory C:\Users\USER_NAME\.platformio\\**packages**
  * delete folder **framework-wizio-pico** ( sources )
  * delete folder **toolchain-gccarmnoneeabi** (compiler, **may not be 
deleted** )
  * delete folder **tool-wizio-pico** ( tools, picoasm )



![pico](https://raw.githubusercontent.com/Wiz-IO/LIB/master/pico/pio-pico.jpg)
***

## Baremetal - New Project
PlatformIO -> Home -> New
* Enter Project Name - Board search '**WizIO-PICO**' boards - Select **Baremetal**
* Click BUILD and you will have basic project ( from template )
* For CPP project, **rename** main.c **to** main.cpp ( if you delete main file, builder will create new main.c as template )
* Connect Pico as Mass Storage Device
* Open **platformio.ini** and edit your settings
* BUILD / UPLOAD
* [READ WIKI - BAREMETAL](https://github.com/Wiz-IO/wizio-pico/wiki/BAREMETAL)

## Arduino - New Project
PlatformIO -> Home -> New
* Enter Project Name - Board search '**WizIO-PICO**' boards - Select **Arduino**
* Connect Pico as Mass Storage Device
* Open **platformio.ini** and edit your settings
* BUILD / UPLOAD
* [READ WIKI - ARDUINO](https://github.com/Wiz-IO/wizio-pico/wiki/ARDUINO)

### NOTE
IF **PICO_STDIO_USB** is used, the Uploader will try ro reset Pico to boot-uf2 mode without button and USB cable remove

<a href="https://raw.githubusercontent.com/Wiz-IO/LIB/master/pico/pico_pins.svg">
<img src="https://raw.githubusercontent.com/Wiz-IO/LIB/master/pico/pico_pins.svg" alt="Raspberry Pi Pico pin out diagram">
</a>

## Thanks to:
* [Timo Sandmann](https://github.com/tsandmann)
* [Dean Blackketter](https://github.com/blackketter)
* [Ivan Kravets ( PlatformIO )](https://platformio.org/)

![pico](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/ILI9341.jpg)

***

>If you want to help / support:   
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)