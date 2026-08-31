function EtapeRecherche({ formData, handleChange }) {

    return (

        <div>

            <h3>Votre recherche d'emploi 🔎</h3>

            <p>
                Indiquez-nous ce que vous recherchez.
            </p>


            <div>

                <label>Statut de recherche</label>

                <select
                    name="statut_recherche"
                    value={formData.statut_recherche}
                    onChange={handleChange}
                >

                    <option value="">
                        -- Choisir --
                    </option>

                    <option value="recherche_active">
                        Recherche active
                    </option>

                    <option value="ouvert_opportunites">
                        Ouvert aux opportunités
                    </option>

                    <option value="pas_recherche">
                        Ne recherche pas
                    </option>

                </select>

            </div>


            <div>

                <label>Disponibilité</label>

                <select
                    name="disponibilite"
                    value={formData.disponibilite}
                    onChange={handleChange}
                >

                    <option value="">
                        -- Choisir --
                    </option>

                    <option value="immediate">
                        Immédiate
                    </option>

                    <option value="1_mois">
                        Dans 1 mois
                    </option>

                    <option value="2_mois">
                        Dans 2 mois
                    </option>

                    <option value="3_mois">
                        Dans 3 mois
                    </option>

                </select>

            </div>

        </div>

    );
}

export default EtapeRecherche;