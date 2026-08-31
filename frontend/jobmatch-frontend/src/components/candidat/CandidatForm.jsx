import { useState } from "react";
import styles from "./CandidatForm.module.css";

// import { useState } from "react";
// import styles from "./Candidat.module.css";

import EtapeInformations from "./EtapeInformations";
import EtapeCompte from "./EtapeCompte";
import EtapeProfessionnel from "./EtapeProfessionnel";
import EtapeRecherche from "./EtapeRecherche";
import EtapeRecapitulatif from "./EtapeRecapitulatif";

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
        mot_de_passe:"",

        niveau_etude: "",
        domaine_metier: "",
        lien_linkedin: "",
        lien_portfolio: "",


        role : "candidat",
    });

    // Modifier une information
    const handleChange = (e) => {

        const { name, value, files } = e.target;

        setFormData({
            ...formData,
            [name]: files ? files[0] : value
        });
    };


    // Étape suivante
    const suivant = () => {

        setErreur("");

        if (etape === 2) {

            if (formData.mot_de_passe !== formData.confirmation_mot_de_passe) {

                setErreur("Les deux mots de passe ne sont pas identiques.");

                return;
            }
        }

        if (etape < 5) {
            setEtape(etape + 1);
        }
    };


    // Étape précédente
    const precedent = () => {

        if (etape > 1) {
            setEtape(etape - 1);
        }

    };


    // Création du profil
    const handleSubmit = () => {

        console.log("Données du candidat :", formData);

        // Ici tu feras plus tard ton appel à l'API Django
    };


    return (

        <div className={styles.candidatContainer}>

            <h2>Créer mon profil candidat</h2>


            {/* Progression */}

            <div className={styles.progression}>

                <span>Étape {etape} sur 4</span>

                <div className={styles.progressionBar}>
                    <div
                        className={styles.progressionActive}
                        style={{
                            width: `${(etape / 4) * 100}%`
                        }}
                    >
                    </div>
                </div>

            </div>


            {/* Contenu de l'étape */}

            <div className={styles.etapeContainer}>

                {etape === 1 && (
                    <EtapeInformations
                        formData={formData}
                        handleChange={handleChange}
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
                    <EtapeRecapitulatif
                        formData={formData}
                    />
                )}


            </div>


            {/* Boutons */}

            <div className={styles.navigation}>

                {etape > 1 && (
                    <button
                        type="button"
                        onClick={precedent}
                    >
                        Retour
                    </button>
                )}


                {etape < 4 && (
                    <button
                        type="button"
                        onClick={suivant}
                    >
                        Continuer
                    </button>
                )}


                {etape === 4 && (
                    <button
                        type="button"
                        onClick={handleSubmit}
                    >
                        Créer mon profil
                    </button>
                )}

            </div>

        </div>

    );
}

export default Candidat;