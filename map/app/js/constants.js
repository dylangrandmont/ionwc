const WELL_LEGEND = "<svg height='10' width='10'>"+
  "<circle cx='5' cy='5' r='4' stroke='black' stroke-width='1' fill='rgb(0,255,0)' />"+
  "</svg> Oil Wells<br><svg height='10' width='10'>"+
  "<circle cx='5' cy='5' r='4' stroke='black' stroke-width='1' fill='rgb(255,0,0)' />"+
  "</svg> Gas Wells<br><svg height='10' width='10'>"+
  "<circle cx='5' cy='5' r='4' stroke='black' stroke-width='1' fill='rgb(0,0,255)' />"+
  "</svg> Water Wells<br><svg height='10' width='10'>"+
  "<circle cx='5' cy='5' r='4' stroke='black' stroke-width='1' fill='rgb(255,255,0)' />"+
  "</svg> Uncategorized Substance<br>"+
  "<svg height='11' width='20'><rect height='10' width='20' stroke='rgb(244, 81, 30)' stroke-width='1' fill='rgb(255,255,255)' /></svg> Proprietary Report Coverage";

const LAND_SALE_LEGEND = "<svg height='10' width='10'>"+
  "<rect height='10' width='10' stroke='rgb(84, 84, 84)' stroke-width='1' fill='rgb(50,226,205)' /></svg>" +
  "<svg height='10' width='10'>"+
  "<rect height='10' width='10' stroke='rgb(84, 84, 84)' stroke-width='2' fill='rgb(50,226,205)' /></svg> Upcoming Sales" +
  "<br>" +
  "<svg height='10' width='10'><rect height='10' width='10' stroke='rgb(84, 84, 84)' stroke-width='1' fill='rgb(255,0,0)' /></svg>" +
  "<svg height='10' width='10'><rect height='10' width='10' stroke='rgb(84, 84, 84)' stroke-width='2' fill='rgb(255,0,0)' /></svg> Past Sales"+
  "<br>" +
  "<svg height='11' width='20'><rect height='10' width='20' stroke='rgb(244, 81, 30)' stroke-width='1' fill='rgb(255,255,255)' /></svg> Proprietary Report Coverage";

var licensingDateRangeTable = "<table class='range-table'><tr><th class='range-th'>Province</th><th class='range-th'>Begin Date</th><th class='range-th'>End Date</th></tr><tr><td class='range-td'>BC</td><td class='range-td'>01/01/2011</td><td class='range-td'>Present</td></tr><tr><td class='range-td'>AB</td><td class='range-td'>01/01/2011</td><td class='range-td'>Present</td></tr><tr><td class='range-td'>SK</td><td class='range-td'>01/01/2011</td><td class='range-td'>Present</td></tr><tr><td class='range-td'>MB</td><td class='range-td'>01/01/2011</td><td class='range-td'>Present</td></tr></table>";
var drillingDateRangeTable = "<table class='range-table'><tr><th class='range-th'>Province</th><th class='range-th'>Begin Date</th><th class='range-th'>End Date</th></tr><tr><td class='range-td'>BC</td><td class='range-td'>01/01/2010</td><td class='range-td'>Present</td></tr><tr><td class='range-td'>AB</td><td class='range-td'>01/01/2012</td><td class='range-td'>Present</td></tr><tr><td class='range-td'>SK</td><td class='range-td'>11/19/2015</td><td class='range-td'>Present</td></tr><tr><td class='range-td'>MB</td><td class='range-td'>06/09/2012</td><td class='range-td'>Present</td></tr></table>";

var landSaleDateRangeTable = "<table class='range-table'>" +
"<tr><th class='range-th'>Province</th><th class='range-th'>Begin Date</th><th class='range-th'>End Date</th></tr>" +
"<tr><td class='range-td'>BC</td><td class='range-td'>01/01/2016</td><td class='range-td'>Present</td></tr>" +
"<tr><td class='range-td'>AB</td><td class='range-td'>01/01/2016</td><td class='range-td'>Present</td></tr>" +
"<tr><td class='range-td'>SK</td><td class='range-td'>01/01/2016</td><td class='range-td'>Present</td></tr>" +
"<tr><td class='range-td'>MB</td><td class='range-td'>01/01/2016</td><td class='range-td'>Present</td></tr>" +
"</table>";

