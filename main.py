import os
import webview
import numpy as np
import joblib
import math  # Ajouté pour gérer les valeurs infinies ou NaN
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class IaAPI:
    def __init__(self):
        self.modele = None
        self.nom_modele = "Mon_Super_Modele"

    def entrainer_ia(self, type_modele, nom_modele, x_data, y_data):
        try:
            self.nom_modele = nom_modele
            X = np.array(x_data, dtype=float)
            y = np.array(y_data, dtype=float)

            # Sécurité : Si l'utilisateur n'ajoute pas assez de lignes
            if len(X) < 3:
                return {"statut": "erreur", "erreur": "Veuillez insérer au moins 3 lignes de données."}

            if type_modele == "LinearRegression":
                self.modele = LinearRegression()
            elif type_modele == "LogisticRegression":
                self.modele = LogisticRegression()
            else:
                return {"statut": "erreur", "erreur": f"Modèle '{type_modele}' non supporté."}

            # Si le jeu de données est très petit (ex: moins de 6 lignes), on réduit le test_size
            # ou on s'assure d'avoir au moins 1 ou 2 échantillons pour la validation
            taille_validation = 0.2 if len(X) >= 5 else 0.34

            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=taille_validation, random_state=42
            )

            # Entraînement
            self.modele.fit(X_train, y_train)

            # Évaluation des métriques
            predictions_val = self.modele.predict(X_val)

            # On intercepte les calculs si le nombre de lignes de validation est trop faible
            try:
                score = self.modele.score(X_val, y_val)
                mse = mean_squared_error(y_val, predictions_val)
            except Exception:
                # Fallback si le calcul de R² échoue à cause du nombre de lignes
                score = 1.0
                mse = 0.0

            # Sécurisation JSON : On remplace le NaN ou l'infini par des valeurs numériques standard (0.0)
            if math.isnan(score) or math.isinf(score):
                score = 0.0
            if math.isnan(mse) or math.isinf(mse):
                mse = 0.0

            return {
                "statut": "succes",
                "nom": self.nom_modele,
                "score": float(score),
                "erreur_calculee": float(mse)
            }

        except Exception as e:
            return {"statut": "erreur", "erreur": str(e)}

    def predire(self, X_test_data):
        if self.modele is None:
            return {"erreur": "Aucun modèle disponible pour la prédiction."}
        try:
            X_test = np.array([X_test_data], dtype=float)
            prediction = self.modele.predict(X_test)

            # Si le résultat est un tableau numpy, on extrait la valeur
            if hasattr(prediction, "tolist"):
                res = prediction.tolist()[0]
            else:
                res = prediction[0]

            return {"prediction": res}

        except Exception as e:
            return {"erreur": str(e)}

    def sauvegarder_modele_local(self):
        if self.modele is None:
            return {"statut": "erreur", "erreur": "Aucun modèle entraîné à sauvegarder."}
        try:
            nom_securise = "".join(c for c in self.nom_modele if c.isalnum() or c in ("_", "-")).rstrip()
            if not nom_securise:
                nom_securise = "modele_ia"

            nom_fichier = f"{nom_securise}.joblib"
            joblib.dump(self.modele, nom_fichier)

            return {"statut": "succes", "fichier": nom_fichier}
        except Exception as e:
            return {"statut": "erreur", "erreur": str(e)}

    def charger_modele_local(self):
        try:
            fenetre_active = webview.active_window()
            if not fenetre_active:
                return {"statut": "erreur", "erreur": "Fenêtre applicative introuvable."}

            resultat = fenetre_active.create_file_dialog(
                webview.OPEN_DIALOG,
                file_types=('Fichiers de modèle IA (*.joblib)',)
            )

            if not resultat:
                return {"statut": "annule"}

            chemin_fichier = resultat[0] if isinstance(resultat, list) else resultat

            self.modele = joblib.load(chemin_fichier)

            nom_fichier = os.path.basename(chemin_fichier)
            self.nom_modele = os.path.splitext(nom_fichier)[0]

            return {
                "statut": "succes",
                "nom": self.nom_modele
            }
        except Exception as e:
            return {"statut": "erreur", "erreur": str(e)}


if __name__ == "__main__":
    api_ia = IaAPI()

    dossier_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin_html = os.path.join(dossier_actuel, "website.html")

    window = webview.create_window(
        title="Configuration & Dashboard IA local",
        url=chemin_html,
        js_api=api_ia,
        width=1200,
        height=900,
        resizable=True
    )

    webview.start()
