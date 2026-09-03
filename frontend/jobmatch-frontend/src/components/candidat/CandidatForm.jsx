import { useState } from "react";
import styles from "./CandidatForm.module.css";

import EtapeInformations from "./EtapeInformations";
import EtapeCompte from "./EtapeCompte";
import EtapeProfessionnel from "./EtapeProfessionnel";
import EtapeRecapitulatif from "./EtapeRecapitulatif";
import EtapePhotoProfil from "./EtapePhotoProfil";

import axios from "axios";

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
    // const handleFormSubmit = async (e) => {
    //     e.preventDefault();

    //     if (etape < TOTAL_ETAPES) {
    //         suivant();
    //         return;
    //     }

    //     console.log("Données du candidat :", formData);

    //     const data = {
    //         utilisateur: {
    //             nom: formData.nom,
    //             prenom: formData.prenom,
    //             email: formData.email,
    //             nom_utilisateur: formData.nom_utilisateur,
    //             telephone: formData.telephone,
    //             date_naissance: formData.date_naissance,

    //             password1: formData.mot_de_passe,
    //             password2: formData.confirmation_mot_de_passe,

    //             photo_profil: formData.photo,
    //         },

    //         niveau_etude: formData.niveau_etude,
    //         domaine_metier: formData.domaine_metier,
    //         lien_linkedin: formData.lien_linkedin,
    //         lien_portfolio: formData.lien_portfolio,
    //     };

    //     try {
    //         const response = await axios.post(
    //             `${import.meta.env.VITE_API_URL}/candidats/`,
    //             data
    //         );

    //         console.log("Inscription réussie :", response.data);

    //     } catch (error) {
    //         console.error(
    //             "Erreur lors de l'inscription :",
    //             error.response?.data || error.message
    //         );
    //     }
    // };

    const handleFormSubmit = async (e) => {
        e.preventDefault();

        if (etape < TOTAL_ETAPES) {
            suivant();
            return;
        }

        const fd = new FormData();

        // Champs imbriqués -> notation "utilisateur.xxx"
        fd.append("utilisateur.nom", formData.nom);
        fd.append("utilisateur.prenom", formData.prenom);
        fd.append("utilisateur.email", formData.email);
        fd.append("utilisateur.nom_utilisateur", formData.nom_utilisateur);
        fd.append("utilisateur.telephone", formData.telephone || "");
        fd.append("utilisateur.date_naissance", formData.date_naissance);
        fd.append("utilisateur.password1", formData.mot_de_passe);
        fd.append("utilisateur.password2", formData.confirmation_mot_de_passe);

        if (formData.photo) {
            // formData.photo doit être un objet File (ex: e.target.files[0])
            fd.append("utilisateur.photo_profil", formData.photo);
        }

        fd.append("niveau_etude", formData.niveau_etude || "");
        fd.append("domaine_metier", formData.domaine_metier);
        fd.append("lien_linkedin", formData.lien_linkedin || "");
        fd.append("lien_portfolio", formData.lien_portfolio || "");

        try {
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/accounts/candidats/`,
                fd
                // Ne PAS fixer Content-Type manuellement, axios/le navigateur
                // ajoute automatiquement "multipart/form-data; boundary=..."
            );
            console.log("Inscription réussie :", response.data);
        } catch (error) {
            console.error(
                "Erreur lors de l'inscription :",
                error.response?.data || error.message
            );
        }
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