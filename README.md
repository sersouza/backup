# AI Airbnb RJ Price Predict System

Este projeto é parte do MVP para a disciplina **Qualidade de Software, Segurança e Sistemas Inteligentes**, cursada na Pós-Graduação em Engenharia de Software da PUC-RJ.

## Objetivo

O **AI Airbnb RJ Price Predict System** é uma aplicação web desenvolvida para auxiliar proprietários de imóveis no Rio de Janeiro a definir o valor diário sugerido para locação no Airbnb. Utilizando informações básicas do imóvel, como:

- **Número de quartos**
- **Número de banheiros**
- **Capacidade de acomodação**
- **Número de camas**
- **Disponibilidade anual (em dias)**
- **Região do imóvel**

O sistema aplica um modelo de aprendizado de máquina para prever um preço sugerido, baseado em dados históricos de locações e características de imóveis similares.

## Funcionalidades

1. **Cadastro de Imóveis:**

   - Os usuários podem inserir dados do imóvel, como nome do proprietário, número de quartos, banheiros, camas, capacidade de acomodação e disponibilidade anual.

2. **Previsão de Preço:**

   - Com base nas informações fornecidas, o sistema calcula um preço diário sugerido para o imóvel, facilitando a tomada de decisão do proprietário em relação ao valor a ser cobrado.

3. **Listagem e Gerenciamento de Imóveis:**
   - O sistema exibe uma lista de todos os imóveis cadastrados, permitindo a exclusão e atualização das informações conforme necessário.

## Tecnologias Utilizadas

- **Front-end:** HTML, CSS e JavaScript
- **Back-end:** Flask (Python)
- **Modelagem de Dados:** Scikit-Learn para treinamento do modelo de previsão
- **Banco de Dados:** SQLite para armazenamento das informações dos imóveis
- **Integração e Deploy:** Implementação e integração de serviços utilizando REST API

## Aplicabilidade

Este sistema é útil para proprietários de imóveis que desejam uma estimativa precisa e rápida do preço de locação, considerando a competitividade do mercado de locações temporárias no Rio de Janeiro.

## Considerações Finais

O projeto, além de ser uma entrega da disciplina, representa um avanço no uso de inteligência artificial aplicada a problemas do mundo real. Ele busca promover a adoção de práticas de qualidade de software e segurança, alinhadas ao desenvolvimento de sistemas inteligentes.

## Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas. A versão do python utilizada foi 3.10.12.

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

Para abrir o frontend da aplicação basta fazer o download do projeto e abrir o arquivo index.html no seu browser.
