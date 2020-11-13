import json
from scipy.spatial import distance
import matplotlib.pyplot as plt
import staticmaps
import matplotlib.image as mpimg
import matplotlib.lines as mlines


def load_from_file(title):
    list = []
    with open('data/' + title + '.txt') as f:
        for line in f:
            line = line.strip()
            list.append([float(i) for i in line.split()])

    return list


def get_closest_point(coordinates):
    min = 1000000
    index = None
    for i in range(len(nodepl)):
        euklid_dist = distance.euclidean((coordinates[0], coordinates[1]), (nodepl[i][0], nodepl[i][1]))
        if euklid_dist < min:
            min = euklid_dist
            index = i
    return index


def find_route(endpoint, data, color, staticmaps_context=None):
    node = nodelist[endpoint]
    while True:
        old_node = node
        node_index = [i for i, x in enumerate(data) if x['index'] == node][0]
        try:
            node = data[node_index]['pre']
        except:
            break
        if staticmaps_context is not None:
            staticmaps_context.add_object(staticmaps.Line(
                [staticmaps.create_latlng(nodepl[nodelist.index(old_node)][0], nodepl[nodelist.index(old_node)][1]),
                 staticmaps.create_latlng(nodepl[nodelist.index(node)][0], nodepl[nodelist.index(node)][1])],
                color=staticmaps.parse_color(color), width=4))
        plt.plot([nodepl[nodelist.index(old_node)][1],
                  nodepl[nodelist.index(node)][1]],
                 [nodepl[nodelist.index(old_node)][0],
                  nodepl[nodelist.index(node)][0]], c=color)


def is_element_of_list(node, list, getindex=False):
    if len(list) == 0:
        return False
    if getindex:
        indexes = [i for i, x in enumerate(list) if x['index'] == node['index']]
        return indexes[0] if len(indexes) else None
    else:
        return node['index'] in [data['index'] for data in list]


def calculate_cost(i, cost='time', x=0):
    if cost == 'euklid':
        point1 = nodepl[x]
        point2 = nodepl[(arclist[i - 1]['neighbour']) - 1]
        euklid_dist = distance.euclidean((point1[0], point1[1]), (point2[0], point2[1]))
        return euklid_dist
    else:
        return arclist[i - 1]['time']


def a_star(start, cost):
    startnode = {"index": start, "label": 0, 'f': arclist[start - 1]['time']}
    temporary = [startnode]
    permanent = []
    while len(temporary) != 0:
        (m, i) = min((v, i) for i, v in enumerate([x['f'] for x in temporary]))
        v_i = temporary[i]
        permanent.append(v_i)
        v_i_index = v_i['index']
        del temporary[i]
        adjacent_nodes = []
        x = nodelist.index(v_i_index)
        if len(nodelist) == x + 1:
            x1 = x
        else:
            x1 = x + 1
        for i in range(nodelist[x], nodelist[x1]):
            neighbour = arclist[i - 1]['neighbour']
            adjacent_nodes.append({'index': nodelist[neighbour - 1]
                                      , 'label': 0, 'cost': calculate_cost(i, cost),
                                   'h': calculate_cost(i, 'euklid', x)})
        for v_j in adjacent_nodes:
            cost_i_j = v_j['cost']
            h_j = v_j['h']
            del v_j['cost']
            del v_j['h']
            if not is_element_of_list(v_j, temporary) and not is_element_of_list(v_j, permanent):
                v_j['label'] = v_i['label'] + cost_i_j
                v_j['pre'] = v_i['index']
                v_j['f'] = v_i['label'] + h_j
                temporary.append(v_j)
            if is_element_of_list(v_j, temporary) and (v_i['label'] + cost_i_j) < v_j['label']:
                v_j['label'] = v_i['label'] + cost_i_j
                v_j['pre'] = v_i['index']
                v_j['f'] = v_i['label'] + h_j
            if is_element_of_list(v_j, permanent) and (v_i['label'] + cost_i_j) < v_j['label']:
                v_j['label'] = v_i['label'] + cost_i_j
                v_j['pre'] = v_i['index']
                v_j['f'] = v_i['label'] + h_j
                temporary.append(v_j)
                i = is_element_of_list(v_j, permanent, getindex=True)
                del permanent[i]

    for i in permanent:
        del i['f']
        del i['label']

    with open("prelist.json", "w") as write_file:
        json.dump(permanent, write_file)
    return permanent


