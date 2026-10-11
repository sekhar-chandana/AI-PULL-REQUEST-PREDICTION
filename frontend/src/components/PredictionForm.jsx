import { useState } from "react";

function PredictionForm({ onPredict }) {

    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState({

        language: 0,
        stars: 3713,
        forks: 1000,
        license: 1,

        review_count: 1,
        approved_reviews: 1,
        commented_reviews: 0,
        comment_count: 0,

        commit_count: 1,
        files_changed: 3,

        additions: 78,
        deletions: 68,

        total_changes: 146,
        total_lines_changed: 146,

        test_files: 0,
        high_risk_files: 0,

        review_time_hours: 24,

        created_year: 2025,
        created_month: 1,
        created_day: 1,
        created_weekday: 2,

        merged: 1

    });

    const handleChange = (event) => {

        const { name, value } = event.target;

        setFormData({

            ...formData,

            [name]: Number(value)

        });

    };

    const handleSubmit = async (event) => {

        event.preventDefault();

        setLoading(true);

        try {

            await onPredict(formData);

        } catch (error) {

            console.error(

                "Prediction Error:",

                error

            );

        } finally {

            setLoading(false);

        }

    };

    return (

        <div className="card">

            <h2>Pull Request Prediction</h2>

            <form onSubmit={handleSubmit}>

                <label>Language Code</label>

                <input
                    type="number"
                    name="language"
                    value={formData.language}
                    onChange={handleChange}
                />

                <label>Stars</label>

                <input
                    type="number"
                    name="stars"
                    value={formData.stars}
                    onChange={handleChange}
                />

                <label>Forks</label>

                <input
                    type="number"
                    name="forks"
                    value={formData.forks}
                    onChange={handleChange}
                />

                <label>License Code</label>

                <input
                    type="number"
                    name="license"
                    value={formData.license}
                    onChange={handleChange}
                />

                <label>Review Count</label>

                <input
                    type="number"
                    name="review_count"
                    value={formData.review_count}
                    onChange={handleChange}
                />

                <label>Approved Reviews</label>

                <input
                    type="number"
                    name="approved_reviews"
                    value={formData.approved_reviews}
                    onChange={handleChange}
                />

                <label>Commented Reviews</label>

                <input
                    type="number"
                    name="commented_reviews"
                    value={formData.commented_reviews}
                    onChange={handleChange}
                />

                <label>Comment Count</label>

                <input
                    type="number"
                    name="comment_count"
                    value={formData.comment_count}
                    onChange={handleChange}
                />

                <label>Commit Count</label>

                <input
                    type="number"
                    name="commit_count"
                    value={formData.commit_count}
                    onChange={handleChange}
                />

                <label>Files Changed</label>

                <input
                    type="number"
                    name="files_changed"
                    value={formData.files_changed}
                    onChange={handleChange}
                />

                <label>Additions</label>

                <input
                    type="number"
                    name="additions"
                    value={formData.additions}
                    onChange={handleChange}
                />

                <label>Deletions</label>

                <input
                    type="number"
                    name="deletions"
                    value={formData.deletions}
                    onChange={handleChange}
                />

                <label>Total Changes</label>

                <input
                    type="number"
                    name="total_changes"
                    value={formData.total_changes}
                    onChange={handleChange}
                />

                <label>Total Lines Changed</label>

                <input
                    type="number"
                    name="total_lines_changed"
                    value={formData.total_lines_changed}
                    onChange={handleChange}
                />

                <label>Test Files</label>

                <input
                    type="number"
                    name="test_files"
                    value={formData.test_files}
                    onChange={handleChange}
                />

                <label>High Risk Files</label>

                <input
                    type="number"
                    name="high_risk_files"
                    value={formData.high_risk_files}
                    onChange={handleChange}
                />

                <label>Review Time Hours</label>

                <input
                    type="number"
                    name="review_time_hours"
                    value={formData.review_time_hours}
                    onChange={handleChange}
                />

                <label>Created Year</label>

                <input
                    type="number"
                    name="created_year"
                    value={formData.created_year}
                    onChange={handleChange}
                />

                <label>Created Month</label>

                <input
                    type="number"
                    name="created_month"
                    value={formData.created_month}
                    onChange={handleChange}
                />

                <label>Created Day</label>

                <input
                    type="number"
                    name="created_day"
                    value={formData.created_day}
                    onChange={handleChange}
                />

                <label>Created Weekday</label>

                <input
                    type="number"
                    name="created_weekday"
                    value={formData.created_weekday}
                    onChange={handleChange}
                />

                <label>Merged</label>

                <input
                    type="number"
                    name="merged"
                    value={formData.merged}
                    onChange={handleChange}
                />

                <button type="submit">

                    {loading
                        ? "Predicting..."
                        : "Predict Risk"
                    }

                </button>

            </form>

        </div>

    );

}

export default PredictionForm;