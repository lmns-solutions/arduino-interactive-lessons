---
lang: bg
permalink: /signals/step-tracker.html
page_id: signals-step-tracker
layout: default
title: L1&#58; Класификация на базата на хеуристика
parent: Класификация
grand_parent: Сигнали
has_toc: false # (по подразбиране)
comments: false
---

# {{ page.title | replace_first:"L",'Lesson '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

Този [Notebook](StepTracker/index.html) представя хеуристичен подход за изчисляване на стъпки с помощта на акселерометър. Notebook е идеално подходящ за тази задача: лесно е да визуализирате данни с [Matplotlib](https://matplotlib.org/), а [NumPy](https://numpy.org/) и [SciPy](https://www.scipy.org/scipylib/index.html) предлагат филтриране, отстраняване на тенденции и други полезни алгоритми за обработка на сигнали. Можете да опитате много идеи, да видите колко добре работят върху някои тестови данни и след това да приложите най-обещаващата си идея на ESP32.

Можете да видите Notebook в [html тук](StepTracker/index.html), но ние също **силно** препоръчваме да работите с нашите Notebooks локално, като изпълните git clone на `https://github.com/makeabilitylab/signals.git` и стартирате [Jupyter Notebook](https://github.com/makeabilitylab/signals/blob/master/Projects/StepTracker/StepTracker-Exercises.ipynb) на вашата система (вижте [бележките за инсталиране](jupyter-notebook.md)).

## Използване на Google Colab

**Важно е да** знаете, че за да работи бележникът Step Tracker Exercise в Colab, трябва да създадете папка с име `Logs` и да копирате поне един лог файл от [тук](https://github.com/makeabilitylab/signals/tree/master/Projects/StepTracker/Logs). Препоръчвам да започнете с [`arduino_accel_righthoodiepocket_3sets_15steps_delay10_9600baud_subset.csv`] (https://github.com/makeabilitylab/signals/blob/master/Projects/StepTracker/Logs/arduino_accel_righthoodiepocket_3sets_15steps_delay10_9600baud_subset.csv), защото е най-прост. 

За да качите данни в Colab, кликнете върху иконата на папката в лявата странична лента, след това създайте нова папка с име "Logs" и кликнете с десния бутон върху тази папка и изберете "Upload". Накрая изберете файла, който искате да качите:

![Снимка на екрана с качване на данни в Google Colab](assets/images/GoogleColab_UploadingData_Screenshot.png)

След като направите това, можете да запазите проекта в Google Drive и да поканите групата си да сътрудничи и да кодира заедно в Colab notebook.

![Снимка на споделяне и сътрудничество в Google Colab](assets/images/GoogleColab_ShareAndCollaborate_Screenshot.png)

## Следващ урок

В [следващия урок](gesturerec-shape-based.md) ще научите как да създадете разпознавател на жестове въз основа на формата за 3D сигнали от акселерометър.

<span class="fs-6">
[Следващо: Разпознаване на жестове въз основа на формата](gesturerec-shape-based.md){: .btn .btn-outline }
</span>
