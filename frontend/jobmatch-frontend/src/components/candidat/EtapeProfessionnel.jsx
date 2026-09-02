function EtapeProfessionnel({ formData, handleChange }) {

    return (

        <div>

            <h3>Votre profil professionnel </h3>

            <p>
                Parlez-nous de votre parcours.
            </p>


            <div>

                <label>Niveau d'étude</label>

                <select
                    name="niveau_etude"
                    value={formData.niveau_etude}
                    onChange={handleChange}
                >

                    <option value="">
                        -- Choisir --
                    </option>

                    <option value="bac">
                        Baccalauréat
                    </option>

                    <option value="bac2">
                        Bac +2 / BTS
                    </option>

                    <option value="bac3">
                        Bac +3
                    </option>
                    <option value="bac4">
                        Bac +4
                    </option>

                    <option value="bac5">
                        Bac +5 / Master
                    </option>

                    <option value="doctorat">
                        Doctorat
                    </option>

                    <option value="autre">
                        Autre
                    </option>

                </select>

            </div>


            <div>

                <label>Domaine métier</label>

                <input
                    type="text"
                    name="domaine_metier"
                    value={formData.domaine_metier}
                    onChange={handleChange}
                    placeholder="Ex : Développement web"
                />

            </div>


            <div>

                <label>LinkedIn</label>

                <input
                    type="url"
                    name="lien_linkedin"
                    value={formData.lien_linkedin}
                    onChange={handleChange}
                />

            </div>


            <div>

                <label>Portfolio</label>

                <input
                    type="url"
                    name="lien_portfolio"
                    value={formData.lien_portfolio}
                    onChange={handleChange}
                />

            </div>

        </div>

    );
}

export default EtapeProfessionnel;