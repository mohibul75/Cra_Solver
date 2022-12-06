import requests #pip3 install requests
import  obj_maker 
import pickle

from nltk.stem import SnowballStemmer
from nltk.tokenize import WordPunctTokenizer #pip3 install nltk
from bs4 import BeautifulSoup #pip install beautifulsoup4


def readJavaDocumentationAndPreprocessing():

    destination_file= "./processed_data/doc_data_preprocessed"
    doc_path="./data/java_docs/api/"
    head_file_path="allclasses-noframe.html"
    
    soup = BeautifulSoup(open(doc_path+head_file_path), 'html.parser',from_encoding='utf-8') #pip install html5lib

    with open("Scrapping_output.txt", 'w') as f: 
                f.write(soup.prettify())


    all_java_classes=soup.find_all("li")
    #print(soup.prettify())

    array_of_classes = []
    for x in all_java_classes:
        array_of_classes.append(str(x))

    content = str(all_java_classes)

    with open("Scrapping_output_with_class_name.txt", 'w') as f: 
                f.write(content)


    all_api=[]

    for _class in all_java_classes :
        class_link = _class.a['href']
        class_name=_class.get_text()
        package_name=_class.a['title'].split(' ')[-1]

        class_soup= BeautifulSoup(open(doc_path+class_link,'r', errors='ignore'),"html.parser", from_encoding='utf-8'  )

        class_block= class_soup.find('div' , class_='block')

        if class_block is None:
            continue 

        tonkenizer=WordPunctTokenizer()

        class_description=tonkenizer.tokenize(class_block.get_text().lower())

        class_object = obj_maker.obj_maker(package_name,class_name,class_description )

        methods_block_heading =class_block.find('h3', string='Method Detail')

        if methods_block_heading is not None:
            
            methods_block=class_block.find('h3', string='Method Detail').parent

            for method in methods_block.find_all('h4') :

                _block= method.parent.find('div',class_='block')

                if _block is  None:
                    continue
                
                class_object.method.append(method.get_text())
                class_object.methods_description_in_raw_text.append(_block.get_text())
                class_object.methods_description_split_into_words.append(tokenizer.tokenize(_block.get_text()).lower())
                class_object.methods_descriptions_stemmed.append(
                    [SnowballStemmer('english').stem(word) for word in method_description]
                )
        all_api.append(class_object)

    pickle.dump(all_api,open(destination_file,"wb"))


if __name__ == "__main__":

    readJavaDocumentationAndPreprocessing()

    javaDocs=pickle.load(open("./processed_data/doc_data_preprocessed","rb"))
    count=0

    for con in javaDocs:
        if "xception" in con.class_name:
            print(con.class_name)
            print(con.class_description)
            count += 1
        else:
            continue
    print(count)
    

