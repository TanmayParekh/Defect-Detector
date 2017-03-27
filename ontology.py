import json

def buildOntology():

    defects = {}
    defects['picture'] = ['blurry', 'fuzzy', 'grainy', 'crappy', 'small', 'dark', 'difficult']
    defects['colors'] = ['bleak', 'poor']
    defects['resolution'] = ['poor', 'low']
    defects['contrast'] = ['poor']
    defects['sharpness'] = ['poor']
    defects['film'] = ['jammed', 'cheap']
    defects['case'] = ['small', 'cheap']
    defects['zipper'] = ['broken', 'absent']
    defects['lens'] = ['defective', 'cheap']
    defects['autofocus'] = ['impossible', 'horrible', 'slow', 'useless', 'absent', 'joke', 'disappointing', 'confusing']
    defects['zoom'] = ['terrible', 'stuck']
    defects['viewfinder'] = ['terrible', 'poor']
    defects['life'] = ['poor', 'short']
    defects['charging'] = ['slow']
    defects['size'] = ['small', 'big']
    defects['sensor'] = ['poor', 'tiny']
    defects['weight'] = ['heavy', 'high']
    defects['design'] = ['poor', 'cheap', 'weak', 'flimsy']
    defects['controls'] = ['limited', 'unintuitive']
    defects['buttons'] = ['unresponsive']
    defects['tripod'] = ['light', 'lightweight']
    defects['mic'] = ['hissing']
    defects['speed'] = ['speed', 'delay']
    defects['release'] = ['loose']
    defects['flash'] = ['slow', 'bright', 'faulty']
    defects['shooting'] = ['slow', 'poor']

    with open('camera_ontology.json', 'w') as outfile:
        json.dump(defects, outfile)

    return defects


if __name__=='__main__':

    buildOntology()
