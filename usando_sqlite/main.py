from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

Base = declarative_base()


# Definição da tabela de clientes
class Cliente(Base):
    __tablename__ = "clientes"
    # Atributos da classe Cliente
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False)
    endereco = Column(String(50), nullable=False)

    conta = relationship(
        "Conta", back_populates="cliente"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


# Definição da tabela de contas
class Conta(Base):
    __tablename__ = "contas"
    # Atributos da classe Conta
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, default="Conta-corrente")
    agencia = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    saldo = Column(Float(asdecimal=True), nullable=False, default=0)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship(
        "Cliente", back_populates="conta"
    )

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero={self.numero}, saldo={self.saldo})"


MOCK_DATA = [
    Cliente(
        nome='Fulano da Silva',
        cpf='111.111.111-11',
        endereco='Rua Sem Saida, 123, Fim do Mundo',
        conta=[
            Conta(
                agencia='0001',
                numero=1234,
                saldo=1000,
            )
        ]
    ),
    Cliente(
        nome='Ciclano de Sousa',
        cpf='123.123.123-12',
        endereco='Rua do Fim, 321, Mundo do Fim',
        conta=[
            Conta(
                agencia='0001',
                numero=9999,
            ),
            Conta(
                tipo='Poupança',
                agencia='0001',
                numero=51009999,
                saldo=300.00,
            )
        ]
    ),
    Cliente(
        nome='Beltrano de Oliveira',
        cpf='123.456.789-00',
        endereco='Rua do Avesso, 999, Mundo Invertido',
        conta=[
            Conta(
                agencia='0001',
                numero=4321,
                saldo=30,
            )
        ]
    ),
]

engine = create_engine("sqlite+pysqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all(MOCK_DATA)
    session.commit()

stmts = [
    {
        "msg": "Recuperando clientes a partir de condição de filtragem",
        "stmt": select(Cliente).where(Cliente.nome.in_(['Fulano da Silva', 'Beltrano de Oliveira'])),
    },
    {
        "msg": "Recuperando contas de Ciclano de Sousa",
        "stmt": select(Conta).where(Conta.id_cliente.in_([2])),
    },
    {
        "msg": "Recuperando informações de maneira ordenada",
        "stmt": select(Conta).order_by(Conta.numero.asc()),
    },
    {
        "msg": "Recuperando informações cruzadas",
        "stmt": select(Cliente.cpf, Conta.saldo).join_from(Cliente, Conta),
    },
    {
        "msg": "Total de instâncias em Conta com saldo positivo",
        "stmt": select(func.count('*')).select_from(Conta).filter(Conta.saldo > 0),
    },
]

for item in stmts:
    print(f"\n{item['msg']}")
    # print(f"\n{item['stmt']}") # Descomente essa linha para imprimir os comando em SQL
    for result in session.scalars(item['stmt']):
        print(result)

connection = engine.connect()
results = connection.execute(stmts[3]['stmt']).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)
