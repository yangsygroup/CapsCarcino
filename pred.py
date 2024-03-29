import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix
import input_data
import math
def eva(pre, true):
    matrix = confusion_matrix(true, pre, labels=[1, 0])
    TP = matrix[0][0]
    TN = matrix[1][1]
    FP = matrix[1][0]
    FN = matrix[0][1]
    SE = 1.0*  TP  / (TP + FN)
    SP = 1.0 * TN / (TN + FP)
    MCC = (TP * TN - FP * FN) / math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))
    ACC = 1.0*(TP + TN) / (TP + TN + FP + FN)
    return TP, TN, FP, FN, SE, SP, MCC,ACC
def runModel(arr,model_path):
    ckpt = tf.train.get_checkpoint_state(model_path)
    saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
    with tf.Session() as sess:
        saver.restore(sess,ckpt.model_checkpoint_path)
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("Placeholder:0")
        y_pred = graph.get_tensor_by_name("Masking/ToInt32:0")
        pred = []
        submit = np.concatenate((arr, np.zeros(shape=[148-arr.shape[0],arr.shape[1]])),0)
        y = sess.run(y_pred, feed_dict = {x: submit})
        y = y.tolist()[0:arr.shape[0]]
        pred += y

    return pred
if __name__ == '__main__':
    train_datadir = "data_set"
    setFileNames = ['train.csv', 'EV.csv', 'EV.csv']
    data = input_data.read_data_sets(train_datadir, setFileNames=setFileNames, one_hot=False)
    trX, trY, teX, teY, vaX, vaY = data.train.images, data.train.labels, data.test.images, \
                                   data.test.labels, data.validation.images, data.validation.labels
    model_path = './model_path/'
    pred_y = runModel(teX, model_path)
    TP, TN, FP, FN, SE, SP, MCC, ACC = eva(pred_y, teY)
    print('test : TP:%.3f;   TN:%.3f;      FP:%.3f;      FN:%.3f;  SE:%.3f  SP:%.3f   MCC:%.3f P:%.3f'%(TP, TN, FP, FN, SE, SP, MCC, ACC ))

