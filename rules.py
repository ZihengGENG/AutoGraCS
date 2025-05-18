# this is the file to define rules
# for now, its just one file with all the rules 
# later we will split it into multiple files for general and specific rules


# import packages
import numpy as np
import graph_construction_functions as gr
import process_strings as pcstr
import river_gage_matches_bridges as utils_rgmb
from utils import distance

# define rules

# rule 1: same class

# # Rule 01
# num_rules_edges += 1
# gracs = gr.match_same_class(gracs, bridge, 'bridge', 'failure_probability', 'risk', ur.rule01_edge)

# # Rule 02
# num_rules_edges += 1
# gracs = gr.match_same_class(gracs, bridge, 'bridge', 'failure_loss', 'risk', ur.rule02_edge)

# # Rule 03
# num_rules_edges += 1
# gracs = gr.match_same_class(gracs, bridge, 'bridge', 'pier_rating', 'failure_probability', ur.rule03_edge)

# # Rule 04
# num_rules_edges += 1
# gracs = gr.match_same_class(gracs, bridge, 'bridge', 'struct_rating', 'failure_probability', ur.rule04_edge)




def rule01_edge(graph, db_in, node_name_in, id_in, db_out, node_name_out, id_out):

    if db_in.equals(db_out) == True and id_in==id_out:
        return True
    else:
        return False



def rule02_edge(graph, db_in, node_name_in, id_in, db_out, node_name_out, id_out):

    if db_in.equals(db_out) == True and id_in==id_out:
        return True
    else:
        return False


def rule03_edge(graph, db_in, node_name_in, id_in, db_out, node_name_out, id_out):

    if db_in.equals(db_out) == True and id_in==id_out:
        return True
    else:
        return False



def rule04_edge(graph, db_in, node_name_in, id_in, db_out, node_name_out, id_out):

    if db_in.equals(db_out) == True and id_in==id_out:
        return True
    else:
        return False




def rule05_edge(graph, db_out, node_name_out, id_out, db_in, node_name_in, id_in):

    # separate the class name and the variable name
    class_name_out, var_name_out = pcstr.extract_class_and_var_names_from_ontoloty(node_name_out)
    class_name_in, var_name_in = pcstr.extract_class_and_var_names_from_ontoloty(node_name_in)

    # Define your rules here
    # 1) should be on the same river
    # 2) distance should be smaller or equal to 1.

    value_out_lon = db_out.loc[db_out['ID'] == id_out, 'Longitude'].values[0]
    value_out_lat = db_out.loc[db_out['ID'] == id_out, 'Latitude'].values[0]
    value_in_lon = db_in.loc[db_in['ID'] == id_in, 'LONG_017_DD'].values[0]
    value_in_lat = db_in.loc[db_in['ID'] == id_in, 'LAT_016_DD'].values[0]

    dist = distance(
        lat1=value_out_lat,
        lon1=value_out_lon,
        lat2=value_in_lat,
        lon2=value_in_lon
        )

    dist_threshold = 5
    if dist<dist_threshold:
        value_out = db_out.loc[db_out['ID'] == id_out, 'STANAME'].values[0]
        value_in = db_in.loc[db_in['ID'] == id_in, 'FEATURES_DESC_006A'].values[0]
        value_out = utils_rgmb.extract_river_name(value_out)
        value_in = utils_rgmb.extract_river_name(value_in)
        value_out_tokens = value_out.split()
        value_in_tokens = value_in.split()

        indicator1 = utils_rgmb.is_valid_match(value_out_tokens, value_in_tokens)
        if indicator1==True:
            return True
    
    return False


