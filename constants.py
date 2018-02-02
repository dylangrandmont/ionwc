# Copyright (C) 2016-2017, Eye on Western Canada
#

import os

IONWC_HOME = os.environ["IONWC_HOME"]

UNKNOWN = 'Unknown'
KML_TEMPLATE = "<Polygon><outerBoundaryIs><LinearRing><coordinates>%s,%s %s,%s %s,%s %s,%s</coordinates></LinearRing></outerBoundaryIs></Polygon>"

# Appoximate age (in Mya) corresponding to the BASE of a formation (unless
# specified otherwise)
# Source: https://landman.ca/pdf/CORELAB.pdf
FORMATION_AGE_DICT = {
    'top surface': 0,
    'surface': 0,
    'paskapoo': 664,
    'belly river': 750,
    'edmonton': 836,
    'top milk river formation': 835,
    'chinook': 845,
    'milk river': 845,
    'upper colorado shale': 875,
    'medicine hat': 900,
    'badheart-muskiki': 905,
    'top second white speckled shale': 900,
    'top second white speckled': 900,
    'cardium': 910,
    'second white specks': 920,
    'second white speckled': 920,
    'doe creek': 950,
    'dunvegan': 970,
    'top mannville group': 980,
    'top fish scale zone': 1000,
    'dunvegan-fish scales': 1025,
    'fish scale-westgate': 1025,
    'top viking formation': 1025,
    'viking': 1020, 
    'bow island': 1025,
    'basal colorado': 1030,
    'base colorado group': 1030,
    'colorado': 1030,
    'top colony member': 1030,
    'paddy': 1020,
    'cadotte': 1030,
    'peace river': 1040,
    'paddy-cadotte-harmon': 1040,
    'notikewin': 1030,
    'spirit river': 1120,
    'notikewin-falher-wilrich': 1120,
    'middle mannville': 1130,
    'basal blairmore': 1190,
    'bullhead': 1250,
    'bluesky': 1250,
    'bluesky-bullhead': 1250,
    'bluesky-gething': 1250,
    'bluesky-gething-dunlevy': 1250,
    'glauconitic': 1250,
    'mannville': 1250,
    'blairmore': 1250,
    'l sandstone of l blair': 1250,
    'base mannville group': 1250,
    'basal quartz': 1250,
    'ostracod': 1270,
    'cadomin': 1280,
    'lower mannville': 1280,
    'lower mannville&jurassic': 1310,
    'ellerslie': 1410,
    'nikanassin': 1470,
    'buick creek-dunlevy' : 1470,
    'cadomin-dunlevy-nikanassin': 1470,
    'kootenay': 1470,
    'base vanguard group': 1680,
    'l mannville - rock creek': 1720,
    'rock creek': 1720,
    'sawtooth': 1740,
    'base shaunavon formation': 1740,
    'top watrous formation': 1750,
    'kootenay/fernie': 1990,
    'fernie': 1990,
    'nordegg': 1910,
    'fernie-nordegg': 1910,
    'jurassic system': 2010,
    'jurassic': 2010,
    'baldonnel': 2300,
    'baldonnel/upper charlie lake': 2300,
    'pardonet-baldonnel': 2300,
    'boundary': 2360,
    'charlie lake': 2370,
    'halfway': 2420,
    'artex-halfway-doig': 2402,
    'charlie lake-halfway-doig': 2470,
    'doig': 2470,
    'montney': 2520,
    'basal montney': 2520,
    'basal montney lag-belloy-golata': 2520,
    'basal montney lag-belloy-stoddart': 2520,
    'triassic': 2520,
    'triassic system': 2520,
    'top paleozoic': 2520,
    'belloy': 2990,
    'stoddart': 3310,
    'base ratcliffe beds': 3400,
    'top midale beds': 3400,
    'base midale beds': 3420,
    'debolt': 3420,
    'turner valley': 3420,
    'elkton':3420,
    'shunda': 3490,
    'base frobisher-alida beds': 3490,
    'livingstone': 3495,
    'pekisko': 3500,
    'base tilston beds': 3500,
    'shunda-pekisko': 3500,
    'rundle': 3500,
    'banff': 3580,
    'base souris valley beds': 3580,
    'bakken': 3600,
    'lwr banff-exshaw': 3600,
    'base bakken formation': 3600,
    'base three forks group': 3640,
    'wabamun': 3650,
    'top torquay formation': 3650,
    'arcs': 3780,
    'nisku': 3780,
    'base birdbear formation': 3780,
    'top duperow formation': 3780,
    'winterburn': 3780,
    'jean marie': 3780,
    'grosmont': 3790,
    'duvernay-majeau lake': 3800,
    'duvernay': 3800,
    'leduc': 3800,
    'woodbend': 3800,
    'woodbend reef': 3800,
    'sulphur point': 3830,
    'muskeg': 3830,
    'beaverhill lake': 3840,
    'slave point-fort vermilion': 3840,
    'slave point': 3840,
    'waterways-otter park-slave point': 3840,
    'sulphur pt.-muskeg-keg river-pine': 3900,
    'keg river': 3900,
    'base winnipegosis formation': 3900,
    'elk point': 3920,
    'top winnipeg formation': 5000,
    'top deadwood formation': 5050,
    'granite wash': 9999,
    'gilwood': 9999,
    'basement': 9999,
    'precambrian system': 9999,
    'top precambrian': 9999,
    '': 9999
}

