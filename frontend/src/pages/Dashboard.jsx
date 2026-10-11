import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import PredictionForm from "../components/PredictionForm";
import PredictionCard from "../components/PredictionCard";
import FeatureTable from "../components/FeatureTable";
import ExplanationCard from "../components/ExplanationCard";
import HistoryTable from "../components/HistoryTable";

import {

    generatePrediction,

    getPredictionHistory

} from "../services/api";

function Dashboard() {

    const [

        prediction,

        setPrediction

    ] = useState(null);

    const [

        history,

        setHistory

    ] = useState([]);

    useEffect(() => {

        loadHistory();

    }, []);

    async function loadHistory() {

        try {

            const response = await getPredictionHistory();

            setHistory(response.data);

        }

        catch (error) {

            console.log(error);

        }

    }

    async function handlePrediction(formData) {

        try {

            const response = await generatePrediction(formData);

            setPrediction(

                response.data

            );

            loadHistory();

        }

        catch (error) {

            console.log(error);

        }

    }

    return (

        <>

            <Navbar />

            <div className="container">

                <PredictionForm

                    onPredict={handlePrediction}

                />

                <PredictionCard

                    prediction={

                        prediction?.prediction

                    }

                />

                <FeatureTable

                    features={

                        prediction?.explanation?.top_features

                    }

                />

                <ExplanationCard

                    explanation={

                        prediction?.explanation

                    }

                />

                <HistoryTable

                    history={history}

                />

            </div>

        </>

    );

}

export default Dashboard;