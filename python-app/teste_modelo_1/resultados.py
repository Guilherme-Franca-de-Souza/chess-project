import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def evaluate_model_performance(csv_file):

    results_df = pd.read_csv(csv_file)


    stockfish_evaluations = results_df['stockfish_evaluation']
    model_predictions = results_df['model_prediction']

    mae = mean_absolute_error(stockfish_evaluations, model_predictions)
    mse = mean_squared_error(stockfish_evaluations, model_predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(stockfish_evaluations, model_predictions)

    print(f"Erro Médio Absoluto (MAE): {mae:.4f}")
    print(f"Erro Médio Quadrático (MSE): {mse:.4f}")
    print(f"Raiz do Erro Quadrático Médio (RMSE): {rmse:.4f}")
    print(f"Coeficiente de Correlação (R²): {r2:.4f}")

if __name__ == "__main__":
    csv_file = 'resultados_avaliacoes.csv' 
    evaluate_model_performance(csv_file)