---
permalink: /advancedio/
page_id: advancedio-index
layout: default
title: Advanced I/O
nav_order: 3
has_toc: false # on by default
has_children: true
comments: true
usetocbot: true
---
# {{ page.title }}
{: .no_toc }

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}
---

Welcome 👋 to the third module in your Physical Computing adventure: **Advanced I/O**. Do not be intimidated by the **advanced** prefix. The content here is not more complicated than the first two modules, though they do build on them:
1. {% include tlink.html id='electronics-index' text='Introduction to Electronics' %}
2. {% include tlink.html id='arduino-index' text='Introduction to Microcontrollers Using Arduino' %}

As usual, these lessons are interactive—that is, they assume that you're following along and building **with us**. They are designed to be completed **in order**. All Arduino code is open source and in this [GitHub repository](https://github.com/makeabilitylab/arduino).

## Output

### {% include tlink.html id='advancedio-oled' text='L1: OLED Displays' %}
In {% include tlink.html id='advancedio-oled' text='this lesson' %}, you will learn about organic light-emitting diode (OLED) displays, basic graphics programming, and a brief introduction to two serial communication protocols called [I<sup>2</sup>C](https://en.wikipedia.org/wiki/I%C2%B2C) (Inter-Integrated Circuit) and [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) (Serial Peripheral Interface).

### {% include tlink.html id='advancedio-vibromotor' text='L2: Vibromotors' %}
In {% include tlink.html id='advancedio-vibromotor' text='this lesson' %}, you will learn about vibration motors (vibromotors), their role in haptic technology, and how to connect them with microcontrollers.

## Input

### {% include tlink.html id='advancedio-smoothing-input' text='L1: Smoothing Input' %}

In {% include tlink.html id='advancedio-smoothing-input' text='this lesson' %}, we will learn how to smooth incoming sensor data using basic digital signal processing. We'll cover a class of digital filters called smoothing algorithms (aka **signal filters**), why they're helpful, and potential tradeoffs in their implementation and use.

<!-- ## Output:
### L1: Vibro motors
### L3: OLED Displays
### L3: Servo motors
### L4: RGB LED Neopixels and beyond

## Input
### L1: Smoothing Input
### L2: Microphones
### L4: accelerometer?
### Joystick?
### L3: Hall effect sensors
### L4: Ultrasonic distance sensor
### L5: Interrupts -->

<!-- ## Computer Communication
L1: Using Arduino as a keyboard or mouse 
L2: Using Serial and parsing with Processing or Python
L3: Web Serial
L4: Node.js -->
