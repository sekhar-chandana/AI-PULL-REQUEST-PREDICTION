function HistoryTable({

    history

}) {

    if (!history || history.length === 0) {

        return (

            <div className="card">

                <h2>

                    Prediction History

                </h2>

                <p>

                    No predictions available.

                </p>

            </div>

        );

    }

    return (

        <div className="card">

            <h2>

                Prediction History

            </h2>

            <table>

                <thead>

                    <tr>

                        <th>ID</th>

                        <th>Prediction</th>

                        <th>Risk Score</th>

                        <th>Confidence</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        history.map((item) => (

                            <tr key={item.prediction_id}>

                                <td>

                                    {item.prediction_id}

                                </td>

                                <td>

                                    {item.prediction}

                                </td>

                                <td>

                                    {item.risk_score}

                                </td>

                                <td>

                                    {item.confidence}%

                                </td>

                            </tr>

                        ))

                    }

                </tbody>

            </table>

        </div>

    );

}

export default HistoryTable;