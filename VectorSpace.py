
import os
import re
import time
import math
import io


total_count = 0
word_map ={}
index_map = {}
original_position = {}

'''
This function adds all the tokens to the hashmap
Input : Each File data contents
Output : Hashmap contains token,count
'''
def add_map(data):
    global total_count  
    token = re.split("[^a-zA-Z0-9]", data)
    for word in token :
        word = word.lower()
        if len(word) >0:
            if word in word_map:
                val = word_map[word]
                word_map[word] = val +1
                total_count = total_count + 1
            else:
                word_map[word] = 1
                total_count = total_count + 1
            
'''
This function removes all the sgml tags and extracts the original text,
and it passes the text data to add_map function
Input : Each corpus data with SGML tags
'''
def process_file(all_files):
    i = 0
    for file in all_files:
        if file != '.DS_Store':
            original_position[file] = i
            i+=1
            file = "cranfield/" + file
            data=open(file,'r').read().replace('\n', ' ')
            start_pos = data.find("<TEXT>") + 6
            end_pos = data.find("</TEXT>")
            data = data[start_pos : end_pos]
            add_map(data)

'''
This helper function helps to print the search results
If the search query has more than 10 results, then it will print only top 10
'''
def top_words(word_map):
    sorted_x = sorted(word_map.items(), key=lambda x: x[1], reverse=True)
    file_length = len(sorted_x)
    if file_length > 11:
        file_length = 10
    for i in range(0,file_length):
        ans = sorted_x[i]
        ans = ans[0]
        print("Rank " + str(i+1) + ": Cranfield " + ans[9:])
    print("Number of Related documents:  " + str(len(sorted_x)))

'''
This function removes all the stop words from the token hashmap
'''    
def remove_stopwords_from_map(word_map,stop_words):
    global total_count
    for word in stop_words:
        if word in word_map:
            val = word_map[word]
            total_count = total_count - val
            del(word_map[word])
            

'''
This function builds the inverted index each word in the word map
word_map - Hashmap contains token after removing stop words
all_files : all file names(1400 files)
'''
def build_inverted_index(word_map, all_files):
    for file in all_files:
        file_name = file
        if file != '.DS_Store':
            file = "cranfield/" + file
            data=open(file,'r').read().replace('\n', ' ')
            start_pos = data.find("<TEXT>") + 6
            end_pos = data.find("</TEXT>")
            data = data[start_pos : end_pos]
            token = re.split("[^a-zA-Z0-9]", data)
            for word in token:
                if word in word_map:
                    if word in index_map:
                        val = index_map[word]
                        if file_name in val:
                            count = val[file_name] + 1
                            val[file_name] = count
                        else:
                            val[file_name] = 1
                        index_map[word] = val                       
                    else:
                        val = {file_name : 1}
                        index_map[word] = val
                
'''
This function takes search key words from the user,and create a rank map based on 
inverted index. It supports upto 3 keywords
'''         
        
def search_query(key_words):
    key_words = key_words.split(' ')
    #print(key_words)
    index_details = []
    rank_map = {}
    check = True
    for ke in key_words:
        if ke not in index_map:
            check = False
            print("Sorry, one your keyword is not found in our index map , please do a new search")
            break
    if len(key_words) == 1 and check:
        if key_words[0] in index_map:
            index_details.append(index_map[key_words[0]])
            for val in index_details[0].keys():
                rank_map[val] = index_details[0][val]
        else:
            print("Keyword not found")
    elif len(key_words) == 2  and check:
        index_details.append(index_map[key_words[0]])
        index_details.append(index_map[key_words[1]])
        set1 = set(index_details[0])
        set2 = set(index_details[1])
        file_name_list = []
        for file_name in set1.intersection(set2):
            file_name_list.append(file_name)
        for files in file_name_list:
            val1 = index_details[0][files]
            val2 = index_details[1][files]
            total_val = val1 + val2
            rank_map[files] = total_val
    elif len(key_words) == 3 and check:
        index_details.append(index_map[key_words[0]])
        index_details.append(index_map[key_words[1]])
        index_details.append(index_map[key_words[2]])
        set1 = set(index_details[0])
        set2 = set(index_details[1])
        set3 = set(index_details[2])
        file_name_list = []
        for file_name in set1.intersection(set2).intersection(set3):
            file_name_list.append(file_name)
        for files in file_name_list:
            val1 = index_details[0][files]
            val2 = index_details[1][files]
            val3 = index_details[2][files]
            total_val = val1+ val2 + val3
            rank_map[files] = total_val
    return rank_map

def generate_tfidf(all_files , position_map):
    tfidf = [[0]*1000 for n in range(1400)]
    i = -1
    for file in all_files:
        file_name = file
        if file != '.DS_Store':
            i +=1
            file = "cranfield/" + file
            data=open(file,'r').read().replace('\n', ' ')
            start_pos = data.find("<TEXT>") + 6
            end_pos = data.find("</TEXT>")
            data = data[start_pos : end_pos]
            token = re.split("[^a-zA-Z0-9]", data)
            stop_words = open("common_words.txt").read().split('\n')
            for s_word in stop_words:
                if s_word in token:
                    token.remove(s_word)
            for word in token:
                if word in position_map:
                    count_word = data.count(word)
                    tf = count_word / len(token)
                    idf = math.log(1400/len(index_map[word]),10)
                    tfidf[i][position_map[word]] = tf * idf
    with open("tfidf.txt", 'a') as out:
        out.write(str(tfidf))
    return tfidf
    
