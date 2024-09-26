import numpy as np
import pickle
import joblib

from model.imovel import Region


class Model:
    def carrega_regiao(regiao: Region):
        # List of all the variables
        variables = [
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
        ]

        # Set all variables to False in an array
        variables_false_array = [False] * len(variables)

        # Convert the regiao enum to its name
        region_name = f"neighbourhood_{regiao.name}"

        # Check if the region name is in the variables list, and set the corresponding position to True
        if region_name in variables:
            index = variables.index(region_name)
            variables_false_array[index] = True

        print(f"Region: {region_name}, Index: {index}")
        print(variables_false_array)

        return variables_false_array

    def carrega_modelo(self, path):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra"""

        if path.endswith(".pkl"):
            model = pickle.load(open(path, "rb"))
        elif path.endswith(".joblib"):
            model = joblib.load(path)
        else:
            raise Exception("Formato de arquivo não suportado")
        return model

    def preditor(model, form):
        """Realiza a predição de um imóvel com base no modelo treinado"""

        # Create the base input array from the form fields
        X_input = np.array(
            [
                form.bathrooms,
                form.bedrooms,
                form.accommodates,
                form.beds,
                form.availability_365,
            ]
        )

        # Call carrega_regiao to get one-hot encoded region data
        region_encoded = Model.carrega_regiao(form.region)

        # Combine the base features with the one-hot encoded region
        X_combined = np.concatenate([X_input, region_encoded])

        # Print for debugging (you can remove this later)
        print(f"Input Features: {X_combined}")

        # Reshape the input to match the model's expected input format
        diagnosis = model.predict(X_combined.reshape(1, -1))

        return diagnosis[0]
