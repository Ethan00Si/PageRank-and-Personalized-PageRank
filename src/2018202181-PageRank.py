import time


def read_file(dataFilename):
    linkOut = {} #临接链表 从head结点指向tail结点

    nodes = {} #存储所有结点 之后用于初始化
    with open(dataFilename) as file:
        for line in file:
            head, tail = [str(x) for x in line.strip().split(',')]
            if not nodes.__contains__(tail):
                nodes[tail] = 0
            if not linkOut.__contains__(head):
                linkOut[head] = []
                nodes[head] = 0
            linkOut[head].append(tail)

    return linkOut, nodes


def deadEnds(link_dict, pagelist):
    '''
    返回所有dead end构成的列表
    dead end是只有入度没有出度的页面
    '''
    dead_end_list = list()

    for each_page in pagelist.keys():
        if each_page not in link_dict.keys():
            dead_end_list.append(each_page)
    return dead_end_list


def mypagerank(link_dict, pagelist, dead_end_list, beta=0.85):
    #迭代计算  时间复杂度为O(V+E)

    n_pages = len(pagelist)  # 页面总数

    r_old = dict()
    r_new = dict()
    for each_page in pagelist.keys():
        r_old[each_page] = 1/n_pages
    convergence = False
    count = 0
    while not convergence:
        dead_end_sum = 0.0
        for each_end in dead_end_list:
            dead_end_sum += beta * r_old[each_end] / n_pages

        # 初始化 r_new
        for each_page in pagelist.keys():
            r_new[each_page] = (1 - beta) / n_pages + dead_end_sum
        for src in link_dict.keys():
            dest_list = link_dict[src]
            src_out_degree = len(dest_list)
            for each_dest in dest_list:
                r_new[each_dest] += beta * r_old[src] / src_out_degree
        #判断是否converge
        err = 0
        threshold = 10e-6
        for each_page in pagelist.keys():
            err += abs(r_old[each_page] - r_new[each_page])
        for each_page in pagelist.keys():
            r_old[each_page] = r_new[each_page]
        convergence = err < threshold
        count += 1
        #print('iteration: ', count, end='\r')
    #print('total iterations: ', count)
    return r_new


def PageRank(input_file_name, damping_factor):
    # PageRank入口
    links, pages = read_file(input_file_name)
    deadends = deadEnds(links, pages)
    #startTime = time.time()
    ranks = mypagerank(links, pages, deadends, damping_factor)
    #print("Calculation costs time: ", time.time() - startTime, ' secs')
    top = sorted(ranks.items(), key=lambda x: (x[1],x[0]), reverse=True)[:10]
    top = [x[0] for x in top]
    return top
    


def init_seed(input_seed, pages):
    # 读入种子文件
    nodes = {}
    with open(input_seed, 'r') as fin:
        for line in fin:
            node_id, prob = line.strip().split(',')
            nodes[node_id] = float(prob)
    
    for item in pages.keys():
        if not nodes.__contains__(item):
            nodes[item] = 0.0
    
    return nodes


def myPPR(link_dict, pagelist, dead_end_list, beta, input_seed, max_iter=1000):
    # PPR 迭代计算部分
    r_old = dict()
    r_init = dict()
    r_new = dict()
    r_old = input_seed.copy()
    convergence = False
    count = 0
    for item in input_seed.keys():
        r_init[item] = (1 - beta) * input_seed[item]
    n_pages = len(pagelist)

    while not convergence:
        dead_end_sum = 0.0
        for each_end in dead_end_list:
            dead_end_sum += beta * r_old[each_end] 
        dead_end_sum = dead_end_sum / n_pages
        
        # 初始化 r_new
        r_new = r_init.copy()
        # 考虑到存在dead end 需要将他们随机分配给每个page 以此保证p的各个维度之和为1
        for item in r_new.keys():
            r_new[item] += dead_end_sum
        for src in link_dict.keys():
            dest_list = link_dict[src]
            src_out_degree = len(dest_list)
            for each_dest in dest_list:
                r_new[each_dest] += beta * r_old[src] / src_out_degree 

        err = 0
        threshold = 10e-6

        for each_page in pagelist.keys():
            err += abs(r_new[each_page]-r_old[each_page])
        convergence = err < threshold

        r_old = r_new.copy()

        count += 1
        if count > max_iter:
            break
        #print('count: ', count, end='\r')
        
    #print('total iterations: ', count)
    return r_new


def PPR(input_graph, input_Seed, damping_factor):
    links, pages = read_file(input_graph)
    deadends = deadEnds(links, pages)
    
    nodes = init_seed(input_Seed, pages)
    #startTime = time.time()
    ranks = myPPR(links, pages, deadends, damping_factor, nodes)
    #print("Calculation costs time: ", time.time() - startTime, ' secs')
    top = sorted(ranks.items(), key=lambda x: (x[1],x[0]), reverse=True)[:10]
    top = [x[0] for x in top ]
    return top

'''
if __name__ == '__main__':
    #startTime = time.time()
    list_10  = PageRank('../input.txt',0.85)
    #print(list_10)
    #list_10 = PPR('../input.txt', '../seeds.txt', 0.85)
    list_10 = list_10
    print(list_10)
'''
