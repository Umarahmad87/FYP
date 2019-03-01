
# coding: utf-8

# In[1]:


from PIL import Image
import numpy as np
import cv2
#import matplotlib.pyplot as plt

# In[2]:


def consecutive_points(arr):
    #print('arr:',arr)
    c_points = np.where(arr==255)[0]
    if(len(c_points)==0):
        c_points = [0]
    #print('c_points:',c_points)
    temp = c_points[0]-1
    new_point = []
    #print(c_points)
    arr_c = []
    for val in c_points:
        #print(val)
        
        if val==temp+1:
            arr_c.append(val)
        else:
            if(len(arr_c)>0):
                yield (int(np.mean(arr_c)),len(arr_c))
                #new_point.append((int(np.mean(arr_c)),len(arr_c)))
            arr_c = []
        temp = val
    #return new_point
def all_data_yeild(img_arr):
    i=0
    while i<len(img_arr):
        a1 = consecutive_points(img_arr[i])
        ap = []
        for val in a1:
            ap.append(val)
        yield ap
        i+=1

#img_arr = img_arr.T
def detect_doors(q):
    while True:
        try:
            img_arr = q.get()
            if(img_arr=="quit"):
                break
            img_arr[img_arr<=254]=0
            all_d = all_data_yeild(img_arr)
            all_val = []
            j = 0
            for val in all_d:
                val2 = list(map(lambda x:x[1],val))

                if(len(val2)>0):
                    all_val.append((val[np.argmax(val2)][0],val[np.argmax(val2)][1],j))
                else:
                    all_val.append(( 0,0,j))
                j+=1


            #print(all_val)
            dist_limit = 70
            all_indexes = np.where(np.array(np.array(list(map(lambda x:x[1],all_val))))>dist_limit)[0]
            try:
                index1 = all_indexes[0]
                index2 = all_indexes[-5]
                #print(index1)
                #print(index2)
                img_arr[all_val[index1][2]][all_val[index1][0]-int(all_val[index1][1]/2):all_val[index1][0]+int(all_val[index1][1]/2) ] = 155
                img_arr[all_val[index2][2]][all_val[index2][0]-int(all_val[index2][1]/2):all_val[index2][0]+int(all_val[index2][1]/2) ] = 155

                index3=index1
                index4=index2
            except:
                index3= 0
                index4= 0



            img_arr = img_arr.T
            all_d = all_data_yeild(img_arr)
            all_val = []
            j = 0
            #print(all_d)
            for val in all_d:
                val2 = list(map(lambda x:x[1],val))

                if(len(val2)>0):
                    all_val.append((val[np.argmax(val2)][0],val[np.argmax(val2)][1],j))
                else:
                    all_val.append(( 0,0,j))
                j+=1

            #print(all_val)
            dist_limit = 100
            all_indexes = np.where(np.array(np.array(list(map(lambda x:x[1],all_val))))>dist_limit)[0]
            try:
                index1 = all_indexes[0]
                index2 = all_indexes[-5]
                #print(index1)
                #print(index2)
                img_arr[all_val[index1][2]][all_val[index1][0]-int(all_val[index1][1]/2):all_val[index1][0]+int(all_val[index1][1]/2) ] = 155
                img_arr[all_val[index2][2]][all_val[index2][0]-int(all_val[index2][1]/2):all_val[index2][0]+int(all_val[index2][1]/2) ] = 155
            except:
                index1 = 0
                index2 = 0 
            img_arr = img_arr.T
            rgb = cv2.cvtColor(img_arr,cv2.COLOR_GRAY2RGB)
            img_rgb=Image.fromarray(rgb)
            rowcol = np.where(rgb[:,:,1]==155)
            rgb[rowcol] = [255,0,0]
            img2=Image.fromarray(rgb)
            #plt.imshow(rgb)
            cv2.imshow('doors', rgb)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #cv2.waitKey(0)
            img2.save('my.png')
        except Exception as e:
            print(e)
            break