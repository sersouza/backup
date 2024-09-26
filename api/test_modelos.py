from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dados = "database/imoveis_golden.csv"
colunas = [
    "bathrooms",
    "bedrooms",
    "accommodates",
    "beds",
    "availability_365",
    "neighbourhood_BARRA_DA_TIJUCA",
    "neighbourhood_BOTAFOGO",
    "neighbourhood_CAMORIM",
    "neighbourhood_CATETE",
    "neighbourhood_CENTRO",
    "neighbourhood_COPACABANA",
    "neighbourhood_FLAMENGO",
    "neighbourhood_GAVEA",
    "neighbourhood_GLORIA",
    "neighbourhood_HUMAITA",
    "neighbourhood_IPANEMA",
    "neighbourhood_JACAREPAGUA",
    "neighbourhood_JARDIM_BOTANICO",
    "neighbourhood_LAGOA",
    "neighbourhood_LARANJEIRAS",
    "neighbourhood_LEBLON",
    "neighbourhood_LEME",
    "neighbourhood_RECREIO_DOS_BANDEIRANTES",
    "neighbourhood_SANTA_TERESA",
    "neighbourhood_SAO_CONRADO",
    "neighbourhood_TIJUCA",
    "neighbourhood_VIDIGAL",
    "price",
]

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]


# Método para testar o modelo de Gradient Boosting a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo_lr():
    # Importando o modelo de Gradient Boosting
    path = "ml_model/best_model.pkl"
    modelo_gb = modelo.carrega_modelo(path)

    # Obtendo as métricas da Gradient Boosting
    mse = avaliador.avaliar(modelo_gb, X, Y)

    print(mse)

    # Testando as métricas da Gradient Boosting
    # Modifique as métricas de acordo com seus requisitos
    assert mse <= 0.3
