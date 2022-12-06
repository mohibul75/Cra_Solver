import re
import pickle


def query_preprocess(query, api_des, api_list):
    api_set = set()
    des_set = set()
    crash = query.content
    crash_names, patterns = crashname_extract(crash)
    query.caused = crash_names
    for name in crash_names:
        if name in api_list:
            des = api_des[name]
            des = " ".join(des)
            des_set.add(des)
            api_set.add(name)
    query.description = des_set
    query.crash_name = api_set
    query.crash_pattern = patterns
    # query.print_query()
    return query


def query_preprocess_hit(query, api_des, api_list):
    api_set = set()
    des_set = set()
    crash = query.content
    crash_names, patterns, reasons = crashname_extract_hit(crash)
    query.caused = crash_names
    query.reason = reasons
    for name in crash_names:
        if name in api_list:
            des = api_des[name]
            des = " ".join(des)
            des_set.add(des)
            api_set.add(name)
    query.description = des_set
    query.crash_name = api_set
    query.crash_pattern = patterns
    # query.print_query()
    return query


def caused_list(stack_trace):
    exc_list = []
    pattern = r"Caused by|caused by|Exception in |exception in "
    stack_list = re.split(pattern, stack_trace)
    for i in stack_list:
        if i == '':
            continue
        else:
            exc_list.append(i)
    return exc_list


def crashname_extract_hit(stack_trace):
    crashes = []
    patterns = []
    reasons = []
    stack_list = caused_list(stack_trace)
    for stack in stack_list:
        crash_names = []
        pattern_list = []
        exception_list = stack.split()
        for exception_line in exception_list:
            line = exception_line.strip()
            if ".java:" in line or "(Native" in line or "(Unknown" in line or ".Java:" in line or ".scala:" in line:
                tmp = line.replace('(', '.')
                if ".java:" in tmp or ".Java:" in tmp or ".scala:" in tmp:
                    tmp = tmp.split('.')[:-2]
                else:
                    tmp = tmp.split('.')[:-1]
                pattern_list.append(tmp)
            elif re.match('at', line) or re.match('Source', line) or re.match('Method', line):
                continue
            else:
                name_list = line.split('.')
                reasons.append(line)
                if len(name_list) >= 3:
                    name = name_list[-1].replace(':', '')
                    crash_names.append(name)
        crashes.extend(crash_names)
        patterns.append(pattern_list)

    crashes = [i for i in crashes if i != '']
    crashes = set(crashes)
    return crashes, patterns, reasons


def crashname_extract(stack_trace):
    crashes = []
    patterns = []
    stack_list = caused_list(stack_trace)
    for stack in stack_list:
        crash_names = []
        pattern_list = []
        exception_list = stack.split()
        for exception_line in exception_list:
            line = exception_line.strip()
            if ".java:" in line or "(Native" in line or "(Unknown" in line or ".Java:" in line or ".scala:" in line:
                tmp = line.replace('(', '.')
                if ".java:" in tmp or ".Java:" in tmp or ".scala:" in tmp:
                    tmp = tmp.split('.')[:-2]
                else:
                    tmp = tmp.split('.')[:-1]
                pattern_list.append(tmp)
            elif re.match('at', line) or re.match('Source', line) or re.match('Method', line):
                continue
            else:
                name_list = line.split('.')
                if len(name_list) >= 3:
                    name = name_list[-1].replace(':', '')
                    crash_names.append(name)
        crashes.extend(crash_names)
        patterns.append(pattern_list)

    crashes = [i for i in crashes if i != '']
    crashes = set(crashes)
    return crashes, patterns


def crash_preprocess(exc_qa, api_des, api_list):
    res = []
    for qa in exc_qa:
        name_set = set()
        crash = qa.exception
        crash_names, patterns = crashname_extract(crash)
        qa.caused = crash_names
        for i in crash_names:
            for name in i:
                if name in api_list:
                    name_set.add(name)
        qa.exc_name = name_set
        qa.exc_pattern = patterns
        res.append(qa)
    return res


def build_doc_dict(javadoc):
    api_des = dict()
    name_list = list()
    for api in javadoc:
        name_list.append(api.class_name)
        api_des[api.class_name] = api.class_description
    return api_des, name_list


if __name__ == '__main__':
    # proprocess these two file both
    exc_qa_file = "../data/exc_qa_hasAnswers"
    # exc_qa_file = "../data/exc_qa_hasAnswers_android"
    exc_qa = pickle.load(open(exc_qa_file, 'rb'))
    javadoc = pickle.load(open('../data/javadoc_pickle_wordsegmented', 'rb'))
    api_description, api_list = build_doc_dict(javadoc)
    print(len(exc_qa))
    res = crash_preprocess(exc_qa, api_description, api_list)
    pickle.dump(res, open(exc_qa_file, 'wb'))

    exc_qa_file = "../data/exc_qa_hasAnswers_android"
    exc_qa = pickle.load(open(exc_qa_file, 'rb'))
    res = crash_preprocess(exc_qa, api_description, api_list)
    pickle.dump(res, open(exc_qa_file, 'wb'))
