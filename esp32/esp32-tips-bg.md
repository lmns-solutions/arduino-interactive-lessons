---
lang: bg
permalink: /esp32/esp32-tips.html
page_id: esp32-esp32-tips
layout: default
title: Съвети за ESP32
parent: ESP32
has_toc: true # (по подразбиране)
usemathjax: true
comments: true
usetocbot: true
nav_order: 9
---
# {{ page.title }}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

Ние сме събрали някои съвети и трикове за ESP32 по-долу.

## Декодиране на грешки в Serial Monitor

ESP32 извежда доста подробни изключения, грешки и следи от стека в Serial Monitor. Например:

```
⸮Guru Meditation Error: Core 1 panic'ed (LoadProhibited).
Изключението не беше обработено. Core 1 register dump:
PC : 0x40080f85 PS : 0x00060530 A0 : 0x800d1a1a A1 : 0x3ffb1f60
A2 : 0x00000009 A3 : 0x00000002 A4 : 0x0800001c A5 : 0x00000003
A6 : 0x00000003 A7 : 0x00000000 A8 : 0x3f401048 A9 : 0xffffffff
A10 : 0xffffffff A11 : 0x00000054 A12 : 0x08000000 A13 : 0x4a000000
A14 : 0xffffffff A15 : 0x00000000 SAR : 0x0000001a EXCCAUSE: 0x0000001c
EXCVADDR: 0xffffffff LBEG : 0x00000000 LEND : 0x00000000 LCOUNT : 0x00000000

ELF файл SHA256: 0000000000000000

Backtrace: 0x40080f85:0x3ffb1f60 0x400d1a17:0x3ffb1f80 0x400d4f2e:0x3ffb1fb0 0x400869bd:0x3ffb1fd0

Рестартиране...
```

За да декодирате тези съобщения, можете да инсталирате [EspExceptionDecoder](https://github.com/me-no-dev/EspExceptionDecoder). Този съвет е предоставен от студента по CSE490 W.Q. Благодарим ви!

### Стъпка 1: Инсталиране на EspExceptionDecoder

Следвайте инструкциите за инсталиране в [README.md](https://github.com/me-no-dev/EspExceptionDecoder).

### Стъпка 2: Изберете "ESP Exception Decoder" от менюто "Tools"

След това отворете Arduino IDE. В менюто "Tools" ще има нова опция, наречена "ESP Exception Decoder". Вижте екранната снимка по-долу.

![](assets/images/ESP32_ESPExceptionDecoder_InToolsMenu.png)
{: .mx-auto .align-center }

**Фигура.** Опцията [EspExceptionDecoder](https://github.com/me-no-dev/EspExceptionDecoder) в менюто "Инструменти" на Arduino IDE.
{: .fs-1 }

### Стъпка 3: Копирайте/поставяйте следата от грешката в стека

Кликването върху тази опция ще отвори нов прозорец, в който можете да копирате/поставите съобщението за грешка:

![](assets/images/ESP32_ESPExceptionDecoder_PasteStackTrace.png)
{: .mx-auto .align-center }

**Фигура.** Прозорецът [EspExceptionDecoder](https://github.com/me-no-dev/EspExceptionDecoder) в Arduino IDE.
{: .fs-1 }

Когато поставихме следата от стека от по-горе, декодерът на изключения генерира следното съобщение:

```
PC: 0x40080f85: __pinMode в /Users/user/Library/Arduino15/packages/esp32/hardware/esp32/1.0.6/cores/esp32/esp32-hal-gpio.c ред 115
EXCVADDR: 0xffffffff

Резултати от декодиране на стека
0x40080f85: __pinMode в /Users/user/Library/Arduino15/packages/esp32/hardware/esp32/1.0.6/cores/esp32/esp32-hal-gpio.c ред 115
0x400d1a17: showLoadScreen() в /Users/user/Desktop/GitProjects/490f-playground/BreakIt32/BreakIt32.ino ред 525
0x400d4f2e: spiInitBus в /Users/user/Library/Arduino15/packages/esp32/hardware/esp32/1.0.6/cores/esp32/esp32-hal-spi.c ред 396
0x400869bd: vPortTaskWrapper в /home/runner/work/esp32-arduino-lib-builder/esp32-arduino-lib-builder/esp-idf/components/freertos/port.c ред 143
```

В този конкретен случай съобщението посочва, че има грешка в ред 525 от кода на потребителя в метода showLoadScreen(). Действително, след проучване, студентът установи, че е използвал грешен номер на пин и коригира това, като преразгледа диаграмата на пиновете на Huzzah32 и актуализира пина.
