from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


model = OllamaLLM(model="llama3.1")

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json

    totalOwners = data.get('totalOwners')
    print(totalOwners)
    source_language = data.get('source_language')
    print(source_language)
    target_language = data.get('target_language')
    print(target_language)
    texts_to_translate = data.get('formDataArray')
    print(texts_to_translate)

    if not all([totalOwners, source_language, target_language, texts_to_translate]):
        return jsonify({'error': 'Missing required parameter'}), 400
    
    template = """
        Translate the text below from {Source} to {Target}. I only want the translation

        Text: {Text}

        Translation:
      """
    #print(template)
    t = template.replace('{Source}', source_language).replace('{Target}', target_language)
    #print(t)

    model = OllamaLLM(model="llama3.1") 
    prompt = ChatPromptTemplate.from_template(t) 
    chain = prompt | model

    try:
        translated_texts = []
        for i in range(totalOwners):
          text = texts_to_translate[i]['text']
          print('history:', text)
          if text != '':
            result = chain.invoke({"Text": text})
          else: result = ''
          translated_texts.append(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'translations': translated_texts}), 200


@app.route('/translate/defects', methods=['POST'])
def translate_defects():
    data = request.json

    totalOwners = data.get('totalOwners')
    print(totalOwners)
    source_language = data.get('source_language')
    print(source_language)
    target_language = data.get('target_language')
    print(target_language)
    defects_to_translate = data.get('formDataArrayD')
    print(defects_to_translate)
    #print(defects_to_translate[0].get('numD'))
    #print(defects_to_translate[1].get('formDataD')[1])

    if not all([totalOwners, source_language, target_language, defects_to_translate]):
        return jsonify({'error': 'Missing required parameter'}), 400
    
    template = """
        Translate the text below from {Source} to {Target}. I only want the translation

        Text: {Text}

        Translation:
      """
    #print(template)
    t = template.replace('{Source}', source_language).replace('{Target}', target_language)
    #print(t)

    model = OllamaLLM(model="llama3.1") 
    prompt = ChatPromptTemplate.from_template(t) 
    chain = prompt | model

    try:
        translated_defects = []
        for i in range(totalOwners):
          defects_owner = []
          for j in range(defects_to_translate[i].get('numD')):
            text = defects_to_translate[i].get('formDataD')[j]['text']
            print('defect:', text)
            if text != '':
                result = chain.invoke({"Text": text})
            else: result = ''
            defects_owner.append(result)
          translated_defects.append(defects_owner)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'translations': translated_defects}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

    