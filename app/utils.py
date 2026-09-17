import numpy as np
from sklearn.linear_model import LinearRegression

# Inițializăm modelul și îl antrenăm cu date fictive
X_train = np.array([[1], [2], [3], [4]])
y_train = np.array([2, 4, 6, 8])  # y = 2 * x
model = LinearRegression()
model.fit(X_train, y_train)

model_2 = LinearRegression()
model_2.fit(X_train, np.array([3, 5, 7, 9]))  # y = 2 * x + 1

def predict(features):
    """Primiți o listă de caracteristici și returnați predicția."""
    features = np.array(features).reshape(-1, 1)
    return model.predict(features).tolist()

def predict_nv_model(features):
    """Primiți o listă de caracteristici și returnați predicția pentru noul model."""
    features = np.array(features).reshape(-1, 1)
    return model_2.predict(features).tolist()
