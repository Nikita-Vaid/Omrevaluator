const mongoose = require("mongoose");

const ExamSchema = new mongoose.Schema({
    examType: { type: String, required: true }, // JEE or NEET
    correctAnswers: { type: Map, of: String }, // Store answers as { "1": "A", "2": "B" }
    results: [
        {
            studentId: String,
            correct: Number,
            incorrect: Number,
            totalMarks: Number,
            questionWise: Object
        }
    ]
});

module.exports = mongoose.model("Exam", ExamSchema);
