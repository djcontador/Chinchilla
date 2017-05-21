from Simulacion import Semestre
from lector_parametros import Variables
from lector_escenarios import Escenarios
variable = Variables()
escenario = Escenarios()
print(variable)
print(escenario.escenarios)
print("caca")

#simulacion = Semestre()

menu = dict()
menu['1']="Add Student."
menu['2']="Delete Student."
menu['3']="Find Student"
menu['4']="Exit"
while True:
    options=menu.keys()

    for entry in options:
      print(entry, menu[entry])

    selection=input("Please Select:")
    if selection =='1':
      print("add")
    elif selection == '2':
      print("delete")
    elif selection == '3':
      print("find")
    elif selection == '4':
      break
    else:
      print("Unknown Option Selected!")