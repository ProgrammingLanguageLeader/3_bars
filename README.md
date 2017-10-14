# The Closest Bars

A program which finds the biggest, the smallest or the nearest bar in Moscow.

# How to use

This script requires Python 3.5 (or higher) installed on your machine

A launching on Linux:

```bash
# possibly requires call of python3 executive instead of just python
$ python bars.py data.json 
Enter a longitude and a latitude: 37.657179 55.758637
The biggest bar
Name:          Спорт бар «Красная машина»
Address:       Автозаводская улица, дом 23, строение 1
Phone number:  (905) 795-15-84
The smallest bar
Name:          Сушистор
Address:       Михалковская улица, дом 8
Phone number:  (495) 230-00-00
The closest bar
Name:          Каро фильм
Address:       улица Земляной Вал, дом 33
Phone number:  (495) 970-17-80
```

The launch on Windows is similar.

To download a file containing JSON information about bars use the following command
```bash
# possibly requires call of python3 executive instead of just python
$ python download_bars_data.py data.json
```
Note, that you have to set **_MOS_RU_API_KEY_** environment variable to download using this script.
To recieve API key visit [Open Data Portal API](https://apidata.mos.ru/) site.

Example of setting the enviromnent on Linux:
```bash
$ export MOS_RU_API_KEY=<your API key>
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
