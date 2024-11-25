import logging
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from data.surf_data_fetcher import spot_data_time

shelly_bp = Blueprint('shelly_bp', __name__)

@shelly_bp.route('/ask', methods=['POST'])
@jwt_required()
def ask():
    data = request.get_json()
    print("Received data:", data)  # Debugging line

    if data is None:
        print("No JSON data received")
        return jsonify({"msg": "No JSON data received"}), 400

    question = data.get('question')
    chat_history = data.get('chat_history', "")
    spots = data.get('spots')
    time_period = data.get('time_period')

    # Validate input data
    if not isinstance(question, str):
        print("Invalid question:", question)
        return jsonify({"msg": "Question must be a string"}), 422
    if not isinstance(chat_history, str):
        print("Invalid chat_history:", chat_history)
        return jsonify({"msg": "Chat history must be a string"}), 422
    if not isinstance(spots, list) or not all(isinstance(spot, str) for spot in spots):
        print("Invalid spots:", spots)
        return jsonify({"msg": "Spots must be a list of strings"}), 422
    if time_period not in ["morning", "noon", "afternoon"]:
        print("Invalid time_period:", time_period)
        return jsonify({"msg": "Invalid time period"}), 422

    print("getting surf conditions")
    surf_data = []
    for spot_id in spots:
        spot_data = spot_data_time(spot_id, time_period)
        surf_data.extend(spot_data)

    template = """
        Answer the following question with like a surfer accent.
        
        General Information to know, you are a surf condition helper AI called ShellyAI
        
        People can give you questions about surf conditions and you can answer them
        
        Please don't make up any information, only answer based on the surf data, this data is only showing the time period of the day where the person wants to go
        
        Respond with only a sentence or two, don't give a long answer, just saying I recommend saying in a funny language where to go surf, then in the second give the data for why you recommend that spot
        
        Here is the surf conditions of the day: {surf_data}
        
        Question: {question}
    """
    
    print("making template")
    # Point to the Ollama service running on the Docker container
    model = OllamaLLM(model="llama3.2:1b", endpoint="http://ollama:11434")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    
    print("making chain invoke starting")
    try:
        answer = chain.invoke({"question": question, "history": chat_history, "surf_data": surf_data})
        print("Response from Ollama:", answer)  # Debugging line
        return jsonify({'answer': answer})
    except Exception as e:
        logging.error("Error invoking chain: %s", str(e))
        return jsonify({"msg": "Error communicating with Ollama service", "error": str(e)}), 500
