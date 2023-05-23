from pprint import pprint

import certifi as certifi
import pymongo as pym

MOCK_DATA = [
    {
        'nome': 'Fulano da Silva',
        'cpf': '111.111.111-11',
        'endereco': 'Rua Sem Saida, 123, Fim do Mundo',
        'conta': [
            {
                'agencia': '0001',
                'numero': 1234,
                'saldo': 1000,
            },
        ],
    },
    {
        'nome': 'Ciclano de Sousa',
        'cpf': '123.123.123-12',
        'endereco': 'Rua do Fim, 321, Mundo do Fim',
        'conta': [
            {
                'agencia': '0001',
                'numero': 9999,
            },
            {
                'tipo': 'Poupança',
                'agencia': '0001',
                'numero': 51009999,
                'saldo': 300.00,
            },
        ],
    },
    {
        'nome': 'Beltrano de Oliveira',
        'cpf': '123.456.789-00',
        'endereco': 'Rua do Avesso, 999, Mundo Invertido',
        'conta': [
            {
                'agencia': '0001',
                'numero': 4321,
                'saldo': 30,
            },
        ],
    }
]


USERNAME = '<username>'
PASSWORD = '<password>'
MONGODB_CLUSTER_URI = '<clustername>.<clusteraddress>.mongodb.net'
DATABASE = '<database>'

MONGO_DB_URI = f'mongodb+srv://{USERNAME}:{PASSWORD}@{MONGODB_CLUSTER_URI}/' \
               f'{DATABASE}?retryWrites=true&w=majority'
client = pym.MongoClient(MONGO_DB_URI, tlsCAFile=certifi.where())

db = client.get_database()
print(db.name)


def populates_clients_db(database):
    clients = database.create_collection(name='clientes')
    client_ids = clients.insert_many(MOCK_DATA)
    print(client_ids.inserted_ids())


print(db.list_collection_names())

clients = db.get_collection(name="clientes")
pprint(clients.find_one({'nome': 'Ciclano de Sousa'}))
for item in clients.find():
    pprint(item)

print(clients.count_documents(filter={'cpf': '111.111.111-11'}))
