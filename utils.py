import networkx as nx
import numpy as np
import math
import heapq

def algorithm_u(ns, m):
    def visit(n, a):
        ps = [[] for i in range(m)]
        for j in range(n):
            ps[a[j + 1]].append(ns[j])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    n = len(ns)
    a = [0] * (n + 1)
    for j in range(1, m + 1):
        a[n - m + j] = j - 1
    return f(m, n, 0, n, a)


class GraCS(nx.DiGraph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clusters = []  # Initialize the clusters attribute as an empty list

    def extract_class_and_var_names(self, input_string):
        start_index = input_string.find('[')
        if start_index == -1:
            return 'temp', 'temp'
        else:
            class_name = input_string[:start_index]
            end_index = input_string.find(']')
            var_name = input_string[end_index+2:]

        return class_name, var_name

    def extract_ontology_name(self, input_string):
        start_index = input_string.find('[')
        if start_index == -1:
            return 'temp_node'
        else:
            class_name = input_string[:start_index]
            end_index = input_string.find(']')
            var_name = input_string[end_index+2:]
            ontology_name = class_name + '.' + var_name

        return ontology_name

    def add_node_info(self, node_name, ID_value=None, class_name_string='TBD',  var_name_string='TBD', value = None, ontology_name_string = 'TBD'):
        if ID_value==None:
            class_name_string, var_name_string = self.extract_class_and_var_names(node_name)
            ontology_name_string = self.extract_ontology_name(node_name)
            self.add_node(node_name, ID = ID_value, class_name=class_name_string, var_name=var_name_string, value = value, ontology_name = ontology_name_string)
        else:
            self.add_node(node_name, ID = ID_value, class_name=class_name_string, var_name=var_name_string, value = value, ontology_name = ontology_name_string)
 
    def add_cluster(self, l):
        for li in l:
            self.clusters.append(li)
            for node_i in li:
                if self.has_node(node_i)==False:
                    self.add_node_info(node_i)

    def add_parents_for_cluster(self, cluster_index, parent_nodes):
        if cluster_index < len(self.clusters):
            cluster = self.clusters[cluster_index]
            for parent_node in parent_nodes:
                for node_i in cluster:
                    if parent_node not in self.predecessors(node_i):
                        self.add_node_info(parent_node)
                        self.add_edge(parent_node, node_i)
    
    def add_children_for_cluster(self, cluster_index, child_nodes):
        if cluster_index < len(self.clusters):
            cluster = self.clusters[cluster_index]
            for child_node in child_nodes:
                for node_i in cluster:
                    if child_node not in self.successors(node_i):
                        self.add_node(child_node)
                        self.add_edge(node_i, child_node)
    
    def add_multiparents_for_cluster(self, cluster_index, parent_prefix):
        if cluster_index < len(self.clusters):
            cluster = self.clusters[cluster_index]
            for parent_node in [f'{parent_prefix}{cluster_index}_{i}' for i in range(1, len(cluster) + 1)]:
                self.add_parents_for_cluster(cluster_index, [parent_node])

    def add_multichildren_for_cluster(self, cluster_index, child_prefix):
        if cluster_index < len(self.clusters):
            cluster = self.clusters[cluster_index]
            for child_node in [f'{child_prefix}{cluster_index}_{i}' for i in range(1, len(cluster) + 1)]:
                self.add_children_for_cluster(cluster_index, [child_node])

    def add_individual_parents_for_cluster(self, cluster_index, parent_prefix):
        if cluster_index < len(self.clusters):
            cluster = self.clusters[cluster_index]
            for i, node_i in enumerate(cluster, start=1):
                parent_node = f'{parent_prefix}{cluster_index}_{i}'
                self.add_node(parent_node)
                self.add_edge(parent_node, node_i)
    
    def add_multiparents_for_all_clusters(self, parent_prefix='u'):
        num_clusters = len(self.clusters)
        for i in range(num_clusters):
            self.add_multiparents_for_cluster(i, parent_prefix)

    def add_individual_parents_for_all_clusters(self, parent_prefix='v'):
        num_clusters = len(self.clusters)
        for i in range(num_clusters):
            self.add_individual_parents_for_cluster(i, parent_prefix)

    def add_single_parent_for_all_clusters(self, parent_prefix):
        for cluster_index in range(len(self.clusters)):
            parent_node = f'{parent_prefix}_cluster_{cluster_index}'
            self.add_parents_for_cluster(cluster_index, [parent_node])
    
    def add_single_child_for_all_clusters(self, child_prefix):
        for cluster_index in range(len(self.clusters)):
            child_node = f'{child_prefix}_cluster_{cluster_index}'
            self.add_children_for_cluster(cluster_index, [child_node])

    def generate_BN_for_random_field(self):
        self.add_multiparents_for_all_clusters(parent_prefix='u')
        self.add_individual_parents_for_all_clusters(parent_prefix='v')

    def temporary_BN_considering_correlations(self):
        self.add_single_parent_for_all_clusters(parent_prefix='u_temp')

    def remove_tempory_node_BN_considering_correlations(self):
        pass

# # Example usage
# my_graph = GraCS()
# added_nodes = my_graph.add_cluster([[1, 2, 3], [4, 5]])

# my_graph.add_parents_for_cluster(0, ['P1', 'P2'])  # Add parents 'P1' and 'P2' for nodes in the first cluster
# my_graph.add_children_for_cluster(0, ['C1', 'C2'])  # Add children 'C1' and 'C2' for nodes in the first cluster

# print(my_graph.edges())  
# # Output: [('P1', 1), ('P1', 2), ('P1', 3), ('P2', 1), ('P2', 2), ('P2', 3), 
# #          (1, 'C1'), (2, 'C1'), (3, 'C1'), (1, 'C2'), (2, 'C2'), (3, 'C2')]

def all_combinations_from_list(li):
    b = [len(ele) for ele in li]
    num_sublists = len(b)
    for_modulo = b.copy()
    for_modulo[-1] = 1
    for i in range(1,num_sublists):
        for_modulo[num_sublists-i-1] = for_modulo[num_sublists-i] * b[num_sublists-i]

    haha = for_modulo[0] * b[0]
    all_combinations = np.zeros((haha,num_sublists)).tolist()
    for idx in range(haha):
        maomao1 = idx
        for i in range(num_sublists):
            maomao2 = int(np.floor(maomao1/for_modulo[i]))
            all_combinations[idx][i] = li[i][maomao2]
            maomao1 = maomao1 % for_modulo[i]

    return all_combinations

def flatten_list(l):
    # This function can flatten a two-level nested list 
    return [item for sublist in l for item in sublist]

def distance(lat1, lon1, lat2, lon2):
    r = 6371  # Radius of the Earth in kilometers
    p = math.pi / 180

    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2

    return 2 * r * math.asin(math.sqrt(a))

def add_candidate(candidates, current_candidate, current_candidate_id, score, top_n):
    """
    Add a candidate to the candidates list while maintaining the top N candidates.

    Parameters:
    - candidates: List of current candidates
    - current_candidate: Candidate to add
    - current_candidate_id: Candidate ID to add
    - score: Score associated with the candidate (used for sorting)
    - top_n: Maximum number of top candidates to maintain
    """
    heapq.heappush(candidates, (score, current_candidate, current_candidate_id))
    if len(candidates) > top_n:
        heapq.heappop(candidates)

# # Example usage of add_candidate function
# candidates_list = []  # List to store candidates

# # Adding candidates with scores
# add_candidate(candidates_list, "Candidate1", 101, 0.8, 3)
# add_candidate(candidates_list, "Candidate2", 102, 0.6, 3)
# add_candidate(candidates_list, "Candidate3", 103, 0.9, 3)
# add_candidate(candidates_list, "Candidate4", 104, 0.7, 3)

# # Displaying the top candidates
# top_candidates = [(candidate, candidate_id) for _, candidate, candidate_id, in candidates_list]
# print("Top Candidates:", top_candidates)



def convert_lat_lon_to_xy(latitude, longitude, radius=6371.0):
    """
    Convert latitude and longitude to Cartesian coordinates (y, x) using Mercator projection.
    
    Parameters:
        latitude (float): Latitude in degrees.
        longitude (float): Longitude in degrees.
        radius (float): Earth's radius in kilometers. Default is 6371.0 km.
    
    Returns:
        tuple: (y, x) Cartesian coordinates.
    """
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)
    
    x = radius * lon_rad
    y = radius * math.log(math.tan(math.pi/4 + lat_rad/2))
    
    return y, x

# # Example usage:
# latitude1 = 37.7749  # Example latitude 1 (San Francisco)
# longitude1 = -122.4194  # Example longitude 1 (San Francisco)

# latitude2 = 37.9
# longitude2 = -122.3

# # Convert latitude and longitude to Cartesian coordinates
# y1, x1 = convert_lat_lon_to_xy(latitude1, longitude1)
# y2, x2 = convert_lat_lon_to_xy(latitude2, longitude2)

# print(f"Latitude 1: {latitude1}, Longitude 1: {longitude1}")
# print(f"Converted Coordinates 1: (y, x) = ({y1}, {x1})")

# print(f"\nLatitude 2: {latitude2}, Longitude 2: {longitude2}")
# print(f"Converted Coordinates 2: (y, x) = ({y2}, {x2})")

# # Calculate distance using original latitude and longitude
# distance_lat_lon = math.sqrt((latitude2 - latitude1)**2 + (longitude2 - longitude1)**2) * 111.32  # Assuming Earth is a perfect sphere

# # Calculate distance using converted x and y coordinates
# distance_xy = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

# print(f"\nDistance using Latitude and Longitude: {distance_lat_lon} km")
# print(f"Distance using Converted Coordinates: {distance_xy} km")

