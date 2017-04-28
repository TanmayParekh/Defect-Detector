import json

# Make a dictionary of equivalent/similar components.
# Replicate the list of describing words for all. (Redundancy in writing is avoided)
def equivalent_components(defect_dict):

    equivalent = {}
    equivalent['picture'] = ['pictures', 'pic', 'pics', 'photo', 'photos', 'shot', 'shots','image','images']
    equivalent['colors'] = ['color','colours','colour']
    equivalent['autofocus'] = ['focus']
    equivalent['battery'] = ['batteries']
    equivalent['display'] = ['screen']
    equivalent['controls'] = ['control']
    equivalent['charging'] = ['charge']
    equivalent['wi-fi'] = ['wireless','wifi']
    equivalent['sound'] = ['pickup', 'sounds', 'audio']

    for comp in equivalent.keys():
        for equiv_comp in equivalent[comp]:
            defect_dict[equiv_comp] = defect_dict[comp]

def generic_features(defect_dict):

    generic = ['terrible','awful','horrible','disappointing','useless','poor','cheap','error','issue','sucked','worse','shuts','shut','broken','joke','trash']

    for comp in defect_dict:
        defect_dict[comp] += generic

def buildOntology():

    defects = {}
    defects['display'] = ['fuzzy','poor','broken','grainy','froze','black','pixilated']
    defects['picture'] = ['blurry', 'fuzzy', 'grainy', 'crappy', 'small', 'dark', 'difficult','unclear','noisy','foggy','pixilated','overexposed','underexposed']
    defects['colors'] = ['bleak', 'poor','drab','unbalanced']
    defects['resolution'] = ['poor', 'low']
    defects['contrast'] = ['poor']
    defects['sharpness'] = ['poor']
    defects['film'] = ['jammed', 'cheap']
    defects['case'] = ['small', 'cheap']
    defects['zipper'] = ['broken', 'absent']
    defects['lens'] = ['defective', 'cheap']
    defects['autofocus'] = ['impossible', 'horrible', 'slow', 'useless', 'absent', 'joke', 'disappointing', 'confusing', 'forever']
    defects['zoom'] = ['terrible', 'stuck','slow','stick','unresponsive','jitters']
    defects['viewfinder'] = ['terrible', 'poor']
    defects['life'] = ['poor', 'short']
    defects['charging'] = ['slow','unefficient','loose']
    defects['size'] = ['small', 'big']
    defects['sensor'] = ['poor', 'tiny']
    defects['weight'] = ['heavy', 'high']
    defects['design'] = ['poor', 'cheap', 'weak', 'flimsy']
    defects['controls'] = ['limited', 'unintuitive']
    defects['buttons'] = ['nonresponsive','non-responsive','unresponsive','small','tiny']
    defects['tripod'] = ['light', 'lightweight']
    defects['mic'] = ['hissing']
    defects['speed'] = ['speed', 'delay', 'awful', 'slow']
    defects['release'] = ['loose']
    defects['flash'] = ['slow', 'bright', 'faulty']
    defects['shooting'] = ['slow', 'poor']
    defects['video'] = ['horrible', 'awful','blurry','grainy','fuzzy','noisy','pixilated','choppy']
    defects['battery'] = ['awful','drain','dead','hot','exhaust']
    defects['memory'] = ['low','less','tiny']
    defects['quality'] = ['poor','low']
    defects['cover'] = ['broken','torn']
    defects['performance'] = ['low']
    defects['shutter'] = ['slow']
    defects['wi-fi'] = ['difficult','unintuitive','slow','unresponsive']
    defects['sound'] = ['loud','fuzzy','muffled']
    defects['lighting'] = ['dark','low']

    generic_features(defects)
    equivalent_components(defects)

    with open('camera_ontology.json', 'w') as outfile:
        json.dump(defects, outfile)

    return defects

def generic_features_2(defect_dict):

    generic = ['not work','didn\'t work','stop working']

    for comp in defect_dict:
        defect_dict[comp] += generic

def build_bigram_ontology():

    bi_defects = {}
    defect['battery'] = ['popping out','wash out','drain out']
    defect['']


if __name__=='__main__':

    buildOntology()
