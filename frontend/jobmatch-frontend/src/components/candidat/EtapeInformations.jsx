function EtapeInformations({ formData, handleChange }) {

    return (

        <div>

            <h3>Faisons connaissance 👋</h3>

            <p>
                Commençons par quelques informations personnelles.
            </p>


            <div>
                <label>Prénom</label>

                <input
                    type="text"
                    name="prenom"
                    value={formData.prenom}
                    onChange={handleChange}
                    required
                />
            </div>


            <div>
                <label>Nom</label>

                <input
                    type="text"
                    name="nom"
                    value={formData.nom}
                    onChange={handleChange}
                />
            </div>


            <div>
                <label>Email</label>

                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                />
            </div>


            <div>
                <label>Date de naissance</label>

                <input
                    type="date"
                    name="date_naissance"
                    value={formData.date_naissance}
                    onChange={handleChange}
                />
            </div>


            <div>
                <label>Téléphone</label>

                <input
                    type="tel"
                    name="telephone"
                    value={formData.telephone}
                    onChange={handleChange}
                />
            </div>


            <div>
                <label>Photo</label>

                <input
                    type="file"
                    name="photo"
                    onChange={handleChange}
                />
            </div>

        </div>

    );
}

export default EtapeInformations;