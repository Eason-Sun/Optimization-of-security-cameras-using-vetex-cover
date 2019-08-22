# Optimization-of-security-cameras-using-vetex-cover

## Problem Definition:
The project is to help the local police department with their installation of security cameras at traffic intersections. It solve a particular kind of optimization problem, called the Vertex Cover problem, in this context. The idea is for the police to be able to minimize the number of cameras they need to install, and still be as effective as possible with their monitoring.

## Input:
The input comprises lines each of which specifies a command. There are 4 kinds of commands.
1) Add a street  
2) Change a street  
3) Remove a street  
4) Generate a graph.  

Here is an example of how this program should work. Example is using the Cartesian coordinate system.

## Add a street: 
Denoted by 'a', it continuously parses user inputs with format a + some empty spaces + street_name with quotation marks + pairs of numbers seperated by some empty spaces. This command does not output anything.

e.g.  
a "Weber Street" (2,-1) (2,2) (5,5) (5,6) (3,8)  
a "King Street S" (4,2) (4,8)  
a "Davenport Road" (1,4) (5,8)   

## Change a street:
Denoted by 'c', it updates the coordinates of a street that has been added.

e.g.  
c "Weber Street" (2,1) (2,2)

## Remove a street:
Denoted by 'r', it deletes a street with its coordinates by the given street name.

e.g.  
r "King Street S"

## Generate a graph:
Denoted by 'g'. It generates the graph according to the current state of all streets' coordinates followed by some rules:

### There is a vertex corresponding to: 
a) each intersection, or  
b) the end-point of a line segment of a street that intersects with another street.  

### There is a edge corresponding to:   
a) At least one of them is an intersection, and,  
b) Both lie on the same street, and,  
c) One is reachable from the other without traversing another vertex.  

Expected output after the add command above (without change and remove):  
V = {  
1: (2,2)  
2: (4,2)  
3: (4,4)  
4: (5,5)  
5: (1,4)  
6: (4,7)  
7: (5,6)  
8: (5,8)  
9: (3,8)  
10: (4,8)  
}  

E = {  
<1,3>,  
<2,3>,  
<3,4>,  
<3,6>,  
<7,6>,  
<6,5>,  
<9,6>,  
<6,8>,  
<6,10>  
}

Note: each vetex has an identifier (1~10 in this case). Edges are consisted of two identifiers for a pair of vertices.


## Error handling:
Errors in inputs are accounted, and brief descriptive error messages are outputed accordingly.

## Unit tests:
python unittest is used, 12 tests are run for each function.
