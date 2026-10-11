import { useState } from "react";

import { predictGitHubPR } from "./api";

function App() {

  const [prUrl, setPrUrl] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const handlePredict = async (event) => {

    event.preventDefault();

    setError("");

    setResult(null);

    if (!prUrl.trim()) {

      setError(
        "Please enter a GitHub Pull Request URL."
      );

      return;

    }

    try {

      setLoading(true);

      const data = await predictGitHubPR(
        prUrl.trim()
      );
        console.log(
  "FULL API RESPONSE:",
  data
);
    console.log(
  "EXPLANATION OBJECT:",
  data.prediction?.explanation
);
      setResult(data);

    } catch (err) {

      setError(
        err.message ||
        "Unable to analyze Pull Request."
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="app">

      <header className="header">

        <h1>
          AI Pull Request Risk Predictor
        </h1>

        <p>
          Analyze GitHub Pull Requests for potential risk
        </p>

      </header>


      <main className="container">

        <form
          onSubmit={handlePredict}
          className="pr-form"
        >

          <label>
            GitHub Pull Request URL
          </label>

          <input
            type="url"
            value={prUrl}
            onChange={(event) =>
              setPrUrl(event.target.value)
            }
            placeholder="https://github.com/owner/repository/pull/123"
          />

          <button
            type="submit"
            disabled={loading}
          >

            {loading
              ? "Analyzing..."
              : "Analyze Pull Request"
            }

          </button>

        </form>


        {error && (

          <div className="error">

            {error}

          </div>

        )}


        {loading && (

          <div className="loading">

            Loading GitHub data and generating prediction...

          </div>

        )}


        {result && (

          <section className="results">

            <h2>
              Pull Request Analysis
            </h2>


            <div className="repository">

              <strong>
                Repository:
              </strong>{" "}

              {result.repository}

            </div>


            <div className="pr-title">

              <strong>
                Pull Request:
              </strong>{" "}

              #{result.pull_request.number}{" "}

              {result.pull_request.title}

            </div>


            <div className="prediction-card">

              <h3>
                Prediction
              </h3>

              <p>
                {result.prediction.prediction?.label}
              </p>

              <p>
                Risk Score:{" "}

                {result.prediction.prediction?.risk_score}
              </p>

              <p>
                Confidence:{" "}

                {result.prediction.prediction?.confidence}
              </p>

              <p>
                Risk Level:{" "}

                {result.prediction.prediction?.risk_level}
              </p>

            </div>


            <div className="features">

              <h3>
                Important Features
              </h3>

              {result.prediction.explanation?.top_features &&

                result.prediction.explanation.top_features.map(
                  (feature, index) => (

                    <div
                      key={index}
                      className="feature"
                    >

                      <strong>
                        {feature.feature}
                      </strong>

                      <span>
                        Impact: {feature.shap_value}
                      </span>

                    </div>

                  )
                )

              }

            </div>


           <div className="explanation">

  <h3>
    AI Explanation
  </h3>

  <div className="ai-explanation">

    {result.prediction?.explanation?.ai_explanation ||
      "AI explanation was not generated."
    }

  </div>

</div>

          </section>

        )}

      </main>

    </div>

  );

}

export default App;