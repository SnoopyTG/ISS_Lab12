from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter(tags=["quiz"])

class Question(BaseModel):
    id: int
    text: str
    options: List[str]
    correct: str

class AnswerSubmission(BaseModel):
    id: int
    answer: str
    score: int = 0

# Questions stored in memory (should be moved to database in production)
questions = [
    Question(
        id=1,
        text="What command lists directory contents?",
        options=["ls", "cd", "rm", "pwd"],
        correct="ls"
    ),
    Question(
        id=2,
        text="Which command searches for text in files?",
        options=["find", "grep", "locate", "cat"],
        correct="grep"
    ),
    Question(
        id=3,
        text="What changes file permissions?",
        options=["chmod", "chown", "mv", "cp"],
        correct="chmod"
    ),
    Question(
        id=4,
        text="Which command displays the current directory?",
        options=["dir", "pwd", "path", "where"],
        correct="pwd"
    ),
    Question(
        id=5,
        text="What removes a file?",
        options=["rm", "del", "erase", "unlink"],
        correct="rm"
    )
]

game_state = {"high_score": 0}

@router.get("/question", status_code=status.HTTP_200_OK)
async def get_question():
    try:
        # Randomly select a question
        question = random.choice(questions)
        return {
            "id": question.id,
            "text": question.text,
            "options": question.options
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get question: {str(e)}"
        )

@router.post("/answer", status_code=status.HTTP_200_OK)
async def submit_answer(answer: AnswerSubmission):
    try:
        question = next((q for q in questions if q.id == answer.id), None)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid question ID"
            )

        is_correct = answer.answer == question.correct
        if is_correct:
            answer.score += 10
            if answer.score > game_state["high_score"]:
                game_state["high_score"] = answer.score

        return {
            "is_correct": is_correct,
            "correct_answer": question.correct,
            "score": answer.score,
            "high_score": game_state["high_score"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process answer: {str(e)}"
        )

@router.get("/highscore", status_code=status.HTTP_200_OK)
async def get_highscore():
    try:
        return {"high_score": game_state["high_score"]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get high score: {str(e)}"
        )
