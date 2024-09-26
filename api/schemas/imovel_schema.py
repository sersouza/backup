from pydantic import BaseModel
from typing import Optional, List
from model.imovel import Imovel, Region
import json
import numpy as np


class ImovelSchema(BaseModel):
    """Define como um novo imóvel a ser inserido deve ser representado"""

    owner_name: str = "Maria"
    bathrooms: int
    bedrooms: int
    accommodates: int
    beds: int
    availability_365: int
    region: Region


class ImovelViewSchema(BaseModel):
    """Define como um imóvel será retornado"""

    id: int = 1
    owner_name: str = "Maria"
    bathrooms: int
    bedrooms: int
    accommodates: int
    beds: int
    availability_365: int
    region: Region
    outcome: float = None


class ImovelBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do proprietário do imóvel.
    """

    owner_name: str = "Maria"


class ListaImoveisSchema(BaseModel):
    """Define como uma lista de imoveis será representada"""

    imoveis: List[ImovelSchema]


class ImovelDelSchema(BaseModel):
    """Define como um imóvel para deleção será representado"""

    owner_name: str = "Maria"


# Apresenta apenas os dados de um imóvel
def apresenta_imovel(imovel: Imovel):
    """Retorna uma representação do imóvel seguindo o schema definido em
    ImovelViewSchema.
    """
    return {
        "id": imovel.id,
        "owner_name": imovel.owner_name,
        "bathrooms": imovel.bathrooms,
        "bedrooms": imovel.bedrooms,
        "accommodates": imovel.accommodates,
        "beds": imovel.beds,
        "availability_365": imovel.availability_365,
        "region": imovel.region.name,
        "outcome": imovel.outcome,
    }


# Apresenta uma lista de imoveis
def apresenta_imoveis(imoveis: List[Imovel]):
    """Retorna uma representação do imóvel seguindo o schema definido em
    ImovelViewSchema.
    """
    result = []
    for imovel in imoveis:
        result.append(
            {
                "id": imovel.id,
                "owner_name": imovel.owner_name,
                "bathrooms": imovel.bathrooms,
                "bedrooms": imovel.bedrooms,
                "accommodates": imovel.accommodates,
                "beds": imovel.beds,
                "availability_365": imovel.availability_365,
                "region": imovel.region.name,
                "outcome": imovel.outcome,
            }
        )

    return {"imoveis": result}
