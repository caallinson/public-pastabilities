from geopy.distance import geodesic 
import pandas as pd


def print_special_requests(df_mama_ready, df_garfield_ready):

    print("\nTotal Mamas: \t\t", len(df_mama_ready))
    print("Gluten Free Mamas: \t", len(df_mama_ready[df_mama_ready['special_gluten'] == True]))
    print("Veg Free Mamas: \t", len(df_mama_ready[df_mama_ready['special_veg'] == True]))
    print("Vegan Free Mamas: \t", len(df_mama_ready[df_mama_ready['special_vgn'] == True]))
    print("Dairy Free Mamas: \t", len(df_mama_ready[df_mama_ready['special_dairy'] == True]))
    print("Nut Free Mamas: \t", len(df_mama_ready[df_mama_ready['special_nut'] == True]))
    print("Other Restriction Mamas: \t", len(df_mama_ready[df_mama_ready['special_other'] == True]))


    print()
    print("\nTotal Garfields: \t", len(df_garfield_ready))
    print("Gluten Free Garfields: \t", len(df_garfield_ready[df_garfield_ready['special_gluten'] == True]))
    print("Veg Free Garfields: \t", len(df_garfield_ready[df_garfield_ready['special_veg'] == True]))
    print("Vegan Free Garfields: \t", len(df_garfield_ready[df_garfield_ready['special_vgn'] == True]))
    print("Dairy Free Garfields: \t", len(df_garfield_ready[df_garfield_ready['special_dairy'] == True]))
    print("Nut Free Garfields: \t", len(df_garfield_ready[df_garfield_ready['special_nut'] == True]))
    print("Other Restriction Garfields: \t", len(df_garfield_ready[df_garfield_ready['special_other'] == True]))

def drive_dist(a,b):
    """Approximate driving distance from straight line distance (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3835347/)"""
    return geodesic(a,b).mi*1.417

def get_mg_distance_dict(df_mama_ready, df_garfield_ready):
    """Return a dictionary of distances between IDs in DF1 and DF2"""
    
    distance_dict = {}

    for i in df_mama_ready.itertuples():
        mama_max_dist = i.miles
        for j in df_garfield_ready.itertuples():
            a_latlong = (i.lat, i.long)
            b_latlong = (j.lat, j.long)
            temp_drive_dist = drive_dist(a_latlong, b_latlong)
            if  temp_drive_dist <= mama_max_dist:
                distance_dict[(i.Index, j.Index)] = temp_drive_dist
    return distance_dict

def get_gg_distance_dict(df_garfield_ready, max_cluster_dist = 3):
    """Return a dictionary of distances between IDs in DF1 and DF2"""
    
    distance_dict = {}

    for i in df_garfield_ready.itertuples():
        for j in df_garfield_ready.itertuples():
            a_latlong = (i.lat, i.long)
            b_latlong = (j.lat, j.long)
            temp_drive_dist = drive_dist(a_latlong, b_latlong)
            if  temp_drive_dist <= max_cluster_dist:
                distance_dict[(i.Index, j.Index)] = temp_drive_dist
    return distance_dict

def get_mama_max_capacity(df_mama_ready):
    """Given a df of mamas, return a dictionary of their maximum capacity"""

    mama_capacity = {}

    for i in df_mama_ready.itertuples():
        mama_capacity[i.Index] = i.quantity
    return mama_capacity

def get_garfield_demand(df_garfield_ready):
    """Given a df of mamas, return a dictionary of their maximum capacity"""
    
    garfield_demand = {}

    for j in df_garfield_ready.itertuples():
        garfield_demand[j.Index] = j.quantity
        
    return garfield_demand

def get_mama_max_dist(df_mama_ready, mama_capacity, default_dist=7):
    """Given a mamas DF, apply rules as follows:
        - If no Max distance is given, take the default_dist
        - Else, take the distance as given in the mama Df
        """
    
    max_dist_mama = {}

    for i in df_mama_ready.itertuples():
        if i.miles <= 0.5:
            max_dist_mama[i.Index] = default_dist
        else:
            max_dist_mama[i.Index] = i.miles
            
    return max_dist_mama

def get_IDs(df):
    id_list = []
    for i in df.itertuples():
        id_list.append(i.Index)
        
    return id_list

