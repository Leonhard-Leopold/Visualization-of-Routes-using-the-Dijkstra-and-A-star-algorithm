# Visualization-of-Routes-using-the-Dijkstra-and-A-star-algorithm
A simple visualization routes calculated by the Dijkstra and A* Algorithm using python

## Installation

Download the source code and use Python 3+ to run the main.py file

```bash
py .\main.py
```

## Usage

After starting the program, the user can choose different options.
First, the start coordinates of the search have to be entered. 
```bash
Enter the start coordinates (the closest data point is found using Euclidean distance)
Enter 'n' to use predefined coordinates
Latitude (Enter 'n' to skip):
```
You can simply enter 'n' to skip this step and use predefined coordinates.

The same has to be done using the goal(s) of the route. One or more coordinates can be added. 
However, this can also be skipped to use 3 predefined coordinates.
```bash
Enter the goal coordinates (the closest data points are found using Euclidean distance)
Enter 'n' to stop entering coordinates
Latitude (Enter 'n' to skip):
```
Lastly the wanted algorithm can be chosen. 
The Dijkstra algorithm uses the second column of the arclist.txt (See Input Files) as cost function
The A* algorithm additionally uses the Euclidean distance between points as a heuristic cost function.  
```bash
Type 'd' to use the Dijkstra algorithm
Type 'a' to use the A* algorithm
Algorithm:
```


## Input Files
In the data folder three .txt files can be found. These represent the adjacency list that defines the network of nodes.
* _nodepl.txt_ defines the coordinates of the nodes
* _nodelist.txt_ is the adjacency list of the nodes
* _arclist.txt_ is the adjacency list of the arcs. The first column is the destination node. The second column defines the cost function. 

These files contain sample data from Graz, Austria, but can be changed to everything as long as the files are formatted accordingly.


## Output
The simplified view of the output that contains all the nodes and an approximation of the route is displayed.
Next, a detailed view is displayed. Here, with the help of [staticmaps](https://pypi.org/project/py-staticmaps/) a map of the area with the routes drawn in it is shown.
Both visualizations are displayed when executing the program and also saved automatically.
Additionally, a file titled _prelist.json_ is created that just includes each node the its predecessor. This can be uses for other path finding purposes.

Simplified View
<img src="https://data.leoleo.at/img/result_simplified.png" height="500" />

Detailed View
<img src="https://data.leoleo.at/img/result_detailed_plot.png" height="500" />

[Detailed View Zoomed In](https://data.leoleo.at/img/result_detailed_zoomed.png)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
