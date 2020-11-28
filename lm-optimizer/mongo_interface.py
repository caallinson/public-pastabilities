import pymongo
import pandas as pd
import optimizer_postprocessing as o_post


def get_filtered_df(db, mama_id_list, garfield_id_list):
    """ 
    Given Pandas DFs for Mama IDs and Garfield IDs, return two dfs ready for optimization
    """
    df_mama = pd.DataFrame(list(db.mama.find({'_id': {"$in": mama_id_list}, "active": True})))
    df_mama = df_mama.set_index('_id')
    if len(mama_id_list) == len(df_mama):
        print("\nMama database successfully extracted from Mongo")
        print("Mama DF Length:", len(df_mama))
        print("Expected Mama DF Length:", len(mama_id_list))
    else:
        print("\nUnexpected row count in mama DF")
        print("Mama DF Length:", len(df_mama))
        print("Expected Mama DF Length:", len(mama_id_list))


    df_garfield = pd.DataFrame(list(db.garfield.find({'_id': {"$in": garfield_id_list}, "active": True})))
    df_garfield = df_garfield.set_index('_id')
    df_garfield['request_date'] = pd.to_datetime(df_garfield['request_date'])
    if len(df_garfield) == len(garfield_id_list):   
        print("\nGarfield database successfully extracted from Mongo")
        print("Garfield DF Length:", len(df_garfield))
        print("Expected Garfield DF Length:", len(garfield_id_list))    
    else:
        print("\nUnexpected row count in Garfield DF")
        print("Mama DF Length:", len(df_garfield))
        print("Expected Mama DF Length:", len(garfield_id_list))
    
    if 'address_concat' not in df_garfield.columns:
        df_garfield["address_concat"] = df_garfield["address"]+", "+ df_garfield["city"]+", "+ df_garfield["state"]+", "+ df_garfield["zip_code"]
              
    return df_mama, df_garfield


def update_optimization_status(db, run_ID, message):
    """Update the optimization status table with a message"""

    db['optimize-control'].find_one_and_update({"_id": run_ID}, {"$set":{"status": message}})
    
    print("Succesfully updated optimization status to:", message)
    print("RunID:", run_ID)
    return


def push_stats_to_mongo(db, run_ID, kpi_dict):
    
    db['optimize-control'].find_one_and_update({"_id": run_ID}, {"$push":{"kpi": kpi_dict}})
    
    print("Successfully loaded KPIs to optimize-control table")
    print("RunID:", run_ID)

    return

def write_matches_to_mongo(db, df_mama_ready, df_garfield_ready, run_ID, matches, mama_id, gg_dist_dict, mg_dist_dict, max_dist_mama, mama_capacity):            
    
    matched_mamas_list = []
    unmatched_mamas_list = []
            
    for i in mama_id:

        mama_name = df_mama_ready.loc[i, "name"]
        mama_freq = df_mama_ready.loc[i, "frequency"]
        distmax = round(max_dist_mama[i])
        max_cap_mama = round(mama_capacity[i])
        email = df_mama_ready.loc[i, "email"]
        phone = str(df_mama_ready.loc[i, "phone"])
        address = str(df_mama_ready.loc[i, "address"])
        form_url = str(df_mama_ready.loc[i, "url"])
        special_capabilities = o_post.is_special(df_garfield_ready, df_mama_ready,i, "mama")


        mama_garfields = []
        for (i2, j2) in matches.keys():
            if i == i2:
                mama_garfields.append(j2)

        max_cluster_dist = 0
        for g1 in mama_garfields:
            for g2 in mama_garfields:
                max_cluster_dist = max(max_cluster_dist, gg_dist_dict[(g1, g2)])

        num_lasagnas = 0
        max_garfield_dist = 0
        special_str = ''
        for g1 in mama_garfields:
            max_garfield_dist = max(max_garfield_dist, mg_dist_dict[(i, g1)])  
            num_lasagnas += matches[(i,g1)]
            if len(o_post.is_special(df_garfield_ready, df_mama_ready,g1, "garfield"))>0:
                special_str += o_post.is_special(df_garfield_ready, df_mama_ready,g1, "garfield")+";"
        special_str = special_str[0:-1]
        
        
        temp_garfield_list = []
        for g1 in mama_garfields:
            temp_garfield_dict = {
                "garfield_id": str(g1),
                'Name': df_garfield_ready.loc[g1, "name"], 
                'Email': df_garfield_ready.loc[g1, "email"], 
                'Phone Number': df_garfield_ready.loc[g1, "phone"], 
                'Address': df_garfield_ready.loc[g1, "address_concat"],
                'Quantity': round(matches[(i,g1)]),
                'Distance': round(mg_dist_dict[(i, g1)],1),
                'Special Requests': o_post.is_special(df_garfield_ready, df_mama_ready,g1, "garfield"),
                'Request Date': df_garfield_ready.loc[g1, "request_date"]
            }
            temp_garfield_list.append(temp_garfield_dict)
        
        temp_dict = {
            'mama_id': str(i),
            'Name': mama_name, 
            'Email': email,
            'Phone Number': phone,
            'Address': address,
            'Form URL': form_url,
            'Frequency': mama_freq,
            'Max Capacity': max_cap_mama , 
            'Lasagnas Matches': round(num_lasagnas), 
            'Capacity Usage': str(round(num_lasagnas))+'/'+str(max_cap_mama),
            'Distance Limit': distmax, 
            'Furthest Garfield':  round(max_garfield_dist,1), 
            'Cluster Distance': round(max_cluster_dist,1) , 
            'Distance Usage': "Distance Limit: "+str(distmax)+", Furthest Garfield: "+str(round(max_garfield_dist,1))+", Max Cluster Dist: "+str(round(max_cluster_dist,1)) , 
            'Special Capabilities': special_capabilities,
            'Special Capabilities in Matching': special_str, 
            'Garfields': temp_garfield_list

        }
        
        if len(mama_garfields)==0:
            unmatched_mamas_list.append(temp_dict)
        else:
            matched_mamas_list.append(temp_dict)
    
    
    # Upload to Mongo
    upload_dict = {"_id": run_ID, 
                   "matched_mamas": matched_mamas_list,
                   "unmatched_mamas": unmatched_mamas_list
                  }
    
    
    db['optimize-results'].replace_one({"_id": run_ID}, upload_dict, upsert = True)
    
    print("Succesfully wrote matches for", len(mama_id), "mamas to the database")
    print("RunID:", run_ID)

    
    return