def transform_query_tfidf(query,position_map):
    query_tfidf = [0] * 1000
    token_query = query.split(' ')
    stop_words = open("common_words.txt").read().split('\n')
    for s_word in stop_words:
        if s_word in token_query:
            token_query.remove(s_word)
    for word in token_query:
        if word in position_map:
            count_word = query.count(word)
            tf = count_word / len(token_query)
            idf = math.log(1400/len(index_map[word]),10)
            query_tfidf[position_map[word]] = tf * idf
    return query_tfidf

def generate_results_t2(tfidf, query_tfidf):
    rank_map_t2 = {}
    j = 0
    for tfidf_row in tfidf:
        sum_val = 0
        tfidf_row_square = 0
        tfidf_query_square = 0
        #print("check")
        for i in range(0,len(tfidf_row)):
            sum_val = sum_val + tfidf_row[i] * query_tfidf[i]
            tfidf_row_square = tfidf_row_square + tfidf_row[i] * tfidf_row[i]
            tfidf_query_square = tfidf_query_square + query_tfidf[i] * query_tfidf[i]
        bottom  = math.sqrt(tfidf_row_square * tfidf_query_square)
        if bottom == 0:
            bottom = 1
        rank_map_t2[j] = sum_val / bottom
        j+=1
    return sorted(rank_map_t2.items(), key=lambda x: x[1], reverse=True)

def generate_results_t3(tfidf, query_tfidf, rank_map ):
    pos = []
    k = 0
    rank_map_t3 = {}
    for val in rank_map.keys():
        pos.append(original_position[val])
    #print(pos)
    for i in pos:
        sum_val = 0
        tfidf_row_square = 0
        tfidf_query_square = 0
        
        for j in range(0,len(tfidf[i])):
            sum_val = sum_val + tfidf[i][j] * query_tfidf[j]
            tfidf_row_square = tfidf_row_square + tfidf[i][j] * tfidf[i][j]
            tfidf_query_square = tfidf_query_square + query_tfidf[j] * query_tfidf[j]
        bottom = math.sqrt(tfidf_row_square * tfidf_query_square)
        if bottom == 0:
            bottom = 1
        rank_map_t3[i] = sum_val / bottom
        k+=1
    return sorted(rank_map_t3.items(), key=lambda x: x[1], reverse=True)
            

def process_results(query, tfidf):
    
    query_tfidf = transform_query_tfidf(query,position_map)
    start_time = time.time()
    result_2 = generate_results_t2(tfidf,query_tfidf)
    original_length_2 = 0
    for val in result_2:
        if val[1] >0:
            original_length_2+=1
            
    
    print("T2 Results")
    print("*************")
    if len(result_2) > 10:
        result_2 = result_2[0:10]
    i = 1
    for val in result_2:
        rank = val[0] + 1
        print( "Rank-" + str(i) + ": cranfield " + str(rank) + " : " + str(val[1]))
        i+=1
    print("---------------")
    print("Total number of related documents " + str(original_length_2) )
    print("---------------")
    
    i = 0
    avg_time_t2 = []
    while i <10:
        start_time = time.time()
        result_2_10times = generate_results_t2(tfidf,query_tfidf)
        avg_time_t2.append(time.time() - start_time)
        i+=1
    for t in avg_time_t2:
        print(t)
    print("Average Execution time T2 " + str(sum(avg_time_t2) / float(len(avg_time_t2))))
        
    rank_map = search_query(query)
    result_3 = generate_results_t3(tfidf,query_tfidf,rank_map)   
    original_length_3 = 0
    for val in result_3:
        if val[1] >0:
            original_length_3+=1
    if len(result_3) > 10:
        result_3 = result_3[0:10]
    print("T3 Results")
    print("*************")
    i = 1
    for val in result_3:
        rank = val[0] + 1
        print( "Rank-" + str(i) + ": cranfield " + str(rank) + " : " + str(val[1]))
        i+=1 
    print("---------------")
    print("Total number of related documents " + str(original_length_3) )
    print("---------------")
    i = 0
    avg_time_t3 = []
    while i <10:
        start_time = time.time()
        result_3_10times = generate_results_t3(tfidf,query_tfidf,rank_map)
        avg_time_t3.append(time.time() - start_time)
        i+=1
    for t in avg_time_t3:
        print(t)
    print("Average Execution time T3 " + str(sum(avg_time_t3) / float(len(avg_time_t3))))

folder_name = input("Please enter the folder name of your dataset ...  ")
all_files = os.listdir(folder_name)
process_file(all_files)
stop_words = open("common_words.txt").read().split('\n')
remove_stopwords_from_map(word_map,stop_words)

build_inverted_index(word_map, all_files)

top_1000_tuple =sorted(word_map.items(), key=lambda x: x[1], reverse=True)
top_1000_words = []
position_map = {}
for i in range(0,1000):
    key_word = top_1000_tuple[i][0]
    top_1000_words.append(key_word)
    position_map[key_word] = i

tfidf =generate_tfidf(all_files, position_map )


check = True
while check:
    query = input("please enter your search query...")
    process_results(query, tfidf)
    con = input("Do you want to continue : Y/N ?....")
    if con == "n"  or con =="N":
        check = False