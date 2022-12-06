from ans_retrieval.stack_preprocess import build_doc_dict, query_preprocess
from ans_retrieval.exception_hit import build_index

def run_batch(in_dir, out_dir, type='java'):

    if type == 'java':
        questions = pickle.load(open("../data/exc_qa_hasAnswers", 'rb'))
        index_dir = "./indexdir/"

    idf = pickle.load(open('../data/ja_idf', 'rb'))
    javadoc = pickle.load(open('../data/javadoc_pickle_wordsegmented', 'rb'))
    api_description, api_list = build_doc_dict(javadoc)
    ix = build_index(index_dir, questions)


if __name__=='__main__':
    run_batch("../data/user_study/java_test/", '../data/user_study/RQ1/java/', 'java')