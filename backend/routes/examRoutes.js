// const express = require("express");
// const multer = require("multer");
// const axios = require("axios");
// const Exam = require("../models/Exam");

// const router = express.Router();
// const upload = multer({ dest: "uploads/" });

// // Upload Answer Key
// router.post("/upload-key", async (req, res) => {
//     try {
//         const { examType, correctAnswers } = req.body;
//         const exam = new Exam({ examType, correctAnswers });
//         await exam.save();
//         res.json({ message: "Answer key uploaded successfully" });
//     } catch (err) {
//         res.status(500).json({ error: err.message });
//     }
// });

// // Process OMR Sheet
// router.post("/process-omr", upload.single("omrSheet"), async (req, res) => {
//     try {
//         const { examType } = req.body;
//         const exam = await Exam.findOne({ examType });
//         if (!exam) return res.status(404).json({ message: "Exam not found" });

//         // Send OMR sheet to Python Flask server
//         const omrResponse = await axios.post("http://127.0.0.1:5000/process-omr", {
//             imagePath: req.file.path,
//             correctAnswers: exam.correctAnswers
//         });

//         // Save result in database
//         exam.results.push(omrResponse.data);
//         await exam.save();

//         res.json(omrResponse.data);
//     } catch (err) {
//         res.status(500).json({ error: err.message });
//     }
// });

// module.exports = router;
const express = require("express");
const multer = require("multer");
const Exam = require("../models/Exam"); // Assuming you have a model for storing exam data
const { evaluateOMR } = require("../controllers/omrController");

const router = express.Router();

// Multer storage setup for OMR sheet uploads
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Route to upload OMR sheet
router.post("/upload-omr", upload.single("omrSheet"), async (req, res) => {
    try {
        const { examType } = req.body;
        if (!req.file) {
            return res.status(400).json({ message: "No OMR sheet uploaded" });
        }
        
        // Send the file to Python for processing
        const result = await evaluateOMR(req.file.buffer, examType);
        res.json(result);
    } catch (error) {
        console.error("Error processing OMR sheet:", error);
        res.status(500).json({ message: "Server error" });
    }
});

// Route to upload correct answers (manual or file)
router.post("/upload-answers", upload.single("answerKey"), async (req, res) => {
    try {
        const { examType, manualAnswers } = req.body;
        
        let answers = {};
        if (req.file) {
            // Process CSV file for correct answers
            const csvData = req.file.buffer.toString();
            csvData.split("\n").forEach(line => {
                const [question, correctAnswer] = line.split(",");
                answers[question.trim()] = correctAnswer.trim();
            });
        } else if (manualAnswers) {
            // Parse manual answers from frontend
            answers = JSON.parse(manualAnswers);
        } else {
            return res.status(400).json({ message: "No answer key provided" });
        }

        // Save to database (optional)
        const exam = new Exam({ examType, answerKey: answers });
        await exam.save();
        
        res.json({ message: "Answer key uploaded successfully" });
    } catch (error) {
        console.error("Error uploading answer key:", error);
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;
