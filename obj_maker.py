class obj_maker:

    def __init__(self, package_name, class_name , class_description):
        self.package_name = package_name
        self.class_name = class_name
        self.class_description = class_description
        self.all_methods = []
        self.methods_description_in_raw_text=[]
        self.methods_description_split_into_words = []
        self.methods_descriptions_stemmed = []
        self.methods_matrix = []
        self.methods_idf_vector = []
        self.class_description_matrix = None
        self.class_description_idf_vector = None

    def print_info(self):
        print(self.package_name + self.class_name + self.class_description)        