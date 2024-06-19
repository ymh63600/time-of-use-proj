import pandas as pd

def dropna(mains_df, appliance_dfs=[]):
        """
        Drops the missing values in the Mains reading and appliance readings and returns consistent data by copmuting the intersection
        """
        print ("Dropping missing values")

        # The below steps are for making sure that data is consistent by doing intersection across appliances
        mains_df = mains_df.dropna()
        ix = mains_df.index
        mains_df = mains_df.loc[ix]
        for i in range(len(appliance_dfs)):
            appliance_dfs[i] = appliance_dfs[i].dropna()
    
        for  app_df in appliance_dfs:
            ix = ix.intersection(app_df.index)
        mains_df = mains_df.loc[ix]
        new_appliances_list = []
        for app_df in appliance_dfs:
            new_appliances_list.append(app_df.loc[ix])
            
        return mains_df,new_appliances_list

def preprocess(time,test,appliances,power, building, sample_period):

    test.set_window(start=time['start_time'],end=time['end_time'])
    test_mains=next(test.buildings[building].elec.mains().load(physical_quantity='power', ac_type=power['mains'], sample_period=sample_period))
    appliance_readings=[]

    for appliance in appliances:
        test_df=next((test.buildings[building].elec[appliance].load(physical_quantity='power', ac_type=power['appliance'], sample_period=sample_period)))
        appliance_readings.append(test_df)
        test_mains , appliance_readings = dropna(test_mains,appliance_readings)
    test_submeters = []
    for i, appliance_name in enumerate(appliances):
        test_submeters.append((appliance_name,[appliance_readings[i]]))

    test_mains = [test_mains]

    return test_mains, test_submeters

def predict(clf, test_elec, test_submeters, model=None,appliance_params=None):
        print ("Generating predictions for :",clf.MODEL_NAME)        
        """
        Generates predictions on the test dataset using the specified classifier.
        """
        
        # "ac_type" varies according to the dataset used. 
        # Make sure to use the correct ac_type before using the default parameters in this code.   
        
           
        pred_list = clf.disaggregate_chunk(test_elec,model = model,appliance_params=appliance_params)

        # It might not have time stamps sometimes due to neural nets
        # It has the readings for all the appliances

        concat_pred_df = pd.concat(pred_list,axis=0)

        gt = {}
        test_submeters_list = list(test_submeters)
        for meter,data in test_submeters:
                concatenated_df_app = pd.concat(data,axis=1)
                index = concatenated_df_app.index
                gt[meter] = pd.Series(concatenated_df_app.values.flatten(),index=index)

        gt_overall = pd.DataFrame(gt, dtype='float32')
        pred = {}

        
        for app_name in concat_pred_df.columns:
            app_series_values = concat_pred_df[app_name].values.flatten()
            # Neural nets do extra padding sometimes, to fit, so get rid of extra predictions
            app_series_values = app_series_values[:len(gt_overall[app_name])]
            pred[app_name] = pd.Series(app_series_values, index = gt_overall.index)
            
        pred_overall = pd.DataFrame(pred,dtype='float32')
        
        return gt_overall, pred_overall