def rule06_edge(graph, db_out, node_name_out, id_out, db_in, node_name_in, id_in):

    # separate the class name and the variable name
    class_name_out, var_name_out = pcstr.extract_class_and_var_names_from_ontoloty(node_name_out)
    class_name_in, var_name_in = pcstr.extract_class_and_var_names_from_ontoloty(node_name_in)

    # Define your rules here
    # 1) should be on the same river
    # 2) distance should be smaller or equal to 1.

    value_out_lon = db_out.loc[db_out['ID'] == id_out, 'Longitude'].values[0]
    value_out_lat = db_out.loc[db_out['ID'] == id_out, 'Latitude'].values[0]
    value_in_lon = db_in.loc[db_in['ID'] == id_in, 'LONG_017_DD'].values[0]
    value_in_lat = db_in.loc[db_in['ID'] == id_in, 'LAT_016_DD'].values[0]

    dist = distance(
        lat1=value_out_lat,
        lon1=value_out_lon,
        lat2=value_in_lat,
        lon2=value_in_lon
        )

    dist_threshold = 5
    if dist<dist_threshold:
        value_out = db_out.loc[db_out['ID'] == id_out, 'STANAME'].values[0]
        value_in = db_in.loc[db_in['ID'] == id_in, 'FEATURES_DESC_006A'].values[0]
        value_out = utils_rgmb.extract_river_name(value_out)
        value_in = utils_rgmb.extract_river_name(value_in)
        value_out_tokens = value_out.split()
        value_in_tokens = value_in.split()

        indicator1 = utils_rgmb.is_valid_match(value_out_tokens, value_in_tokens)
        if indicator1==True:
            return True
    
    return False


def rule07_edge(graph, db_out, node_name_out, id_out, db_in, node_name_in, id_in):

    # separate the class name and the variable name
    class_name_out, var_name_out = pcstr.extract_class_and_var_names_from_ontoloty(node_name_out)
    class_name_in, var_name_in = pcstr.extract_class_and_var_names_from_ontoloty(node_name_in)

    # # get the row
    # idx_out_temp = db_out['ID'] == id_out
    # idx_in_temp = db_in['ID'] == id_in

    # Define your rules here
    # 1) calculate the distance and return -distance

    value_out_lon = db_out.loc[db_out['ID'] == id_out, 'EPSG4326x'].values[0]
    value_out_lat = db_out.loc[db_out['ID'] == id_out, 'EPSG4326y'].values[0]
    value_in_lon = db_in.loc[db_in['ID'] == id_in, 'LONG_017_DD'].values[0]
    value_in_lat = db_in.loc[db_in['ID'] == id_in, 'LAT_016_DD'].values[0]

    dist = distance(
        lat1=value_out_lat,
        lon1=value_out_lon,
        lat2=value_in_lat,
        lon2=value_in_lon
        )
    
    return -dist

    # value_out = db_out.loc[idx_out_temp, 'Route'].values[0]
    # value_in = db_in.loc[idx_in_temp, 'Route'].values[0]
    # x1 = value_out == value_in
    # if x1 == False:
    #     return False
    # else:
    #     value_out = db_out.loc[idx_out_temp, 'Y_axis'].values[0]
    #     value_in = db_in.loc[idx_in_temp, 'Y_axis'].values[0]
    #     x = np.abs(value_out - value_in)
    #     if x <= 1:
    #         return True
    #     else:
    #         return False



# # The name of the rule function as a string
# rule_name = 'rule01_edge'

# # Use the dictionary to get the function by name and call it
# rule_function = rule_functions.get(rule_name)

# if rule_function is not None and callable(rule_function):
#     rule_function()
# else:
#     print(f"Function {rule_name} not found.")

