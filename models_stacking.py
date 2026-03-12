import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.ensemble import StackingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


from sklearn.linear_model import ElasticNetCV, LassoCV, LinearRegression, RidgeCV

def train_models(csv_path="data/kalshi_w_macro_markets.csv"):
    df = pd.read_csv(csv_path)
    df = df.drop(columns=["mean_C25", "mean_H25", "exp_rate_open_interest"]).fillna(0)

    target_col = "Day Change %"
    dates = pd.to_datetime(df["Date"])

    X = df.drop(columns=["Date", target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test, _, idx_test = train_test_split(X, y, np.arange(len(df)), test_size=0.2, random_state=42)

    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    y_hat_train_linear = linear_model.predict(X_train)
    y_hat_test_linear = linear_model.predict(X_test)
    r2_score_linear = r2_score(y_test, y_hat_test_linear)
    train_mse_linear = mean_squared_error(y_train, y_hat_train_linear)
    test_mse_linear = mean_squared_error(y_test, y_hat_test_linear)

    lasso_model = Pipeline([
        ("scaler", StandardScaler()),
        ("lasso", LassoCV(cv=5, random_state=42))
    ])
    lasso_model.fit(X_train, y_train)
    y_hat_train_lasso = lasso_model.predict(X_train)
    y_hat_test_lasso = lasso_model.predict(X_test)
    train_mse_lasso = mean_squared_error(y_train, y_hat_train_lasso)
    test_mse_lasso = mean_squared_error(y_test, y_hat_test_lasso)
    r2_score_lasso = r2_score(y_test, y_hat_test_lasso)
    

    ridge_model = Pipeline([
        ("scaler", StandardScaler()),
        ("ridge", RidgeCV(cv=5))
    ])
    ridge_model.fit(X_train, y_train)
    y_hat_train_ridge = ridge_model.predict(X_train)
    y_hat_test_ridge = ridge_model.predict(X_test)
    train_mse_ridge = mean_squared_error(y_train, y_hat_train_ridge)
    test_mse_ridge = mean_squared_error(y_test, y_hat_test_ridge)
    r2_score_ridge = r2_score(y_test, y_hat_test_ridge)

    elastic_model = Pipeline([
        ("scaler", StandardScaler()),
        ("elastic", ElasticNetCV(cv=5, random_state=42))
    ])
    elastic_model.fit(X_train, y_train)
    y_hat_train_elastic = elastic_model.predict(X_train)
    y_hat_test_elastic = elastic_model.predict(X_test)
    train_mse_elastic = mean_squared_error(y_train, y_hat_train_elastic)
    test_mse_elastic = mean_squared_error(y_test, y_hat_test_elastic)
    r2_score_elastic = r2_score(y_test, y_hat_test_elastic)

    random_forest_model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    random_forest_model.fit(X_train, y_train)
    y_hat_train_rf = random_forest_model.predict(X_train)
    y_hat_test_rf = random_forest_model.predict(X_test)
    train_mse_rf = mean_squared_error(y_train, y_hat_train_rf)
    test_mse_rf = mean_squared_error(y_test, y_hat_test_rf)
    r2_score_rf = r2_score(y_test, y_hat_test_rf)

    model_stack = StackingRegressor(
        estimators=[
            ("lasso", lasso_model),
            ("rf", random_forest_model)
        ],
        final_estimator=LinearRegression()
    )
    model_stack.fit(X_train, y_train)
    y_hat_train_stack = model_stack.predict(X_train)
    y_hat_test_stack = model_stack.predict(X_test)
    train_mse_stack = mean_squared_error(y_train, y_hat_train_stack)
    test_mse_stack = mean_squared_error(y_test, y_hat_test_stack)
    r2_score_stack = r2_score(y_test, y_hat_test_stack)

    results_df = pd.DataFrame({
        "model": ["Linear Regression", "Lasso", "Ridge", "Elastic Net", "Random Forest", "Stacking Regressor"],
        "train_mse": [train_mse_linear, train_mse_lasso, train_mse_ridge, train_mse_elastic, train_mse_rf, train_mse_stack],
        "test_mse": [test_mse_linear, test_mse_lasso, test_mse_ridge, test_mse_elastic, test_mse_rf, test_mse_stack],
        "r2_score": [r2_score_linear, r2_score_lasso, r2_score_ridge, r2_score_elastic, r2_score_rf, r2_score_stack]
    })
    models = {
        "Linear":        linear_model,
        "Lasso":         lasso_model,
        "Ridge":         ridge_model,
        "Elastic Net":   elastic_model,
        "Random Forest": random_forest_model,
        "Stacking":      model_stack,
    }

    lasso_coefs = lasso_model.named_steps["lasso"].coef_
    ridge_coefs = ridge_model.named_steps["ridge"].coef_
    elastic_coefs = elastic_model.named_steps["elastic"].coef_

    coef_table = pd.DataFrame({
        "feature": X.columns,
        "Lasso Coef": lasso_coefs,
        "Ridge Coef": ridge_coefs,
        "Elastic Net Coef": elastic_coefs
    })
    coef_table["abs_lasso"] = coef_table["Lasso Coef"].abs()
    coef_table = coef_table.sort_values(by="abs_lasso", ascending=False).drop(columns=["abs_lasso"])
    
    return models, X_test, y_test, dates, idx_test, results_df, coef_table  

if __name__ == "__main__":
    models, X_test, y_test, dates, idx_test, results_df, coef_table = train_models()
    print(results_df)
    print(coef_table.head(15))
    results_df.to_csv("data/model_comparison.csv", index=False)
    coef_table.to_csv("data/coef_table.csv", index=False)