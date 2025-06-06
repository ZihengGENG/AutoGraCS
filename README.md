# README for `AutoGraCS`  
Bureau of Transportation Statistics (BTS), U.S. Department of Transportation (USDOT)  
`2025-06-06`  

## Summary of Code  
`This repository contains the implementation of AutoGraCS, a framework that automates the generation of knowledge graphs (KGs) for complex systems using user-defined ontologies, rules, and databases. The methodology is published in the following paper: Cheng, M., Shah, S. M. H., Nanni, A., & Gao, H. O. (2024). Automated knowledge graphs for complex systems (AutoGraCS): Applications to management of bridge networks. Resilient Cities and Structures, 3(4), 95–106. https://doi.org/10.1016/j.rcns.2024.11.001`  

A. [General Information](#a-general-information)  
B. [Sharing/Access & Policies Information](#b-sharingaccess-and-policies-information)  
C. [Data and Related Files Overview](#c-data-and-related-files-overview)  
D. [Methodological Information](#d-methodological-information)  
E. [Data-Specific Information for: What Do Americans Think About Federal Tax Options to Support Transportation? Results From Year Fifteen of a National Survey [supporting dataset]](#e-data-specific-information)  
F. [Update Log](#f-update-log)  

**Title of Code:**  `AutoGraCS: Automated Knowledge Graphs for Complex Systems`  

**Description of the Code:** `This code contains the implementation of AutoGraCS, a framework that automates the generation of knowledge graphs (KGs) for complex systems using user-defined ontologies, rules, and databases.`  

**Paper Archive Link:** <https://doi.org/10.1016/j.rcns.2024.11.001>  

**Authorship Information:**  

>  *Principal Data Creator or Data Manager Contact Information*  
>  Name: `Minghui Cheng` ([`0000-0002-8983-5148`](`https://orcid.org/0000-0002-8983-5148`))   
>  Institution: `University of Miami` [(ROR ID: `https://ror.org/02dgjyy92`)]
>  Address: `McArthur Engineering Building, 1251 Memorial Dr, Coral Gables, Florida 33146`  
>  Email: `minghui.cheng@miami.edu`  

>  *Data Distributor Contact Information*  
>  Name: `Ziheng Geng` ([`0000-0003-3050-494X`](`https://orcid.org/0000-0003-3050-494X`))     
>  Institution: `University of Miami` [(ROR ID: `https://ror.org/02dgjyy92`)]
>  Address: `McArthur Engineering Building, 1251 Memorial Dr, Coral Gables, Florida 33146`  
>  Email: `ziheng.geng@miami.edu`  

>  *Organizational Contact Information*  
>  Name: `Minghui Cheng` ([`0000-0002-8983-5148`](`https://orcid.org/0000-0002-8983-5148`))   
>  Institution: `University of Miami` [(ROR ID: `https://ror.org/02dgjyy92`)]
>  Address:  `McArthur Engineering Building, 1251 Memorial Dr, Coral Gables, Florida 33146`  
>  Email: `minghui.cheng@miami.edu`  

**Date of data collection and update interval:** `2025-06-06`  

**Geographic location of data collection:** `Coral Gables, Miami` United States [(GeoNames URI: http://sws.geonames.org/6252001/)](http://sws.geonames.org/6252001/)  

**Information about funding sources that supported the collection of the data:** `This project was funded through US Department of Transportation Tier 1 University Transportation Center CREATE Award No. 69A3552348330. ` 

## B. Sharing/Access and Policies Information  

**Recommended citation for the code:**  

>  `Elsevier` (`2024`). *`Automated knowledge graphs for complex systems (AutoGraCS): Applications to management of bridge networks`*. <https://doi.org/10.1016/j.rcns.2024.11.001>  

**Licenses/restrictions placed on the data:** This document is disseminated under the sponsorship of the U.S. Department of Transportation in the interest of information exchange. The United States Government assumes no liability for the contents thereof.  

**Was data derived from another source?:** `No`  

This document was created to meet the requirements enumerated in the U.S. Department of Transportation's [Plan to Increase Public Access to the Results of Federally-Funded Scientific Research Version 1.1](https://doi.org/10.21949/1520559) and [Guidelines suggested by the DOT Public Access website](https://doi.org/10.21949/1503647), in effect and current as of December 03, 2020.  

 
## C. Code and Related Files Overview  

File List for the `AutoGraCS`  

>  1. Filename: `bridges_MiamiDade.csv`  
>  Short Description:  `This dataset comprises bridge inventory data specific to Miami-Dade County, extracted from the National Bridge Inventory maintained by the Federal Highway Administration. It serves as the foundational dataset for constructing the knowledge graph used in risk assessment of the bridge network. The dataset includes detailed information on bridge identification, condition ratings, geographic locations, and other relevant attributes.`   

>  2. Filename: `florida_gages.csv`  
>  Short Description:  `This dataset contains river gage information for Miami-Dade County, obtained from the United States Geological Survey (USGS). It serves as a critical component in the development of the knowledge graph for bridge network risk assessment, as bridge failure probabilities are closely linked to river scour conditions. The dataset provides detailed information on gage identification, flow and stage measurements, geographic coordinates, and other relevant hydrological attributes. `  

>  3. Filename: `ptms_MiamiDade.csv`  
>  Short Description:  `This dataset includes traffic monitoring site information for Miami-Dade County, sourced from the Florida Department of Transportation (FDOT). It serves as an essential component in constructing the knowledge graph for bridge network risk assessment, as traffic data are integral to evaluating the potential consequences of bridge failure. The dataset contains detailed information on site identification, annual average daily traffic (AADT), geographic coordinates, and other pertinent attributes.`  

>  4. Filename: `ontology.py`  
>  Short Description:  `This file defines the ontology that captures the multi-domain knowledge and represents the relationships within and across sub-systems and components. Herein, we provide an example ontology tailored for monitoring the risk of bridges, where entities and attributes are represented as nodes and their interdependencies are encoded as edges. `  

>  5. Filename: `process_strings.py`  
>  Short Description:  `This file provides utility functions for parsing structured ontology strings used in knowledge graph representations. Specifically, it includes functions to extract the numerical value enclosed in a string, extract the ontology name from a string, and separate the class name and variable name from an indexed string or a formatted ontology string. `  

>  6. Filename: `rules.py`  
>  Short Description:  `This file defines a set of rule functions used to evaluate pairs of variables and determine whether an edge should be established between them in the knowledge graph. A total of ten rules are implemented to address various scenarios, including relationships between variables within the same class, across different classes, and those that exhibit statistical correlation.`  

>  7. Filename: `utils.py`  
>  Short Description:  This file defines the core data structures and utility functions used for constructing and managing a directed knowledge graph, particularly within the GraCS (knowledge graphs for complex systems) framework. It integrates graph construction, clustering logic, spatial computations, and combinatorial utilities.`  

>  8. Filename: `river_gage_matches_bridges.py`  
>  Short Description:  `Insert File 8 Description Here`  

>  9. Filename: `graph_construction_functions.py`  
>  Short Description:  `This file defines a rule-based matching algorithm to identify potential connections between river gages and bridges in Miami-Dade County based on spatial proximity. Key functionalities include spatial distance computation, text processing and semantic matching.`  

>  10. Filename: `main_file.py`  
>  Short Description:  `This file constructs a pipeline for generating the knowledge graph for complex systems. It systematically reads, preprocesses, and semantically links data based on a predefined ontology and a library of rule-based matching functions. Key functions include data loading and preprocessing, graph initialization, ontology-driven graph construction, clustering for random fields.`  

>  11. Filename: `README.md`  
>  Short Description:  `Insert File 10 Description Here`  

## D. Methodological Information   

**Description of methods used for collection/generation of data:** `To ensure the flexibility and extensibility of the AutoGraCS framework, the ontology and rule files are written by the user.`  

**Instrument or software-specific information needed to interpret the data:** `The codes are written using Python language.`  

## E. Data-Specific Information   

1. `bridges_MiamiDade.csv`  
- Number of variables (columns): `128`  
- Number of cases/rows: `1035`  
- Each row represents: `A bridge`  
- Data Dictionary/Variable List: `No`  
- Missing data codes: `Appropriate Skip`  

2. `florida_gages.csv`  
- Number of variables (columns): `16`  
- Number of cases/rows: `620`  
- Each row represents: `A river gage`  
- Data Dictionary/Variable List: `No`  
- Missing data codes: `Appropriate Skip`  

3. `ptms_MiamiDade.csv`  
- Number of variables (columns): `18`  
- Number of cases/rows: `1648`  
- Each row represents: `A traffic monitoring site`  
- Data Dictionary/Variable List: `No`  
- Missing data codes: `Appropriate Skip`  

## F. Update Log  

This README.txt file was originally created on `2025-06-06 Here` by `Ziheng Geng` ([`0000-0003-3050-494X`](`https://orcid.org/0000-0003-3050-494X`)), `PhD student`, `University of Miami` <`zxg383@miami.edu`>  
 
`2025-06-06`: Original file created  


