# This file includes the important functions that
# construct the graph including linking nodes to create a new edge
# and finding clusters.

import networkx as nx
import utils
from sklearn.cluster import AgglomerativeClustering
import process_strings as pcstr

def match_same_class(graph, db, class_name, var_name_out, var_name_in, rule_func):

    ontology_name_in = class_name + '.' + var_name_in
    ontology_name_out = class_name + '.' + var_name_out
    all_nodes = list(graph.copy().nodes)
    
    # Here is an exhuastive search for the nodes with the correct ontology name,
    # which is very slow.

    for i in all_nodes:
        node_temp = graph.nodes[i]
        ontology_temp = node_temp['ontology_name']
        if ontology_temp == ontology_name_in:
            node_name_in = i
            id_same_class = node_temp['ID']
            node_name_out = class_name + '[' + str(id_same_class) + '].' + var_name_out
            indicator = rule_func(graph, db, node_name_out, id_same_class, db, node_name_in, id_same_class)
            if indicator == True:
                # when I add the nodes, I will add attributes
                idx_temp = db['ID'] == id_same_class
                value_temp = db.loc[idx_temp, var_name_out].values[0]
                graph.add_node(node_name_out, ID=id_same_class, class_name=class_name, var_name=var_name_out, value = value_temp, ontology_name = ontology_name_out)
                graph.add_edge(node_name_out, i)


    return graph

def match_two_classes(graph, db_out, class_name_out, var_name_out, db_in, class_name_in, var_name_in, rule_func):

    ontology_name_in = class_name_in + '.' + var_name_in
    ontology_name_out = class_name_out + '.' + var_name_out
    all_nodes = list(graph.copy().nodes)

    for i in all_nodes:
        node_temp = graph.nodes[i]
        id_in = node_temp['ID']
        ontology_temp = node_temp['ontology_name']
        if ontology_temp == ontology_name_in:
            node_name_in = i
            for j in range(len(db_out)):
                id_out = db_out.loc[j, 'ID']
                node_name_out = class_name_out + '[' + str(id_out) + '].' + var_name_out
                indicator = rule_func(graph, db_out, node_name_out, id_out, db_in, node_name_in, id_in)
                if indicator == True:
                    idx_temp = db_out['ID'] == id_out
                    value_temp = db_out.loc[idx_temp, var_name_out].values[0]
                    graph.add_node(node_name_out, ID=id_out, class_name=class_name_out, var_name=var_name_out, value = value_temp, ontology_name = ontology_name_out)
                    graph.add_edge(node_name_out, node_name_in)

    return graph

def match_two_classes_rank(graph, db_out, class_name_out, var_name_out, db_in, class_name_in, var_name_in, rule_func, num_top_candidates=3):

    ontology_name_in = class_name_in + '.' + var_name_in
    ontology_name_out = class_name_out + '.' + var_name_out
    all_nodes = list(graph.copy().nodes)

    for i in all_nodes:
        node_temp = graph.nodes[i]
        id_in = node_temp['ID']
        ontology_temp = node_temp['ontology_name']
        if ontology_temp == ontology_name_in:
            node_name_in = i
            candidates_list = []  # List to store candidates
            for j in range(len(db_out)):
                id_out = db_out.loc[j, 'ID']
                node_name_out = class_name_out + '[' + str(id_out) + '].' + var_name_out
                score = rule_func(graph, db_out, node_name_out, id_out, db_in, node_name_in, id_in)
                utils.add_candidate(candidates_list, node_name_out, id_out, score, num_top_candidates)

            # Add candidates to the graph
            for _, candidate, candidate_id in candidates_list:
                idx_temp = db_out['ID'] == candidate_id
                value_temp = db_out.loc[idx_temp, var_name_out].values[0]
                graph.add_node(candidate, ID=id_out, class_name=class_name_out, var_name=var_name_out, value = value_temp, ontology_name = ontology_name_out)
                graph.add_edge(candidate, node_name_in)

                # if indicator == True:
                #     idx_temp = db_out['ID'] == id_out
                #     value_temp = db_out.loc[idx_temp, var_name_out].values[0]
                #     graph.add_node(node_name_out, ID=id_out, class_name=class_name_out, var_name=var_name_out, value = value_temp, ontology_name = ontology_name_out)
                #     graph.add_edge(node_name_out, node_name_in)
    
    return

def itself_node_candidates(graph, class_name, var_name):

    itself_node_candidates_list = []
    ontology_name = class_name + '.' + var_name
    all_nodes = list(graph.copy().nodes)

    for node_i in all_nodes:
        
        node_temp = graph.nodes[node_i]
        ontology_temp = node_temp['ontology_name']
        if ontology_temp == ontology_name:
            itself_node_candidates_list.append(node_i)

    return itself_node_candidates_list, ontology_name

