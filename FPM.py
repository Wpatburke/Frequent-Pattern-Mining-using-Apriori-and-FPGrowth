import numpy as np 
#from StringIO import StringIO
import re
import itertools


#Find Frequent Itemsets
def Apriori(data,min_sup):

    
	EachCandidate = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	CountOfEachCandidate = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
	Class = ['Age:','Workclass:','fnlwgt:','Education','EducationNum:','MaritialStatus:','Occupation:','RelationShip:','Race:','Sex:','Capitol-Gain:','Capitol-Loss:','HoursPerWeeks:','Native-Country:','Salary:']
	count = 0 

	D = []

	for row in data:
		count = count + 1
		pattern = re.compile("^\s+|\s*,\s*|\s+$")
		row = ([x for x in pattern.split(row) if x])
		row[0] = int(row[0])/10
		D.append(row)
		for i in range(0,len(row)):
			if i == 2: 
				continue
			if i == 10: 
				continue
			if i == 11: 
				continue
			if row[i] in EachCandidate[i]:
				for k in range(len(EachCandidate[i])):
					if row[i] == EachCandidate[i][k]:
						CountOfEachCandidate[i][k] = CountOfEachCandidate[i][k] + 1
				if len(EachCandidate) == 0:
					EachCandidate[i].append(row[i])
			else:
				EachCandidate[i].append(row[i])
				CountOfEachCandidate[i].append(1)

	# print CountOfEachCandidate
	# print("")
	# print EachCandidate
	# print("")

	i = 0
	j = 0

	#print count

	while i < len(CountOfEachCandidate):
		while j < len(CountOfEachCandidate[i]):
			#print len(CountOfEachCandidate[i])
			if((CountOfEachCandidate[i][j]/float(count)) < min_sup):
				CountOfEachCandidate[i].pop(j)
				EachCandidate[i].pop(j)
				j=-1
			j = j + 1
		j = 0
		i = i + 1


	# print CountOfEachCandidate
	# print("")
	# print EachCandidate

	L1 = []
	i = 0
	j = 0

	while i < len(CountOfEachCandidate):
		#print len(CountOfEachCandidate[i])
		if len(CountOfEachCandidate[i]) == 0:
			CountOfEachCandidate.pop(i)
			EachCandidate.pop(i)
			Class.pop(i)
		i = i + 1

	#while i < len(CountOfEachCandidate):
	#	while j < len(CountOfEachCandidate[i]):
	#		j = j + 1
	#	i = i + 1

	print("======================================================================")
	print "min count:", min_sup * count
	#print "CountOfEachCandidate: ", CountOfEachCandidate
	print("")
	#print "EachCandidate",EachCandidate

	i = 0
	j = 0

	while i < len(CountOfEachCandidate):
		while j < len(CountOfEachCandidate[i]):
			#print i
			value = str(EachCandidate[i][j])  #str(Class[i]) + str(EachCandidate[i][j])
			L1.append(value)
			j = j + 1
		j = 0
		i = i + 1
	print("")
	print "L1: ", L1
	L1Count = []
	for i in CountOfEachCandidate:
		if len(i) != 0:
			L1Count.append(i)

	print "L1Count:",L1Count
	print len(L1Count)

	def GenerateFrequentTwoItems(L1):
		L2=[]
		i = 0
		j = 1
		while i < len(L1):
			while j < len(L1):
				L2.append([L1[i],L1[j]])
				j = j + 1
			i = i + 1
			j = i + 1
		return L2


	def ScanAndCount(D,L2,L2Count):
		for row in D:
			i = 0
			while i < len(L2):
				if (L2[i][0] in row) and (L2[i][1]):
					L2Count[i] = L2Count[i] + 1
				i = i + 1
		return L2Count

	def Scan(D,Li):
		
		Licount = [0] * len(Li)
		LiTruthValue = []
		#print LiTruthValue
		#InThere = True
		i=1
		j=0
		for row in D:
			#LiTruthValue = [[]]*len(Li)
			i = 0
			j = 0
			while i < len(Li):
				LiTruthValue = []
				while j < len(Li[i]):
					if Li[i][j] in row:
						LiTruthValue.append(1)
						#print"Li[i]:", Li[i][j]
						#LiTruthValue[i].append(1)
						#print LiTruthValue
					else:
						LiTruthValue.append(0)
					
					j = j + 1
				j = 0
				if all(LiTruthValue) == True:
					Licount[i] += 1
				i = i + 1
		return Licount




	L2 = GenerateFrequentTwoItems(L1)

	#print "C2: ", L2
	L2Count = [0]*len(L2)

	#print "C2Count: ",L2Count
	L2Count = ScanAndCount(D,L2,L2Count)
	#print "ScanAndCount(D,L2,L2Count): ", ScanAndCount(D,L2,L2Count)


	def Prune(L2, L2Count, min_sup):
		i = 0
		while i < len(L2Count):
			if (L2Count[i]/float(count) < min_sup):
				L2Count.pop(i)
				L2.pop(i)
				i = -1
			i = i + 1
		return L2, L2Count

	L2, L2Count = Prune(L2,L2Count,min_sup)


	print("")
	print "L2: ", L2
	print "L2Count: ", L2Count
	print("")
	print len(L2)

	L2Copy = L2 
	

	def GenerateFrequentItemSets(L2Copy):
		C3 = []
		AlreadyGenerated=[]
		i = 0
		k = -1
		while i < len(L2Copy): # -1
			
			while k < len(L2Copy):
				j = -1
				k = k + 1
				if k == i or k == len(L2Copy):
					continue

				
				while j < len(L2Copy[i])-1:
					j = j + 1
					if j == len(L2Copy[i])-1:
						continue
					#print i,k, j
					if L2Copy[i][j] == L2Copy[k][j]:
						if [i,k] in AlreadyGenerated:
							continue
						#print k
						if L2Copy[k][-1] in L2Copy[i]:
							continue
						C3.append(L2Copy[i]+[L2Copy[k][-1]])
						AlreadyGenerated.append([k,i])
			k = -1
			i = i + 1
			#L2Copy.pop(i)
		return C3

	sets = 1
	Li = L2Copy
	i = 3

	while sets != 0:
		Ci = GenerateFrequentItemSets(Li)
		CiCount = Scan(D,Ci)
		Li,Licount = Prune(Ci,CiCount,min_sup)
		if len(Li)==0:
			break
		print "L",i,":", Li
		print "L",i,"count:", Licount
		print("")
		sets = len(Li)
		print sets
		i = i + 1



