import Pyro4
import time

@Pyro4.expose
class Employee:

    def __init__(self):

        self.infos = []

        self.name = ''
        self._office = ''
        self._salary = 0.0

    def __str__(self):
        return '{} -> {} -> {}\n'.format(self.name, self.office, self.salary)

    @property
    def office(self):
        return self._office

    @office.setter
    def office(self, office):
        if office.upper() in ['OPERADOR', 'PROGRAMADOR']:
            self._office = office.upper()
        else:
            raise

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, salary):
        if salary >= 0:
            self._salary = salary
        else:
            raise

    def store(self, name, office, salary):
        self.name = name
        self._salary = salary
        self._office = office.upper()

        self.infos.append([self.name, self._office, self._salary])

    def take(self):
        return self.infos
    
    def update(self):

        offices = {'OPERADOR': lambda salary : salary * 1.2,
                   'PROGRAMADOR': lambda salary : salary * 1.18}
        new_sal = offices[self.office](self.salary)
        self.infos[-1][2] = new_sal

        print('Novo Salario igual : {}'.format(new_sal))

        return new_sal

    def show(self):
        for i in self.infos:
            print("Nome: {0} Cargo: {1} Salario: {2:10.4f}".format(i[0], i[1], i[2]))

def main():
    Pyro4.Daemon.serveSimple(
        {
            Employee: "projeto1.employee"
        },
        ns = True
    )

'''
def main():

    employee = Employee()
    with Pyro4.Daemon() as daemon:
        request = daemon.register(employee)

        with Pyro4.locateNS() as ns:
            ns.register("projeto1.employee.", request)

        print("Server ready ...")
        daemon.requestLoop()

'''

if __name__ == '__main__':
    main()
