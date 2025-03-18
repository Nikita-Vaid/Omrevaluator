import cv2
import numpy as np

def process_omr(image_path, correct_answers):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)

    # Example: Assume we detect 20 answers and match them with correct ones
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
