#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Library

import json
import pandas as pd
import re


# ### Get Only ApiCall Log

# In[2]:


# Show Row Data
path_file = "../log_file/LuckyLocker.log"
with open(path_file) as log_report:
    log_splitted = []
                
    for log in log_report:
        splited = log.split('\t')
        splited.pop(5)

        dict = {"timestamp" : splited[0],"process" : splited[1],"pid" : splited[2],"tid" : splited[3],"type" : splited[4], "value" : splited[5],}
        log_splitted.append(dict)


# In[3]:


df_log = pd.DataFrame(log_splitted)
# df_log


# In[4]:


# Check The Type equal to ApiCall (U)
log_api = []

for log in log_splitted:
   if (log['type'] == 'ApiCall (U)' and 'Executing' not in log['value'] and 'WerFault.exe' not in log['process']):
    log_api.append(log)
    
df_split_log = pd.DataFrame(log_api)
df_split_log.to_csv("splitted.csv")


# In[5]:


# df_split_log


# ### Splitting Log Report

# In[6]:


#Splitting value column 
apicall_list= []
return_value_list = []

# Check if return value exist
semicolon_delimiter = ';'

for value in df_split_log['value']:
    data_split = value.split(semicolon_delimiter)
        
    #store to dictionary
    apicall_list.append(data_split[0])
    
    if len(data_split) >1:
        return_value_list.append(data_split[1])
    else:
        return_value_list.append('null')


# In[7]:


# Log Report Dictionary
log_dct = {
    'apicall' : apicall_list,
    'return_value' : return_value_list
}


# In[8]:


df_log_report = pd.DataFrame(log_dct)

# df_log_report


# ### Splitting ApiCall Log

# In[9]:


apicall_splitted = []

for value in df_log_report['apicall']:
    splitted = value.split('(', 1)
    apicall_splitted.append(splitted)


# In[10]:


apicall_splitted[1]


# In[11]:


list_api = []
list_argument = []

for value in df_log_report['apicall']:
    delete_last_chr = re.sub(".$", '', value)
    split_value = delete_last_chr.split('(', 1)
    list_api.append(split_value[0])
    list_argument.append(split_value[1])


# In[12]:


apicall_dct = {
    'api' : list_api,
    'argument' : list_argument
}


# In[13]:


df_apicall = pd.DataFrame(apicall_dct)
# df_apicall


# ### Splitting Argument

# In[14]:


split_argument = []

for arg in df_apicall['argument']:
    splitted = arg.split(',')
    split_argument.append(splitted)


# In[15]:


# split_argument


# In[16]:


# # Check longest argument
# for arg in split_argument: 
#     print("Number of Arf : " + str(len(arg)))


# In[17]:


# Check longest argument
def longest(list):
    longest_list = max(len(arg) for arg in list)
    return longest_list


# In[18]:


print("The longest arg : " + str(longest(split_argument)) + " arguments")


# In[19]:


arg_dict = {}
longest_arg = longest(split_argument)

for i in range(longest_arg):
    index_name = 'argument ' + str(i + 1)
    arg_dict[index_name] = []

arg_dict


# In[20]:


#Check Every Argument
for i in split_argument:
#     import pdb;pdb.set_trace()
    for j in range(longest_arg):
        index_name = 'argument ' + str(j + 1)
        if len(i) > j: 
            arg_dict[index_name].append(i[j])
        else:
            arg_dict[index_name].append('null')
            


# In[21]:


for i in arg_dict.values():
    print(len(i))


# In[22]:


df_argument = pd.DataFrame(arg_dict)
# df_argument

# arg_dict


# In[23]:


# Join all dataframe
df_temp = df_split_log.drop(['value'], axis=1).join(df_apicall.drop(['argument'], axis=1)).join(df_argument).join(df_log_report['return_value'])


pd.set_option("display.max_rows", None, "display.max_columns", None)

log_report_csv = pd.DataFrame(df_temp)
log_report_csv.to_csv('../csv_file/log_report.csv')


# In[24]:


# log_report_csv[:10]


# In[25]:


print(log_report_csv['api'][0])
log_report_csv.columns


# In[26]:


log_report_csv = log_report_csv[:4000]


# # Parser

# In[27]:


# log_report_csv


# In[28]:


# fill null wit nothing
log_report_csv = log_report_csv.replace('null', 'Nothing', regex=True)


# In[29]:


# log_report_csv


# In[30]:


print(log_report_csv['argument 1'][0])


# In[31]:


# Create Dictionary
sequence_dict = {
    'sequence' : [],
    'api start' : [],
    'api list' : [],
    'which argument' :[],
    'which argument index' : []
}
total_argument = longest_arg


# In[32]:


index = 0
seq = 1
for api in log_report_csv['api']:
#     index = 0
    api_list = []
    arg_list = []
    arg_index_list = []
#     api_list.append(api)
#     print(api_list)
#     print(api)
    for args in range(total_argument):
        arg = log_report_csv['argument ' + str(args+1)][index]
#         print('=============== Position in ', arg, '===========')
        if arg == 'Nothing':
#             print('arg is "nothing", continue')
#             index += 1
            continue
        for i in range(len(log_report_csv['argument 1'])):
    #         print(i+1)
            if i < index:
#                 print('index', i+1, 'continue')
                continue
    #         print(arg , log_report_csv['argument 1'][i])
            for j in range(total_argument):
#                 print('argument ' + str(j+1))
#                 print(arg, 'compare with', log_report_csv['argument ' + str(j+1)][i])
                if log_report_csv['argument ' + str(j+1)][i]=='Nothing':
    #                 print('NOTHING nih ngab')
                    continue
                if arg==log_report_csv['argument ' + str(j+1)][i]:
                    api_list.append(log_report_csv['api'][i])
                    arg_list.append('argument ' + str(j+1))
                    arg_index_list.append(i)
#                     print('SAME value')
#     #                 print(api_list)
#                 else:
#                     print('UNEQUAL value')
            if i+1 ==len(log_report_csv['argument 1']):
#                 print('stuck')
#                 print('sequence :',seq)
#                 print('api_start :', api)
#                 print('api :', api_list)
                sequence_dict['sequence'].append(('sequence ' + str(seq)))
                sequence_dict['api start'].append(api)
                sequence_dict['api list'].append(api_list)
                sequence_dict['which argument'].append(arg_list)
                sequence_dict['which argument index'].append(arg_index_list)
                api_list = []
                arg_list = []
                arg_index_list = []
#                 api_list.append(api)
    seq+=1
    index += 1


# In[35]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

df = pd.DataFrame(sequence_dict)


# In[36]:


df[['sequence','api list']]


# In[37]:


df[['sequence','api list']].to_csv('api sequence.csv')


# In[ ]:




