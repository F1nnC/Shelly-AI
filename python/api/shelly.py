from .surf import get_surf_conditions_time
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from sqlalchemy.exc import SQLAlchemyError

shelly_bp = Blueprint('shelly', __name__)

@shelly_bp.route('/ask', methods=['POST'])
@jwt_required()
def ask():
    data = request.get_json()
    question = data.get('question')
    chat_history = data.get('chat_history')
    time_surf = data.get('time_surf')

    print("getting surf conditions")
    surf_data = get_surf_conditions_time(time_surf)


    template = """
        Answer the following question with like a surfer accent.
        
        General Information to know, you are a surf condition helper AI called ShellyAI
        
        People can give you questions about surf conditions and you can answer them
        
        Please don't make up any information, only answer based on the surf data, this data is only showing the time period of the day where the person wants to go
        
        Respond with only a sentence or two, don't give a long answer, just saying I recommend blank because of blank make sure to mention some data from the surf data, wave height is important
        
        Here is the surf conditions of the day: {surf_data}
        
        Here is the conversation history: {history}
        
        Question: {question}
    """
    
    print("making template")
    model = OllamaLLM(model="llama3.2:1b")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    print("making chain invoke starting")
    answer = chain.invoke({"question": question, "history": chat_history, "surf_data": surf_data})

    return jsonify({'answer': answer})