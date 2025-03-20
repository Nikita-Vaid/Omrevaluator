const mongoose = require("mongoose");

const AnswerKeySchema = new mongoose.Schema({
    examType: { type: String, required: true, unique: true },  // "JEE" or "NEET"
    answers: { type: Object },  // Stores manual answers (JSON format)
    csvPath: { type: String }   // Stores path to CSV file (if uploaded)
});

module.exports = mongoose.model("AnswerKey", AnswerKeySchema);
