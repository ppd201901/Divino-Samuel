import Pyro4
import Pyro4.util
import sys

sys.excepthook = Pyro4.util.excepthook

class Client:

    def __init__(self, remoteObj):
        self.remoteObj = remoteObj

    def start(self):
        name = input("Digite o nome do Funcionario : ").strip()
        office = input("Digite funcao do mesmo : ").strip()
        salary = int(input("Digite o salário : ").strip())

        self.remoteObj.store(name, office, salary)
        self.new_value = self.remoteObj.update()

    def show(self):
        self.remoteObj.show()
        name , cargo , sal = self.remoteObj.take()[-1]
        print("Nome -> {0} Cargo -> {1} NovoSalario = {2}".format(name, cargo, sal))

def connect():

    proxy = Pyro4.Proxy("PYRONAME:projeto1.employee")
    if not proxy:
        raise ValueError("no object remote avaliable")
    return proxy

def main():
    proxy = connect()
    client = Client(proxy)

    while True:
        client.start()
        client.show()

if __name__ == "__main__":
    main()
