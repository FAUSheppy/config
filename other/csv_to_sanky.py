import ezodf
import matplotlib.pyplot as plt
import plotly.graph_objects as go

d = ezodf.opendoc("lebensmittel.ods")
s = d.sheets[0]

COL_GROUPS = 0
COL_NAME   = 1
COL_PRICE  = 4

SKIP_FIRST_ROW = True
NAME_TO_GROUP_SUM = dict()
GROUP_SUMS = dict()

COLOR_LIST = [
    "papayawhip",
    "indianred",
    "lime",
    "aqua",
    "aquamarine",
    "wheat",
    "sienna",
    "silver",
    "darksalmon",
    "pink",
    "tomato",
    "honeydew",
    "plum",
    "yellowgreen",
    "darkcyan",
    "cornflowerblue",
    "maroon",
    "azure",
    "crimson",
    "hotpink",
    "peachpuff",
    "violet",
    "mediumspringgreen",
    "teal",
    "tan",
    "darkgoldenrod",
    "chocolate",
    "mistyrose",
]

sankeyDict = {
    "data" : [{
        "type" : "sankey",
        "node" : {
            "label" : [],
            "color" : []
        },
        "link" : {
            "source" : [],
            "target" : [],
            "value"  : [],
            "color"  : [],
            "label" :  []
        }
    }]
}

for r in s.rows():

    if SKIP_FIRST_ROW:
        SKIP_FIRST_ROW = False
        continue

    group = r[COL_GROUPS].value
    name  = r[COL_NAME].value
    price = r[COL_PRICE].value

    if not any((group, name, price)):
        continue

    # normalize price
    price = int(price)

    if name not in NAME_TO_GROUP_SUM:
        NAME_TO_GROUP_SUM.update( { name : (group, price) } )
    else:
        group, cur = NAME_TO_GROUP_SUM[name]
        NAME_TO_GROUP_SUM.update({ name : (group, cur + price) })

    # group updates #
    if group not in GROUP_SUMS:
        GROUP_SUMS.update({ group : price })
    else:
        GROUP_SUMS[group] += price

# nodes
for k,v in NAME_TO_GROUP_SUM.items():
    name = k
    group, summary = v
    
    # labels #
    if group not in sankeyDict["data"][0]["node"]["label"]:
        sankeyDict["data"][0]["node"]["label"].append(group)
    sankeyDict["data"][0]["node"]["label"].append(name)

    sankeyDict["data"][0]["node"]["color"].append("lightgray")

LABELS_ALL = sankeyDict["data"][0]["node"]["label"] 
COLOR_COUNTER = 0
# links
for k,v in NAME_TO_GROUP_SUM.items():
    name = k
    group, summary = v
   
    print(group)
    # links #
    sankeyDict["data"][0]["link"]["source"].append(LABELS_ALL.index(group))
    sankeyDict["data"][0]["link"]["target"].append(LABELS_ALL.index(name))
    sankeyDict["data"][0]["link"]["value"].append(summary)
    sankeyDict["data"][0]["link"]["label"].append("{} €".format(summary))
    sankeyDict["data"][0]["link"]["color"].append(COLOR_LIST[COLOR_COUNTER%len(COLOR_LIST)])
    COLOR_COUNTER += 1

# group base connection
base = "Lebensmittel"
sankeyDict["data"][0]["node"]["label"].append(base)
for group, summary in GROUP_SUMS.items():
    sankeyDict["data"][0]["link"]["source"].append(LABELS_ALL.index(base))
    sankeyDict["data"][0]["link"]["target"].append(LABELS_ALL.index(group))
    sankeyDict["data"][0]["link"]["value"].append(summary)
    sankeyDict["data"][0]["link"]["label"].append("{} €".format(summary))
    sankeyDict["data"][0]["link"]["color"].append(COLOR_LIST[COLOR_COUNTER%len(COLOR_LIST)])
    COLOR_COUNTER += 1

# checks & validate
sankey_tmp = {
    "sankey" : {
        "nodes" : [],
        "links" : []
    }
}
for name in NAME_TO_GROUP_SUM.keys():
    if name in GROUP_SUMS:
        raise ValuerError("Group must not exist as name: {}".format(name))

# build for external json
for name in LABELS_ALL:
    element = { "name" : name }

    if name == base:
        pass
    elif name not in GROUP_SUMS:
        element.update({"layer" : 2 })
    else:
        element.update({"layer" : 1 })

    sankey_tmp["sankey"]["nodes"].append(element)

for i, source in enumerate(sankeyDict["data"][0]["link"]["source"]):

    target = sankeyDict["data"][0]["link"]["target"][i]
    color  = sankeyDict["data"][0]["link"]["color"][i]
    value  = sankeyDict["data"][0]["link"]["value"][i]
    label  = sankeyDict["data"][0]["link"]["label"][i]

    # build for external json
    sankey_tmp["sankey"]["links"].append({ "fill" : color,
                                           "source" : source,
                                           "target" : target,
                                           "value" : value
                                         })

    tupel = (source >= 0, target >=0, color, value is not None, label is not None)

    print(source, target)
    if not len(sankeyDict["data"][0]["node"]["label"]) > max(source, target):
        raise ValueError("Src or target out of bounds: {}".format(max(source, target)))

    if not all(tupel):
        raise ValueError("Missing mandatory value [source, target, color, value, label] [{}, {}, {}, {}, {}]".format(source, target, color, value, label))

    print(source, target, color)

# save file
import json
with open("sankey-tmp.json", "w") as f:
    json.dump(sankey_tmp, f, indent=2)

# do sankey
fig = go.Figure(data=[go.Sankey(
    valueformat = ".0f",
    valuesuffix = "EUR",
    # Define nodes
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label = sankeyDict['data'][0]['node']['label'],
      color = sankeyDict['data'][0]['node']['color']
    ),
    # Add links
    link = dict(
      source = sankeyDict['data'][0]['link']['source'],
      target = sankeyDict['data'][0]['link']['target'],
      value  = sankeyDict['data'][0]['link']['value'],
      label  = sankeyDict['data'][0]['link']['label'],
      color  = sankeyDict['data'][0]['link']['color']
))])
fig.show()
fig.write_image("test.png")