def get_objective_scores(df_mama_ready, df_garfield_ready, mg_distance_dict):
    score_dict = {}

    for (i,j) in mg_distance_dict.keys():
        
        garf_gluten = df_garfield_ready.loc[j, "special_gluten"]
        garf_veg = df_garfield_ready.loc[j, "special_veg"]
        garf_vgn = df_garfield_ready.loc[j, "special_vgn"]
        garf_dairy = df_garfield_ready.loc[j, "special_dairy"]
        garf_nut = df_garfield_ready.loc[j, "special_nut"]
        garf_other = df_garfield_ready.loc[j, "special_other"]
        garf_family = df_garfield_ready.loc[j, "num_kids"]
        garf_days_old = df_garfield_ready.loc[j, "days_since_request"]

        mama_gluten = df_mama_ready.loc[i, "special_gluten"]
        mama_veg = df_mama_ready.loc[i, "special_veg"]
        mama_vgn = df_mama_ready.loc[i, "special_vgn"]
        mama_dairy = df_mama_ready.loc[i, "special_dairy"]
        mama_nut = df_mama_ready.loc[i, "special_nut"]
        mama_other = df_mama_ready.loc[i, "special_other"]
        mama_freq = df_mama_ready.loc[i, "frequency"]

        # default score for a match
        score_dict[(i,j)] = 1

        # negative score for delivering to someone that you don't have capabilities for
        if (garf_gluten and not mama_gluten) or (garf_veg and not mama_veg) or (garf_vgn and not mama_vgn) or (garf_dairy and not mama_dairy) or (garf_other and not mama_other) :
            score_dict[(i,j)] = -9999 
        
        # Bonus for families
        if (garf_family>0):
            score_dict[(i,j)] += 1

        # Bonus for old requests (+1.5 for 2 or more weeks old, +0.7 for over a week old)
        if garf_days_old >= 14:
            score_dict[(i,j)] += 1.1
        elif garf_days_old >= 7:
            score_dict[(i,j)] += 0.7

        # bonus if you're monthly or bi-weekly
        if mama_freq == "each month" or mama_freq == "once a month":
            score_dict[(i,j)] += 0.2
            
        elif mama_freq == "every other week":
            score_dict[(i,j)] += 0.1

        # Bonus for making special delivery
        if (garf_gluten or garf_veg or garf_vgn or garf_dairy or garf_nut or garf_other) and ((garf_gluten and mama_gluten) or not garf_gluten) and ((garf_veg and mama_veg) or not garf_veg) and ((garf_vgn and mama_vgn) or not garf_vgn) and ((garf_dairy and  mama_dairy) or not garf_dairy) and ((garf_other and  mama_other) or not garf_other) and ((garf_other and  mama_other) or not garf_other):
            score_dict[(i,j)] += 0
                
    return score_dict

def optimization_preprocessing(df_mama_ready, df_garfield_ready, default_dist, max_cluster_dist):
    """ Run various functions to get the needed dictionaries for optimization"""
    
    # GET OPTIMIZATION DICTIONARIES
    
    ##### 1. Distance dictionaries
    mg_dist_dict = get_mg_distance_dict(df_mama_ready,df_garfield_ready)
    print("Successfully generated distance dictionaries:")
    print("Mama-Garfield Dict Length: ", len(mg_dist_dict))
    gg_dist_dict = get_gg_distance_dict(df_garfield_ready, max_cluster_dist)
    print("Successfully generated distance dictionaries:")
    print("Mama-Garfield Dict Length: ", len(mg_dist_dict))
    print("Garfield-Garfield Dict Length: ", len(gg_dist_dict))


    #### 2. Get max capacity for mamas
    mama_capacity = get_mama_max_capacity(df_mama_ready)
    print("Successfully generated capacity dictionary for", len(mama_capacity), "mamas")

    #### 3. Get demand for garfields
    garfield_demand = get_garfield_demand(df_garfield_ready)
    print("Successfully generated demand dictionary for", len(garfield_demand), "garfields")

    #### 4. Get maximum distance travel limit
    max_dist_mama = get_mama_max_dist(df_mama_ready, mama_capacity, default_dist)
    print("Successfully generated distance dictionary for", len(max_dist_mama), "mamas")
    
    #### 5. Get IDs
    mama_id = get_IDs(df_mama_ready)
    garfield_id = get_IDs(df_garfield_ready)
    print("Successfully generated ID dictionary for garfields and mamas")
    
    #### 6. Get Objective Function
    score_dict = get_objective_scores(df_mama_ready, df_garfield_ready, mg_dist_dict)
    print("Successfully generated scores dictionary with", len(score_dict), "entries")

    return mg_dist_dict, gg_dist_dict, mama_capacity, garfield_demand, max_dist_mama, mama_id, garfield_id, score_dict











