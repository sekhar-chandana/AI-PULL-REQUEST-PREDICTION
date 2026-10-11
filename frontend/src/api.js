// import axios from "axios";

// const api = axios.create({

//     baseURL: "http://127.0.0.1:8000/api"

// });

// export const getHealth = () =>

//     api.get("/health");


// export const getLatestPrediction = () =>

//     api.get("/prediction/latest");


// export const getPredictionHistory = () =>

//     api.get("/predictions");


// export const generatePrediction = (data) =>

//     api.post(

//         "/predict",

//         data

//     );

// export default api;


const API_BASE_URL = "http://127.0.0.1:8000";

export async function predictGitHubPR(prUrl) {
  const response = await fetch(
    `${API_BASE_URL}/api/predict/github`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        pr_url: prUrl,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Prediction request failed"
    );
  }

  return data;
}