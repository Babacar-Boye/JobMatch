import styles from "./Etape.module.css";

function EtapeInformations({ formData, handleChange, erreur }) {

    return (

        <div className={styles.etape}>

            <h3 className={styles.etapeTitre}>Faisons connaissance 👋</h3>

            <p className={styles.etapeSousTitre}>
                Commençons par quelques informations personnelles.
            </p>

            <div className={styles.champ}>
                <label htmlFor="prenom">Prénom</label>
                <input
                    type="text"
                    id="prenom"
                    name="prenom"
                    value={formData.prenom}
                    onChange={handleChange}
                />
            </div>

            <div className={styles.champ}>
                <label htmlFor="nom">Nom</label>
                <input
                    type="text"
                    id="nom"
                    name="nom"
                    value={formData.nom}
                    onChange={handleChange}
                />
            </div>

            <div className={styles.champ}>
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                />
            </div>

            <div className={styles.champ}>
                <label htmlFor="date_naissance">Date de naissance</label>
                <input
                    type="date"
                    id="date_naissance"
                    name="date_naissance"
                    value={formData.date_naissance}
                    onChange={handleChange}
                />
            </div>

            <div className={styles.champ}>
                <label htmlFor="telephone">Téléphone</label>
                <input
                    type="tel"
                    id="telephone"
                    name="telephone"
                    value={formData.telephone}
                    onChange={handleChange}
                />
            </div>

            <div className={styles.champ}>
                <label htmlFor="photo">Photo</label>
                <input
                    type="file"
                    id="photo"
                    name="photo"
                    onChange={handleChange}
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

export default EtapeInformations;