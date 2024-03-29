#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
    name = "MOHAMMAD HAMZAH AKHTAR"
    email = "hamzah18051@iiitd.ac.in"
    roll_num = "2018051"
    x=0
    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        self.validate()

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """
        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def min_dist(self, start_node, end_node, path, visited ):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
            vertices = [1, 2, 3, 4, 5, 6]
            edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6)]
        
        '''
        
        d={} ; dist = 0
        self.start_node = start_node ; self.end_node = end_node ; x = start_node
       	for i in self.vertices:
            d[i] = False
        dist = 0   
        visited[start_node]=True
        neighbours = [] ; length = len(self.edges)
        path.append(start_node) ; x = path
        if start_node == end_node:
            return path    
        all_path = []  
        for i in range(length):
            for j in range(2):
                if (j==0) and (self.edges[i][j]==start_node):
                    if self.edges[i][1] not in visited:
                        neighbours.append(self.edges[i][1])
                        visited[self.edges[i][1]]=True
                elif (j==1) and (self.edges[i][j]==start_node):            
                    if self.edges[i][0] not in visited:
                        neighbours.append(self.edges[i][0]) 
                        visited[self.edges[i][0]]=True  
        returned_paths = []
        for next_node in neighbours:
            temp_dict = dict(visited); temp_path = list(path)
            if next_node not in temp_path:
                returned_paths = self.min_dist(next_node,end_node,temp_path,temp_dict)  
                if returned_paths != None:
                    all_path.append(returned_paths)
        if start_node != self.x :
            if not returned_paths:
                return None
            else:
                return all_path[0]
        distance_list = []
        for i in all_path:
            distance_list.append(len(i)-1)
        dist = min(distance_list)
        return dist,all_path    
        raise NotImplementedError
    

    def all_shortest_paths(self, start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        self.x = start_node
        distance , pos_path= self.min_dist(start_node, end_node, path=[],visited={})
        paths = self.all_paths(start_node, end_node, distance, pos_path)
        return paths
        raise NotImplementedError

    def all_paths(self, node, destination, dist, possible_path):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """
        shortest_path = []
        for i in possible_path:
            if len(i)-1==dist:
                shortest_path.append(i)
        if not shortest_path:
            return None
        else:   
            return shortest_path
        raise NotImplementedError

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """
        t=list(self.vertices)
        t.remove(node); length=len(t) ; pair_of_nodes=[]; b_w_c = 0
        for i in range(length-1):
            for j in range(i+1,length):
                p=[]
                p.append(t[i]) ; p.append(t[j])
                if p not in pair_of_nodes:
                    pair_of_nodes.append(p)
        for i in pair_of_nodes:
            y = 0
            shortest_path = self.all_shortest_paths(i[0],i[1])
            x = len(shortest_path)
            for i in shortest_path:
                if node in i:
                    y+=1
            b_w_c += y/x
        return b_w_c    
        raise NotImplementedError

    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """
        all_nodes_bwc = {} ; all_bwc=[] ; top_k = [] 
        for i in self.vertices:
            all_nodes_bwc[i] = self.betweenness_centrality(i)
            bwc = self.betweenness_centrality(i)
            all_bwc.append(bwc)
        max_bwc = max(all_bwc)
        for i in self.vertices:
            if(all_nodes_bwc[i]==max_bwc):
                top_k.append(i)
        return top_k  

        raise NotImplementedError

if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6)]

    graph = Graph(vertices, edges)
    #print(graph.all_shortest_paths(1,6))
    print(graph.top_k_betweenness_centrality())
