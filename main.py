# Задание №1
import zipfile
import hashlib
import requests
import re
import os
import csv


arch_file = 'C:\\Users\\1162\\Desktop\\Papka\\директорий для первой лабы\\'  # путь к архиву
test_zip = zipfile.ZipFile(arch_file + 'tiff-4.2.0_lab1.zip')

#Просмотр содержимого архива
test_zip_files = test_zip.namelist()
print(test_zip_files)




current_directory = os.getcwd()
test_zip.extractall(current_directory + "\\Test_folder")


txt_files = []
directory_to_extract_to = 'Test_folder'
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        if file.endswith('.txt'):
            txt_files.append(os.path.join(root, file))
print(txt_files)

print("Значения хеша для всех файлов тхт")
for file in txt_files:
    # Чтение файла
    target_file_data = open(file, 'rb').read() # было битовое считывание
    # Получение MD5 хеша
    result = hashlib.md5(target_file_data).hexdigest()
    print(result)
# Задание №3
print("Найти файл MD5 хеш которого равен target_hash")
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
# target_hash = "5abeabc600bac08d641612b14cf66dae" # файл READ.txt
target_file = ''
target_file_data = ''  # содержимое искомого файла

for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        target_file_data_current = open(root + '\\' + file, 'rb').read()
        # Unicode-objects must be encoded before hashing
        result = hashlib.md5(target_file_data_current).hexdigest()
        if result == target_hash:
            target_file = file
            target_file_data = target_file_data_current
print(target_file)
print(target_file_data)



r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы
counter = 0
headers = []

lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
headers = re.sub("<.*?>", " ", lines[0])
headers = re.sub("\  +", " ", headers)
del lines[0]
ln = len(lines)-1

for line in lines:
        temp = re.sub("<.*?>", ';', line)

        temp = re.sub(r'\(.+?\)', '', temp)

        temp = re.sub(r'/\xF0\x9F\x93\x9D/u', '', temp)

        temp = re.sub("\;+",';', temp)

        temp = temp.strip(";")

        tmp_split = temp.split(";")

        if counter != ln:
            country_name = tmp_split[0]
            country_name = country_name[country_name.find(" ") + 1:]
            country_name = country_name[1:]
        else:
            del tmp_split[0]
            country_name = tmp_split[0]

        """
        if tmp_split[3] == '0*':
            tmp_split[3] = 0
        if tmp_split[3] != '0' and tmp_split[3] != 0:
            tmp_split[3] = re.sub('\xa0', "", tmp_split[3])
        """
        if tmp_split[3] == '_':
            tmp_split[3] = '0%'
        #if tmp_split[4] != -1:
         #   tmp_split[4] = re.sub('\xa0', "", tmp_split[4])

        col1_val = int(re.sub('\xa0', "", tmp_split[1]))
        col2_val = int(re.sub('\xa0', "", tmp_split[2]))
        col3_val = str(re.sub('\xa0', "", tmp_split[3]))


        result_dct.update({country_name: (col1_val, col2_val, col3_val)})
        """
        for key, value in result_dct.items():
            print(key, ':', value)
        """

        output = open('data.csv', 'w')
        output.write(headers)
        output.write('\n')
        for key, value in result_dct.items():
            output.write(key)
            output.write(" ; ")
            output.write(str(value))
            output.write('\n')
        counter += 1


target_country = input("Введите название страны: ")
print(result_dct[target_country][0], result_dct[target_country][1], result_dct[target_country][2])
output.close()