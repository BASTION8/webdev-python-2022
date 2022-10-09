# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
template = '''
Prefix               {Prefix}
AD/Metri             {AD_Metric} 
Next-Hop             {Next_Hop} 
Last update          {Last_update}
Outbound Interface   {Outbound_Interface} 
'''

# open - открытие файла. ospf.txt - имя файла. r - ружим открытия файла(открыть файл только для чтения)

with open("ospf.txt", "r") as f:
  # По каждой строчке
  for line in f:
    # Разделяем строчку по пробелу
    ospf_route_list = line.split()
    # помещаем в переменную значение строк
    # strip - избавиться от символов  
    result = {'Prefix': ospf_route_list[1],
          'AD_Metric': ospf_route_list[2].strip("[]"),
          'Next_Hop': ospf_route_list[4].strip(','),
          'Last_update': ospf_route_list[5].strip(','),
          'Outbound_Interface': ospf_route_list[6]}
  print(template.format(**result))
