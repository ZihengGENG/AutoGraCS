import pandas as pd
from utils import distance
from sklearn.preprocessing import LabelEncoder
from math import radians, cos, sin, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Radius of Earth in kilometers. Use 6371 for kilometers
    radius = 6371
    distance = radius * c
    return distance

# List of positional words to identify river names and general descriptors to avoid mismatch
positional_words = ['NEAR', 'NR', 'ON', 'AT']
general_descriptors = ['PRONG', 'BRANCH', 'FORK', 'NORTH', 'SOUTH', 'EAST', 'WEST']
skip_descriptors = {'RIVER', 'CREEK', 'CANAL', 'BAY', 'FORK', 'NORTH', 'SOUTH', 'EAST', 'WEST', 'LAKE', 'SPRING', 'CK', 'CRK', 'RVR', 'RV','PRONG', 'LEVEE'}

# Abbreviation dictionary
abbreviations = {
    "N": "NORTH",
    "S": "SOUTH",
    "E": "EAST",
    "W": "WEST",
    "RVR": "RIVER",
    "LTL": "LITTLE"
}

def expand_abbreviations(word):
    return abbreviations.get(word.upper(), word)

def extract_river_name(desc):
    desc = desc.upper()
    if desc.startswith("'") and desc.endswith("'"):
        desc = desc[1:-1]
    tokens = desc.split()
    for i, token in enumerate(tokens):
        if token in positional_words:
            return ' '.join(tokens[:i])
    return desc  


def is_valid_match(bridge_tokens, gage_tokens):
    # Convert descriptions to lists of words
    bridge_words = bridge_tokens
    gage_words = gage_tokens

    # Find the rightmost overlapping skip descriptor
    rightmost_overlap = -1
    for desc in skip_descriptors:
        if desc in bridge_words and desc in gage_words:
            rightmost_overlap = max(rightmost_overlap, max(bridge_words.index(desc), gage_words.index(desc)))

    # If there is an overlapping skip descriptor
    if rightmost_overlap != -1:
        # Check to the left of the rightmost skip descriptor
        for i in range(rightmost_overlap - 1, -1, -1):
            if i < len(bridge_words) and i < len(gage_words):
                if bridge_words[i] == gage_words[i]:
                    if bridge_words[i] not in skip_descriptors:
                        return True
        return False

    # If no overlapping skip descriptors, check for at least two consecutive matching words
    bridge_set = set(bridge_tokens) - skip_descriptors
    gage_set = set(gage_tokens) - skip_descriptors
    common_words = list(bridge_set & gage_set)
    if len(common_words) < 2:
        return False
    # Check for consecutive words
    for i in range(len(common_words) - 1):
        if common_words[i+1] == common_words[i]:
            return True
    return False


if __name__ == '__main__':
    
    gages = pd.read_csv("florida_gages.csv")
    bridges = pd.read_csv("bridges_MiamiDade.csv")

    gages["RIVER_NAME"] = gages["STANAME"].apply(extract_river_name).str.upper()
    bridges["RIVER_NAME"] = bridges["FEATURES_DESC_006A"].apply(extract_river_name).str.upper()

    matches = []

    for idx, bridge in bridges.iterrows():
        bridge_tokens = bridge["RIVER_NAME"].split()
        bridge_desc = bridge["FEATURES_DESC_006A"]
        bridge_lon = bridge['LONG_017_DD']
        bridge_lat = bridge['LAT_016_DD']
        
        for j, gage in gages.iterrows():
            gage_tokens = gage["RIVER_NAME"].split()
            gage_desc = gage["STANAME"]
            gage_lon = gage['Longitude']
            gage_lat = gage['Latitude']
            
            distance = calculate_distance(bridge_lat, bridge_lon, gage_lat, gage_lon)
            
            if is_valid_match(bridge_tokens, gage_tokens):
                dist = distance(lat1=bridge_lat, lon1=bridge_lon, lat2=gage_lat, lon2=gage_lon)
                matches.append({
                    "BRIDGE_ID": bridge["ID"],
                    "GAGE_ID": gage["ID"],
                    "BRIDGE_DESC": bridge_desc,
                    "GAGE_DESC": gage_desc,
                    "BRIDGE_LON": bridge_lon,
                    "BRIDGE_LAT": bridge_lat,
                    "GAGE_LON": gage_lon,
                    "GAGE_LAT": gage_lat,
                    "DISTANCE": dist
                })


    matches_df = pd.DataFrame(matches)
    print(matches_df)

    matches_df.to_csv('matches.csv')


# --------------------------------------
    # matches = []

    # # match river gages itself
    # for j1, gage1 in gages.iterrows():
    #     gage1_tokens = gage1["RIVER_NAME"].split()
    #     gage1_desc = gage1["STANAME"]
    #     gage1_lon = gage1['Longitude']
    #     gage1_lat = gage1['Latitude']
        
    #     for j2, gage2 in gages.iterrows():
    #         gage2_tokens = gage2["RIVER_NAME"].split()
    #         gage2_desc = gage2["STANAME"]
    #         gage2_lon = gage2['Longitude']
    #         gage2_lat = gage2['Latitude']
            
    #         if j1 < j2:
            
    #             if is_valid_match(gage1_tokens, gage2_tokens):
    #                 dist = distance(lat1=gage1_lat, lon1=gage1_lon, lat2=gage2_lat, lon2=gage2_lon)
    #                 matches.append({
    #                     "GAGE_ID": gage1["ID"],
    #                     "GAGE_ID2": gage2["ID"],
    #                     "GAGE_DESC": gage1_desc,
    #                     "GAGE_DESC2": gage2_desc,
    #                     "GAGE_LON": gage1_lon,
    #                     "GAGE_LAT": gage1_lat,
    #                     "GAGE_LON2": gage2_lon,
    #                     "GAGE_LAT2": gage2_lat,
    #                     "DISTANCE": dist
    #                 })
    
    # matches_df = pd.DataFrame(matches)
    # print(matches_df)

    # matches_df.to_csv('matches_gages_gages.csv')



    # # # Preprocess river gages dataset
    # # # Categorize the river names into clusters based on their descriptions

    # # Initialize a LabelEncoder to assign unique numerical labels to river descriptions
    # label_encoder = LabelEncoder()

    # # Encode the river descriptions to numerical labels
    # gages['Encoded_Labels'] = label_encoder.fit_transform(gages['RIVER_NAME'])

    # # Create a dictionary to store clusters based on river descriptions
    # river_clusters = {}

    # # Assign cluster labels to the data
    # for i, label in enumerate(gages['Encoded_Labels']):
    #     if label not in river_clusters:
    #         river_clusters[label] = [i]
    #     else:
    #         for j in river_clusters[label]:
    #             # The code is not correct right now!!! I will come back to correct it.
    #             if is_valid_match(gages['RIVER_NAME'].iloc[i], gages['RIVER_NAME'].iloc[j]):
    #                 gages['Encoded_Labels'].iloc[i] = gages['Encoded_Labels'].iloc[j]
    #                 break
    #         else:
    #             river_clusters[label].append(i)

    # # Now, 'Encoded_Labels' column in the DataFrame contains the final numerical labels for each river gage
    # print(gages)