import { useState } from "react";
import axios from "axios";

const UploadKey = () => {
    const [examType, setExamType] = useState("");
    const [correctAnswers, setCorrectAnswers] = useState({});

    const handleSubmit = async () => {
        await axios.post("http://localhost:5000/api/exams/upload-key", {
            examType,
            correctAnswers
        });
        alert("Answer Key Uploaded!");
    };

    return (
        <div>
            <h2>Upload Answer Key</h2>
            <input type="text" placeholder="Exam Type" onChange={e => setExamType(e.target.value)} />
            <textarea onChange={e => setCorrectAnswers(JSON.parse(e.target.value))} />
            <button onClick={handleSubmit}>Upload</button>
        </div>
    );
};

export default UploadKey;