class Node(object):

    def __init__(self, data, frequency, parent):

        self.data = data
        self.frequency = frequency
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, data):
        for node in self.children:
            if node.data == data:
                return True

        return False

    def add_parent(self,obj):
        self.parent = obj
        return None

    def get_child(self, data):
        for node in self.children:
            if node.data == data:
                return node

        return None

    def set_frequency(self,obj):
        self.frequency = obj
        return None

    def add_child(self, data):
        child = Node(data, 1, self)
        self.children.append(child)
        return child


class FPTree(object):

    def __init__(self, transactions, threshold, root_value, root_count):
        self.obj = self.FirstScan(transactions, threshold)
        self.basket = self.basket(self.obj)
        self.root = self.build_FPTree(transactions, root_value, root_count, self.obj, self.basket)

    def FirstScan(self, transactions, threshold):
        items = {}
        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        for item in items.keys():
            if items[item] < threshold:
                del items[item]

        return items

    def basket(self, obj):
        basket = {}
        for key in obj.keys():
            basket[key] = None

        return basket

    def build_FPTree(self, transactions, root_value,root_count, obj, basket):

        root = Node(root_value, root_count, None)

        for transaction in transactions:
            sorted_items = [x for x in transaction if x in obj]
            sorted_items.sort(key=lambda x: obj[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, basket)

        return root

    def mine_FrequentItemsets(self, threshold):

        Itemsets = {}
        mining = sorted(self.obj.keys(),
                              key=lambda x: self.obj[x])

        for item in mining:
            tempes = []
            conditional_tree_input = []
            node = self.basket[item]

            while node is not None:
                tempes.append(node)
                node = node.link


            for temp in tempes:
                frequency = temp.frequency
                path = []
                parent = temp.parent

                while parent.parent is not None:
                    path.append(parent.data)
                    parent = parent.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)


            subtree = FPTree(conditional_tree_input, threshold,
                             item, self.obj[item])
            FrequentItemsets = subtree.mine(threshold)

            for Itemset in FrequentItemsets.keys():
                if Itemset in Itemsets:
                    Itemsets[Itemset] = Itemsets[Itemset] + FrequentItemsets[Itemset]
                else:
                    Itemsets[Itemset] = FrequentItemsets[Itemset]

        return Itemsets


    def Prune(L2, L2Count, min_count):
        i = 0
        #print "min_count", min_count
        while i < len(L2Count):
            #print "L2Count", L2Count[i]
            #print "L2", L2[i]
            if (L2Count[i]< min_count):
                L2Count.pop(i)
                L2.pop(i)
                i = -1
            i = i + 1
        return L2, L2Count

    def insert_tree(self, items, node, basket):

        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.frequency += 1
        else:
            child = node.add_child(first)


            if basket[first] is None:
                basket[first] = child
            else:
                current = basket[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, basket)

    def treeIsStraight(self, node):

        number_of_children = len(node.children)
        if number_of_children > 1:
            return False
        elif number_of_children == 0:
            return True
        else:
            return True and self.treeIsStraight(node.children[0])

    def index(value, List):
        found = 0
        i = 0
        while i < len(List):
            if value == List[i]:
                break
            i = i + 1
        if i == 223:
            return 222
        return i

    def mine(self, threshold):

        if self.treeIsStraight(self.root):
            return self.generate()
        else:
            return self.Itemsets(self.mine_FrequentItemsets(threshold))

    def Itemsets(self, Itemsets):

        temp = self.root.data

        if temp is not None:
            new_Itemsets = {}
            for key in Itemsets.keys():
                new_Itemsets[tuple(sorted(list(key) + [temp]))] = Itemsets[key]

            return new_Itemsets

        return Itemsets

    def generate(self):

        Itemsets = {}
        items = self.obj.keys()

        if self.root.data is None:
            temp_value = []
        else:
            temp_value = [self.root.data]
            Itemsets[tuple(temp_value)] = self.root.frequency

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                Itemset = tuple(sorted(list(subset) + temp_value))
                Itemsets[Itemset] = \
                    min([self.obj[x] for x in subset])

        return Itemsets