def dijkstra(start, cost):
    startnode = {"index": start, "label": 0}
    temporary = [startnode]
    permanent = []

    while len(temporary) != 0:
        (m, i) = min((v, i) for i, v in enumerate([x['label'] for x in temporary]))
        v_i = temporary[i]
        permanent.append(v_i)
        v_i_index = v_i['index']
        del temporary[i]
        adjacent_nodes = []
        x = nodelist.index(v_i_index)
        if len(nodelist) == x + 1:
            x1 = x
        else:
            x1 = x + 1
        for i in range(nodelist[x], nodelist[x1]):
            neighbour = arclist[i - 1]['neighbour']
            c = calculate_cost(i, cost)
            adjacent_nodes.append({'index': nodelist[neighbour - 1]
                                      , 'label': 0, 'cost': c})
        for v_j in adjacent_nodes:
            cost_i_j = v_j['cost']
            del v_j['cost']
            if not is_element_of_list(v_j, temporary) and not is_element_of_list(v_j, permanent):
                v_j['label'] = v_i['label'] + cost_i_j
                v_j['pre'] = v_i['index']
                temporary.append(v_j)
            if is_element_of_list(v_j, temporary) and (v_i['label'] + cost_i_j) < v_j['label']:
                v_j['label'] = v_i['label'] + cost_i_j
                v_j['pre'] = v_i['index']

    for i in permanent:
        del i['label']

    with open("prelist.json", "w") as write_file:
        json.dump(permanent, write_file)
    return permanent


arclist = load_from_file("arclist")
for i in range(len(arclist)):
    arclist[i] = {"neighbour": int(arclist[i][0]), "time": arclist[i][1]}
nodelist = load_from_file("nodelist")
nodelist = [int(x[0]) for x in nodelist]
nodepl = load_from_file("nodepl")

answer = input(
    "Enter the start coordinates (the closest data point is found using Euclidean distance) \n"
    "Enter 'n' if you want to use predefined coordinates\nLatitude (Enter 'n' to skip): ").strip()
if answer == "no" or answer == "n":
    startpoint = [47.0672794, 15.4403575]
    startpoint_val = nodelist[get_closest_point(startpoint)]
else:
    lat = float(answer)
    long = float(input("Longitude: ").strip())
    startpoint = [lat, long]
    startpoint_val = nodelist[get_closest_point(startpoint)]

goal_coordinates = []
while True:
    answer = input(
        "Enter the goal coordinates (the closest data points are found using Euclidean distance) \n"
        "Enter 'n' to stop entering coordinates\nLatitude (Enter 'n' to skip): ").strip()
    if answer == "no" or answer == "n":
        break
    else:
        lat = float(answer)
        long = float(input("Longitude: ").strip())
        closest_point = [lat, long]
        goal_coordinates.append(closest_point)

if len(goal_coordinates) == 0:
    goal_coordinates = [[47.0255465, 15.3934554], [47.0772596, 15.4733993], [47.1104009, 15.4029102]]

answer = input("Type 'd' to use the Dijkstra algorithm\n"
               "Type 'a' to use the A* algorithm\nAlgorithm: ").strip()

algo_used = "Dijkstra Algorithm"
if answer == "d":
    permanent = dijkstra(startpoint_val, 'time')
elif answer == 'a':
    permanent = a_star(startpoint_val, 'time')
    algo_used = "A* Algorithm"
