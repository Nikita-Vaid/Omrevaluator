# import cv2
# import numpy as np
# import json
# import os
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Function to process OMR sheet
# def process_omr(omr_path, answer_key):
#     img = cv2.imread(omr_path, cv2.IMREAD_GRAYSCALE)
    
#     if img is None:
#         return {"error": "Could not read OMR sheet"}

#     # Convert to binary image
#     _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)

#     num_questions = len(answer_key)
#     results = {"total_score": 0, "total_correct": 0, "total_incorrect": 0}

#     # Simulating answer detection
#     for i in range(num_questions):
#         detected_answer = str(np.random.choice(['A', 'B', 'C', 'D']))  # Replace with actual detection logic
#         correct_answer = answer_key.get(str(i + 1), "")

#         if detected_answer == correct_answer:
#             results["total_score"] += 4
#             results["total_correct"] += 1
#         else:
#             results["total_score"] -= 1
#             results["total_incorrect"] += 1

#     return results

# # API to receive OMR file and answer key
# @app.route("/process-omr", methods=["POST"])
# def process_omr_api():
#     if "omrSheet" not in request.files or "answerKey" not in request.form:
#         return jsonify({"error": "OMR sheet or answer key missing"}), 400

#     omr_file = request.files["omrSheet"]
#     answer_key = json.loads(request.form["answerKey"])
    
#     save_path = os.path.join("uploads", omr_file.filename)
#     os.makedirs("uploads", exist_ok=True)
#     omr_file.save(save_path)

#     results = process_omr(save_path, answer_key)
#     return jsonify(results)

# # Run Flask server
# if __name__ == "__main__":
#     app.run(port=5001, debug=True)
   


# import cv2
# import numpy as np
# import json
# import os
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Function to detect the filled bubble
# def detect_answer(thresh, contours, question_index):
#     """
#     Detect the filled bubble for a given question using pixel intensity.
#     """
#     num_options = 4  # Assuming 4 options per question: A, B, C, D
#     choices = ['A', 'B', 'C', 'D']

#     # Get the specific 4 bubbles for this question
#     question_bubbles = contours[question_index * num_options : (question_index + 1) * num_options]

#     if len(question_bubbles) < num_options:
#         return "N/A"  # Not enough bubbles detected

#     bubble_intensity = []

#     for idx, bubble in enumerate(question_bubbles):
#         x, y, w, h = cv2.boundingRect(bubble)
#         roi = thresh[y:y+h, x:x+w]  # Crop bubble region
#         filled_pixels = cv2.countNonZero(roi)  # Counting non-zero pixels

#         bubble_intensity.append((filled_pixels, choices[idx]))

#     # Sort by intensity (most filled = lowest value)
#     sorted_bubbles = sorted(bubble_intensity, key=lambda x: x[0])
#     detected_choice = sorted_bubbles[0][1]  # The option with the least intensity (darkest)

#     # Debugging: Print detected choices
#     print(f"Question {question_index + 1}: Detected bubbles -> {bubble_intensity}, Selected -> {detected_choice}")

#     return detected_choice

# # Function to process OMR sheet
# def process_omr(omr_path, answer_key):
#     img = cv2.imread(omr_path, cv2.IMREAD_GRAYSCALE)
    
#     if img is None:
#         return {"error": "Could not read OMR sheet"}

#     # **🔹 Preprocessing for better detection**
#     blurred = cv2.GaussianBlur(img, (5, 5), 0)  # Reduce noise
#     _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # Adaptive thresholding

#     # **🔹 Morphological operations to refine contours**
#     kernel = np.ones((3,3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)  # Remove noise

#     # Detect contours (bubbles)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # **Filter small contours to remove noise**
#     contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

#     # **Sort contours properly (Row-wise first, then column-wise)**
#     def sort_contours(cnts):
#         """ Sort contours from top to bottom, then left to right """
#         bounding_boxes = [cv2.boundingRect(c) for c in cnts]
#         cnts_sorted = sorted(zip(cnts, bounding_boxes), key=lambda b: (b[1][1], b[1][0]))
#         return [cnt[0] for cnt in cnts_sorted]

#     contours = sort_contours(contours)

#     num_questions = len(answer_key)
#     results = {"total_score": 0, "total_correct": 0, "total_incorrect": 0, "question_wise": {}}

#     for i in range(num_questions):
#         detected_answer = detect_answer(thresh, contours, i)
#         correct_answer = answer_key.get(str(i + 1), "")