MONTH_DICT = {
    'JAN':'01',
    'FEB':'02',
    'MAR':'03',
    'APR':'04',
    'MAY':'05',
    'JUN':'06',
    'JUL':'07',
    'AUG':'08',
    'SEP':'09',
    'OCT':'10',
    'NOV':'11',
    'DEC':'12',
    'JANUARY':'01',
    'FEBRUARY': '02',
    'MARCH': '03',
    'APRIL': '04',
    'MAY': '05',
    'JUNE': '06',
    'JULY': '07',
    'AUGUST': '08',
    'SEPTEMBER': '09',
    'OCTOBER': '10',
    'NOVEMBER': '11',
    'DECEMBER': '12'
}

NUMBER_TO_MONTH_MAP = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}

BC_WELL_NAME_TO_OPERATOR_MAP = {
    'apache '      :'Apache Canada Ltd.',
    'arcres'       :'ARC Resources Ltd.',
    'black swan'   :'Black Swan Energy',
    'blz '         :'Blz Energy Ltd.',
    'bonavista'    :'Bonavista Energy Corporation',
    'canbriam'     :'Canbriam Energy Inc.',
    'chevron woodside' :'Chevron Woodside',
    'chinook'      :'Chinook Energy Inc.',
    'cop'          :'Conocophillips',
    'crew'         :'Crew Energy Inc.',
    'dejour'       :'Dejour Energy Alberta Ltd.',
    'devon'        :'Devon',
    'endurance'    :'Endurance Energy Ltd.',
    'enerplus'     :'Enerplus',
    'ecog'         :'EOG Resources',
    'falls creek'  :'Falls Creek Resources Inc.',
    'harvest'      :'Harvest Operations Corp.',
    'husky'        :'Husky Energy Inc.',
    'ikkuma'       :'Ikkuma Resources Corp.',
    'imp '         :'Imperial Oil',
    'ish '         :'Ish Energy Ltd.',
    'leucrotta'    :'Leucrotta Exploration Inc.',
    'lone pine'    :'Lone Pine Resources Inc.',
    'lts'          :'Lightstream Resources Ltd.',
    'mancal'       :'Mancal Energy Inc.',
    'murphy'       :'Murphy Oil Company Ltd.',
    'nexen'        :'Nexen Energy',
    'para'         :'Paramount Resources Ltd.',
    'pengrowth'    :'Pengrowth Energy Corporation',
    'penn west'    :'Penn West Petroleum',
    'polar star'   :'Polar Star Canadian Oil and Gas Ltd.',
    'quattro '     :'Quattro Exploration & Production',
    'quicksilver'  :'Quicksilver Resources Canada',
    'sdel '        :'Sinopec Daylight Energy Ltd.',
    'secure '      :'Secure Energy Services Inc.',
    'shell'        :'Shell Canada Limited',
    'spyglass'     :'Spyglass Resources Corp.',
    'srl'          :'Storm Resources Ltd.',
    'storm'        :'Storm Resources Ltd.',
    'suncor'       :'Suncor Energy Inc.',
    'taqa '        :'Taqa North Ltd.',
    'terra '       :'Terra Energy Corporation',
    'tervita'      :'Tervita Corporation',
    'whitecap'     :'Whitecap Resources Inc.',
    'venturion'    :'Venturion Oil Limited',
    'painted pony' :'Painted Pony Petroleum Ltd.',
    'progress'     :'PROGRESS ENERGY CANADA LTD.',
    'eca'          :'Encana Corporation',
    'saguaro'      :'Saguaro Resources Ltd',
    'cnrl'         :'Canadian Natural Resources Limited',
    'csri'         :'Canadian Spirit Resources Inc.',
    'tourmaline'   :'Tourmaline Oil Corp.',
    'huron resources' :'Huron Resources Corp.',
    'kelt'         :'Kelt Exploration Ltd',
    'yoho'         :'Yoho Resources Inc.',
    'ugrbc'        :'Unconventional Gas Resources',
    'woodside et al ': 'Woodside et al.'
}