def itself_clusters(graph, class_name, var_name, rule_func, db=None):

    node_candidates_list, ontology_name = itself_node_candidates(graph, class_name=class_name, var_name=var_name)
    all_nodes = list(graph.copy().nodes)

    ncl_numeric_values = rule_func(node_candidates_list, db) # ncl stands for node_candidates_list

    # We use Agglomerative Clustering
    # 
    linkage_method = 'single' # linkage criterion.
    distance_threshold = 2.0001
    clustering = AgglomerativeClustering(n_clusters=None,affinity='precomputed', distance_threshold=distance_threshold,linkage=linkage_method).fit(ncl_numeric_values)

    # # We use Agglomerative Clustering (the old code)
    # linkage_method = 'single' # linkage criterion.
    # distance_threshold = 2.0001
    # clustering = AgglomerativeClustering(n_clusters=None,distance_threshold=distance_threshold,linkage=linkage_method).fit(ncl_numeric_values)

    # print(clustering.labels_)
    node_clusters = [[] for x in range(clustering.n_clusters_)]
    for i in range(len(node_candidates_list)):
        node_temp = node_candidates_list[i]
        cluster_id = clustering.labels_[i]
        node_clusters[cluster_id].append(node_temp)
        
    num_nodes = len(node_candidates_list)
    list_ontology_name = [ontology_name] * num_nodes

    return node_clusters, list_ontology_name

def join_node_clusters(node_clusters_store, node_clusters_temp):

    for cluster_i in node_clusters_temp:
        node_clusters_store.append(cluster_i)

    return node_clusters_store


def check_number_of_elements_in_node_clusters(l1, l2):
    # Right now, we have (1) a nested list which stores node clusters
    # and (2) a list which stores the corresponding ontology names.
    # l1 is the nested list, l2 is the list (not nested).
    # So this function is to check whether the number of nodes in l1
    # equals to that in l2

    l_flatten = utils.flatten_list(l1)
    if len(l_flatten)==len(l2):
        return True
    else:
        print('node clusters are wrong')
        return False


def select_candidates_correlated_node_clusters(correlated_varialbes_name, node_clusters, l_ontology_name):
    # There are lots of node clusters. Within the node clusters,
    # some nodes may be correlated.
    # This function tries to find those correlated candidates
    # correlated_variables_name is the ontology names for correlated variables
    # node_clusters means node clusters (nested list), l_ontology_name is the list
    # with the corresponding ontology names.

    check_match_num_elements = check_number_of_elements_in_node_clusters(node_clusters, l_ontology_name)
    if check_match_num_elements == False:
        print('wrong node clusters or list of ontology names')
        return 
    
    node_clusters_correlate = []
    list_clusters_correlate_ontology_name = []
    i_start = 0
    for node_clusters_i in node_clusters:
        ontology_name_temp = l_ontology_name[i_start]
        i_end = i_start+len(node_clusters_i)
        if ontology_name_temp in correlated_varialbes_name:
            node_clusters_correlate.append(node_clusters_i)
            list_clusters_correlate_ontology_name.extend(l_ontology_name[i_start:i_end])
        i_start = i_end

    return node_clusters_correlate, list_clusters_correlate_ontology_name


def change_list_to_graph_for_node_clusters(G,l):
    for li in l:
        size_li = len(li)
        if size_li==1:
            G.add_node(li[0])
        else:
            G.add_node(li[0])
            for i in range(size_li-1):
                G.add_node(li[i+1])
                G.add_edge(li[i], li[i+1])
    
    return G


def correlate_clusters(node_clusters, rule_func, db=None):

    # We should provide a node clusters to this function
    # This is because we should first find node clusters for itself (i.e., random field)
    # then we will find node clusters for correlation.

    node_candidates_list = utils.flatten_list(node_clusters)
    ncl_numeric_values = rule_func(node_candidates_list, db) # ncl stands for node_candidates_list

    # We use Agglomerative Clustering
    linkage_method = 'single' # linkage criterion.
    distance_threshold = 2.001
    clustering = AgglomerativeClustering(n_clusters=None,distance_threshold=distance_threshold,linkage=linkage_method).fit(ncl_numeric_values)

    # print(clustering.labels_)
    node_clusters = [[] for x in range(clustering.n_clusters_)]
    for i in range(len(node_candidates_list)):
        node_temp = node_candidates_list[i]
        cluster_id = clustering.labels_[i]
        node_clusters[cluster_id].append(node_temp)

    return node_clusters


def join_clusters_correlate(l_clusters, l_correlate):
    # l_clusters is the list that contains node clusters (random field)
    # l_correlate is the list that contains node clusters (statistically correlated)
    # This function joins these two lists by linking clusters.
    # It is done through adding edges between clusters.
    G_cluster_correlate_temp = nx.Graph()
    G_cluster_correlate_temp = change_list_to_graph_for_node_clusters(G_cluster_correlate_temp, l_clusters)
    G_cluster_correlate_temp = change_list_to_graph_for_node_clusters(G_cluster_correlate_temp, l_correlate)

    S = [G_cluster_correlate_temp.subgraph(c).copy() for c in nx.connected_components(G_cluster_correlate_temp)]
    l_clusters_correlate = []
    for Si in S:
        l_clusters_correlate.append(list(Si.nodes))

    return l_clusters_correlate

