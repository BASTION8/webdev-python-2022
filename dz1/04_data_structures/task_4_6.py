# -*- coding: utf-8 -*-
"""
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.
"""

ospf_route = "      10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
# Разделяем по пробелу
config = ospf_route.split()
print(ospf_route)
print ('Prefix\t\t\t',config[0])
print ('AD/Metric\t\t',config[1])
# -1 - без последнего символа (,)
print ('Next-Hop\t\t',config[3][:-1])
# -1 - без последнего символа (,)
print ('Last update\t\t',config[4][:-1])
print ('Outbound Interface\t',config[5])
