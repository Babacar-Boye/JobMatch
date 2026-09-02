import { useEffect, useState } from "react";
import styles from "./Etape.module.css";

function Ligne({ label, valeur }) {
    return (
        <div className={styles.recapLigne}>
            <span className={styles.recapLabel}>{label}</span>
            <span className={styles.recapValeur}>{valeur || "—"}</span>
        </div>
    );
}

function LigneTable({ label, valeur }) {
    return (
        <div className={styles.recapTableLigne}>
            <span className={styles.recapTableLabel}>{label}</span>
            <span className={styles.recapTableValeur}>{valeur || "—"}</span>
        </div>
    );
}

function EtapeRecapitulatif({ formData }) {

    const [apercu, setApercu] = useState(null);

    // Génère l'aperçu de la photo choisie (ou rien si aucune photo)
    useEffect(() => {
        if (!formData.photo) {
            setApercu(null);
            return;
        }

        const url = URL.createObjectURL(formData.photo);
        setApercu(url);

        return () => URL.revokeObjectURL(url);
    }, [formData.photo]);

    return (

        <div className={styles.etape}>

            <h3 className={styles.etapeTitre}>Vérifiez votre profil</h3>

            <p className={styles.etapeSousTitre}>
                Vérifiez vos informations avant de créer votre profil.
            </p>

            {/* Rectangle du haut : infos personnelles + photo/compte */}
            <div className={styles.recapBoite}>
                <div className={styles.recapHaut}>

                    <div className={styles.recapColonneInfos}>
                        <Ligne label="Nom" valeur={formData.nom} />
                        <Ligne label="Prénom" valeur={formData.prenom} />
                        <Ligne label="Date de naissance" valeur={formData.date_naissance} />
                        <Ligne label="Email" valeur={formData.email} />
                        <Ligne label="Téléphone" valeur={formData.telephone} />
                    </div>

                    <div className={styles.recapColonnePhoto}>
                        <div className={`${styles.avatarCercle} ${styles.avatarCercleStatique}`}>
                            {apercu ? (
                                <img
                                    src={apercu}
                                    alt="Photo de profil"
                                    className={styles.avatarImage}
                                />
                            ) : (
                                <svg
                                    className={styles.avatarSilhouette}
                                    viewBox="0 0 24 24"
                                    width="30"
                                    height="30"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="1.6"
                                >
                                    <circle cx="12" cy="8" r="4" />
                                    <path d="M4 20c0-4 3.5-6 8-6s8 2 8 6" />
                                </svg>
                            )}

                            <span className={styles.avatarCamera}>
                                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z" />
                                    <circle cx="12" cy="13" r="3.4" />
                                </svg>
                            </span>
                        </div>

                        <span className={styles.recapNomUtilisateur}>
                            {formData.nom_utilisateur || "—"}
                        </span>
                    </div>

                </div>
            </div>

            {/* Rectangle du bas : profil professionnel, présenté comme un tableau */}
            <div className={styles.recapBoite}>
                <div className={styles.recapTable}>
                    <LigneTable label="Niveau d'étude" valeur={formData.niveau_etude} />
                    <LigneTable label="Domaine métier" valeur={formData.domaine_metier} />
                    <LigneTable label="LinkedIn" valeur={formData.lien_linkedin} />
                    <LigneTable label="Portfolio" valeur={formData.lien_portfolio} />
                </div>
            </div>

        </div>

    );
}

export default EtapeRecapitulatif;