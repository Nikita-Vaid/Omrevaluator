const axios = require("axios");

exports.evaluateOMR = async (omrImage, examType) => {
    try {
        const response = await axios.post("http://127.0.0.1:5000/process-omr", {
            omrImage: omrImage.toString("base64"), 
            examType
        });
        return response.data;
    } catch (error) {
        console.error("Error in OMR processing:", error);
        throw new Error("OMR processing failed");
    }
};
