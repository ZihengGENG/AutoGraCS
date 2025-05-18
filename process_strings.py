def extract_numerical_value(input_string):

    start_index = input_string.find('[') + 1 # find value after ‘[‘
    end_index = input_string.find(']') # find value before ‘]‘
    numerical_value = input_string[start_index:end_index]

    return int(numerical_value) # return as int (if you want as string, simply remove int)

# # Example usage:
# input_string = "river_gage[2].water_depth"
# result = extract_numerical_value(input_string)

def extract_ontology_name(input_string):
    start_index = input_string.find('[')
    class_name = input_string[:start_index]
    end_index = input_string.find(']')
    var_name = input_string[end_index+2:]
    ontology_name = class_name + '.' + var_name

    return ontology_name

def extract_class_and_var_names(input_string):
    start_index = input_string.find('[')
    class_name = input_string[:start_index]
    end_index = input_string.find(']')
    var_name = input_string[end_index+2:]

    return class_name, var_name  

# # Example usage:
# input_string = "river_gage[2].water_depth"
# result = extract_ontology_name(input_string)
# haha1, haha2 = extract_class_and_var_names(input_string)

def extract_class_and_var_names_from_ontoloty(input_string):
    start_index = input_string.find('.')
    class_name = input_string[:start_index]
    var_name = input_string[start_index+1:]

    return class_name, var_name

if __name__ == "__main__":

    # input_string = "river_gage[2].water_depth"
    # result = extract_ontology_name(input_string)
    # haha1, haha2 = extract_class_and_var_names(input_string)

    # input_string_ontology = "river_gage.water_depth"
    # haha1, haha2 = extract_class_and_var_names_from_ontoloty(input_string_ontology)

    print("Testing functions in utils.py")

