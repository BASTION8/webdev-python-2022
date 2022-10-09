# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

from os import access


def get_int_vlan_map(config_filename):
    # два словаря 
    access_vlan = {}
    trunk_vlan = {}
    with open(config_filename) as f:
        for line in f:
            # rstrip - убираем пустые строки
            line = line.rstrip()
            # Если строка начинается с ... то из этой строчки берем 2 слово(интерфейс)
            if line.startswith("interface"):
                interface = line.split()[1]
            # если access vlan в строчке то берем последний элемент из строчки(сам номер интерфейса)
            elif "access vlan" in line:
                access_vlan[interface] = int(line.split()[-1])
            # если trunk allowed в строчке. берем номера интерфейсы в виде списка
            elif "trunk allowed" in line:
                trunk_vlan[interface] = [int(vlan) for vlan in line.split()[-1].split(',')]
        return access_vlan, trunk_vlan


x = get_int_vlan_map("config_sw1.txt")
print(x)