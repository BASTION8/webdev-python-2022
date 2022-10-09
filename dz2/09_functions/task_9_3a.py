# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map(config_filename):
    access_vlan = {}
    trunk_vlan = {}
    with open(config_filename) as f:
        for line in f:
            line = line.rstrip()
            # если начинается с interface Fast записываем номер интерфейса
            if line.startswith("interface Fast"):
                interface = line.split()[1]
                # В словарь с названием интерфейса(ключ) записываем параметр VLAN 1(перезапишем потом если будет access vlan )
                access_vlan[interface] = 1
            elif "access vlan" in line:
                access_vlan[interface] = int(line.split()[-1])
            elif "trunk allowed" in line:
                trunk_vlan[interface] = [int(vlan) for vlan in line.split()[-1].split(',')]
                # удаляем ключ значение из access_vlan 
                del access_vlan[interface]
        return access_vlan, trunk_vlan

# Логика такая: сначала в access vlan записываем все, затем выпиливаем trunk_vlan, чтобы обработать VLAN 1

x = get_int_vlan_map("config_sw2.txt")
print(x)