import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# JEE and NEET Scoring Rules
JEE_SCORING = {"Section1": {"correct": 4, "incorrect": -1}, "Section2": {"correct": 4, "incorrect": -1}}
NEET_SCORING = {"correct": 4, "incorrect": -1}

def process_omr(image_path, correct_answers):
    """ Process OMR sheet image and evaluate answers. """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)

    # Simulating detected answers (Replace with actual detection logic)
    detected_answers = {str(i + 1): "A" for i in range(len(correct_answers))}

    correct = 0
    incorrect = 0
    question_wise = {}

    for q_no, correct_ans in correct_answers.items():
        student_ans = detected_answers.get(q_no, "X")  # X means not attempted
        if student_ans == correct_ans:
            correct += 1
            question_wise[q_no] = "Correct"
        else:
            incorrect += 1
            question_wise[q_no] = "Incorrect"

    total_marks = (correct * 4) - (incorrect * 1)
    
    return {
        "correct": correct,
        "incorrect": incorrect,
        "totalMarks": total_marks,
        "questionWise": question_wise
    }

@app.route("/process-omr", methods=["POST"])
def process_omr_api():
    """ API Endpoint to process OMR sheets. """
    data = request.json
    exam_type = data.get("examType")
    omr_image_data = base64.b64decode(data["omrImage"])

    # Save image temporarily
    image_path = "temp_omr.png"
    with open(image_path, "wb") as f:
        f.write(omr_image_data)

    # Load correct answers (Assuming JSON format)
    correct_answers = {"1": "A", "2": "B", "3": "C"}  # Replace with actual answer key loading logic

    result = process_omr(image_path, correct_answers)

    return jsonify({
        "total_score": result["totalMarks"],
        "total_correct": result["correct"],
        "total_incorrect": result["incorrect"],
        "questionWise": result["questionWise"]
    })

if __name__ == "__main__":
    app.run(debug=True)


