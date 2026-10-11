function ExplanationCard({

    explanation

}) {

    if (!explanation) {

        return (

            <div className="card">

                <h2>AI Explanation</h2>

                <p>

                    No explanation available.

                </p>

            </div>

        );

    }

    return (

        <div className="card">

            <h2>

                AI Explanation

            </h2>

            <p>

                {explanation.ai_explanation}

            </p>

            <hr />

            <h3>

                Recommendation

            </h3>

            <p>

                {explanation.recommendation}

            </p>

        </div>

    );

}

export default ExplanationCard;