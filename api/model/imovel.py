import enum
from sqlalchemy import Column, String, Integer, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from model import Base


# Define the enum using Python's enum.Enum
class Region(enum.Enum):
    BARRA_DA_TIJUCA = "barra_da_tijuca"
    BOTAFOGO = "botafogo"
    CAMORIM = "camorim"
    CATETE = "catete"
    CENTRO = "centro"
    COPACABANA = "copacabana"
    FLAMENGO = "flamengo"
    GAVEA = "gavea"
    GLORIA = "gloria"
    HUMAITA = "humaita"
    IPANEMA = "ipanema"
    JACAREPAGUA = "jacarepagua"
    JARDIM_BOTANICO = "jardim_botanico"
    LAGOA = "lagoa"
    LARANJEIRAS = "laranjeiras"
    LEBLON = "leblon"
    LEME = "leme"
    RECREIO_DOS_BANDEIRANTES = "recreio_dos_bandeirantes"
    SANTA_TERESA = "santa_teresa"
    SAO_CONRADO = "sao_conrado"
    TIJUCA = "tijuca"
    VIDIGAL = "vidigal"


class Imovel(Base):
    __tablename__ = "imoveis"

    id = Column(Integer, primary_key=True)
    owner_name = Column("Owner", String, nullable=False)
    bathrooms = Column("Bathrooms", Integer, nullable=False)
    bedrooms = Column("Bedrooms", Integer, nullable=False)
    accommodates = Column("Accommodates", Integer, nullable=False)
    beds = Column("Beds", Integer, nullable=False)
    availability_365 = Column("Availability_365", Integer, nullable=False)
    region = Column(Enum(Region), nullable=False)
    outcome = Column("Price", Float, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(
        self,
        owner_name: str,
        bathrooms: int,
        bedrooms: int,
        accommodates: int,
        beds: int,
        availability_365: int,
        region: Region,
        outcome: float = None,
        data_insercao: Union[datetime, None] = None,
    ):
        """
        Cria um Imóvel

        Arguments:
            owner_name: nome do proprietário
            bathrooms: número de banheiros
            bedrooms: número de quartos
            accommodates: número de acomodações
            beds: número de camas
            availability_365: disponibilidade em 365 dias
            region: região do imóvel
            outcome: preço da diária
            data_insercao: data de inserção (opcional)
        """
        self.owner_name = owner_name
        self.bathrooms = bathrooms
        self.bedrooms = bedrooms
        self.accommodates = accommodates
        self.beds = beds
        self.availability_365 = availability_365
        self.region = region
        self.outcome = outcome

        # Set the insertion date to now if not provided
        self.data_insercao = data_insercao or datetime.now()