BC_WELL_NAME_TO_FIELD_MAP = {
    'aitken': 'Aitken Creek',
    'altares': 'Altares',
    ' beg ': 'Beg',
    'bivouac': 'Bivouac',
    ' boundary ': 'Boundary Lake',
    'brassey': 'Brassey',
    'bubbles': 'Bubbles',
    'buick': 'Buick Creek',
    'caribou': 'Caribou',
    'daiber': 'Daiber',
    'dawson': 'Dawson',
    'dunedin': '',
    'etsho': 'Etsho',
    'fireweed': 'Fireweed',
    'fortune': 'Fortune',
    'goose': 'Goose',
    'graham': 'Graham',
    'groundbirch': 'Groundbirch',
    'gunnell': 'Gunnell Creek',
    'halfway': 'Halfway',
    'hay': 'Hay River',
    'helmet': 'Helmet',
    'inga': 'Inga',
    'jedney': 'Jedney',
    'julienne': 'Julienne Creek',
    'kelly': 'Kelly',
    'kiwigana': 'Kiwigana',
    'kobes': 'Kobes',
    'komie': 'Komie',
    'laprise': 'Laprise Creek',
    'lily': 'Lily Lake',
    'maxhamish': 'Maxhamish Lake',
    'mica': 'Mica',
    'monias': 'Monias',
    'muskrat': 'Muskrat',
    'n aitken': 'Aitken Creek North',
    'n bubbles': 'Bubbles North',
    'nig': 'Nig Creek',
    'noel': 'Noel',
    'oak': 'Oak',
    'ojay': 'Ojay',
    'parkland': 'Parkland',
    'pickell': 'Pickell',
    'pocketknife': 'Pocketknife',
    'saturn': 'Saturn',
    'sierra': 'Sierra',
    'septimus': 'Septimus',
    'sundown': 'Sundown',
    'sunrise': 'Sunrise',
    'sunset prairie': 'Sunset Prairie',
    'swan lake': 'Swan Lake',
    'tattoo': 'Tattoo',
    'town': 'Townsend',
    ' tower ': 'Tower Lake',
    'w beg': 'Beg West',
    'w gundy': 'Gundy Creek West',
    'w jedney': 'Jedney West',
    'w peejay': 'Peejay West',
    'w stoddart': 'Stoddart West',
    'weasel': 'Weasel'
}

MB_WELL_NAME_TO_OPERATOR_MAP = {
    'arc'   :"ARC Resources Ltd.",
    'black gold': 'Black Gold Energy Ltd.',
    'cnrl ': 'Canadian Natural Resources Limited',
    'corex ': 'Corex Resources Ltd.',
    'corval':"Corval Energy Ltd.",    
    'cpec'  :"Crescent Point Energy",    
    'elcano':"Elcano Exploration Inc.",
    'eog'     :"EOG RESOURCES CANADA INC.",
    'evergro ': 'Evergro Energy Corporation',
    'flushing': 'Flushing Energy Corp.',
    'fort'  :"Fort Calgary Resources Ltd.",
    'highmark ': 'Highmark Exploration Inc.',
    'interwest': 'Interwest Petroleums Ltd.',
    'kinwest': 'Kinwest 2008 Energy Inc.',
    'legacy':"Legacy Oil + Gas Inc.",
    'melita': 'Melita Resources Ltd.',
    'nal ': 'Nal Resources Limited',
    'paradise ': 'Paradise Petroleums Ltd.',
    'penn'  :"Penn West Petroleum Ltd.",
    'petrobakken':'Petrobakken Energy Ltd.',
    'petro one': 'Petro One Energy Corp.',
    'red beds ': 'Red Beds Resources Limited',
    'riflemen': 'Riflemen Exploration Ltd.',
    'surge ': 'Surge Energy Inc.',
    't. bird': 'T. Bird Oil Ltd.',
    'tundra':"Tundra Oil and Gas Partnership"
}

