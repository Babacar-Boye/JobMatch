import { useEffect, useRef, useState } from "react";
import styles from "./Etape.module.css";

function EtapePhotoProfil({ formData, handleChange, erreur }) {

    const inputRef = useRef(null);
    const [apercu, setApercu] = useState(null);

    // Génère un aperçu de l'image choisie, et nettoie l'URL quand elle change
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

            <h3 className={styles.etapeTitre}>Photo de profil </h3>

            <p className={styles.etapeSousTitre}>
                Ajoutez une photo pour que les recruteurs vous reconnaissent.
            </p>

            <div className={styles.avatarZone}>

                <button
                    type="button"
                    className={styles.avatarCercle}
                    onClick={() => inputRef.current?.click()}
                    aria-label="Choisir une photo de profil"
                >
                    {apercu ? (
                        <img
                            src={apercu}
                            alt="Aperçu de la photo de profil"
                            className={styles.avatarImage}
                        />
                    ) : (
                        <svg
                            className={styles.avatarSilhouette}
                            viewBox="0 0 24 24"
                            width="34"
                            height="34"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.6"
                        >
                            <circle cx="12" cy="8" r="4" />
                            <path d="M4 20c0-4 3.5-6 8-6s8 2 8 6" />
                        </svg>
                    )}

                    <span className={styles.avatarCamera}>
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z" />
                            <circle cx="12" cy="13" r="3.4" />
                        </svg>
                    </span>
                </button>

                <input
                    ref={inputRef}
                    type="file"
                    id="photo"
                    name="photo"
                    accept="image/*"
                    onChange={handleChange}
                    className={styles.avatarInputCache}
                />

                <span className={styles.avatarTexte}>
                    {formData.photo ? formData.photo.name : "Ajouter une photo"}
                </span>

            </div>

            {erreur && (
                <p className={styles.erreur}>
                    {erreur}
                </p>
            )}

        </div>
    );
}

export default EtapePhotoProfil;