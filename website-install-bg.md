---
lang: bg
permalink: /website-install.html
page_id: website-install
layout: default
title: Инсталиране на уебсайт
has_toc: false # включено по подразбиране
nav_exclude: true
usetocbot: true
---

# {{ page.title | replace_first:„L“,'Урок '}}
{: .no_toc }

## Съдържание
{: .no_toc .text-delta }

1. Съдържание
{:toc}
---

Този уебсайт е създаден в [Jekyll](https://jekyllrb.com/), който е генератор на статични сайтове, създаден на езика [Ruby](https://www.ruby-lang.org/en/). Не е необходимо да знаете Ruby, за да създавате сайтове с Jekyll, но трябва да знаете [markdown](https://www.markdownguide.org/) и html/css. Ние използваме Jekyll шаблон, наречен [„Just the Docs“](https://pmarsceill.github.io/just-the-docs/).

## Настройка на средата за разработка
По-долу ще ви разведем през настройката на средата за разработка както на Mac, така и на Windows. 

Независимо от платформата, която използвате, първата стъпка е да клонирате [physcomp repo](https://github.com/makeabilitylab/physcomp). Отворете командния ред и изпълнете:

```
> git clone https://github.com/makeabilitylab/physcomp.git`
```

Забележка: Аз използвам [GitHub Desktop](https://desktop.github.com/), което силно препоръчвам. VSCode също има вградена git поддръжка.

### Mac
Инсталирането на необходимите библиотеки и настройването на вашата среда за разработка е лесно на Mac (много по-трудно на Windows).

#### Следвайте официалното ръководство за инсталиране
За MacOS просто следвайте [официалното ръководство за инсталиране](https://jekyllrb.com/docs/installation/macos/). Тъй като трябва да инсталирате средата за разработка XCode, [Homebrew](https://brew.sh/), [Ruby](https://www.ruby-lang.org/en/) и [Jekyll](https://jekyllrb.com/), този процес на инсталиране може да отнеме около 1 час (в зависимост от скоростта на изтегляне).

Следвайте инструкциите за инсталиране внимателно. Аз изпълних всички стъпки, с изключение на [rbenv частта](https://jekyllrb.com/docs/installation/macos/#rbenv) (тъй като използвам Ruby само за Jekyll, няма нужда да избирам между няколко версии на Ruby в моята среда за разработка).

#### Изпълнете „bundle install“ в директорията physcomp
След като завършите последната стъпка в [ръководството за инсталиране на MacOS](https://jekyllrb.com/docs/installation/macos/), която е изпълнение на командата `> sudo gem install -n /usr/local/bin/ jekyll`, отидете в папката `physcomp` и въведете `> bundle install`. Забележка: Аз обикновено правя това от терминала на VSCode.

#### Изпълнете „bundle exec jekyll serve“ в директорията physcomp
Накрая въведете `> bundle exec jekyll serve` в папката `physcomp`. Отново, аз обикновено правя това от терминала на VSCode.

И това е всичко! Надяваме се, че сървърът ще работи на [http://127.0.0.1:4000/physcomp/](http://127.0.0.1:4000/physcomp/).

#### Възможни проблеми
Току-що изпробвах този пълен процес на инсталиране от начало до край и се сблъсках със следния проблем при последната команда:

```
jonf-macbook:physcomp jonf$ bundle exec jekyll serve
Конфигурационен файл: /Users/jonf/Git/physcomp/_config.yml
Източник: /Users/jonf/Git/physcomp
Дестинация: /Users/jonf/Git/physcomp/_site
Инкрементално изграждане: деактивирано. Активирайте с --incremental
Генериране...
 
Отдалечена тема: Използване на тема pmarsceill/just-the-docs
завършено за 17,425 секунди.
Автоматично регенериране: активирано за „/Users/jonf/Git/physcomp“
bundler: не успя да зареди командата: jekyll (/usr/local/lib/ruby/gems/3.0.0/bin/jekyll)

/usr/local/lib/ruby/gems/3.0.0/gems/jekyll-3.9.0/lib/jekyll/commands/serve/servlet.rb:3:in `require': не може да се зареди такъв файл -- webrick (LoadError)
```
Проблемът е, че webrick вече не се предлага с Ruby 3.0. За да разреша този проблем, просто въведох `> bundle add webrick` и след това отново `> bundle exec jekyll serve`. И тогава нещата заработиха!

### Windows

В миналото съм се опитвал да инсталирам Jekyll в Windows, но без успех. За съжаление, това е сложно. Всъщност, на [уебсайта на Jekyll](https://jekyllrb.com/docs/installation/windows/) се казва, че Windows не се поддържа официално:

> Въпреки че Windows не е официално поддържана платформа, тя може да се използва за стартиране на Jekyll с подходящи настройки.
{: .fs-4 }

Ето обаче как в крайна сметка успях да го направя да работи. Тези инструкции са възпроизведени от мен (Джон) и Лианг. Ура!

#### Изтеглете и стартирайте Ruby Installer
**Първо**, въпреки че тази документация е стара, аз започнах с това ръководство [Run Jekyll on Windows](https://jekyll-windows.juthilo.com/). Първата стъпка гласи да инсталирате Ruby чрез уебсайта [rubyinstaller.org](http://rubyinstaller.org/downloads/) и след това да инсталирате Ruby Devkit; обаче най-новите версии на Ruby Installer за Windows също ви позволяват да инсталирате Devkit. Ето какво направих.
 

По-конкретно, изтеглих и инсталирах [Ruby+Devkit 2.7.X (x64) инсталатора](https://rubyinstaller.org/downloads/), който според уебсайта RubyInstaller „предоставя най-голям брой съвместими gems и инсталира MSYS2 Devkit заедно с Ruby, така че gems с C-разширения могат да бъдат компилирани веднага“.

Когато командният прозорец на Ruby Installer ви попита коя опция да инсталирате (вижте екранната снимка по-долу), просто натиснете „Enter“.

![Показва прозорец от Ruby Installer. Просто натиснете Enter](assets/images/RubyInstaller_JustHitEnter.png)
**Фигура.** Когато се появи прозорецът, просто натиснете Enter, за да приемете настройките по подразбиране.
{: .fs-1 }

Възможно е да ви бъде зададен въпрос за втори път. Отново натиснете „Enter“.

![Показва подкана от Ruby Installer. Просто натиснете Enter](assets/images/RubyInstaller_Question2_JustHitEnter.png)
**Фигура.** Ако ви бъде зададен въпрос за втори път, просто натиснете Enter, за да приемете настройките по подразбиране.
{: .fs-1 }

Когато Ruby Installer приключи, той просто изчезва. Така че, преминаваме към следващата стъпка!

#### Изпълнете „gem install jekyll“
**Второ**, след това отворих `Windows Powershell` и въведох `gem install jekyll`:

```
gem install jekyll
Изтегляне на jekyll-4.1.1.gem
Изтегляне на mercenary-0.4.0.gem
Успешно инсталиран mercenary-0.4.0
Успешно инсталиран jekyll-4.1.1
Анализиране на документацията за mercenary-0.4.0
Инсталиране на ri документацията за mercenary-0.4.0
Анализиране на документацията за jekyll-4.1.1
Инсталиране на ri документация за jekyll-4.1.1
Инсталирането на документацията за mercenary, jekyll приключи след 16 секунди
2 инсталирани gems
```

Ето екранна снимка:

![Екранна снимка на командата gem install jekyll](assets/images/GemInstallJekyllScreenshot.png)
**Фигура.** Снимка на PowerShell, изпълняващ командата `gem install jekyll`.
{: .fs-1 }

#### Изпълнете „gem install github-pages“
**Трето**, след това опитах да инсталирам `github-pages` чрез: `gem install github-pages`. Изпълнете:

```
> gem install github-pages
```

Това работи добре на някои от нашите Windows системи, но на други не успява. Ако при вас е успяло, чудесно! Преминете към следващата стъпка. Ако не, проверете грешката по-долу и вижте дали съответства на вашия проблем (или се свържете с нас за помощ и копирайте/поставяйте резултата от грешката в имейла си или в съобщение в Slack).

##### Обработка на грешка при инсталиране на github-pages

```
ГРЕШКА: Грешка при инсталиране на github-pages:
Последната версия на nokogiri (>= 1.10.4, < 2.0), която поддържа вашия Ruby & RubyGems, е 1.10.9. Опитайте да я инсталирате с `gem install nokogiri -v 1.10.9` и след това изпълнете отново текущата команда
nokogiri изисква Ruby версия >= 2.3, < 2.7.dev. Текущата версия на Ruby е 2.7.0.0.
```

Така че опитах:

```
> gem install nokogiri -v 1.10.9
ГРЕШКА: Грешка при инсталирането на nokogiri:
Последната версия на nokogiri (= 1.10.9), която поддържа вашия Ruby & RubyGems, беше 1.10.9. Опитайте да го инсталирате с `gem install nokogiri -v 1.10.9`
nokogiri изисква Ruby версия >= 2.3, < 2.7.dev. Текущата версия на Ruby е 2.7.0.0.
```

Но и това не се получи. И като се има предвид, че нямам представа колко трудно би било да понижа версията на Ruby и дали това би повредило други зависимости, търсих в интернет и намерих този [проблем](https://github.com/sparklemotion/nokogiri/issues/1961) в Nokogiri GitHub. Тогава опитах [това](https://github.com/sparklemotion/nokogiri/issues/1961#issuecomment-581851368):

```
> gem inst nokogiri --pre
Изтегляне на nokogiri-1.11.0.rc2-x64-mingw32.gem
Nokogiri е изграден с пакетираните библиотеки: libxml2-2.9.10, libxslt-1.1.34, zlib-1.2.11, libiconv-1.15.
Успешно инсталиран nokogiri-1.11.0.rc2-x64-mingw32
Анализиране на документацията за nokogiri-1.11.0.rc2-x64-mingw32
Инсталиране на ri документация за nokogiri-1.11.0.rc2-x64-mingw32
Инсталирането на документацията за nokogiri приключи след 10 секунди
1 gem инсталиран
```

Работи. Супер!

Но все още не мога да инсталирам github pages, буу!

```
gem install github-pages
ГРЕШКА: Грешка при инсталирането на github-pages:
Последната версия на nokogiri (>= 1.10.4, < 2.0), която поддържа вашия Ruby & RubyGems, беше 1.10.9. Опитайте да я инсталирате с `gem install nokogiri -v 1.10.9` и след това изпълнете отново текущата команда
nokogiri изисква Ruby версия >= 2.3, < 2.7.dev. Текущата версия на Ruby е 2.7.0.0.
```

Така че просто прескочих до последната стъпка и изпълних `bundle install` и нещата заработиха. Надявам се да помогне и на вас!

#### Изпълнете „bundle install“
![Снимка на командата bundle install](assets/images/BundleInstallScreenshot.png)

От командния ред променете директориите на `physcomp`. На моя компютър:

```
> cd c:\git\physcomp
```

След това изпълнете `bundle install`:

```
C:\git\physcomp> bundle install
Извличане на метаданни за gem от https://rubygems.org/...........
Извличане на метаданни за gem от https://rubygems.org/.
Решаване на зависимости.....
Използване на concurrent-ruby 1.1.8
Използване на i18n 0.9.5
Извличане на minitest 5.14.4
Инсталиране на minitest 5.14.4
...
Използване на github-pages 218
Извличане на wdm 0.1.1
Инсталиране на wdm 0.1.1 с native extensions
Пакетът е готов! 2 зависимости Gemfile, 100 gems са инсталирани.
Използвайте `bundle info [gemname]`, за да видите къде е инсталиран пакетът gem.
```

Успяхте!

## Изпълнение на уебсайта локално

Ако разполагате с необходимите библиотеки и софтуерна инфраструктура (например Jekyll), можете да отворите терминал в VSCode и да въведете:

```
> bundle exec jekyll serve 
```

Уебсайтът трябва да е достъпен на [http://127.0.0.1:4000/physcomp/](http://127.0.0.1:4000/physcomp/).

### Bundle exec не работи в терминала на VSCode

Ако получите грешка като следната, може да се наложи да *рестартирате* компютъра си (не само VSCode).

![](assets/images/BundleExecJekyllServeFailsInVSCodeScreenshot.png)

```
Опитайте новата мултиплатформена PowerShell https://aka.ms/pscore6

PS D:\Git\physcomp> bundle exec jekyll serve 
bundle : Терминът „bundle” не се разпознава като име на cmdlet, функция, скрипт файл или оперативна програма. Проверете 
правописа на името или, ако е включен път, проверете дали пътят е правилен и опитайте отново.
В ред:1 символ:1
+ bundle exec jekyll serve
+ ~~~~~~
+ CategoryInfo : ObjectNotFound: (bundle:String) [], CommandNotFoundException
+ FullyQualifiedErrorId : CommandNotFoundException
```

За да разрешите тази грешка, просто рестартирайте компютъра си, отворете отново VSCode и опитайте отново. Това ми помогна!

## Разработване на уебсайта
1. Изтеглете [VS Code](https://code.visualstudio.com/Download)
2. Отворете папката `physcomp` в VS Code
3. Използвайте markdown, за да създадете нови страници. Ние използваме шаблона Jekyll [„Just the Docs“](https://pmarsceill.github.io/just-the-docs/).
4. Прочетете повече за разработката на уебсайтове [тук](website-dev.md)
