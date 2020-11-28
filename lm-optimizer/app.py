from __future__ import print_function
from flask import Flask
from ortools.linear_solver import pywraplp
import pandas as pd
import numpy as np
import pymongo
from bson import ObjectId
import csv
import optimizer_preprocessing as o_pre
import optimizer_solver as o_solver
import optimizer_postprocessing as o_post
import mongo_interface as mongo_int
import sys
import time
import datetime
import traceback

app = Flask(__name__)

@app.route('/whereitat')
def helpme():
    return pywraplp.__file__

@app.route('/')
def root_message():
    return "app.route(''/'') does not exist. Try /hello or /optimize/[runID]"

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/time')
def cur_time():
    return 'The time is: ' + str(datetime.datetime.now())

@app.route('/optimize/<orch_run_ID>')
def optimizer_driver(orch_run_ID):

    s = time.time()

    #####
    # 0. Prepare run settings
    #####

    # Inputs and validation
    from_mongo_flag = False
    from_excel_flag = True

    write_to_mongo_flag = False
    write_to_csv_flag = True

    if from_mongo_flag and write_to_mongo_flag and orch_run_ID != "default":
        write_error_to_mongo = True
    else:
        write_error_to_mongo = False

    if from_mongo_flag and from_excel_flag:
        return "Can only select one FROM flag"

    data_path_excel = "../../data/"
    results_path_excel = "../../results/"

    # Set RunID and Time
    if orch_run_ID == "default":
        run_ID = "2020-11-16T18:35:06.167Z"
        run_date = datetime.datetime.strptime("2020-11-16", "%Y-%m-%d")
        print("Running default RunID:", run_ID)
        print("Using date from RunID: ", run_ID[0:10])
    else:
        run_ID = orch_run_ID

        # try to extract date from RunID. Otherwise use today
        try:
            date_str = run_ID[0:10]
            run_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            print("Using date from RunID: ", run_ID[0:10])
        except:
            try:
                date_str = run_ID[0:8]
                run_date = datetime.datetime.strptime(date_str, "%Y%m%d")
                print("Using date from RunID: ", run_ID[0:8])
            except:
                run_date = datetime.datetime.today()
                print("Defaulting to today's date for run date: ", datetime.datetime.strftime(run_date, "%Y-%m-%d"))

    # Set parameters
    distance_parameter = 0.01 #weight of distance in objective function
    mama_parameter = 0.3 #weight of maximizing mamas in objective function
    cluster_dist = 3 # miles
    default_dist = 7 # miles

    # Mongo Credentials
    if from_mongo_flag:
        mongo_user = 'fake_username'
        mongo_pwd = 'fakepassword'

        client = pymongo.MongoClient('mongodb+srv://'+mongo_user+':'+mongo_pwd+'@lasagna-class-project-d.ljwaj.mongodb.net/endless-pastabilities?retryWrites=true&w=majority')
        db = client['endless-pastabilities']
    
    
    #####
    # 1. Get Mama IDs and Garfield IDs from optimization
    #####
    try:
        if from_mongo_flag:
            runid_query = {"_id": run_ID}
            mongo_int.update_optimization_status(db, run_ID, "calculating")

            garfield_id_collection =  db['optimize-requests'].find_one(runid_query, {"_id": 0, "garfields": 1})
            garfield_id_list =   garfield_id_collection['garfields']
            garfield_id_list = [ObjectId(x) for x in garfield_id_list]

            mama_id_collection =  db['optimize-requests'].find_one(runid_query, {"_id": 0, "mamas": 1})
            mama_id_list = mama_id_collection['mamas']
            mama_id_list = [ObjectId(x) for x in mama_id_list]
    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error while fetching mamas and garfield IDs from optimize request. Check the RunID"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg

    try:
        if from_excel_flag: 
            df_mama= pd.read_excel(data_path_excel + 'latest-supplier_' + run_ID + '.xlsx')
            df_garfield= pd.read_excel(data_path_excel + 'latest-requestor_' + run_ID + '.xlsx')
            df_garfield['request_date'] = pd.to_datetime(df_garfield['request_date'])

            df_mama_ready = df_mama[(df_mama['quantity'] > 0)]
            df_garfield_ready = df_garfield[(df_garfield['quantity'] > 0)]
    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error while reading and prepping mamas and garfields table from Excel"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg      
    

    #####
    # 2. Get filtered Mongo DFs for mamas and Garfields based on Mama and Garfield IDs
    #####
    try:
        if from_mongo_flag:
            df_mama_ready, df_garfield_ready = mongo_int.get_filtered_df(db, mama_id_list, garfield_id_list)
    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error while matching optimize request IDs to mama and garfield Mongo tables"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg

    # Add a column to df_garfield_ready for # of days since request
    df_garfield_ready['days_since_request'] = (df_garfield_ready['request_date'] - run_date)/np.timedelta64(1,'D')


    #####
    # 3. Print overview of data and special requests
    #####

    try:
        o_pre.print_special_requests(df_mama_ready, df_garfield_ready)
    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error while printing mama and garfield special requests"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg

    #####
    # 4. Run Pre-Processing
    #####
    try:
        mg_dist_dict, gg_dist_dict, mama_capacity, garfield_demand, max_dist_mama, mama_id, garfield_id, score_dict = o_pre.optimization_preprocessing(df_mama_ready, df_garfield_ready, default_dist, cluster_dist)
    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error in optimization preprocessing"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg

    #####
    # 5. Create and run model
    #####
    try:
        matches = o_solver.lasagna_solver(df_mama_ready, df_garfield_ready, mg_dist_dict, gg_dist_dict, mama_capacity, garfield_demand, max_dist_mama, mama_id, garfield_id, score_dict, cluster_dist, distance_parameter, mama_parameter)
    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error in solving optimization"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg
    
    #####
    # 6. Print stats
    #####
    try:
        o_post.print_matches(matches, df_garfield_ready, df_mama_ready, mg_dist_dict, max_dist_mama, garfield_demand, mama_capacity)
        o_post.print_mama_path_stats(matches, df_garfield_ready, df_mama_ready, mg_dist_dict, gg_dist_dict, mama_id,max_dist_mama)
        kpi_dict = o_post.print_stats(matches, df_garfield_ready, df_mama_ready)
    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error in printing optimization statistics"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg

    #####
    # 7. Write results
    #####

    try:
        if write_to_mongo_flag:
            mongo_int.write_matches_to_mongo(db, df_mama_ready, df_garfield_ready, run_ID, matches, mama_id, gg_dist_dict, mg_dist_dict, max_dist_mama, mama_capacity)
            mongo_int.update_optimization_status(db,run_ID, "success")
            mongo_int.push_stats_to_mongo(db, run_ID, kpi_dict)
    except:
        msg =str(traceback.format_exc()) + "\n\n"+  "Encountered an error in optimization post-processing, pushing to Mongo"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg

    try:
        if write_to_csv_flag:
            print("trying to print results to: ", results_path_excel + "default")
            o_post.write_csv_output(results_path_excel + run_ID[0:13], df_mama_ready, df_garfield_ready, matches, mama_id, gg_dist_dict, mg_dist_dict, max_dist_mama, mama_capacity)

    except:
        msg = str(traceback.format_exc()) + "\n\n"+ "Encountered an error in optimization post-processing, writing to CSV"
        if write_error_to_mongo:
            mongo_int.update_optimization_status(db, run_ID, "Failed: " + msg)
        return "0: " + msg    

    print("Run Complete!!!!!!")
    print(str(int(time.time() - s)) + ' seconds elapsed.')

    if write_to_csv_flag:
        return "Run "+ run_ID +" complete and results are in CSV!!!!!!<br> "+str(int(time.time() - s)) + " seconds elapsed."

    if write_to_mongo_flag:
        if orch_run_ID == "default":
            return "Default run, "+ run_ID +", is complete!!!!!!<br> "+str(int(time.time() - s)) + " seconds elapsed."
        else:
            return "Run "+ run_ID +" complete and results are in Mongo!!!!!! <br> "+str(int(time.time() - s)) + " seconds elapsed."
