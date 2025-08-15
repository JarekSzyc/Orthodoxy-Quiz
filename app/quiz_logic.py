from typing import Dict, List, Tuple
import json
import random
question_type = Dict[str, List[Tuple[str, float]]]

def validate_question(question_object: question_type) -> None:
    """
    Sanity check.

    Make absolute sure that question has proper structure and expected parameters.
    """
    assert isinstance(question_object, dict), f'Question type is not dictionary! Actual type: {type(question_object)}'
    assert 'Question text' in question_object.keys(), 'No "Question text" key within Question Object!'
    assert isinstance(question_object['Question text'], str) and len(question_object['Question text']), 'Question text must be a non-empty string!'
    assert 'Answers' in question_object.keys(), 'No "Answers" key within Question Object!'
    assert len(question_object['Answers'])>1, 'There need to be at least two answers for any given question!'
    for answer in question_object['Answers']:
        assert len(answer)==2, f"The answer has to have string value and float value. No more, no less!\nCurrently it has length = {len(answer)}"
        assert isinstance(answer[0], str) and len(answer[0]), 'Answer must be a non-empty string!'
        assert answer[1] >= 0 and answer[1] <= 1, 'Invalid Orthodoxy value - must be 0 <= val <= 1'
    # to think if it's not too restrictive
    assert question_object['Answers'][0][1]==1.0, 'First Answer must be fully complient with the Catholic Doctrine!'
    assert question_object['Answers'][-1][1]==0.0, 'Last Answer must be fully incompatible with the Catholic Doctrine!'

def validate_all_questions(questions: List[question_type]) -> None:
    """
    Loop over all question objects

    Skip check if deployed on Production
    """
    for q in questions:
        validate_question(q)
    print(f"---\nALL CHECKS ARE GOOD! Number of questions: {len(questions)}\n---\n")

def load_questions_from_json(filepath: str, need_validation:bool=False) -> List[question_type]:
    """
    Safety assumptions later checked by validate_all_questions()
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert inner lists to tuples to match type hints (type purism at this point)
        for q in data:
            q['Answers'] = [tuple(a) for a in q['Answers']]
        
        if need_validation:
            validate_all_questions(data)
        return data

    except FileNotFoundError:
        raise RuntimeError(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error parsing JSON file {filepath}: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error loading questions from {filepath}: {e}")

def generate_random_user_answers(questions:List[question_type]) -> List[int]:
    """
    For actual list of questions get valid answer example (indices of answers)
    """
    res = []
    for q in questions:
        res.append(random.randint(0, len(q['Answers'])-1))
    return res

def calculate_orthodoxy_score(questions:List[question_type], user_answers:List[int], precision:int=4) -> float:
    """
    Return single value based on answers' weights.

    0 <= score <= 1
    """
    assert len(questions), f'THERE MUST BE AT LEAST ONE QUESTION PRESENT!!!'
    assert len(questions)==len(user_answers), f'There is different number of questions and answers!!! ({len(questions)} vs {len(user_answers)})'
    score = 0
    for q, a in zip(questions, user_answers):    
        score += q['Answers'][a][1]
    return round(score/len(questions), precision)

if __name__=="__main__":
    questions = load_questions_from_json('questions.json', need_validation=True)
    
    example_user_answers = generate_random_user_answers(questions)
    score_calculated = calculate_orthodoxy_score(questions, example_user_answers)

    print(f'Your score: {score_calculated*100:.0f}% ')