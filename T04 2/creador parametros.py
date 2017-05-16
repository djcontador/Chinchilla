import csv

matriz_nota_esperada = {'header': "(1.1-3.9), (4.0-5.9), (6.0-6.9), (7.0-7.0)",
                        '1': "(0-3), (3-5), (5-7), (7-8)",
                        '2': "(0-4), (4-7), (7-8), (8-9)",
                        '3': "(0-2), (2-5), (5-7), (7-8)",
                        '4': "(0-3), (4-6), (6-8), (8-9)",
                        '5': "(0-4), (4-8), (8-9), (9-10)",
                        '6': "(0-5), (5-8), (8-10), (10-11)",
                        '7': "(0-4), (4-7), (7-9), (9-10)",
                        '8': "(0-3), (3-6), (6-8), (8-9)",
                        '9': "(0-2), (2-5), (5-7), (7-8)",
                        '10': "(0-5), (5-8), (8-10), (10-11)",
                        '11': "(0-3), (3-6), (6-8), (8-9)",
                        '12': "(0-3), (3-8), (8-9), (9-10)"}

with open('parametros_nota_esperada.csv', 'w') as csvfile:
    fieldnames = ['1', '5', '12', '6', 'header', '11', '10', '3', '4', '2', '7', '9', '8']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(matriz_nota_esperada)


dificultad = {'1': 2, '2': 2, '3': 3, '4': 5, '5': 7, '6': 10,
                      '7': 7, '8': 9, '9': 1, '10': 6, '11': 6, '12': 5}

with open('parametros_dificultad.csv', 'w') as csvfile:
    fieldnames = ['1', '5', '12', '6', '11', '10', '3', '4', '2', '7', '9', '8']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(dificultad)