def rule01_rf(l, db):
    num_nodes_l = len(l)

    # Get the id value of list l
    object_id_l = []
    for li in l:
        numeric_temp = pcstr.extract_numerical_value(li)
        object_id_l.append(numeric_temp)

    # ## Access and obtain all required information from db
    num_values = 2 # This is a user input
    value_name_list = ['Longitude', 'Latitude']

    # Obtain the information for list l
    values_store_l = np.zeros((num_values,num_nodes_l)).tolist()
    for i in range(num_nodes_l):
        j = 0
        idx_temp = db['ID'] == object_id_l[i]
        for value_name in value_name_list:
            value_temp = db.loc[idx_temp, value_name].values[0]
            values_store_l[j][i] = value_temp
            j += 1

    # Initialize the numpy array. The array will be used for clustering (sklearn)
    values_store_l = np.array(values_store_l)
    values_store_l = values_store_l.T

    # Calculate the custom affinity matrix using your distance function
    affinity_matrix = np.zeros((values_store_l.shape[0], values_store_l.shape[0]))

    for i in range(values_store_l.shape[0]):
        for j in range(i + 1, values_store_l.shape[0]):
            affinity_matrix[i, j] = distance(values_store_l[i, 0], values_store_l[i, 1], values_store_l[j, 0], values_store_l[j, 1])
            affinity_matrix[j, i] = affinity_matrix[i, j]

    return affinity_matrix

    # numeric_values_store = np.zeros((num_values,num_nodes_l))

    # continuous_value_idx = [1] # The indice of the variables that are continuous
    # for continuous_idx in continuous_value_idx:
    #     values_list_temp = values_store_l[continuous_idx].copy()
    #     values_list_temp = np.array(values_list_temp)
    #     numeric_values_store[continuous_idx,:] = values_list_temp


    # # Give a numeric values to categorical variables
    # multiply_cat = [1000] # give a large numeric value. Different numeric values for different categorical variables
    # categorical_value_idx = [0] # The indice of the variables that are categorical
    # # Note: multiply_cat and categorical_value_idx should have the same dimension
    # multiply_cat_i = 0
    # for categorical_idx in categorical_value_idx:
    #     values_list_temp = values_store_l[categorical_idx].copy()
    #     values_list_temp = np.array(values_list_temp)
    #     numeric_values_list_temp = np.zeros(num_nodes_l)
    #     # These categorical variables are in chaos,
    #     # therefore, we need to do some data cleaning first.
    #     # I think this should be done before running the research code.
    #     values_set = np.unique(values_list_temp) # Find duplicate values. In the future, this should be fuzzy match.
    #     values_set = np.array(values_set)
    #     j = 1
    #     for values_cat_i in values_set:
    #         idx_temp = np.nonzero(values_list_temp == values_cat_i)
    #         numeric_values_list_temp[idx_temp] = j * multiply_cat[multiply_cat_i]
    #         j += 1
    #     numeric_values_store[categorical_idx,:] = numeric_values_list_temp
    #     multiply_cat_i += 1       
    
    # return numeric_values_store.T # Transpose it so that match sklearn 

def rule01_correlate(l, db=None):
    # l is the list that comes from the node clusters that may be correlated.
    # db is the databases.

    num_nodes_l = len(l)

    # Get the id value of list l
    object_id_l = []
    for li in l:
        numeric_temp = pcstr.extract_numerical_value(li)
        object_id_l.append(numeric_temp)

    # ## Access and obtain all required information from db
    # For this example, we don't need to obtain values from the databases
    num_values = 0 # This is a user input
    value_name_list = []

    # Initialize the numpy array. The array will be used for clustering (sklearn)
    # Because of the default rule, I will do "+1" when initializing the list
    numeric_values_store = np.zeros((num_values+1,num_nodes_l)) # +1 to consider object id, which is the default rule

    # Default rule !!!!!
    # The correlated values should be within the same object,
    # which means object id should be the same.
    # To differentiate objects, we assign different values to different objects
    multiply_object_id = 1000
    values_list_temp = multiply_object_id * np.array(object_id_l)
    numeric_values_store[-1,:] = values_list_temp

    return numeric_values_store.T # Transpose it so that match sklearn


# Create a dictionary to map rule names to functions
rule_functions = {
    'rule01_edge': rule01_edge,
    'rule02_edge': rule02_edge,
    'rule03_edge': rule03_edge,
    'rule04_edge': rule04_edge,
    'rule05_edge': rule05_edge,
    'rule06_edge': rule06_edge,
    'rule07_edge': rule07_edge,
    'rule01_rf': rule01_rf,
    'rule02_rf': rule01_rf, # rule02_rf is the same as rule01_rf
    'rule01_correlate': rule01_correlate
}