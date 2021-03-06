# Author：马肖
# E-mail：maxiaoscut@aliyun.com
# Github：https://github.com/Albertsr

# 出处：蚂蚁金服-风险大脑-支付风险识别大赛(第一赛季) 
# https://dc.cloud.alipay.com/index#/topic/data?id=4
# TPR1：当FPR等于0.001时的TPR; TPR2：当FPR等于0.005时的TPR; TPR3：当FPR等于0.01时的TPR
# 模型成绩 = 0.4 * TPR1 + 0.3 * TPR2 + 0.3 * TPR3


import numpy as np
from sklearn.metrics import confusion_matrix, make_scorer

def weighted_coverage(y_true, y_prob, thresholds_num=1000):    
    thresholds = np.linspace(np.min(y_prob), np.max(y_prob), thresholds_num)
    
    # get_tpr_fpr根据给定的阈值，返回TPR、FPR
    def get_tpr_fpr(threshold):
        y_pred = np.array([int(i > threshold) for i in y_prob])
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        tpr = tp / (tp + fn)
        fpr = fp / (fp + tn)
        return tpr, fpr
    
    # 根据不同的阈值生成对应的一系列TPR、FPR
    # sklearn.metrics自带的roc_curve返回的tprs, fprs个数较少，最终的加权覆盖率不精准，不予采纳
    tprs, fprs = np.vectorize(get_tpr_fpr)(thresholds)    
    
    # min_delta_index返回与target_fpr最接近的阈值索引
    def min_delta_index(target_fpr):
        delta = np.array([np.abs(fpr - target_fpr) for fpr in fprs])
        return np.argmin(delta)
    
    # 获取FPR与目标值0.001、0.005、0.01最接近时对应的索引及其对应的TPR
    min_indices = [min_delta_index(i) for i in [0.001, 0.005, 0.01]]
    target_tprs = np.array([tprs[index] for index in min_indices])
    
    # 获取最终的加权TPR
    weights = np.array([0.4, 0.3, 0.3])
    return np.dot(weights, target_tprs)
