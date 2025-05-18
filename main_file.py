import pandas as pd
import utils
import rules as ur
import ontology as ontlg
import process_strings as pcstr
import graph_construction_functions as gcf
import networkx as nx
import pickle
import random

# I do not know how to automatically read all csv files,
# so I read them one by one here

# Load datasets
bridge = pd.read_csv('bridges_MiamiDade.csv')
river_gage = pd.read_csv('florida_gages.csv')
stcs = pd.read_csv('ptms_MiamiDade.csv')

# river_gage['COUNTY_COD'] = 86

# add extra columns to all the datasets

temp_bridge = pd.read_csv('bridges_MiamiDade.csv')
temp_river_gage = pd.read_csv('florida_gages.csv')
temp_stcs = pd.read_csv('ptms_MiamiDade.csv')


# rename the structure column on bridge dataset to ID
bridge.rename(columns={'STRUCTURE_': 'ID'}, inplace=True)

extra_columns_bridges = set(temp_bridge.columns) - set(bridge.columns)
extra_columns_river_gage = set(temp_river_gage.columns) - set(river_gage.columns)
extra_columns_stcs = set(temp_stcs.columns) - set(stcs.columns)


# Function to fill new columns with random string values from MiamiDade datasets
def fill_with_random_values_from_miamidade(main_df, miamidade_df, extra_columns):
    for column in extra_columns:

        non_null_values = miamidade_df[column].dropna().values
        if len(non_null_values) > 0:
            main_df[column] = [random.choice(non_null_values) for _ in main_df.index]
        else:
            main_df[column] = None # If the MiamiDade column has only null values, fill the new column with null values

# Add extra columns and fill with random values
fill_with_random_values_from_miamidade(bridge, temp_bridge, extra_columns_bridges)
fill_with_random_values_from_miamidade(river_gage, temp_river_gage, extra_columns_river_gage)
fill_with_random_values_from_miamidade(stcs, temp_stcs, extra_columns_stcs)



if 'COUNTY_COD ' in bridge.columns:
    print("The bridge dataset has a column named 'COUNTY_COD'.")
else:
    print("The bridge dataset does not have a column named 'COUNTY_COD'.")

# Get unique county codes from the bridge dataset to iterate over
# county_codes = bridge['COUNTY_COD '].unique()

# river_gage['COUNTY_COD'] = [random.choice(county_codes) for _ in range(len(river_gage))]

dataframes = {
    'bridge': bridge,
    'river_gage': river_gage,
    'stcs': stcs
}

# Initialize a directed graph
# gracs = nx.DiGraph()
gracs = utils.GraCS()

# ######### start: add leaf nodes #########
# Selection criterion provided by the user
idx_temp = bridge['COUNTY_CODE_003'] == 86

ontology_name_leaf_node = 'bridge.risk'
class_name = 'bridge'
var_name = 'risk'

# Based on the selection criterion, we get the leaf nodes
# and we add the leaf nodes to the graph
bridge_id = bridge.loc[idx_temp,'ID'].values
for i in bridge_id:
    node_name_temp = 'bridge[' + str(i) + '].' + var_name
    # when I add the nodes, I will add attributes
    idx_temp = bridge['ID'] == i
    value_temp = bridge.loc[idx_temp, var_name].values[0]
    gracs.add_node(node_name_temp, ID=i, class_name='bridge', var_name='risk', value = value_temp, ontology_name = ontology_name_leaf_node)

num_rules_leaf_nodes = 0
num_rules_leaf_nodes += 1
# ######### end: add leaf nodes #########


# # ##### Read the existing gracs file #####
# # The existing gracs file saves the graph of previous teps.
# # The graph is saved as a pickle file.
# # The graph has read bridge-related nodes, river_gage-related nodes, and stcs-related nodes.
# # gracs = nx.read_gpickle("graph_try01.pkl")
# gracs = nx.read_gpickle("graph_with_clusters.pkl")

# with open('graph_try_pickle.pkl', 'wb') as f:
#     pickle.dump(gracs, f)

# # Load the graph using pickle
# with open('graph_try_pickle.pkl', 'rb') as f:
#     loaded_graph = pickle.load(f)


# We read the ontology.
# Each edge of the ontology has two nodes.
# I use the a function to separate the class name and variable names.
# If two nodes have the same class name, I will call function match_same_class
# If two nodes have different class names, I will call function match_two_classes
# If two nodes have different class names and the edge type is two, I will call function match_two_classes_rank
# I will use a dictionary to map the condition to the function.

# Create a dictionary to map conditions to match functions
match_functions = {
    'same_class': gcf.match_same_class,
    'two_classes': gcf.match_two_classes,
    'two_classes_rank': gcf.match_two_classes_rank,
}

