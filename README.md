# Loan outcome prediction

Credit risk modelling is a crucial part of any lending operation. It encompasses not only the prediction of default probability, but also capital allocation decisions in a resource-constrained environment aimed at maximizing long-term risk-adjusted returns. Credit risk modelling is relevant to any institution or individual seeking financial returns through repeated lending - where portfolio diversification across borrowers is the primary mechanism for managing exposure and smoothing outcomes over time.

The aim of this project is to assist in decision-making by using machine learning techniques for both default risk and overall returns prediction. In the simplest sense, it focuses primarily on maximizing profits by selecting loans with positive expected returns, setting aside sequence-of-return risk, capital constraints and portfolio path dependency, though quantitative time-dependent financial modelling techniques can be used going forward. 

It can be achieved by following approaches:
-	using regression methods to predict per-loan return and discovering the threshold which maximizes overall portfolio return;
-	using classification methods to predict probability of default and discovering the probability threshold that maximizes overall portfolio return.

The decision-making lives in a tradeoff between loan quality and its return. We don’t want to approve either too few, or too risky loans. We can compare different methods to figure out which approach leads to the best outcome. We are not interested in raw accuracy, but in business applicability in operational conditions. 

Interest rates are interesting in this regard, because they are both risk and return variable, able to leak the information about credit-worthiness into the model. Efficient market hypothesis claims that they are naturally discovered by markets incorporating all the available information, and we tend to agree. Therefore, there is little use in modelling interest rates, as they can be used as-is. Otherwise, we would need to model both the proposition of banks and the demand from clients at given prices. Though using tiny mispricings to our advantage can prove beneficial, and if anything, it’s the primary concern of modelling. Without them, we would simply approve all the loans at market rates. 

### Dataset
We use LendingClub loan dataset, arguably the most comprehensive publically available dataset on consumer lending. It includes both information about each of the loans and credit history of individual borrowers. Key columns include outcome: loan status, total payment and loan amount, loan information: amount, issue date, purpose, description, credit bureau statistics - 2.2M rows and 151 columns in total. When modelling, we remove features that leak information from the future, do feature engineering, convert data types. Depending on the model, we perform imputation of missing values, scaling and outlier clipping. Those decisions are represented in [columns.xlsx](columns.xlsx).

### Metrics
In order to quantify the increase in return through using decision-making framework on a prediction of a model, simple lift score has been implemented. Over a decent sample, it orders the prediction values and discovers a threshold which allows to maximize the return by choosing only the predictions with the values above that threshold. Later this threshold can be used for decision-making on the new data.


### Models 
In total 8 models have been compared. Their metrics are presented in the [table](model_results.xlsx) below:

| model name                             | XGBoostRegressor | LightGBMRegressor | DecisionTreeRegressor | PLS        | ElasticNet | LightGBMClassifier | DeepDecisionTreeClassifier | ShallowDecisionTreeClassifier |
|----------------------------------------|------------------|-------------------|-----------------------|------------|------------|--------------------|----------------------------|-------------------------------|
| model type                             | regression       | regression        | regression            | regression | regression | classification     | classification             | classification                |
| cross-validation test lift             | 1,7840           | 1,8024            | 1,6425                | 1,6218     | 1,6204     | 1,5610             | 1,3490                     | 1,2492                        |
| cross-validation train lift            | 1,8966           | 2,0624            | 1,6510                | 1,6264     | 1,6250     | 1,7588             | 1,4679                     | 1,2537                        |
| test split lift                        | 1,7214           | 1,7361            | 1,5882                | 1,5867     | 1,5855     | 1,5063             | 1,3302                     | 1,2160                        |
| train split lift                       |                  |                   | 1,6473                | 1,6254     | 1,6252     | 1,7390             | 1,4588                     | 1,2553                        |
| cross-validation test   RMSE/log-loss  | 4988,0000        | 4971,0000         | 5082,0000             | 5160,0000  | 5160,0000  | 0,4436             | 0,4749                     | 0,4698                        |
| cross-validation train   RMSE/log-loss | 4897,0000        | 4774,0000         | 5067,0000             | 5158,0000  | 5157,0000  | 0,4224             | 0,4559                     | 0,4692                        |
| test split RMSE/log-loss               | 4948,0000        | 4925,0000         | 5026,0000             | 5098,0000  | 5098,0000  | 0,4434             | 0,4701                     | 0,4702                        |
| train split RMSE/log-loss              | 4952,0000        | 4892,0000         | 5073,0000             | 5158,0000  | 5157,0000  | 0,4247             | 0,4574                     | 0,4693                        |
| cross-validation test R2/ROC   AUC     | 0,1164           | 0,1227            | 0,0830                | 0,0544     | 0,0547     | 0,7348             | 0,6890                     | 0,6766                        |
| cross-validation train R2/ROC   AUC    | 0,1484           | 0,1907            | 0,0884                | 0,0553     | 0,0556     | 0,7742             | 0,7071                     | 0,6781                        |
| test split R2/ROC AUC                  | 0,1094           | 0,1174            | 0,0810                | 0,0543     | 0,0545     | 0,7358             | 0,6892                     | 0,6764                        |
| train split R2/ROC AUC                 | 0,1291           | 0,1504            | 0,0863                | 0,0552     | 0,0556     | 0,7697             | 0,7047                     | 0,6782                        |

Regression models, being able to learn not only the probability of default, but also the magnitude of resulting return, have been consistently able to outperform classification models. LightGBM boosted model, due to its performance compared to XGBoost, and leaf-wise growth, was able to create a model with the largeset lift. Decision tree through tuning pruning alpha had shown a decent lift with an ability to easily interpret the prediction by traversing the tree. Partial least squares and ElasticNet have shown similar results. Unlike decision tree, ElasticNet incorporated almost all the features, aiming in understanding the relationships between them and the outcome.

### Deployment
The LightGBM regression model has been deployed and containerized into two services: an inference service responsible for running predictions, and a Django web service that utilizes the model while receiving, processing, and saving borrower and loan information. A measure of a degree of confidence in the decision was developed to report to the user, as raw predictions are not necessarily as interpretable.

### Run

**Prerequisites:** Docker, Docker Compose

1. Clone the repository
2. Copy `.env.example` to `.env` and set `SECRET_KEY`
3. Run `docker compose up --build`

The web interface is available at `http://localhost:8000`. The inference service API and documentation is available at `http://localhost:8001/docs`.
