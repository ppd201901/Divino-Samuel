import json

class Message:

    def __init__(self, name=None, sensor=None,  uuid=None, dados=None, tipo=None):

        self.topic = name
        self.exchange = sensor
        self.uuid = uuid
        self.dados = dados
        self.tipo = tipo

        self.mydict = {'topic': self.topic, 'exchange': self.exchange, 'id': self.uuid, 'tipo': tipo, 'payload': self.dados}

    def _jsonDump(self):
        return json.dumps(self.mydict)
