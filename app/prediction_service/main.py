import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

from fastapi import FastAPI
from contextlib import asynccontextmanager


from src.loan_input import LoanInput
from src.predictor import LoanPredictor

predictor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global predictor
    predictor = LoanPredictor("model.lgbm", "bins.npy")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict(loan: LoanInput):
    confidence, decision = predictor.predict(loan)
    return {
        "confidence": confidence,
        "decision": decision,
    }
