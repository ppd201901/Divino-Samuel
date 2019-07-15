import  pika

class RabbitMQ:

    def __init__(self, **kargs ):

        login,password = kargs.get('login'), kargs.get('password')

        if login:
            self.login = login
        else:
            self.login = 'admin'

        if password:
            self.password = password
        else:
            self.password = 'password'

        self.credentials = self.login, self.password

        server = kargs.get('server')
        if server:
            self.server = server
        else:
            raise pika.exceptions.AuthenticationError

        exchange = kargs.get('exchange')
        if exchange:
            self.exchange = exchange
        else:
            self.exchange =''

        routingkey = kargs.get('routingkey')
        if(routingkey):
            self.routingKey = routingkey
        else:
            self.routingKey=""

        self.credentials = pika.PlainCredentials(self.login, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server, credentials=self.credentials))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')
        self.queue = self.channel.queue_declare(queue=self.routingKey, durable=True)
        self.channel.queue_bind(exchange=self.exchange, queue= routingkey, routing_key=routingkey )

    def publish(self, msg):

        #connection, channel, queue = self.makeChannel()

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routingKey,
            body=msg,
            properties=pika.BasicProperties(delivery_mode=2,))

        self.connection.close()
