import google.generativeai as genai
import re

# Configure Gemini API key (make sure this key is correct and secure)
genai.configure(api_key="AIzaSyBOHXVPbBX2tHur1mPiP0Yspi-gCr-6y30")

def generate_questions(topic, concept, difficulty="beginner to advance level", num_questions=10):
    # Step 1: Generate 10 multiple choice questions
    prompt = (
        f"Your task is to generate EXACTLY {num_questions} multiple-choice questions on the concept '{concept}' "
f"in the programming language '{topic}'.\n\n"

"IMPORTANT RULES (follow strictly):\n"
"1. Generate ONLY 10 questions. Not more. Not less. NO EXCEPTIONS.\n"
"2. Number the questions from 1 to 10 — all numbers must be present, in order.\n"
"3. Each question must have exactly four options labeled as (A), (B), (C), and (D).\n"
"4. After each question, on a new line, write the correct answer in this format: Answer: A\n"
"5. On a new line AFTER the answer, add a brief explanation (1–3 lines max) in this format:\n"
"Explanation: Your explanation here.\n"
"6. DO NOT include any extra text, titles, or formatting outside of the pattern below.\n"
"7. DO NOT include bullets, asterisks, or dots before question numbers or options.\n\n"

"Use the EXACT following format:\n"
"1. Question text?\n"
"(A) Option A\n"
"(B) Option B\n"
"(C) Option C\n"
"(D) Option D\n"
"Answer: B\n"
"Explanation: This is a short explanation for why B is correct.\n"
"..."

    )

    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Step 2: Parse the questions
    q_chunks = re.split(r"(?=\d+\.\s)", raw)
    questions = []
    question_texts = []

    for chunk in q_chunks:
        lines = chunk.strip().splitlines()
        if len(lines) < 6:
            continue

        question_text = lines[0].strip()[3:].strip()
        question_texts.append(question_text)
        options = {
            "A": lines[1].split(")", 1)[-1].strip(),
            "B": lines[2].split(")", 1)[-1].strip(),
            "C": lines[3].split(")", 1)[-1].strip(),
            "D": lines[4].split(")", 1)[-1].strip(),
        }
        answer_match = re.search(r"Answer:\s*([A-D])", lines[5], re.IGNORECASE)
        correct_answer = answer_match.group(1).upper() if answer_match else None
        

        explanation = lines[6].strip() if len(lines) > 6 else "Explanation not available"
        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_answer,
            "explanation": explanation  # Placeholder for now
        })

    # Step 3: Generate short explanations for each question
    explanation_prompt = (
    "For each of the following programming questions, provide a detailed, beginner-friendly explanation in 5 to 8 lines. "
    "Each explanation should clearly describe the concept, the reasoning behind the correct answer, and any important details a learner should understand.\n\n"
    + "\n".join([f"{i+1}. {q}" for i, q in enumerate(question_texts)])
)


    explanation_response = model.generate_content(explanation_prompt)
    explanation_lines = explanation_response.text.strip().splitlines()

    # Add explanations to corresponding questions
    explanation_index = 0
    for line in explanation_lines:
        if explanation_index < len(questions) and line.strip():
            questions[explanation_index]["explanation"] = line.strip()
            explanation_index += 1

    return questions
