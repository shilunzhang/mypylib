#------------------------------------------------------
# Library for percolation process on networks.
# Author: Shilun Zhang
# Email: 779158969@qq.com
#------------------------------------------------------

import numpy as np
from functools import reduce
import operator as op

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer//denom

# Implementation of Site Percolation
# Ref: Newman M. Networks: an introduction[M]. Oxford university press, 2010.
class cluster:
	def __init__(self, id, nodes):
		self.id = id
		if isinstance(nodes, list):
			self.nodes = nodes
		else:
			self.nodes = [nodes]
		self.size = len(self.nodes)

	def AddNodes(self, nodes):
		if not isinstance(nodes, list):
			self.nodes.append(nodes)
		else:
			self.nodes += nodes
		self.size = len(self.nodes)

	def PrintInfo(self, printNodes=False):
		print('ID: %s\n'%self.id)
		print('Size: %s\n'%self.size)
		if printNodes:
			print('Nodes: ')
			print(*self.nodes)

class clustSeq:
	def __init__(self):
		self.clusters = dict()
		self.clustNum = 0

	def AddCluster(self, cluster):
		if cluster.id in self.clusters:
			raise ValueError('Added cluster\'s id existed in clusters!')
		else:
			self.clusters[cluster.id] = cluster
			self.clustNum += 1

	def MaxClustSize(self):
		if self.clustNum == 0:
			return 0
		else:
			return np.max([c.size for c in self.clusters.values()])

	def AllNodes(self):
		nodes = []
		for c in self.clusters.values():
			nodes += c.nodes
		return nodes

	def FindCluster(self, nodeId):
		id = -1
		for c in self.clusters:
			if nodeId in self.clusters[c].nodes:
				id = c
				break
		return id
	
	def MergeCluster(self, cid, netEdges):
		allNodes = self.AllNodes()
		originNodeId = self.clusters[cid].nodes[0]
		originClusterId = cid
		for o, t in netEdges:
			if originNodeId in [o, t]:
				targetNodeId = (o if originNodeId==t else t)
				if targetNodeId in allNodes:
					targetClusterId = self.FindCluster(targetNodeId)
#					print('TargetCluster: %s'%targetClusterId)
					if targetClusterId == originClusterId:
						continue
					assert targetClusterId in self.clusters
					if self.clusters[targetClusterId].size <= self.clusters[originClusterId].size:
						self.clusters[originClusterId].AddNodes(self.clusters[targetClusterId].nodes)
						self.clusters.pop(targetClusterId)
						self.clustNum -= 1
					else:
						self.clusters[targetClusterId].AddNodes(self.clusters[originClusterId].nodes)
						self.clusters.pop(originClusterId)
						self.clustNum -= 1
						originClusterId = targetClusterId
					
				
def FindEdge(net, node, directed=False):
	edge = []
	for o, t in net:
		if node in [o, t]:
			edge.append(o if node!=o else t)
	return edge

def SitePerc(net, netSize, phi):
	sr = np.zeros(netSize+1, dtype=float)
	sr[1] = 1/netSize
	for r in range(2, netSize+1):
#		print(r)
		clusters = clustSeq()
		occupNodes = np.random.choice(netSize, r, replace=False)
		cid = 0
		for node in occupNodes:
			newCluster = cluster(cid, node)
			clusters.AddCluster(newCluster)
			clusters.MergeCluster(cid, net)
			cid += 1
		sr[r] = clusters.MaxClustSize()/netSize
	s = np.sum([ncr(netSize, r) * phi**r * (1-phi)**(netSize-r) * sr[r] for r in range(netSize+1)])
	return s