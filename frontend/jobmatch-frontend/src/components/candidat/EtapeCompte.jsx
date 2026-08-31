import styles from "./EtapeCompte.module.css";

function EtapeCompte({ formData, handleChange, erreur }) {

    return (
        <div>

            <h3>Créer votre compte</h3>

            <p>
                Choisissez vos identifiants de connexion.
            </p>

            <div>
                <label>Nom d'utilisateur</label>

                <input
                    type="text"
                    name="nom_utilisateur"
                    value={formData.nom_utilisateur}
                    onChange={handleChange}
                />
            </div>

            <div>
                <label>Mot de passe</label>

                <input
                    type="password"
                    name="mot_de_passe"
                    value={formData.mot_de_passe}
                    onChange={handleChange}
                    placeholder="••••••••"
                />
            </div>

            <div>
                <label>Confirmer le mot de passe</label>

                <input
                    type="password"
                    name="confirmation_mot_de_passe"
                    value={formData.confirmation_mot_de_passe}
                    onChange={handleChange}
                    placeholder="••••••••"
                />

                {erreur && (
                    <p className={styles.erreur}>
                        {erreur}
                    </p>
                )}
            </div>

        </div>
    );
}

export default EtapeCompte;