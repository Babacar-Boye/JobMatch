import styles from "./Etape.module.css";

function Ligne({ label, valeur }) {
    return (
        <div className={styles.recapLigne}>
            <span className={styles.recapLabel}>{label}</span>
            <span className={styles.recapValeur}>{valeur || "—"}</span>
        </div>
    );
}

function EtapeRecapitulatif({ formData }) {

    return (

        <div className={styles.etape}>

            <h3 className={styles.etapeTitre}>Vérifiez votre profil</h3>

            <p className={styles.etapeSousTitre}>
                Vérifiez vos informations avant de créer votre profil.
            </p>

            <h4 className={styles.recapSection}>Informations personnelles</h4>
            <Ligne label="Prénom" valeur={formData.prenom} />
            <Ligne label="Nom" valeur={formData.nom} />
            <Ligne label="Email" valeur={formData.email} />
            <Ligne label="Date de naissance" valeur={formData.date_naissance} />
            <Ligne label="Téléphone" valeur={formData.telephone} />
            <Ligne label="Photo" valeur={formData.photo ? formData.photo.name : ""} />

            <h4 className={styles.recapSection}>Compte</h4>
            <Ligne label="Nom d'utilisateur" valeur={formData.nom_utilisateur} />

            <h4 className={styles.recapSection}>Profil professionnel</h4>
            <Ligne label="Niveau d'étude" valeur={formData.niveau_etude} />
            <Ligne label="Domaine métier" valeur={formData.domaine_metier} />
            <Ligne label="LinkedIn" valeur={formData.lien_linkedin} />
            <Ligne label="Portfolio" valeur={formData.lien_portfolio} />

        </div>

    );
}

export default EtapeRecapitulatif;