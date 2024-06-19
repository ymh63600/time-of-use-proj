from nilmtk.seq2point import Seq2Point
from nilmtk.rnn import RNN
from nilmtk.WindowGRU import WindowGRU
from nilmtk.dae import DAE
from nilmtk import DataSet
from nilmfunc import preprocess,predict
from tensorflow.keras.models import load_model
import pandas as pd
from config import Config_Time

def pred(test_path, time):

    test = DataSet(test_path)

    building = 1
    power = {'mains': ['apparent'],'appliance': ['active']}
    appliances = ['fridge','dish washer','light','microwave','electric oven','sockets','electric space heater','electric stove']
    sample_period = 60
    

    model1 = load_model("model/windowgru-temp-weights-fridge-final.h5")
    model2 = load_model("model/rnn-temp-weights-dish_washer-final.h5")
    model3 = load_model("model/dae-temp-weights-light-final.h5")
    model4 = load_model("model/seq2point-temp-weights-microwave-final.h5")
    model5 = load_model("model/seq2point-temp-weights-electric_oven-final.h5")
    model6 = load_model("model/seq2point-temp-weights-sockets-final.h5")
    model7 = load_model("model/seq2point-temp-weights-electric_space_heater-final.h5")
    model8 = load_model("model/seq2point-temp-weights-electric_stove-final.h5")

    appliance_params = {'fridge': {'mean': 209.1253, 'std': 65.182846},
                        'dish washer': {'mean': 0.09603385, 'std': 4.3867},
                        'light': {'mean': 0.7303633, 'std': 9.639374},
                        'microwave': {'mean': 0.0, 'std': 100},
                        'electric oven': {'mean': 139.02312, 'std': 752.4712},
                        'sockets': {'mean': 0.22585046, 'std': 7.018574},
                        'electric space heater': {'mean': 294.91782, 'std': 40.08285},
                        'electric stove': {'mean': 134.78987, 'std': 110.01223}}
    
    pred_overall={}
    gt_overall={}
    
    models = {'fridge': model1}
    classifiers ={'WindowGRU':WindowGRU({}),}
    for name,clf in classifiers.items():
        
        test_mains, test_submeters = preprocess(time,test,appliances,power, building, sample_period)
        gt_overall,overall = predict(clf,test_mains, test_submeters,models,appliance_params)
        pred_overall.update(overall)
    
    classifiers ={'RNN':RNN({})}
    models = {'dish washer': model2,}        
    for name,clf in classifiers.items():

        test_mains, test_submeters = preprocess(time,test,appliances,power, building, sample_period)
        gt_overall,overall = predict(clf,test_mains, test_submeters,models,appliance_params)
        pred_overall.update(overall)
    
    classifiers = {'DAE':DAE({})}
    models = {'light': model3,}        
    for name,clf in classifiers.items():

        test_mains, test_submeters = preprocess(time,test,appliances,power, building, sample_period)
        gt_overall,overall = predict(clf,test_mains, test_submeters,models,appliance_params)
        pred_overall.update(overall)
    
    classifiers = {'Seq2Point':Seq2Point({})}
    models = {
        'microwave': model4, 
        'electric oven': model5,
        'sockets': model6,
        'electric space heater': model7, 
        'electric stove': model8,
    }
    for name,clf in classifiers.items():

        test_mains, test_submeters = preprocess(time,test,appliances,power, building, sample_period)
        gt_overall,overall = predict(clf,test_mains, test_submeters,models,appliance_params)
        pred_overall.update(overall)
    
    return gt_overall,pred_overall

def create_csv(path, time):

    pred_overall={}
    gt_overall={}

    path = path
    time = time

    gt_overall, pred_overall = pred(path,time)
    
    df = pd.DataFrame(pred_overall)
    df.to_csv(f"pred_csv/{time['start_time']}_{time['end_time']}.csv")


if __name__ == '__main__':
    create_csv(Config_Time.testpath,Config_Time.time)
    