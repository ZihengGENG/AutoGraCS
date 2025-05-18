import networkx as nx
ont = nx.DiGraph()




# read from ontology

e_bunch = {
            '01': ( ('bridge.failure_probability', 'bridge.risk'), 0, None),
            '02': ( ('bridge.failure_loss', 'bridge.risk'), 0, None),
            '03': ( ('bridge.SUBSTRUCTURE_COND_060', 'bridge.failure_probability'), 0, None),
            '04': ( ('bridge.SUPERSTRUCTURE_COND_059', 'bridge.failure_probability'), 0, None),
            '05': ( ('river_gage.STAGE', 'bridge.failure_probability'), 0, None),
            '06': ( ('river_gage.FLOW', 'bridge.failure_probability'), 0, None),
            '07': ( ('stcs.AADT', 'bridge.failure_loss'), 1, 10)
        }

var_random_field = ['river_gage.STAGE', 'river_gage.FLOW']
var_correlated = [['river_gage.STAGE', 'river_gage.FLOW']]

ont.add_edges_from(e_bunch)

leaf_nodes = [x for x in ont.nodes() if ont.out_degree(x)==0]
num_leaf_nodes = len(leaf_nodes)

edge_list = list(ont.edges)
num_edges = len(edge_list)


# print(ont.edges)