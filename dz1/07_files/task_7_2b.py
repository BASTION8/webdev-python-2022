# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

ignore = ["duplex", "alias", "configuration"]

file_name = "config_sw1.txt"


new_file_name = "new_config_sw1.txt"
# w - открыть файл для записи
with open(file_name) as f, open(new_file_name, "w") as f_new:
    for line in f:
        word_from_file = line.split()
        word_from_file_ingnore = set(word_from_file) & set(ignore)
        if not line.startswith("!") and not word_from_file_ingnore:
            # записать в файл одну строку(добавляет новую)
            f_new.write(line)