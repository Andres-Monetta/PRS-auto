#!/usr/bin/python

# importo rutinas para trabajar con el sistema operativo
import os
from os import listdir
from os.path import isfile, join

# importo rutinas de expresiones regulares
import re

# genero los paths para los directorios base
script_dir = os.path.dirname(__file__)
data_path  = "data"
abs_file_path = os.path.join(script_dir, data_path)

# declaro los paths para los dos archivos
rcv_path = os.path.join(abs_file_path, 'last-image-rcv')
prs_path = os.path.join(abs_file_path, 'last-image-prs')

# abro los dos archivos para trabajar con ellos
# el primero es de solo lectura, y el segundo es de lectura escritura
ultima_recibida  = open(rcv_path, 'r')
ultima_procesada = open(prs_path, 'r+')

# para cada linea del archivo, la imprimo
for line in ultima_recibida:
  print line
  # tomo la linea y genero un arreglo con sus palabras
  rcv_split = line.split(".")
# for

# para cada linea del archivo, la imprimo
for line in ultima_procesada:
  print line
  # tomo la linea y genero un arreglo con sus palabras
  prs_split = line.split(".")
# for

# 2016.09.245.163507
# 2016.09.244.163507

print rcv_split
print prs_split

# rcv_split[1] y prs_split[1] es el año
# si prs[año] es menor estricto que rcv[año]
#   genero los años que faltan entre medio
#   desde prs[año] hasta rcv[año] voy metiendo los valores en un arreglo
#   pj prs[año]=2011, rcv[año]=2015, años = [2011, 2012, 2013, 2014, 2015]

# Luego repito para el mes

# y por ultimo hago un for doble anidado, por año y mes, para generar los paths

# luego, para cada path ...

pattern = re.compile(".*prs.*")

# listo solo los archivos del path elegido y que cumplen la expresion regular
files_in_dir = [f for f in listdir(abs_file_path)
                if isfile(join(abs_file_path, f)) and
                pattern.match(f)
               ] # for f in

print files_in_dir
