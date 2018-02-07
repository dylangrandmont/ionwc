app.controller('annotationController', ['$scope', '$sce', function($scope, $sce) {

  $scope.advert = {
    label:"Petrel Robertson Consulting Ltd. Reports",
    val: true,
    edges: [{
      url: 'http://ionwc.com/prcl/kml/wilrich.kml?v=3',
      text: "../prcl/prcl-wilrich-report",
      php: 'prcl-wilrich-contactform.php'
    },{
      url:'http://ionwc.com/prcl/kml/bivouac.kml?v=3',
      text: "../prcl/prcl-bivouac-report",
      php: 'prcl-bivouac-contactform.php'
    },{
      url:'http://ionwc.com/prcl/kml/kaybob_notikewin.kml?v=3',
      text: "../prcl/prcl-kaybob-report",
      php: 'prcl-kaybob-contactform.php'
    },{
      url:'http://ionwc.com/prcl/kml/rock_creek.kml?v=3',
      text: "../prcl/prcl-rock-creek-report",
      php: 'prcl-rock-creek-contactform.php'
    },{
      url:'http://ionwc.com/prcl/kml/sagd_screening.kml?v=3',
      text: "../prcl/prcl-sagd-report",
      php: 'prcl-sagd-contactform.php'
    },{
      url:'http://ionwc.com/prcl/kml/wild_river.kml?v3',
      text: "../prcl/prcl-wild-river-report",
      php: 'prcl-wild-river-contactform.php'
    }]
  };

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

  $scope.advertEdges = []
  $scope.geologicalEdges = [];
  $scope.licensingTrends = [];

  var generatePrefix = function(phpFile) {
    return "<img src='../prcl/prcl-logo.jpg' ><div class='ribbon'><span>SUMMARY</span></div><br><br><button class='btn btn-danger' data-toggle='collapse' data-target='#contact-form' style='color: white; background-color: #f4511e'><b>Click to Arrange a Presentation on this Study</b></button><div id='contact-form' class='collapse'><iframe src='../prcl/" + phpFile + "' frameborder='0' width='100%' height='480' ></iframe></div><br>";
  };

  for (var i in $scope.advert.edges) {
    var advertEdge = new google.maps.KmlLayer($scope.advert.edges[i].url, {
      preserveViewport: true,
      suppressInfoWindows: true
    });

    $scope.advertEdges.push(advertEdge);
  }

  angular.element(document).ready(function () {

    google.maps.event.addListener($scope.advertEdges[0], 'click', function(event) {
      var text = $.ajax({
        url: "../prcl/prcl-wilrich-report",
        async: false
      }).responseText;

      pfx = generatePrefix('prcl-wilrich-contactform.php');
      text = pfx + text;

      adContent.innerHTML = text;
      adModal.style.display = "block";
    });

    google.maps.event.addListener($scope.advertEdges[1], 'click', function(event) {
      var text = $.ajax({
        url: "../prcl/prcl-bivouac-report",
        async: false
      }).responseText;

      pfx = generatePrefix('prcl-bivouac-contactform.php');
      text = pfx + text;

      adContent.innerHTML = text;
      adModal.style.display = "block";
    });

    google.maps.event.addListener($scope.advertEdges[2], 'click', function(event) {
      var text = $.ajax({
        url: "../prcl/prcl-kaybob-report",
        async: false
      }).responseText;

      pfx = generatePrefix('prcl-kaybob-contactform.php');
      text = pfx + text;

      adContent.innerHTML = text;
      adModal.style.display = "block";
    });

    google.maps.event.addListener($scope.advertEdges[3], 'click', function(event) {
      var text = $.ajax({
        url: "../prcl/prcl-rock-creek-report",
        async: false
      }).responseText;

      pfx = generatePrefix('prcl-rock-creek-contactform.php');
      text = pfx + text;

      adContent.innerHTML = text;
      adModal.style.display = "block";
    });

    google.maps.event.addListener($scope.advertEdges[4], 'click', function(event) {
      var text = $.ajax({
        url: "../prcl/prcl-sagd-report",
        async: false
      }).responseText;

      pfx = generatePrefix('prcl-sagd-contactform.php');
      text = pfx + text;

      adContent.innerHTML = text;
      adModal.style.display = "block";
    });

    google.maps.event.addListener($scope.advertEdges[5], 'click', function(event) {
      var text = $.ajax({
        url: "../prcl/prcl-wild-river-report",
        async: false
      }).responseText;

      pfx = generatePrefix('prcl-wild-river-contactform.php');
      text = pfx + text;

      adContent.innerHTML = text;
      adModal.style.display = "block";
    });

    for (var i in $scope.advertEdges) {
      $scope.advertEdges[i].setMap(null);
    }
  });

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

  $scope.$watch("advert.val", function(n){
    for (var i in $scope.advertEdges)
    {
      if ($scope.advertEdges[i].getMap() != null) {
        $scope.advertEdges[i].setMap(null);
      } else {
        $scope.advertEdges[i].setMap(map);
      }
    }
  }, true );

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