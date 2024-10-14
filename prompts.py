import sys
from yachalk import chalk
sys.path.append("..")

import json
import ollama.client as client


def extractConcepts(prompt: str, metadata={}, model="mistral-openorca:latest"):
    SYS_PROMPT = (
    "Your task is to extract differential diagnoses from each chunk, and for each differential diagnosis you need to extract   suggested by, confirmed by, and finalized by the predictable outcome of management. "
    
    "For every disease you need to find different differential diagnoses, and for each diagnosis, you need to find three things: suggested by, confirmed by, and finalized by the predictable outcome of management. "
    
    "Your task is to extract the key concepts (and non-personal entities) mentioned in the given context. "
    "Extract only the most important and atomistic concepts. If needed, break the concepts down to the simpler concepts. "
    "Categorize the concepts in one of the following categories: "
    
    "[differential diagnoses, confirmed by, suggested by, Finalized by the predictable outcome of management]\n"
    
    "Format your output as a list of JSON with the following format:\n"
    
    "[\n"
    '  {\n'
    '      "disease": "The disease",\n'
    '      "diagnoses": {\n'
    '          "diagnose 1": {\n'
    '              "Suggested by": "Suggested by field which you extracted",\n'
    '              "Confirmed by": "Confirmed by field which you extracted",\n'
    '              "Initial Management": "Finalized by the predictable outcome of management which you extracted"\n'
    '          },\n'
    '          "diagnose 2": {\n'
    '              "Suggested by": "Suggested by field which you extracted",\n'
    '              "Confirmed by": "Confirmed by field which you extracted",\n'
    '              "Initial Management": "Finalized by the predictable outcome of management which you extracted"\n'
    '          },\n'
    '          "diagnose 3": {\n'
    '              "Suggested by": "Suggested by field which you extracted",\n'
    '              "Confirmed by": "Confirmed by field which you extracted",\n'
    '              "Initial Management": "Finalized by the predictable outcome of management which you extracted"\n'
    '          }\n'
    '     }\n'
    '  }\n'
    ']\n'
)

    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result


def graphPrompt(input: str, metadata={}, model="mistral-openorca:latest"):
    if model == None:
        model = "mistral-openorca:latest"

    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

    SYS_PROMPT = (
        "You are a network graph maker who extracts terms and their relations from a given context. "
        "You are provided with a context chunk (delimited by ```) Your task is to extract the ontology "
        "of terms mentioned in the given context. These terms should represent the key concepts as per the context. \n"
        "Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.\n"
            "\tTerms may include object, entity, organization, disease, symptoms, suggested, confirmed, patient, treatment, cause, classification, clinical symptoms, viruses, bacteria,  \n"
            "\tcondition, acronym, documents, service, concept, etc.\n"
            "\tTerms should be as atomistic as possible\n\n"
        "Thought 2: Think about how these terms can have one on one relation with other terms.\n"
            "\tTerms that are mentioned in the same sentence or the same paragraph are typically related to each other.\n"
            "\tTerms can be related to many other terms\n\n"
        "Thought 3: Find out the relation between each such related pair of terms. \n\n"
         "Format your output as a list of JSON with the following format:\n"
         "[\n"
    '  {\n'
    '      "disease": "The disease",\n'
    '      "diagnoses": {\n'
    '          "diagnose 1": {\n'
    '              "Suggested by": "Suggested by field which you extracted",\n'
    '              "Confirmed by": "Confirmed by field which you extracted",\n'
    '              "Initial Management": "Finalized by the predictable outcome of management which you extracted"\n'
    '          },\n'
    '          "diagnose 2": {\n'
    '              "Suggested by": "Suggested by field which you extracted",\n'
    '              "Confirmed by": "Confirmed by field which you extracted",\n'
    '              "Initial Management": "Finalized by the predictable outcome of management which you extracted"\n'
    '          },\n'
    '          "diagnose 3": {\n'
    '              "Suggested by": "Suggested by field which you extracted",\n'
    '              "Confirmed by": "Confirmed by field which you extracted",\n'
    '              "Initial Management": "Finalized by the predictable outcome of management which you extracted"\n'
    '          }\n'
    '     }\n'
    '  }\n'
    ']\n'
    )

    USER_PROMPT = f"context: ```{input}``` \n\n output: "
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)
    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None
    return result
