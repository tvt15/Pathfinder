# Pathfinder
A* pathfinder
/*
H(n)= gives a score respresenting the shortest distance between the current point and end point regard less of the path being existent or not, found using formulas we used.
G(n)=gives a score representing the current shortest path found between two points during the search
F(n)= gives the combined score of H(n) and G(n)
we priortize the path being taken on basis of the F(n) score of the path so that we are alawys taking the most efficient path possible and not just brute forcing
