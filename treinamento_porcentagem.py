import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)


# ======== Leitura dos dados =========
data = pd.read_csv("feijoes_dataset.csv", sep=';')

X = data.drop(['label'], axis=1)
y = data['label']


# ======== Função de treinamento =========
def treinar_e_gerar_relatorio(X, y, split, modelo_nome):
    print(f"\n### Treinando com split {int(split*100)}/{int((1-split)*100)} ###")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=(1 - split), random_state=42, stratify=y
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

    best_model = gs.best_estimator_
    y_pred = best_model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted')
    rec = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    conf_mat = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, zero_division=0)

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(best_model, X, y, cv=kf, scoring='f1_weighted')

    # ======== Salvar modelo =========
    joblib.dump(best_model, f'{modelo_nome}.pkl')

    # ======== Salvar relatório =========
    with open(f'{modelo_nome}_relatorio.txt', 'w') as f:
        f.write(f"### Split: {int(split*100)}/{int((1-split)*100)}\n")
        f.write(f"Melhores parâmetros: {gs.best_params_}\n")
        f.write(f"Melhor F1 CV GridSearch: {gs.best_score_:.4f}\n\n")
        f.write("=== Métricas Gerais ===\n")
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision (w): {prec:.4f}\n")
        f.write(f"Recall    (w): {rec:.4f}\n")
        f.write(f"F1-score  (w): {f1:.4f}\n\n")
        f.write("=== Matriz de Confusão ===\n")
        f.write(f"{conf_mat}\n\n")
        f.write("=== Relatório de Classificação ===\n")
        f.write(f"{class_report}\n\n")
        f.write(f"=== 5-Fold CV F1 ===\n")
        f.write(f"Média: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}\n")

    print(f"Modelo salvo como {modelo_nome}.pkl")
    print(f"Relatório salvo como {modelo_nome}_relatorio.txt")


# ======== Rodar para os 3 splits =========
splits = [0.7, 0.8, 0.9]

for split in splits:
    nome = f"bean_classifier_{int(split*100)}_{int((1-split)*100)}"
    treinar_e_gerar_relatorio(X, y, split, nome)
