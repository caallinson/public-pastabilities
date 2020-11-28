import pandas as pd
import csv
import datetime

def print_matches(matches, df_garfield_ready, df_mama_ready, mg_dist_dict, max_dist_mama, garfield_demand, mama_capacity):
    
    print('\n--------\nMatches:')
    for (i,j) in matches.keys():
            i_name = df_mama_ready.loc[i, "name"][0:12]
            j_name = df_garfield_ready.loc[j, "name"][0:12]
            print((i_name,j_name),": \t", round(matches[(i,j)]), "\t Distance:", round(mg_dist_dict[(i,j)]), " \t Max Distance:", round(max_dist_mama[i])," \t Requests:", round(garfield_demand[j]), " \t Mama Cap:", round(mama_capacity[i]))

    return 

def is_special(df_garfield_ready, df_mama_ready, j_id, user_type):
    
    if user_type=="garfield":
        glut = df_garfield_ready.loc[j_id,"special_gluten"]
        veg = df_garfield_ready.loc[j_id,"special_veg"]
        vgn = df_garfield_ready.loc[j_id,"special_vgn"]
        dairy = df_garfield_ready.loc[j_id,"special_dairy"]
        nut = df_garfield_ready.loc[j_id,"special_nut"]
        other = df_garfield_ready.loc[j_id,"special_other"]
    elif user_type=="mama":
        glut = df_mama_ready.loc[j_id,"special_gluten"]
        veg = df_mama_ready.loc[j_id,"special_veg"]
        vgn = df_mama_ready.loc[j_id,"special_vgn"]
        dairy = df_mama_ready.loc[j_id,"special_dairy"]
        nut = df_mama_ready.loc[j_id,"special_nut"]
        other = df_mama_ready.loc[j_id,"special_other"]

    
    #HAS NUT AND OTHER
    special_bools = [glut, veg, vgn, dairy, nut, other] 
    special_strings = ["gluten, ", "vegan, ", "vegetarian, ", "dairy, ", "nut, ", "other, "]

    
    special_str = ''
    for i in range(len(special_bools)):
        special_str += special_bools[i] * special_strings[i]
    
    special_str = special_str[0:-2]
    
    
    return special_str

def get_capabilities_dict(df):
    """Given a Pandas DF, Create a dictionary with capabilities of mamas"""
    
    glut = {}
    veg = {}
    vgn = {}
    dairy = {}
    nut = {}
    other = {}

    for i in df.itertuples():
        glut[i.Index] = 1 if i.special_gluten is True else 0
        veg[i.Index] = 1 if i.special_veg is True else 0
        vgn[i.Index] = 1 if i.special_vgn is True else 0
        dairy[i.Index] = 1 if i.special_dairy is True else 0
        nut[i.Index] = 1 if i.special_nut is True else 0
        other[i.Index] = 1 if i.special_other is True else 0

    
    return glut, veg, vgn, dairy, nut, other

def print_mama_path_stats(matches, df_garfield_ready, df_mama_ready, mg_dist_dict, gg_dist_dict, mama_id, max_dist_mama):
    print("\n--------\nMama Path Information:")
    for i in mama_id:
        i_name = df_mama_ready.loc[i, "name"][0:15]

        mama_garfields = []
        for (i2, j2) in matches.keys():
            if i == i2:
                mama_garfields.append(j2)
        
        max_cluster_dist = 0
        for g1 in mama_garfields:
            for g2 in mama_garfields:
                max_cluster_dist = max(max_cluster_dist, gg_dist_dict[(g1, g2)])
        
        max_garfield_dist = 0
        for g1 in mama_garfields:
            max_garfield_dist = max(max_garfield_dist, mg_dist_dict[(i, g1)])

        print(i_name, "Path: \t Num garfields:", len(mama_garfields), "\t Max cluster dist:", round(max_cluster_dist,1), "\t Furthest garfield:", round(max_garfield_dist), "\t Max dist:", round(max_dist_mama[i]))
    return

def print_stats(matches, df_garfield_ready, df_mama_ready):
    z_count = 0
    lasagnas_delivered = 0
    special_deliveries = 0
    
    mama_glut, mama_veg, mama_vgn, mama_dairy, mama_nut, mama_other = get_capabilities_dict(df_mama_ready)
    garfield_glut, garfield_veg, garfield_vgn, garfield_dairy, garfield_nut, garfield_other = get_capabilities_dict(df_garfield_ready)
    
    for (i,j) in matches.keys():
        z_count += 1
        lasagnas_delivered += matches[(i,j)]
        
        if (garfield_glut[j] == 1) or (garfield_veg[j] == 1) or (garfield_vgn[j] == 1) or (garfield_dairy[j] == 1):
            special_deliveries  += matches[(i,j)]

    print("\n--------\nRun Statistics:")
    print("Total Deliveries:", z_count, "matches, ", round(lasagnas_delivered), "lasagnas")

    # Deliveries requested
    pp_garfield_requests = df_garfield_ready['quantity'].sum()
    print("Requests:", round(lasagnas_delivered), "/", pp_garfield_requests, "Lasagnas  (", round(lasagnas_delivered/pp_garfield_requests*100),"% demand met)")


    # mama capacity
    pp_mama_capacity = df_mama_ready['quantity'].sum()
    print("mama Capacity Used:", round(lasagnas_delivered), "/", pp_mama_capacity, "Lasagnas  (",round(lasagnas_delivered/pp_mama_capacity*100),"% utilization)")

    # Special deliveries
    print("Special deliveries:", special_deliveries)
    
    
    # Create data structure to update to mongo
    kpi_dict = {"kpi_num_matches_made": int(z_count),
                "kpi_num_lasagnas_delivered": int(lasagnas_delivered),
                "kpi_total_lasagna_demand": int(pp_garfield_requests),
                "kpi_pct_demand_met": float(round(lasagnas_delivered/pp_garfield_requests*100,1)),
                "kpi_total_lasagna_supply": int(pp_mama_capacity),
                "kpi_pct_supply_met": float(round(lasagnas_delivered/pp_mama_capacity*100,1)),
                "kpi_special_deliveries": int(special_deliveries)}

    
    return kpi_dict

