function PredictionCard({

    prediction

}) {

    if (!prediction) {

        return (

            <div className="card">

                <h2>Prediction</h2>

                <p>No prediction generated.</p>

            </div>

        );

    }

    return (

        <div className="card">

            <h2>Prediction Result</h2>

            <p>

                <strong>Prediction:</strong>

                {" "}

                {prediction.label}

            </p>

            <p>

                <strong>Risk Score:</strong>

                {" "}

                {prediction.risk_score}

            </p>

            <p>

                <strong>Confidence:</strong>

                {" "}

                {prediction.confidence}%

            </p>

            <p>

                <strong>Risk Level:</strong>

                {" "}

                {prediction.risk_level}

            </p>

        </div>

    );

}

export default PredictionCard;