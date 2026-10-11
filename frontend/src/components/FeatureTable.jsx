function FeatureTable({

    features

}) {

    if (!features) {

        return null;

    }

    return (

        <div className="card">

            <h2>Top Features</h2>

            <table>

                <thead>

                    <tr>

                        <th>Feature</th>

                        <th>SHAP Value</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        features.map((feature, index) => (

                            <tr key={index}>

                                <td>

                                    {feature.feature}

                                </td>

                                <td>

                                    {feature.shap_value}

                                </td>

                            </tr>

                        ))

                    }

                </tbody>

            </table>

        </div>

    );

}

export default FeatureTable;