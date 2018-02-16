app.controller('annotationController', ['$scope', '$sce', function($scope, $sce) {

  $scope.geoEdgesCheckboxes = [{
    label:"Upper Cardium Shoreface",
    val:false,
    url: 'http://ionwc.com/data/kml/fg2304c_uppshoreface.kml'
  },{
    label:"Middle Cardium Shoreface",
    val:false,
    url: 'http://ionwc.com/data/kml/fg2304b_MidShoreface.kml'
  },{
    label:"Lower Cardium Barrier Sand",
    val:false,
    url: 'http://ionwc.com/data/kml/fg2304a_LwrBar.kml'
  },{
    label:"Oil Sands",
    val:false,
    url: 'http://ionwc.com/data/kml/fg2304a_LwrBar.kml'
  },{
    label:"Triassic Subcrop",
    val:false,
    url: 'http://ionwc.com/data/kml/triassic_subcrop.kml'
  },{
    label:"Permian Subcrop",
    val:false,
    url: 'http://ionwc.com/data/kml/fg1513_ln_II.kml'
  },{
    label:"Stoddart Subcrop",
    val:false,
    url: 'http://ionwc.com/data/kml/fg1408_Stoddart.kml'
  },{
    label:"Banff/Exshaw/Bakken Subcrop",
    val:false,
    url: 'http://ionwc.com/data/kml/fg1408_bnffexsw.kml'
  },{
    label:"Wabamun Subcrop",
    val:false,
    url: 'http://ionwc.com/data/kml/fg1335_ln_II.kml'
  },{
    label:"Beaver Hill Lake Reef/Bank Margin",
    val:false,
    url: 'http://ionwc.com/data/kml/BHL_MarginsReefs.kml'
  },{
    label:"Leduc Reefs and Platforms",
    val:false,
    url: 'http://ionwc.com/data/kml/leduc_reef.kml'
  },{
    label:"Presqu'ile Barrier",
    val:false,
    url: 'http://ionwc.com/data/kml/presquile_barrier.kml'
  },{
    label:"Dawson Creek Graben Complex",
    val:false,
    url: 'http://ionwc.com/data/kml/dawson_graben_complex.kml'
  },{
    label:"Liard Basin",
    val:false,
    url:'http://ionwc.com/data/kml/liard_basin.kml'
  },{
    label:"Sedimentary Basin Edge",
    val:false,
    url: 'http://ionwc.com/data/kml/wcsb.kml'
  }];

  $scope.licensingTrendsCheckboxes = [{
    label: 'Bakken Trend',
    val: false,
    queryWhere: "'TerminatingZone' CONTAINS IGNORING CASE 'bakken'"
  },{
    label: 'Bluesky Trend',
    val: false,
    queryWhere: "'TerminatingZone' CONTAINS IGNORING CASE 'bluesky'"
  },{
    label: 'Cardium Trend',
    val: false,
    queryWhere: "'TerminatingZone' CONTAINS IGNORING CASE 'cardium'"
  },{
    label: 'Duvernay Trend',
    val: false,
    queryWhere: "'TerminatingZone' CONTAINS IGNORING CASE 'duvernay'"
  },{
    label: 'McMurray Trend',
    val: false,
    queryWhere: "'TerminatingZone' CONTAINS IGNORING CASE 'mcmurray'"
  },{
    label: 'Oil Sands (All) Trend',
    val: false,
    queryWhere: "'SubstanceCode'='2'"
  },{
    label: 'Montney Trend',
    val: false,
    queryWhere: "'TerminatingZone' CONTAINS IGNORING CASE 'montney'"
  },{
    label: 'Viking Trend',
    val: false,
    queryWhere: "'TerminatingZone' CONTAINS IGNORING CASE 'viking'"
  }];

  $scope.geologicalEdges = [];
  $scope.licensingTrends = [];

  for (var i in $scope.geoEdgesCheckboxes) {
    var geologicalEdge = new google.maps.KmlLayer($scope.geoEdgesCheckboxes[i].url, {
      preserveViewport: true,
      suppressInfoWindows: true
    });

    $scope.geologicalEdges.push(geologicalEdge);
  }

  for (var i in $scope.licensingTrendsCheckboxes) {
    var licensingTrend = new google.maps.FusionTablesLayer({
      query: {
        select: '\'Geocodable address\'',
        from: '1y5xOfRjx-FnsGz7LWc4SeJNoOxgG54i7V-6iEsnX',
        where: $scope.licensingTrendsCheckboxes[i].queryWhere
      },
      heatmap: {
        enabled: true
      }
    });
    $scope.licensingTrends.push(licensingTrend);
  }

  $scope.$watch("geoEdgesCheckboxes", function(n){
    for (var i in n) {
      if (n[i].val) {
        $scope.geologicalEdges[i].setMap(map);
      } else {
        $scope.geologicalEdges[i].setMap(null);
      }
    }
  }, true );

  $scope.$watch("licensingTrendsCheckboxes", function(n){
    for (var i in n) {
      if (n[i].val) {
        $scope.licensingTrends[i].setMap(map);
      } else {
        $scope.licensingTrends[i].setMap(null);
      }
    }
  }, true );
}]);