# Source for pool codes:
# http://www.gov.mb.ca/iem/petroleum/f_p_codes/poolbook.pdf
MB_POOL_CODE_TO_ZONE_MAP = {
    '159' :'Lodgepole',
    '160' :'Bakken',
    '162' :'Bakken-Three Forks',
    '165' :'Three Forks',
    '244' :'Mission Canyon',
    '310' :'Favel',
    '329' :'Lower Amaranth',
    '342' :'Mission Canyon',
    '343' :'Mission Canyon',
    '344' :'Mission Canyon',
    '452' :'Lodgepole',
    '559' :'Lodgepole',
    '629' :'Lower Amaranth',
    '652' :'Lodgepole',
    '653' :'Lodgepole',
    '729' :'Lower Amaranth',
    '735' :'Lower Amaranth-Mission Canyon',
    '741' :'Mission Canyon',
    '742' :'Mission Canyon',
    '743' :'Mission Canyon',
    '744' :'Mission Canyon',
    '951' :'Lodgepole',
    '954' :'Lodgepole',
    '955' :'Lodgepole',
    '959' :'Lodgepole',
    '962' :'Bakken-Three Forks',
    '1053' :'Lodgepole',
    '1352' :'Lodgepole',
    '1353' :'Lodgepole',
    '1452' :'Lodgepole',
    '1560' :'Bakken',
    '1562' :'Bakken-Three Forks',
    '1762' :'Bakken-Three Forks',
    '9919' :'Melita',
    '9940' :'Lower Amaranth-Lodgepole',
    '9944' :'Mission Canyon'
}

BC_POSTING_DATES_TO_SALE_DATE_MAP = {
    '2016.01': '2016.01.20',
    '2016.02': '2016.02.24',
    '2016.03': '2016.03.23',    
    '2016.04': '2016.04.20',
    '2016.05': '2016.05.18',
    '2016.06': '2016.06.15',
    '2016.07': '2016.07.13',    
    '2016.08': '2016.08.10',
    '2016.09': '2016.09.07',
    '2016.10': '2016.10.05',
    '2016.11': '2016.11.02',    
    '2016.12': '2016.12.14', 
    '2017.01': '2017.01.18',
    '2017.02': '2017.02.22',
    '2017.03': '2017.03.22',    
    '2017.04': '2017.04.19',
    '2017.05': '2017.05.17',
    '2017.06': '2017.06.21',
    '2017.07': '2017.07.26',    
    '2017.08': '2017.08.23',
    '2017.09': '2017.09.20',
    '2017.10': '2017.10.18',
    '2017.11': '2017.11.15',
    '2017.12': '2017.12.13',
    '2018.01': '2018.01.17',
    '2018.02': '2018.02.21',
    '2018.03': '2018.03.21',
    '2018.04': '2018.04.18',
    '2018.05': '2018.05.16',
    '2018.06': '2018.06.13',
    '2018.07': '2018.07.11',
    '2018.08': '2018.08.15',
    '2018.09': '2018.09.12',
    '2018.10': '2018.10.10',
    '2018.11': '2018.11.14',
    '2018.12': '2018.12.12',
}

# Source: http://www.economy.gov.sk.ca/publicofferings
SK_POSTING_NUMBER_TO_SALE_DATE = {
    '369': '2016.02.02',
    '370': '2016.04.12',
    '371': '2016.06.07',
    '372': '2016.08.09',
    '373': '2016.10.04',
    '374': '2016.12.06',
    '375': '2017.02.07',
    '376': '2017.04.11',
    '377': '2017.06.06',
    '378': '2017.08.01',
    '379': '2017.10.03',
    '380': '2017.12.05'
}