var wellAttributions = "<p>Well data is sourced from provincial regulators: <a href='https://www.bcogc.ca/industry-zone/activity-levels' target='_blank'>British Columbia Oil and Gas Commission</a>, <a href='http://www.aer.ca/data-and-publications/statistical-reports/st1' target='_blank'>Alberta Energy Regulator</a>, government of <a href='http://www.economy.gov.sk.ca/oilandgas/wellbullfile/archives/' target='_blank'>Saskatchewan</a>, and government of <a href='http://www.gov.mb.ca/iem/petroleum/reports/' target='_blank'>Manitoba</a>. Geological edges are sourced from the Alberta Geological Survey's <a href='http://ags.aer.ca/reports/atlas-of-the-western-canada-sedimentary-basin' target='_blank'>Atlas of the Western Canada Sedimentary Basin</a>. The DLS grid as well as the British Columbia NTS grids are sourced from Natural Resources Canada and are available under the Open Government Licence <a href='http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst/f907a02c-f592-5261-ab4e-4bdae67a73ad.html'>here</a>.</p>"
var landSaleAttributions = "Land posting data is sourced from provincial bodies: <a href='http://www.energy.alberta.ca/Tenure/607.asp' target='_blank'>Alberta Energy</a>, <a href='http://www2.gov.bc.ca/gov/content/industry/natural-gas-oil/petroleum-natural-gas-tenure' target='_blank'>government of British Columbia</a>, <a href='http://www.economy.gov.sk.ca/pngdispositions' target='_blank'>government of Saskatchewan</a>, and <a href='http://www.gov.mb.ca/iem/petroleum/landinfo/landsale.html' target='_blank'>government of Manitoba</a>. Geological edges are sourced from the Alberta Geological Survey's <a href='http://ags.aer.ca/reports/atlas-of-the-western-canada-sedimentary-basin' target='_blank'>Atlas of the Western Canada Sedimentary Basin</a>. The DLS grid as well as the British Columbia NTS grids are sourced from Natural Resources Canada and are available under the Open Government Licence <a href='http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst/f907a02c-f592-5261-ab4e-4bdae67a73ad.html'>here</a>.";

var disclaimer = "The information contained within this page is believed to be true and accurate at its time \
	of production. Nonetheless, Eye on Western Canada shall not be liable for the accuracy of such information and \
	the information contained herein shall be used at the sole risk and discretion of the user.";

const COPYRIGHT_RANGE = "2016-2018";

var mapOptions = {
  center: {lat: 56, lng: -111},
  zoom: 5,
  scaleControl: true,
  streetViewControl: false,
  mapTypeId: google.maps.MapTypeId.TERRAIN,
  mapTypeControlOptions: {position: google.maps.ControlPosition.BOTTOM_CENTER},
};

var chartOptions = {
  colors: ['#f4511e'], 
  title: '',
  titleTextStyle: {fontName: 'Arial', fontSize: 14,  bold: true},       
  legend: 'none', 
  width: 320,
  height: 250,
  hAxis: {},
  vAxis: {format: 'short'},
  chartArea: {left: '14%', width:'89%'}
}

var tableOptions = {
  width: 320,
  height:300
};

var stubChartOptions = {
  colors: ['#f4511e'], 
  title: '',
  titleTextStyle: {fontName: 'Arial', fontSize: 14,  bold: true},       
  legend: 'none', 
  width: 320,
  height: 250,
  hAxis: {textPosition: 'none'},
  vAxis: {format: 'short'},
  chartArea: {left: '14%', width:'89%', top:'20%', height:'80%'}
};

var pieChartOptions = { 
  titleTextStyle: {fontName: 'Arial', fontSize: 14,  bold: true},
  title: '',
  width: 320, 
  height: 200,  
  is3D: true,
  chartArea: {width:'92%', height: '80%',top:'20%', left: '4%'},
  sliceVisibilityThreshold: 0.01,   
  pieSliceTextStyle: {color: 'black'},
  legend: {position: 'labeled'},
  pieSliceText: 'none'
};

var markerColors = [
  {where: "'SubstanceCode' = 4", markerOptions: { iconName: "small_yellow"}},
  {where: "'SubstanceCode' = 2", markerOptions:{ iconName: "measle_brown"}},
  {where: "'SubstanceCode' = 0", markerOptions:{ iconName: "small_green"}},
  {where: "'SubstanceCode' = 3", markerOptions:{ iconName: "small_blue"}}
];

var tableIDs = {
  drilling: '1lc9vWq_M45gnsL5VLLNsLKBPlPQ2LgCOWxt_kUHI',
  licensing: '1c5dt503OlbDr5-nRRP-xsotq3cTuJeBx3p5K_Ri7',
  upComingLandSale: '1kEPGipJ6rVtYNDcj96g7sGwzCvdxlY2WyU1cHY-L',
  previousLandSale: '1jCuFLgiI-K7ftnl7OGewbeQ2yLkNuRKOWgYckHp3'
};

var zones = [
  {
    label: 'All Formations (Surface-Basement)',
    age: '-1'
  },
  {
    label: 'Surface',
    age: '0'
  },
  {
    label: 'Belly River',
    age: '750'
  },
  {
    label: 'Cardium',
    age: '910'
  },
  {
    label: 'Viking',
    age: '1020'
  },
  {
    label: 'Bluesky',
    age: '1040'
  },
  {
    label: 'Nordegg',
    age: '1910'
  },
  {
    label: 'Charlie Lake',
    age: '2370'
  },
  {
    label: 'Halfway',
    age: '2420'
  },
  {
    label: 'Montney',
    age: '2520'
  },
  {
    label: 'Belloy',
    age: '2990'
  },
  {
    label: 'Debolt',
    age: '3420'
  },
  {
    label: 'Bakken/Exshaw',
    age: '3600'
  },
  {
    label: 'Nisku',
    age: '3780'
  },
  {
    label: 'Duvernay',
    age: '3800'
  },
  {
    label: 'Leduc',
    age: '3800'
  },
  {
    label: 'Slave Point',
    age: '3840'
  },
  {
    label: 'Basement',
    age: '9999'
  }
];
