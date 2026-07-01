from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from retriever import search_assessments, filter_remote
from gemini import ask_gemini

from retriever import (
    search_assessments,
    filter_remote,
    compare_assessments
)
app = FastAPI()



@app.get("/health")
def health():
    return {"status": "ok"}



class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]




@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages
    user_query = messages[-1].content.lower()
    # Build conversation context
    conversation_text = " ".join(
        [m.content.lower() for m in messages if m.role == "user"]
    )

   

    off_topics = [
        "weather",
        "movie",
        "cricket",
        "football",
        "politics",
        "recipe"
    ]

    if any(word in user_query for word in off_topics):
        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }



    vague_queries = [
        "assessment",
        "test",
        "need assessment",
        "i need an assessment",
        "i need a test"
    ]

    if len(messages) == 1:

        if any(q in user_query for q in vague_queries):

            return {
                "reply": "Sure! What role are you hiring for? (Example: Java Developer, Python Developer, Sales Manager)",
                "recommendations": [],
                "end_of_conversation": False
            }



    if len(messages) == 3:

        return {
            "reply": "How many years of experience does the candidate have?",
            "recommendations": [],
            "end_of_conversation": False
        }


    if len(messages) == 5:

        return {
            "reply": "Is this for hiring (selection) or employee development?",
            "recommendations": [],
            "end_of_conversation": False
        }



    assessments = search_assessments(conversation_text)

  

    if "remote" in user_query:

        assessments = filter_remote(assessments)

        recommendations = []

        for item in assessments[:10]:

            recommendations.append({
                "name": item.get("name", ""),
                "url": item.get("link", ""),
                "test_type": item.get("test_type", "")
            })

        return {
            "reply": "Updated recommendations: Showing only remote-enabled SHL assessments.",
            "recommendations": recommendations,
            "end_of_conversation": False
        }

  

    if len(assessments) == 0:

        return {
            "reply": "I couldn't find any matching SHL assessments. Could you provide more details?",
            "recommendations": [],
            "end_of_conversation": False
        }
    


    if "compare" in user_query:
        text = user_query.replace("compare", "")

        names = text.split(" and ")

        if len(names) == 2:

            test1, test2 = compare_assessments(
               names[0].strip(),
               names[1].strip()
            )

            if test1 and test2:

               comparison = f"""
    Comparison

    Assessment 1:
    Name : {test1['name']}
    Duration : {test1.get('duration','N/A')}
    Remote : {test1.get('remote','N/A')}
    Adaptive : {test1.get('adaptive','N/A')}

    Assessment 2:
    Name : {test2['name']}
    Duration : {test2.get('duration','N/A')}
    Remote : {test2.get('remote','N/A')}
    Adaptive : {test2.get('adaptive','N/A')}
    """

            return {
                "reply": comparison,

                "recommendations": [

                    {
                        "name": test1["name"],
                        "url": test1["link"],
                        "test_type": test1.get("test_type", "")
                    },

                    {
                        "name": test2["name"],
                        "url": test2["link"],
                        "test_type": test2.get("test_type", "")
                    }

                ],

                "end_of_conversation": False

            }


    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Use ONLY the assessments provided below.

Never recommend assessments outside this list.

User Query:
{user_query}

Matching Assessments:
{assessments}

Explain why each assessment is suitable.

Return only recommendations from the catalog.
"""

    reply = ask_gemini(prompt)


    recommendations = []

    for item in assessments[:10]:

        recommendations.append({

            "name": item.get("name", ""),
            "url": item.get("link", ""),
            "test_type": item.get("test_type", "")

        })

    return {

        "reply": reply,

        "recommendations": recommendations,

        "end_of_conversation": False

    }