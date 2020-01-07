
def get_features(feature_set, n_features = 10,  total = 10):
    set_to_return = list()
    if n_features == 1:
        set_to_return = [[feature_set[i]] for i in range(total)]
    elif n_features == 2:
        set_to_return = [[feature_set[i], feature_set[j]] for i in range(total) for j in range(i+1,total)]
    elif n_features == 3:
        set_to_return = [[feature_set[i], feature_set[j], feature_set[k]] for i in range(total) for j in range(i+1,total) for k in range(j+1,total)]
    elif n_features == 4:
        set_to_return = [[feature_set[i],feature_set[j],feature_set[k],feature_set[l]] for i in range(total) for j in range(i+1,total) for k in range(j+1,total) for l in range(k+1,total)]
    elif n_features == 5:
        set_to_return = [[feature_set[i],feature_set[j],feature_set[k],feature_set[l],feature_set[m]] for i in range(total) for j in range(i+1,total) for k in range(j+1,total) for l in range(k+1,total) for m in range(l+1,total)]    
    elif n_features == 6:
        set_to_return = [[feature_set[i],feature_set[j],feature_set[k],feature_set[l],feature_set[m], feature_set[n]] for i in range(total) for j in range(i+1,total) for k in range(j+1,total) for l in range(k+1,total) for m in range(l+1,total) for n in range(m+1,total)]    
    elif n_features == 7:
        set_to_return = [[feature_set[i],feature_set[j],feature_set[k],feature_set[l],feature_set[m], feature_set[n], feature_set[o]] for i in range(total) for j in range(i+1,total) for k in range(j+1,total) for l in range(k+1,total) for m in range(l+1,total) for n in range(m+1,total) for o in range(n+1, total)]    
    elif n_features == 8:
        set_to_return = [[feature_set[i],feature_set[j],feature_set[k],feature_set[l],feature_set[m], feature_set[n], feature_set[o], feature_set[p]] for i in range(total) for j in range(i+1,total) for k in range(j+1,total) for l in range(k+1,total) for m in range(l+1,total)  for n in range(m+1,total) for o in range(n+1, total) for p in range(o+1, total)]    
    elif n_features == 9:
        set_to_return = [[feature_set[i],feature_set[j],feature_set[k],feature_set[l],feature_set[m], feature_set[n], feature_set[o], feature_set[p], feature_set[q]] for i in range(total) for j in range(i+1,total) for k in range(j+1,total) for l in range(k+1,total) for m in range(l+1,total)  for n in range(m+1,total) for o in range(n+1, total) for p in range(o+1, total) for q in range(p+1, total)]
    elif n_features == 10:
        set_to_return = [feature_set[i] for i in range(total)]
    return set_to_return