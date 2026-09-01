import styles from "./Etape.module.css";

function EtapeCompte({ formData, handleChange, erreur }) {

    return (
        <div className={styles.etape}>

            <h3 className={styles.etapeTitre}>Créer votre compte</h3>

            <p className={styles.etapeSousTitre}>
                Choisissez vos identifiants de connexion.
            </p>

            <div className={styles.champ}>
                <label htmlFor="nom_utilisateur">Nom d'utilisateur</label>
                <input
                    type="text"
                    id="nom_utilisateur"
                    name="nom_utilisateur"
                    value={formData.nom_utilisateur}
                    onChange={handleChange}
                />
            </div>

            <div className={styles.champ}>
                <label htmlFor="mot_de_passe">Mot de passe</label>
                <input
                    type="password"
                    id="mot_de_passe"
                    name="mot_de_passe"
                    value={formData.mot_de_passe}
                    onChange={handleChange}
                    placeholder="••••••••"
                />
            </div>

            <div className={styles.champ}>
                <label htmlFor="confirmation_mot_de_passe">Confirmer le mot de passe</label>
                <input
                    type="password"
                    id="confirmation_mot_de_passe"
                    name="confirmation_mot_de_passe"
                    value={formData.confirmation_mot_de_passe}
                    onChange={handleChange}
                    placeholder="••••••••"
                />
            </div>

            {erreur && (
                <p className={styles.erreur}>
                    {erreur}
                </p>
            )}

        </div>
    );
}

export default EtapeCompte;