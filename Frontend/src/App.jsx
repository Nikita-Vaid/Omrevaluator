import React, { useState } from "react";
import axios from "axios";

function App() {
    const [omrFile, setOmrFile] = useState(null);
    const [answerFile, setAnswerFile] = useState(null);
    const [manualAnswers, setManualAnswers] = useState({});
    const [examType, setExamType] = useState("JEE");
    const [results, setResults] = useState(null);

    const handleOMRUpload = async () => {
        const formData = new FormData();
        formData.append("omrSheet", omrFile);
        formData.append("examType", examType);

        try {
            const response = await axios.post("http://localhost:5000/api/exams/upload-omr", formData);
            setResults(response.data);
        } catch (error) {
            console.error("Error uploading OMR:", error);
            alert("Failed to evaluate OMR sheet.");
        }
    };

    const handleAnswerUpload = async () => {
        const formData = new FormData();
        if (answerFile) {
            formData.append("answerKey", answerFile);
        } else {
            formData.append("manualAnswers", JSON.stringify(manualAnswers));
        }
        formData.append("examType", examType);

        try {
            await axios.post("http://localhost:5000/api/exams/upload-answers", formData);
            alert("Answer key uploaded successfully!");
        } catch (error) {
            console.error("Error uploading answers:", error);
            alert("Failed to upload answer key.");
        }
    };

    return (
        <div>
            <h1>OMR Evaluation System</h1>

            <label>Choose Exam Type:</label>
            <select value={examType} onChange={(e) => setExamType(e.target.value)}>
                <option value="JEE">JEE Mains</option>
                <option value="NEET">NEET</option>
            </select>

            <h2>Upload OMR Sheet</h2>
            <input type="file" onChange={(e) => setOmrFile(e.target.files[0])} />
            <button onClick={handleOMRUpload}>Upload & Evaluate</button>

            <h2>Upload Answer Key</h2>
            <input type="file" onChange={(e) => setAnswerFile(e.target.files[0])} />
            <button onClick={handleAnswerUpload}>Upload Answer Key</button>

            {results && (
                <div>
                    <h2>Results</h2>
                    <p><strong>Total Score:</strong> {results.total_score}</p>
                    <p><strong>Total Correct:</strong> {results.total_correct}</p>
                    <p><strong>Total Incorrect:</strong> {results.total_incorrect}</p>
                </div>
            )}
        </div>
    );
}

export default App;

