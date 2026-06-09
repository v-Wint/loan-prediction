import lightgbm as lgb
import numpy as np
from src.loan_input import LoanInput

class LoanPredictor:
    def __init__(self, model_path: str, bins_path: str):
        self.model = lgb.Booster(model_file=model_path)
        self.bins = np.load(bins_path)
        self.threshold = -75
        self.threshold_percentile = int(np.searchsorted(self.bins, 0))


    def predict(self, loan: LoanInput) -> dict:
        df = loan.to_df()
        expected_return = float(self.model.predict(df)[0])
        return self.to_score(expected_return), expected_return >= self.threshold

    def to_score(self, value):
        shifted = value - self.threshold
        p = int(np.searchsorted(self.bins, shifted))
        zero_p = self.threshold_percentile
        
        if shifted >= 0:
            score = int(round((p - zero_p) / (100 - zero_p) * 100))
        else:
            score = int(round((p - zero_p) / zero_p * 100))
        
        return max(-100, min(100, score))
