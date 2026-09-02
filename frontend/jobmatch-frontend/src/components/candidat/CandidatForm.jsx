import { useState } from "react";
import styles from "./CandidatForm.module.css";

import EtapeInformations from "./EtapeInformations";
import EtapeCompte from "./EtapeCompte";
import EtapeProfessionnel from "./EtapeProfessionnel";
import EtapeRecapitulatif from "./EtapeRecapitulatif";
import EtapePhotoProfil from "./EtapePhotoProfil";

const TOTAL_ETAPES = 5;

function Candidat() {

    const [etape, setEtape] = useState(1);
    const [erreur, setErreur] = useState("");

    const [formData, setFormData] = useState({
        nom: "",
        prenom: "",
        email: "",
        date_naissance: "",
        telephone: "",
        photo: null,

        nom_utilisateur: "",
        mot_de_passe: "",
        confirmation_mot_de_passe: "",

        niveau_etude: "",
        domaine_metier: "",
        lien_linkedin: "",
        lien_portfolio: "",

        role: "candidat",
    });

    // Modifier une information
    const handleChange = (e) => {
        const { name, value, files } = e.target;

        setFormData({
            ...formData,
            [name]: files ? files[0] : value
        });
    };

    // Vérifie l'étape en cours, renvoie un message d'erreur ou "" si tout va bien
    const validerEtape = () => {

        if (etape === 1) {
            if (formData.prenom.trim() === "") return "Donnez votre prénom.";
            if (formData.nom.trim() === "") return "Donnez votre nom de famille.";
            if (formData.email.trim() === "") return "Donnez votre email.";
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) return "Cet email ne semble pas valide.";
            if (formData.date_naissance === "") return "Donnez votre date de naissance.";
            if (formData.telephone.trim() === "") return "Donnez votre numéro de téléphone.";
        }

        if (etape === 2) {
            if (formData.nom_utilisateur.trim() === "") return "Choisissez un nom d'utilisateur.";
            if (formData.mot_de_passe === "") return "Créez un mot de passe.";
            if (formData.mot_de_passe.length < 6) return "Le mot de passe doit contenir au moins 6 caractères.";
            if (formData.confirmation_mot_de_passe === "") return "Confirmez votre mot de passe.";
            if (formData.mot_de_passe !== formData.confirmation_mot_de_passe) return "Les deux mots de passe ne sont pas identiques.";
        }

        return "";
    };

    // Étape suivante
    const suivant = () => {
        const message = validerEtape();

        if (message) {
            setErreur(message);
            return;
        }

        setErreur("");

        if (etape < TOTAL_ETAPES) {
            setEtape(etape + 1);
        }
    };

    // Étape précédente
    const precedent = () => {
        setErreur("");

        if (etape > 1) {
            setEtape(etape - 1);
        }
    };

    // Soumission (bouton "Continuer" / "Créer mon profil", ou touche Entrée)
    const handleFormSubmit = (e) => {
        e.preventDefault();

        if (etape < TOTAL_ETAPES) {
            suivant();
            return;
        }

        console.log("Données du candidat :", formData);
        // Ici viendra l'appel à l'API Django
    };

    return (
        <div className={styles.page}>
            <form className={styles.card} onSubmit={handleFormSubmit} noValidate>

                <h2 className={styles.title}>Créer mon profil candidat</h2>

                {/* Progression */}
                <div className={styles.progression}>
                    <span className={styles.progressionTexte}>
                        Étape {etape} sur {TOTAL_ETAPES}
                    </span>

                    <div className={styles.progressionBarre}>
                        <div
                            className={styles.progressionActive}
                            style={{ width: `${(etape / TOTAL_ETAPES) * 100}%` }}
                        />
                    </div>
                </div>

                {/* Contenu de l'étape */}
                <div className={styles.etapeContainer} key={etape}>

                    {etape === 1 && (
                        <EtapeInformations
                            formData={formData}
                            handleChange={handleChange}
                            erreur={erreur}
                        />
                    )}

                    {etape === 2 && (
                        <EtapeCompte
                            formData={formData}
                            handleChange={handleChange}
                            erreur={erreur}
                        />
                    )}

                    {etape === 3 && (
                        <EtapeProfessionnel
                            formData={formData}
                            handleChange={handleChange}
                        />
                    )}

                    {etape === 4 && (
                        <EtapePhotoProfil
                            formData={formData}
                            handleChange={handleChange}
                            erreur={erreur}
                        />
                    )}

                    {etape === 5 && (
                        <EtapeRecapitulatif formData={formData} />
                    )}

                </div>

                {/* Boutons */}
                <div className={styles.navigation}>
                    {etape > 1 ? (
                        <button
                            type="button"
                            className={styles.btnRetour}
                            onClick={precedent}
                        >
                            Retour
                        </button>
                    ) : <span />}

                    <button type="submit" className={styles.btnSuivant}>
                        {etape < TOTAL_ETAPES ? "Continuer" : "Créer mon profil"}
                    </button>
                </div>

            </form>
        </div>
    );
}

export default Candidat;