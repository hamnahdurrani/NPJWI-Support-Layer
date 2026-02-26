from model import EvaluationRequest, UserInput

def build_evaluation_request(
    access_code: str,
    user_id: str,
    question: str
) -> EvaluationRequest:

    return EvaluationRequest(
        usageKey=user_id,
        userID=user_id,
        accessCode=access_code,
        userInput=UserInput(
            text=question
        )
    )