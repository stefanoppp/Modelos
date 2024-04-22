from variables import *
def perdida():
    perdida=indice_conductividad*sup/espesor
    return perdida
if __name__ == "__main__":
    print(perdida())