else:
    print("Incorrect input, using dijkstra")
    permanent = dijkstra(startpoint_val, 'time')

print("Generating the simplified version ...")
min_lat = min((v for v in ([x[0] for x in nodepl])))
max_lat = max((v for v in ([x[0] for x in nodepl])))
min_long = min((v for v in ([x[1] for x in nodepl])))
max_long = max((v for v in ([x[1] for x in nodepl])))

plt.ylim(min_lat, max_lat)
plt.xlim(min_long, max_long)
plt.xlabel('Longitude [°]')
plt.ylabel('Latitude [°]')
plt.title(algo_used + " - Simplified view")
help_array = []
for i in nodepl:
    help_array.append([i[1], i[0]])
plt.scatter(*zip(*help_array), s=1, c="#8d8d8d")
plt.scatter((startpoint[1],), (startpoint[0],), c="#ff1515", s=50)
legend = [mlines.Line2D([], [], color='w', mfc='#ff1515', mec='#ff1515', marker='o', markersize=8, label='Startpoint')]

colors = ["#2db60a", "#0ab6b6", "#b60ab1", "#0a37b6", "#b6690a", "#0ab64f", "#0a6fb6", "#740ab6", "#2b6435", "#642b48",
          "#333"]

context = staticmaps.Context()
context.add_object(staticmaps.Marker(staticmaps.create_latlng(startpoint[0], startpoint[1]),
                                     color=staticmaps.parse_color("#ff1515"), size=12))
context.add_object(staticmaps.Marker(staticmaps.create_latlng(min_lat, min_long),
                                     color=staticmaps.parse_color("#ffffff00"), size=0))
context.add_object(staticmaps.Marker(staticmaps.create_latlng(max_lat, max_long),
                                     color=staticmaps.parse_color("#ffffff00"), size=0))

for index, i in enumerate(goal_coordinates):
    color = colors[index % len(colors)]
    legend.append(mlines.Line2D([], [], color=color, markersize=15, label='Optimal Route to Point ' + str(index + 1)))
    plt.scatter(*zip(*[[i[1], i[0]]]), c=color, s=25)
    context.add_object(
        staticmaps.Marker(staticmaps.create_latlng(i[0], i[1]), color=staticmaps.parse_color(color), size=12))
    find_route(get_closest_point(i), permanent, color, staticmaps_context=context)

ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0 + box.width * 0.175, box.y0 + box.height * 0.35, box.width * 0.65, box.height * 0.65])
plt.legend(handles= [mlines.Line2D([], [], color='w', mfc='#8d8d8d', mec='#8d8d8d', marker='o',
                                          markersize=3, label='Data Points')]+ legend, loc='upper center',
           bbox_to_anchor=(0.48, -0.27), fancybox=True, shadow=True, ncol=2)

plt.savefig('result_simplified.png', dpi=300)
print("Saved the simplified version to result_simplified.png ...")
print("Displaying the simplified version ...")
plt.show()

print("Generating the full version ...")
image = context.render_cairo(3000, 3000)
image.write_to_png("result_detailed.png")
print("Saved the detailed version to 'result_detailed.png'")

svg_image = context.render_svg(3000, 3000)
with open("result_detailed.svg", "w", encoding="utf-8") as f:
    svg_image.write(f, pretty=True)
print("Saved the detailed version to 'result_detailed.svg'")

print("Displaying the detailed version ...")
img = mpimg.imread('result_detailed.png')
fig, ax = plt.subplots()
imgplot = ax.imshow(img, zorder=0, extent=(min_long, max_long, min_lat, max_lat), aspect='equal')
ax.set_xlim(min_long, max_long)
ax.set_ylim(min_lat, max_lat)
plt.xlabel('Longitude [°]')
plt.ylabel('Latitude [°]')
plt.title(algo_used + " - Detailed Version")
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.35, box.width, box.height * 0.65])
plt.legend(handles=legend, loc='upper center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=True, ncol=2)
plt.show()
