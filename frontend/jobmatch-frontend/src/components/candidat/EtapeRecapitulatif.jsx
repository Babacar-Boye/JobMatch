function EtapeRecapitulatif({ formData }) {

    return (

        <div>

            <h3>Vérifiez votre profil</h3>

            <p>
                Vérifiez vos informations avant de créer votre profil.
            </p>


            <h4>Informations personnelles</h4>

            <p>
                <strong>Prénom :</strong> {formData.prenom}
            </p>

            <p>
                <strong>Nom :</strong> {formData.nom}
            </p>

            <p>
                <strong>Email :</strong> {formData.email}
            </p>

            <p>
                <strong>Date de naissance :</strong>{" "}
                {formData.date_naissance}
            </p>

            <p>
                <strong>Téléphone :</strong> {formData.telephone}
            </p>


            <h4>Compte</h4>

            <p>
                <strong>Nom d'utilisateur :</strong>{" "}
                {formData.nom_utilisateur}
            </p>


            <h4>Profil professionnel</h4>

            <p>
                <strong>Niveau d'étude :</strong>{" "}
                {formData.niveau_etude}
            </p>

            <p>
                <strong>Domaine :</strong>{" "}
                {formData.domaine_metier}
            </p>

        </div>

    );
}

export default EtapeRecapitulatif;