def write_csv_output(run_ID, df_mama_ready, df_garfield_ready, matches, mama_id, gg_dist_dict, mg_dist_dict, max_dist_mama, mama_capacity):
    print("Trying to write CSV...")
    
    with open(run_ID+'_output_matched_mamas.csv', mode = 'w',  newline='') as csv_file_matched, open(run_ID+'_output_unmatched_mamas.csv', mode = 'w',  newline='') as csv_file_unmatched:
            
            fieldnames = ['Regional Leader', 'Region', 'Mama Name', 'Google Doc URL', 'Recipient Name', 'Recipient Has Kids?', 'Match Quantity',  'Mama Capacity', 'Recipient Distance', 'Mama Max Distance', 'Mama Cluster Distance', 'Mama Frequency', 'Request Date', 'Recipient Special Request', 'Mama Special Capabilities', 'Mama Email', 'Mama Phone Number']


            writer_matched = csv.DictWriter(csv_file_matched, fieldnames=fieldnames)
            writer_unmatched = csv.DictWriter(csv_file_unmatched, fieldnames=fieldnames)

            writer_matched.writeheader()
            writer_unmatched.writeheader()

            for i in mama_id:
                # determine if mama is matched or not
                matched_mama = False
                for (i2, j2) in matches.keys():
                    if i == i2:
                        matched_mama = True
                
                # get info for mama
                mama_regional_leader = df_mama_ready.loc[i, "regional_leader"]
                mama_region = df_mama_ready.loc[i, "region"]
                mama_name = df_mama_ready.loc[i, "name"]
                try:
                    mama_url = df_mama_ready.loc[i, "url"] if not isnan(df_mama_ready.loc[i, "url"]) else "-"
                except:
                    mama_url = "TBD"
                
                mama_capacity_temp = round(mama_capacity[i])
                mama_max_dist = round(max_dist_mama[i])
                mama_freq = df_mama_ready.loc[i, "frequency"]
                mama_special = is_special(df_garfield_ready, df_mama_ready, i, "mama")
                mama_email = df_mama_ready.loc[i, "email"]
                mama_phone = str(df_mama_ready.loc[i, "phone"])

                if matched_mama:
                    for (i2,j) in matches.keys():
                        if i == i2:
                            garfield_name = df_garfield_ready.loc[j, "name"]
                            garfield_kids = "Yes" if df_garfield_ready.loc[j, "num_kids"] > 0 else "No" 
                            match_qty = round(matches[(i,j)])
                            match_dist = round(mg_dist_dict[(i,j)],1)
                            garfield_special = is_special(df_garfield_ready, df_mama_ready, j, "garfield")
                            max_cluster_dist = 0
                            garfield_request_date = datetime.datetime.strftime(df_garfield_ready.loc[j, "request_date"], "%Y-%m-%d")

                            mama_garfields = []
                            for (i3, j3) in matches.keys():
                                if i == i3:
                                    mama_garfields.append(j3)

                            for g1 in mama_garfields:
                                for g2 in mama_garfields:
                                    max_cluster_dist = max(max_cluster_dist, gg_dist_dict[(g1, g2)])

                            writer_matched.writerow({
                                'Regional Leader': mama_regional_leader,
                                'Region': mama_region,
                                'Mama Name': mama_name, 
                                'Google Doc URL': mama_url, 
                                'Recipient Name': garfield_name, 
                                'Recipient Has Kids?': garfield_kids,
                                'Match Quantity': match_qty, 
                                'Mama Capacity': mama_capacity_temp, 
                                'Recipient Distance': match_dist, 
                                'Mama Max Distance': mama_max_dist, 
                                'Mama Cluster Distance': round(max_cluster_dist,1), 
                                'Mama Frequency': mama_freq, 
                                'Request Date': garfield_request_date,
                                'Recipient Special Request': garfield_special, 
                                'Mama Special Capabilities': mama_special, 
                                'Mama Email': mama_email, 
                                'Mama Phone Number': mama_phone
                            })
                else:

                    writer_unmatched.writerow({
                        'Regional Leader': mama_regional_leader,
                        'Region': mama_region,
                        'Mama Name': mama_name, 
                        'Google Doc URL': mama_url, 
                        'Recipient Name': "-", 
                        'Recipient Has Kids?': "-",
                        'Match Quantity': "-", 
                        'Mama Capacity': mama_capacity_temp, 
                        'Recipient Distance': "-", 
                        'Mama Max Distance': mama_max_dist, 
                        'Mama Cluster Distance': "-", 
                        'Mama Frequency': mama_freq, 
                        'Request Date': "-",
                        'Recipient Special Request': "N/A", 
                        'Mama Special Capabilities': mama_special, 
                        'Mama Email': mama_email, 
                        'Mama Phone Number': mama_phone
                    })