def sort(M,N):
    swaps = 1
    CompleteList = M
    CompleteListCount = N

    while swaps != 0 :
        i = 0
        swaps = 0
        while i < len(CompleteListCount)-1:
            a = CompleteListCount[i]
            b = CompleteListCount[i+1]

            c = CompleteList[i]
            d = CompleteList[i+1]
            
            if a < b:
                holder = a
                CompleteListCount[i] = b
                CompleteListCount[i+1] = a

                holder = c
                CompleteList[i] = d
                CompleteList[i+1] = c

                swaps = swaps + 1
            i = i + 1
    return CompleteList, CompleteListCount

def main():

    data = open('/Users/williamburke/Desktop/CSC440/CSC440Project1/Adult.txt', 'r')
    min_sup = .4 # fraction of how often an item occurs over the total number of transactions
    print("Apriori")
    Apriori(data,min_sup)
    print("FPGrowth")
    data = open("/Users/williamburke/Desktop/CSC440/CSC440Project1/Adult.txt")
    EachCandidate = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    CountOfEachCandidate = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    Class = ['Age:','Workclass:','fnlwgt:','Education','EducationNum:','MaritialStatus:','Occupation:','RelationShip:','Race:','Sex:','Capitol-Gain:','Capitol-Loss:','HoursPerWeeks:','Native-Country:','Salary:']
    count = 0 


        # D.append(row)
        # for i in range(0,len(row)):
        #     if i == 2: 
        #         continue
        #     if i == 10: 
        #         continue
        #     if i == 11: 
        #         continue
        #     if row[i] in EachCandidate[i]:
        #         for k in range(len(EachCandidate[i])):
        #             if row[i] == EachCandidate[i][k]:
        #                 CountOfEachCandidate[i][k] = CountOfEachCandidate[i][k] + 1
        #         if len(EachCandidate) == 0:
        #             EachCandidate[i].append(row[i])
        #     else:
        #         EachCandidate[i].append(row[i])
        #         CountOfEachCandidate[i].append(1)



    lines = data.readlines()
    transactions = [None] * len(lines)
    for i, line in enumerate(lines):
        transactions[i] = [str(x) for x in lines[i].split()]

    for row in transactions:
        temp = row[0]
        temp = temp[:2]
        temp = int(temp)
        temp = int(temp/float(10))
        row[0] = str(temp)
    i = 0
    # for row in transactions:
    #     if i == 20:
    #         break
    #     print row
    #     i = i + 1


    min_support = .4*len(lines)
    tree = FPTree(transactions, min_support, None, None)
    Itemsets = tree.mine(min_support)

    print  Itemsets.keys()
    print  len(Itemsets)

main()