# Read the e_bunch of the ontology and then automatically call the corresponding function to link the nodes
for key, ontlg_value in ontlg.e_bunch.items():
    idx = int(key)
    e_ontlg = ontlg_value[0]
    rule_type_indicator = ontlg_value[1]
    num_top_edges = ontlg_value[2]
    class_name_out, var_name_out = pcstr.extract_class_and_var_names_from_ontoloty(e_ontlg[0])
    class_name_in, var_name_in = pcstr.extract_class_and_var_names_from_ontoloty(e_ontlg[1])
    # The name of the rule function as a string
    rule_name = f'rule{(idx):02d}' + '_edge'
    # Use the dictionary to get the function by name and call it
    rule_function = ur.rule_functions.get(rule_name)

    # Get the condition and call the corresponding function
    if class_name_in == class_name_out and rule_type_indicator == 0:
        condition = 'same_class'


        print('class_name_in:', class_name_in)
        print('var_name_in:', var_name_in)
        print('class_name_out:', class_name_out)
        print('var_name_out:', var_name_out)
        print()
        # Get the appropriate match function based on the condition
        match_function = match_functions.get(condition)
        # Call the match function
        if match_function is not None:
            match_function(
                gracs, 
                db=dataframes.get(class_name_in), 
                class_name=class_name_in, 
                var_name_out=var_name_out, 
                var_name_in=var_name_in, 
                rule_func=rule_function
            )
    elif class_name_in != class_name_out and rule_type_indicator == 0:
        condition = 'two_classes'

        print('class_name_in:', class_name_in)
        print('var_name_in:', var_name_in)
        print('class_name_out:', class_name_out)
        
        print('var_name_out:', var_name_out)
        print()
        # Get the appropriate match function based on the condition
        match_function = match_functions.get(condition)
        # Call the match function
        if match_function is not None:
            match_function(
                gracs, 
                db_out=dataframes.get(class_name_out), 
                class_name_out=class_name_out, 
                var_name_out=var_name_out, 
                db_in=dataframes.get(class_name_in), 
                class_name_in=class_name_in, 
                var_name_in=var_name_in, 
                rule_func=rule_function
            )
    elif class_name_in != class_name_out and rule_type_indicator == 1:
        condition = 'two_classes_rank'

        print('class_name_in:', class_name_in)
        print('var_name_in:', var_name_in)
        print('class_name_out:', class_name_out)
        print('var_name_out:', var_name_out)
        print()
        # Get the appropriate match function based on the condition
        match_function = match_functions.get(condition)
        # Call the match function
        if match_function is not None:
            match_function(
                gracs, 
                db_out=dataframes.get(class_name_out), 
                class_name_out=class_name_out, 
                var_name_out=var_name_out, 
                db_in=dataframes.get(class_name_in), 
                class_name_in=class_name_in, 
                var_name_in=var_name_in, 
                rule_func=rule_function,
                num_top_candidates=num_top_edges
            )



# All the variables that can be a random field will be clustered
node_clusters_graph_rf  = [] # This is a nested list. Each sublist is a cluster
# Each variable in the cluster correspons to an ontology name, which stores in the list
list_clusters_ontology_name = [] # This is a flatten list 

# First process the variables that can be modelled by a random field
for idx in range(len(ontlg.var_random_field)):
    var_rf = ontlg.var_random_field[idx] # rf is short for random field
    class_name, var_name = pcstr.extract_class_and_var_names_from_ontoloty(var_rf)
    database_itself = dataframes.get(class_name)

    # The name of the rule function as a string
    rule_name = f'rule{(idx+1):02d}' + '_rf'
    # Use the dictionary to get the function by name and call it
    rule_function = ur.rule_functions.get(rule_name)

    node_clusters_current, list_clusters_ontology_name_current = gcf.itself_clusters(gracs, class_name, var_name, rule_function, database_itself)
    node_clusters_graph_rf = gcf.join_node_clusters(node_clusters_graph_rf, node_clusters_current)
    list_clusters_ontology_name.extend(list_clusters_ontology_name_current)

# Then we link those nodes that may be correlated.
for idx in range(len(ontlg.var_correlated)):
    # The name of the rule function as a string
    rule_name = f'rule{(idx+1):02d}' + '_correlate'
    # Use the dictionary to get the function by name and call it
    rule_function = ur.rule_functions.get(rule_name)
    # get the correlated variables, which is a sublist. 
    # Each sublist contains the ontology names of the variables that can be correlated.
    correlated_variables_ontology_name = ontlg.var_correlated[idx] 
    node_correlate_graph_rf, list_correlate_ontology_name = gcf.select_candidates_correlated_node_clusters(correlated_variables_ontology_name, node_clusters_graph_rf, list_clusters_ontology_name)
    node_correlate_graph_rf = gcf.correlate_clusters(node_correlate_graph_rf, rule_function)

# Join the clusters for random field and correlated variables
clusters_list = gcf.join_clusters_correlate(node_clusters_graph_rf, node_correlate_graph_rf)

# Add the cluster list to the graph
gracs.add_cluster(clusters_list)
# Create a temporary node that represents correlations.
gracs.temporary_BN_considering_correlations()

# # Save the graph to a pickle file
# nx.write_gpickle(gracs, "graph.pkl")\
with open('graph_with_clusters.pkl', 'wb') as f:
    pickle.dump(gracs, f)


# # Read the graph back from the pickle file
# loaded_gracs = nx.read_gpickle("graph.pkl")

# # Save the edge list to a text file
# nx.write_edgelist(gracs, "edge_list.txt")

# # Read the edge list back (optional)
# loaded_gracs = nx.read_edgelist("edge_list.txt")

print('end')
