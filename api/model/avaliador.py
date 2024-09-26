from sklearn.metrics import mean_squared_error


class Avaliador:

    def avaliar(self, modelo, X_test, Y_test):
        """Faz uma predição e avalia o modelo com métricas de regressão."""
        predicoes = modelo.predict(X_test)

        # Calcular o erro quadrático médio (MSE)
        mse = mean_squared_error(Y_test, predicoes)

        # Retorna as métricas de avaliação: RMSE, MAE, e R²
        return mse
