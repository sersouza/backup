from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from model.imovel import Imovel
from schemas.imovel_schema import (
    ImovelBuscaSchema,
    ImovelSchema,
    ImovelViewSchema,
    apresenta_imoveis,
    apresenta_imovel,
)
from model import Session, Imovel, Model
from logger import logger
from schemas import *
from flask_cors import CORS
import numpy as np


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
imovel_tag = Tag(
    name="Imovel",
    description="Adição, visualização, remoção e predição do preço diários de imóveis no Airbnb do RJ",
)


# Rota home
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de imoveis
@app.get(
    "/imoveis",
    tags=[imovel_tag],
    responses={"200": ImovelViewSchema, "404": ErrorSchema},
)
def get_imoveis():
    """Lista todos os imóveis cadastrados na base
    Retorna uma lista de imóveis cadastrados na base.
    """
    session = Session()

    # Buscando todos os imoveis
    imoveis = session.query(Imovel).all()

    if not imoveis:
        logger.warning("Não há imoveis cadastrados na base :/")
        return {"message": "Não há imoveis cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d imoveis econtrados" % len(imoveis))
        return apresenta_imoveis(imoveis), 200


# Rota de adição de imovel
@app.post(
    "/imovel",
    tags=[imovel_tag],
    responses={"200": ImovelViewSchema, "400": ErrorSchema, "409": ErrorSchema},
)
def predict(form: ImovelSchema):
    """Adiciona um novo imovel à base de dados
    Retorna uma representação do imóvel com seu preço associado.

    Args:
        owner_name (str): nome do proprietário do imovel
        accommodates (int): número de acomodações
        availability_365 (int): disponibilidade em dias dentro de 365 dias
        bathrooms (int): número de banheiros
        bedrooms (int): número de quartos
        beds (int): número de camas
        region (str): região onde o imóvel está localizado

    Returns:
        dict: representação do imovel e preço associado
    """

    # Carregando modelo
    ml_path = "ml_model/best_model.pkl"
    modelo_obj = Model()
    modelo = modelo_obj.carrega_modelo(ml_path)
    log_price = Model.preditor(modelo, form)

    imovel = Imovel(
        owner_name=form.owner_name.strip(),
        bathrooms=form.bathrooms,
        bedrooms=form.bedrooms,
        accommodates=form.accommodates,
        beds=form.beds,
        availability_365=form.availability_365,
        region=form.region,
        outcome=np.exp(log_price),
    )
    logger.debug(f"Adicionando imóvel do proprietário: '{imovel.owner_name}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se o imóvel já existe na base
        if session.query(Imovel).filter(Imovel.owner_name == form.owner_name).first():
            error_msg = "Imóvel já existente na base :/"
            logger.warning(
                f"Erro ao adicionar imóvel do proprietário'{imovel.owner_name}', {error_msg}"
            )
            return {"message": error_msg}, 409

        # Adicionando imóvel
        session.add(imovel)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado imovel de nome: '{imovel.owner_name}'")
        return apresenta_imovel(imovel), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        print(e)
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao adicionar imóvel do proprietário '{imovel.owner_name}', {error_msg}"
        )
        return {"message": error_msg}, 400


# Métodos baseados em nome
# Rota de busca de imovel por nome do proprietário
@app.get(
    "/imovel",
    tags=[imovel_tag],
    responses={"200": ImovelViewSchema, "404": ErrorSchema},
)
def get_imovel(query: ImovelBuscaSchema):
    """Faz a busca por um imovel cadastrado na base a partir do nome do proprietário

    Args:
        owner_name (str): nome do proprietário

    Returns:
        dict: representação do imóvel e preço associado
    """

    imovel_owner_name = query.owner_name
    logger.debug(f"Coletando dados sobre imovel do proprietário #{imovel_owner_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    imovel = (
        session.query(Imovel).filter(Imovel.owner_name == imovel_owner_name).first()
    )

    if not imovel:
        # se o imovel não foi encontrado
        error_msg = (
            f"Imovel do proprietário {imovel_owner_name} não encontrado na base :/"
        )
        logger.warning(
            f"Erro ao buscar imovel do proprietário '{imovel_owner_name}', {error_msg}"
        )
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"imovel econtrado do: '{imovel.owner_name}'")
        # retorna a representação do imovel
        return apresenta_imovel(imovel), 200


# Rota de remoção de imovel por nome do proprietário
@app.delete(
    "/imovel",
    tags=[imovel_tag],
    responses={"200": ImovelViewSchema, "404": ErrorSchema},
)
def delete_imovel(query: ImovelBuscaSchema):
    """Remove um imovel cadastrado na base a partir do nome do proprietário

    Args:
        owner_name (str): nome do proprietário

    Returns:
        msg: Mensagem de sucesso ou erro
    """

    imovel_owner_name = unquote(query.owner_name)
    logger.debug(f"Deletando dados sobre imovel do(a) #{imovel_owner_name}")

    # Criando conexão com a base
    session = Session()

    # Buscando imovel
    imovel = (
        session.query(Imovel).filter(Imovel.owner_name == imovel_owner_name).first()
    )

    if not imovel:
        error_msg = "Imóvel não encontrado na base :/"
        logger.warning(
            f"Erro ao deletar imóvel do(a)'{imovel_owner_name}', {error_msg}"
        )
        return {"message": error_msg}, 404
    else:
        session.delete(imovel)
        session.commit()
        logger.debug(f"Deletado imovel do(a) #{imovel_owner_name}")
        return {
            "message": f"imovel do(a) {imovel_owner_name} removido com sucesso!"
        }, 200
