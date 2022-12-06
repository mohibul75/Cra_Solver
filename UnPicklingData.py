import pickle
import json

def retrieve_api_name(java_doc):
    name=list()
    api=dict()

    for element in java_doc:
        name.append(element.class_name)
        api[element.class_name]=element.class_description

    with open("myfile.txt", 'w') as f: 
            f.write(json.dumps(api))

if __name__=='__main__':

    qa=pickle.load(open('exc_qa_hasAnswers', 'rb'))

    java_doc=pickle.load(open('javadoc_pickle_wordsegmented',"rb"))

    retrieve_api_name(java_doc)