# coding=utf-8

import os
import pickle
from whoosh import index
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import scoring
from whoosh import qparser, query

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from ans_retrieval.stack_preprocess import build_doc_dict, query_preprocess, query_preprocess_hit
from ans_retrieval.utils import subtokens, load_input


def load_data(questions):
    data = dict()
    # questions = pickle.load(open(file, 'rb'))
    for ques in questions:
        data[ques.id] = ques.exception
    return data


def clean_line(line):
    stop_words = set(stopwords.words('english'))
    line = re.sub('\W+', ' ', line)
    word_tokens = word_tokenize(line)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    sent = ' '.join(filtered_sentence)
    return sent


def clean_data(data):
    stop_words = set(stopwords.words('english'))
    result = dict()
    for id in data:
        line = data[id]
        line = re.sub('\W+', ' ', line)
        word_tokens = word_tokenize(line)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        sent = ' '.join(filtered_sentence)
        result[id] = sent
    return result


def build_index(dir, qa_file):
    schema = Schema(id=NUMERIC(stored=True), content=TEXT(stored=True))
    indexdir = dir
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
        ix = index.create_in(indexdir, schema)
    else:
        ix = index.open_dir(indexdir)
        return ix

    writer = ix.writer()
    td = load_data(qa_file)
    corpus = clean_data(td)

    for i in corpus:
        ques = corpus[i]
        writer.add_document(id=i, content=ques)

    writer.commit()
    return ix


def pos_score_fn(searcher, fieldname, text, matcher):
    poses = matcher.value_as("positions")
    return 1.0 / (poses[0] + 1)


def query_scoring(ix, exc, api_description, api_list):
    exc = query_preprocess_hit(exc, api_description, api_list)
    exc_text = clean_line(exc.content)
    exc_name = clean_line(" ".join(exc.reason))
    # if len(exc.crash_name) == 0:
    #     exc_name = clean_line(" ".join(exc.caused))
    # else:
    #     exc_name = clean_line(" ".join(exc.crash_name))
    ids = list()
    pos_weighting = scoring.FunctionWeighting(pos_score_fn)
    searcher = ix.searcher(weighting=scoring.BM25F)
    og = qparser.OrGroup.factory(0.9)
    # search by crash name first and the the whole context
    qu1 = QueryParser("content", ix.schema, group=og).parse(exc_name)
    results = searcher.search(qu1, limit=50)
    # qu2 = QueryParser("content", ix.schema, group=og).parse(exc_text)
    # results = searcher.search(qu2, filter=qu1, limit=1000)

    for i in range(50):
        _id = results[i]["id"]
        ids.append(_id)
    return ids


if __name__ == '__main__':
    javadoc = pickle.load(open('../data/javadoc_pickle_wordsegmented', 'rb'))
    api_description, api_list = build_doc_dict(javadoc)
    questions = pickle.load(open("../data/exc_qa_hasAnswers", 'rb'))
    questions_android = pickle.load(open('../data/exc_qa_hasAnswers_android', 'rb'))
    questions.extend(questions_android)
    # index_dir = "./indexdir/"
    # index_dir = "./ja_indexdir/"
    index_dir = "./android_indexdir/"
    ix = build_index(index_dir, questions_android)

    # exception_file = "./test_exception"
    # qu = load_input(exception_file)
    # print("First filter...")
    # ids = query_scoring(ix, qu, api_description, api_list)
    # print(ids)
