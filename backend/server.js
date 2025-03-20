const express = require("express");
const multer = require("multer");
const mongoose = require("mongoose");
const cors = require("cors");
const axios = require("axios");
const fs = require("fs");
const path = require("path");
const FormData = require("form-data"); // ✅ Import FormData correctly

const AnswerKey = require("./models/AnswerKey");

const app = express();
app.use(cors());
app.use(express.json());

// ✅ Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/omr_evaluator")
    .then(() => console.log("✅ MongoDB Connected"))
    .catch(err => console.error("❌ MongoDB Connection Failed:", err));

// ✅ Configure Multer for File Uploads
const upload = multer({ dest: "uploads/" });
/* -----------------------------------
   ✅ Upload Answer Key (Manual or CSV)
----------------------------------- */
app.post("/api/exams/upload-answers", upload.single("answerKey"), async (req, res) => {
    try {
        const { examType, manualAnswers } = req.body;
        let answerData = {};

        if (req.file) {
            // ✅ Read and Parse CSV File
            const csvData = fs.readFileSync(req.file.path, "utf8");
            const lines = csvData.split("\n");
            lines.forEach(line => {
                const [qNo, ans] = line.trim().split(",");
                if (qNo && ans) answerData[qNo] = ans;
            });
        } else if (manualAnswers) {
            answerData = JSON.parse(manualAnswers);
        }

        if (!answerData || Object.keys(answerData).length === 0) {
            return res.status(400).json({ error: "Invalid answer key format" });
        }

        // ✅ Save Answer Key in MongoDB
        await AnswerKey.findOneAndUpdate(
            { examType },
            { examType, answers: answerData },
            { upsert: true, new: true }
        );

        res.json({ message: "✅ Answer key uploaded successfully!" });
    } catch (error) {
        console.error("❌ Error uploading answer key:", error);
        res.status(500).json({ error: "Failed to upload answer key" });
    }
});

/* -----------------------------------
   ✅ Upload & Evaluate OMR Sheet
----------------------------------- */
app.post("/api/exams/upload-omr", upload.single("omrSheet"), async (req, res) => {
    try {
        const { examType } = req.body;
        if (!req.file) return res.status(400).json({ error: "OMR sheet is required" });

        // ✅ Fetch the Answer Key from MongoDB
        const answerKeyDoc = await AnswerKey.findOne({ examType });
        if (!answerKeyDoc) return res.status(400).json({ error: "Answer key not found" });

        const answerKey = answerKeyDoc.answers;

        // ✅ Prepare FormData for Flask API
        const omrFormData = new FormData();
        omrFormData.append("omrSheet", fs.createReadStream(req.file.path));
        omrFormData.append("answerKey", JSON.stringify(answerKey));

        // ✅ Send Request to OMR Processing API
        const response = await axios.post("http://localhost:5001/process-omr", omrFormData, {
            headers: omrFormData.getHeaders(),
        });

        res.json(response.data);
    } catch (error) {
        console.error("❌ Error processing OMR:", error);
        res.status(500).json({ error: "Failed to evaluate OMR sheet" });
    }
});

/* -----------------------------------
   ✅ Start Express Server
----------------------------------- */
const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));

// PS D:\TestPlatform\backend> netstat -ano | findstr :5000
// >> 
//   TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING       25512
//   TCP    [::]:5000              [::]:0                 LISTENING       25512
// PS D:\TestPlatform\backend> netstat -ano | findstr :5000
// taskkill /PID 23996 /F

// SUCCESS: The process with PID 25512 has been terminated.
// PS D:\TestPlatform\backend> npm start
