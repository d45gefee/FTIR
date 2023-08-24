# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 09:57:19 2023

@author: User
"""

def generar_columnas(documento):
    columnas = []
    p = []

    for fila in documento:
        puntos = [i for i, caracter in enumerate(fila) if caracter == '.']
        num_puntos = len(puntos)
        p.append(puntos)

        if num_puntos == 0:
            columnas.append([fila])
        else:
            columnas_fila = []
            inicio = 0

            for i in range(num_puntos):
                punto = puntos[i]
                columna = fila[inicio:punto]
                columnas_fila.append(columna)
                inicio = punto - i - 1

            columna_final = fila[inicio:]
            columnas_fila.append(columna_final)

            columnas.append(columnas_fila)

    col = []
    for i in range(len(documento)):
        fila = documento[i]
        col0 = fila[0:(p[i][0]-1)]
        col1 = fila[(p[i][0]-1):(p[i][1]-1)]
        col2 = fila[(p[i][1]-1):(p[i][2]-2)]
        col3 = fila[(p[i][2]-2):(p[i][3]-1)]
        col4 = fila[(p[i][3]-1):]
        col.append((col0, col1, col2, col3,col4))

    return columnas, p, col

archivo = open("dipole.txt", "r")
fila_Angles = None
lineas = archivo.readlines()
archivo.close()

resultado,p,col = generar_columnas(lineas)

# Eliminar guiones ("-") de col
col = [[columna.replace("-", "") for columna in fila] for fila in col]

col = [[float(columna) for columna in fila] for fila in col]

# Multiplicar tercera fila de col por -1
for i in range(len(col)):
    col[i][3]=-1* col[i][3]

# nombre_archivo = "col.txt"
# with open(nombre_archivo, "w") as archivo:
#     for fila in col:
#         archivo.write("\t".join(fila) + "\n")

nombre_archivo = "col.txt"
with open(nombre_archivo, "w") as archivo:
    for fila in col:
        if isinstance(fila, str):
            archivo.write(fila + "\n")
        else:
            archivo.write("\t".join(repr(valor) for valor in fila) + "\n")
