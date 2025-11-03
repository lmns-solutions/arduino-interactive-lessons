---
permalink: /esp32/
page_id: esp32-index
layout: default
title: ESP32
nav_order: 6
has_toc: false # on by default
has_children: true
nav_exclude: false
usetocbot: true
---
# {{ page.title }}
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}
---

![A collage of ESP32 boards](assets/images/ESP32Variants_FromS1-S3.png)
**Figure.** The [ESP32](https://www.espressif.com/en/products/socs/esp32) has quickly become **the** platform to learn and use for IoT projects. The ESP32s are fast, have WiFi and Bluetooth, and many are around $10 USD! And the best part is: you can program them with Arduino! So, all of your learning from {% include tlink.html id='arduino-index' text='previous lessons' %} can be applied here!
{: .fs-1 }

These tutorials are interactive and designed to be completed **in order**. All ESP32 code is open source and in this [GitHub repository](https://github.com/makeabilitylab/arduino/tree/master/ESP32).

{: .note }
If this is your first time on our website, welcome 👋🏽! The following ESP32 lessons assume that you have completed both our {% include tlink.html id='electronics-index' text='Intro to Electronics' %} and {% include tlink.html id='arduino-index' text='Intro to Arduino' %} tutorial series. While not absolutely necessary, we recommend you start there!

<!-- TODO: add in link to Tinkercad circuits here... -->

## {% include tlink.html id='esp32-esp32' text='Lesson 1: Introduction to the ESP32' %}

In {% include tlink.html id='esp32-esp32' text='this lesson' %}, you'll learn about the ESP32, how it differs from and relates to the Arduino platform, and how to program and use the Huzzah32 ESP32 board.

## {% include tlink.html id='esp32-led-blink' text='Lesson 2: Blinking an LED' %}

Introduces how to program the ESP32 using the Arduino IDE and ESP32 Arduino library ({% include tlink.html id='esp32-led-blink' text='link' %})

## {% include tlink.html id='esp32-led-fade' text='Lesson 3: Fading an LED with PWM' %}

In this {% include tlink.html id='esp32-led-fade' text='lesson' %}, you'll learn how to use PWM output on the ESP32 to fade an LED on and off. The ESP32 Arduino library does not have an `analogWrite` method, so you'll learn how to use PWM via an alternative method.

## {% include tlink.html id='esp32-pot-fade' text='Lesson 4: Analog Input' %}

In this {% include tlink.html id='esp32-pot-fade' text='lesson' %}, you'll learn how to use analog input on the ESP32 by building a potentiometer-based LED fader.

## {% include tlink.html id='esp32-tone' text='Lesson 5: Playing Tones' %}

 Arduino's [`tone()`](https://www.arduino.cc/reference/en/language/functions/advanced-io/tone/) method is not supported on the ESP32. In this {% include tlink.html id='esp32-tone' text='lesson' %}, you'll learn how to play tones using the `ledcWriteTone` and `ledcWriteNote` in [esp32-hal-ledc.c](https://github.com/espressif/arduino-esp32/blob/master/cores/esp32/esp32-hal-ledc.c).

## {% include tlink.html id='esp32-capacitive-touch-sensing' text='Lesson 6: Capacitive Touch Sensing' %}

The ESP32 has built-in circuitry and software for capacitive touch sensing ([docs](https://github.com/espressif/esp-iot-solution/blob/master/documents/touch_pad_solution/touch_sensor_design_en.md#1-introduction-to-touch-sensor-system)). In {% include tlink.html id='esp32-capacitive-touch-sensing' text='this lesson' %}, we’ll use the touch sensing functionality to turn on an LED.

## {% include tlink.html id='esp32-iot' text='Lesson 7: Internet of Things' %}

The ESP32 is exciting not just because of its speed, memory, and GPIO capabilities but also because it is truly a modern Internet of Things (IoT) board with Wi-Fi and Bluetooth support. In this lesson, we'll learn how to use WiFi and the IoT platform [Adafruit IO](https://learn.adafruit.com/welcome-to-adafruit-io) to upload sensor data in real-time.