#         if detected_answer == correct_answer:
#             results["total_score"] += 4
#             results["total_correct"] += 1
#             results["question_wise"][str(i + 1)] = {"detected": detected_answer, "correct": correct_answer, "status": "correct"}
#         else:
#             results["total_score"] -= 1
#             results["total_incorrect"] += 1
#             results["question_wise"][str(i + 1)] = {"detected": detected_answer, "correct": correct_answer, "status": "incorrect"}

#     return results


# # API to receive OMR file and answer key
# @app.route("/process-omr", methods=["POST"])
# def process_omr_api():
#     if "omrSheet" not in request.files or "answerKey" not in request.form:
#         return jsonify({"error": "OMR sheet or answer key missing"}), 400

#     omr_file = request.files["omrSheet"]
#     answer_key = json.loads(request.form["answerKey"])
    
#     save_path = os.path.join("uploads", omr_file.filename)
#     os.makedirs("uploads", exist_ok=True)
#     omr_file.save(save_path)

#     results = process_omr(save_path, answer_key)
#     return jsonify(results)

# # Run Flask server
# if __name__ == "__main__":
#     app.run(port=5001, debug=True)

import cv2
import numpy as np

# Define choices (A, B, C, D)
CHOICES = ['A', 'B', 'C', 'D']

# Define the threshold for considering a bubble as filled
FILLED_BUBBLE_THRESHOLD = 0.6  

def preprocess_scanned_image(image_path):
    """Load and preprocess the scanned OMR sheet image."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to detect bubbles clearly
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 5
    )

    return image, gray, thresh

def detect_bubbles(thresh):
    """Find bubbles in the thresholded image."""
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours top to bottom and left to right
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
    
    return contours

def get_marked_option(thresh, contours, question_index):
    """Detect the marked bubble for a specific question."""
    num_options = len(CHOICES)

    # Get the four bubbles for the question
    question_bubbles = contours[question_index * num_options: (question_index + 1) * num_options]

    if len(question_bubbles) < num_options:
        print(f"[DEBUG] Question {question_index + 1}: Not enough bubbles detected!")
        return "N/A"

    bubble_filled_ratio = []

    for idx, bubble in enumerate(question_bubbles):
        x, y, w, h = cv2.boundingRect(bubble)
        roi = thresh[y:y + h, x:x + w]  # Crop the bubble region
        filled_pixels = cv2.countNonZero(roi)  # Count the number of dark pixels
        
        total_pixels = w * h  # Total pixels in the bubble area
        fill_ratio = filled_pixels / total_pixels  # Compute the fill ratio
        
        bubble_filled_ratio.append((fill_ratio, CHOICES[idx]))

    # Sort bubbles by fill ratio (most filled first)
    bubble_filled_ratio.sort(reverse=True, key=lambda x: x[0])

    print(f"[DEBUG] Question {question_index + 1}: Fill Ratios -> {bubble_filled_ratio}")

    # Select the most filled bubble if above the threshold
    most_filled = bubble_filled_ratio[0]  

    if most_filled[0] > FILLED_BUBBLE_THRESHOLD:
        detected_answer = most_filled[1]
    else:
        detected_answer = "N/A"

    print(f"[DEBUG] Question {question_index + 1}: Detected Answer -> {detected_answer}")

    return detected_answer

def process_scanned_omr(image_path, correct_answers):
    """Process the scanned OMR sheet and evaluate answers."""
    image, gray, thresh = preprocess_scanned_image(image_path)
    contours = detect_bubbles(thresh)

    print(f"[DEBUG] Total contours detected: {len(contours)}")

    detected_answers = []
    score = 0

    for q in range(len(correct_answers)):
        detected = get_marked_option(thresh, contours, q)
        detected_answers.append(detected)

        if detected == correct_answers[q]:
            score += 4  # +4 for correct
        elif detected != "N/A":
            score -= 1  # -1 for incorrect

        print(f"[DEBUG] Question {q + 1}: Detected -> {detected}, Correct -> {correct_answers[q]}")

    print(f"Total Score: {score}")
    return detected_answers, score

# Example Usage
image_path = "scanned_omr_sheet.jpg"  # Change to your scanned OMR sheet path
correct_answers = ['B', 'C', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B']  # Example correct answers

detected_answers, total_score = process_scanned_omr(image_path, correct_answers)
