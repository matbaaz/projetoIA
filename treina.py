import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

data = pd.read_csv("feijoes_dataset.csv", sep=";")

#X = data.drop(['class','file'], axis=1)
#y = data['class']
print(data.columns)
X = data.drop(['label'], axis=1)
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(random_state=42))
])


param_grid = {
    'clf__n_estimators':     [50, 100, 200],
    'clf__max_depth':        [None, 5, 10],
    'clf__min_samples_leaf': [1, 2, 4]
}

gs = GridSearchCV(pipe, param_grid, cv=5,
                  scoring='f1_weighted', n_jobs=-1, verbose=1)
gs.fit(X_train, y_train)

print("\nMelhores parâmetros:", gs.best_params_)
print("Best CV F1:", gs.best_score_)


best_model = gs.best_estimator_
y_pred     = best_model.predict(X_test)

print("\n=== Métricas Gerais ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision (w):", precision_score(y_test, y_pred, average='weighted'))
print("Recall    (w):", recall_score(y_test, y_pred, average='weighted'))
print("F1-score  (w):", f1_score(y_test, y_pred, average='weighted'))

print("\n=== Matriz de Confusão ===")
print(confusion_matrix(y_test, y_pred))

print("\n=== Relatório de Classificação ===")
print(classification_report(y_test, y_pred, zero_division=0))


kf     = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(best_model, X, y, cv=kf, scoring='f1_weighted')
print(f"\n5-Fold CV F1 médio: {scores.mean():.4f} ± {scores.std():.4f}")


import joblib
joblib.dump(best_model, 'bean_classifier_rf.pkl')
print("\nModelo salvo em bean_classifier_rf.pkl")
