#!/usr/bin/python

# importo el modulo funciones
import funciones
from datetime import date, timedelta, datetime

# importo rutinas para trabajar con el sistema operativo
import os
from   os      import listdir
from   os.path import isfile, join

# importo rutinas de expresiones regulares
import re

#########################################
#########################################
# Defino las rutas a los archivos para poder trabajar con ellos
#########################################

# genero los paths para los directorios base
script_dir    = os.path.dirname(__file__)
data_path     = "data"
abs_file_path = os.path.join(script_dir, data_path)

# declaro los paths para los dos archivos
prs_path = os.path.join(abs_file_path, 'last-image-prs')
rcv_path = os.path.join(abs_file_path, 'last-image-rcv')

# abro los dos archivos para trabajar con ellos
# el primero es de solo lectura, y el segundo es de lectura escritura
ultima_procesada = open(prs_path, 'r+')
ultima_recibida  = open(rcv_path, 'r')

#########################################
#########################################
# Recorro las lineas de los documentos y las imprimo
#########################################

# para cada linea del archivo, la imprimo
for line in ultima_procesada:
  print line
  # tomo la linea y genero un arreglo con sus palabras
  prs_split = line.split(".")
# for

# para cada linea del archivo, la imprimo
for line in ultima_recibida:
  print line
  # tomo la linea y genero un arreglo con sus palabras
  rcv_split = line.split(".")
# for

#########################################
#########################################
# Realizo operaciones de impresion en pantalla para ver los parametros
#########################################

print prs_split
print rcv_split

prs_year  = int(prs_split[0]) # la primer palabra del arreglo es el ano
prs_month = int(prs_split[1]) # la segunda palabra del arreglo es el mes
prs_doy   = int(prs_split[2]) # la tercera palabra del arreglo es el doy
prs_hms   = prs_split[3]      # la cuarta palabra del arreglo es la hora-minuto-segundo

st_hour   = int(prs_hms[0:2])
st_min    = int(prs_hms[2:4])
st_scnd   = int(prs_hms[4:6])

rcv_year  = int(rcv_split[0]) # la primer palabra del arreglo es el ano
rcv_month = int(rcv_split[1]) # la segunda palabra del arreglo es el mes
rcv_doy   = int(rcv_split[2]) # la tercera palabra del arreglo es el doy
rcv_hms   = rcv_split[3]      # la cuarta palabra del arreglo es la hora-minuto-segundo

en_hour    = int(rcv_hms[0:2])
en_min     = int(rcv_hms[2:4])
en_scnd    = int(rcv_hms[4:6])

#########################################
#########################################
# Genero los datatypes date para iterar entre ellos y leo las carpetas
#########################################

# genero los numeros enteros para realizar el chequeo de archivos que quiero
#            ano                mes            doy            hora+minuto+segundo
start_timestamp = int(prs_split[0] + prs_split[1] + prs_split[2] + prs_hms)
end_timestamp   = int(rcv_split[0] + rcv_split[1] + rcv_split[2] + rcv_hms)

print start_timestamp
print end_timestamp

path_list = []

# hago un doble for de anos y meses
# los anos iteran desde el primero hasta el ultimo
for year in range(prs_year, rcv_year + 1):

  primer_mes = 1
  ultimo_mes = 12

  # para el primer ano solo debo iterar desde el mes del archivo
  # y para el ultimo ano solo debo iterar hasta el mes del archivo
  if year == prs_year:
    primer_mes = prs_month
  # if

  if year == rcv_year:
    ultimo_mes = rcv_month
  # if

  for month in range(primer_mes, ultimo_mes + 1):

    # Path a los raw: day[0] = year, day[1] = month (completado con ceros hasta tener dos char)
    path_string = "/sat/raw-sat/" + str(year) + "/" + str(month).zfill(2) + "/"
    data_path   = os.path.abspath(path_string)

    print data_path

    # day[0] = year, day[2] = doy
    # el patron queda .*year\.doy.*\.nc
    string_patron = ".*" + str(year) + "\." + ".*" + "\.nc$"
    pattern       = re.compile(string_patron)

    print string_patron

    for f in listdir(data_path):
      if isfile(join(data_path, f)) and pattern.match(f):
        nombre  = f.split(".")
        ano     = nombre[1]
        mes     = funciones.ymd(int(nombre[1]),int(nombre[2]))[1]
        mes_str = str(mes).zfill(2)
        doy     = nombre[2]
        hms     = nombre[3]
        timestamp = int( ano + mes_str + doy + hms )

        if timestamp > start_timestamp and timestamp <= end_timestamp:
          path_list.extend([f])
        # if

      # if
    # for

  # for month

# for year

for f in sorted(path_list):
  print f
