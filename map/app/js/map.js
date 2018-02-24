var map;

var app = angular.module('mapApp', ['ngAnimate', 'ngSanitize', 'ui.bootstrap', 'ngRoute'])
.config(['$locationProvider', function($locationProvider) {
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
  }])
.controller('mapController', ['$scope', '$rootScope', '$sce', '$location', function($scope, $rootScope, $sce, $location) {

  map = new google.maps.Map(document.getElementById('map'), mapOptions);

  infowindow = new google.maps.InfoWindow();
  infowindow.setZIndex(100);

  $rootScope.dateService = new DateService();

  $rootScope.drillingLayer = new google.maps.FusionTablesLayer({
    suppressInfoWindows: true,
    query: {
      select: 'address',
      from: tableIDs.drilling,
      where:  "'DrillDate' >= '" + $rootScope.dateService.getDefaultWellStartDate() + "'"
    },
    styles: markerColors
  });

  $rootScope.licencingLayer = new google.maps.FusionTablesLayer({
    suppressInfoWindows: true,
    query: {
      select: 'address',
      from: tableIDs.licensing,
      where: "'Date' >= '" + $rootScope.dateService.getDefaultWellStartDate() + "'"
    },
    styles: markerColors
  });

  $rootScope.upComingLandSaleLayer = new google.maps.FusionTablesLayer({
    suppressInfoWindows: true,
    query: {
      select: '\'Geocodable address\'',
      from: tableIDs.upComingLandSale,
      where: "'saleDate' >= '" + $rootScope.dateService.getReformatedDate(new Date()) + "'"
    },
    options: {
      styleId: 2,
      templateId: 2
    }
  });

  $rootScope.previousLandSaleLayer = new google.maps.FusionTablesLayer({
    suppressInfoWindows: true,
    query: {
      select: '\'Geocodable address\'',
      from: tableIDs.previousLandSale
    },
  });

  google.maps.event.addListener($rootScope.drillingLayer, 'click', function(e) {
    if (infowindow) {
      infowindow.close();
    } else {
      infowindow = new google.maps.InfoWindow();
      infowindow.setZIndex(100);
    }

    var content = "<h4 style='font-size:15px; margin-bottom: 10px;'>" + e.row['Licensee'].value.toUpperCase() + "</h4>"
     + "<b>Well Name: </b>" + e.row['Well Name'].value + "<br>"
     + "<b>Licence No.: </b>" + e.row['License Number'].value + "<br>"
     + "<b>UWI: </b>" + e.row['UWI'].value + "<br>"
     + "<b>" + "Spud Date:" + " </b>" + e.row["DrillDate"].value + "<br>"
     + "<b>Field/Pool: </b>" + e.row['Field/Pool'].value + "<br>"
     + "<b>Terminating Zone: </b>" + e.row['TerminatingZone'].value + "<br>"
     + "<b>Orientation: </b>" + e.row['Orientation'].value + "<br>"
     + "<b>Substance: </b>" + e.row['Substance'].value + "<br>"
    
    infoWindowContent = infowindow.setContent(content);
    infowindow.setPosition(e.latLng);
    infowindow.open(map);
  });

  google.maps.event.addListener($rootScope.licencingLayer, 'click', function(e) {
    if (infowindow) {
      infowindow.close();
    } else {
      infowindow = new google.maps.InfoWindow();
      infowindow.setZIndex(100);
    }

    var content = "<h4 style='font-size:15px; margin-bottom: 10px;'>" + e.row['Licensee'].value.toUpperCase() + "</h4>"
     + "<b>Well Name: </b>" + e.row['Well Name'].value + "<br>"
     + "<b>Licence No.: </b>" + e.row['License Number'].value + "<br>"
     + "<b>UWI: </b>" + e.row['UWI'].value + "<br>"
     + "<b>" + "License Date:" + " </b>" + e.row["Date"].value + "<br>"
     + "<b>Field/Pool: </b>" + e.row['Field/Pool'].value + "<br>"
     + "<b>Terminating Zone: </b>" + e.row['TerminatingZone'].value + "<br>"
     + "<b>Orientation: </b>" + e.row['Orientation'].value + "<br>"
     + "<b>Substance: </b>" + e.row['Substance'].value + "<br>"
    
    infoWindowContent = infowindow.setContent(content);
    infowindow.setPosition(e.latLng);
    infowindow.open(map);
  });

  google.maps.event.addListener($rootScope.upComingLandSaleLayer, 'click', function(e) 
  {
    if (infowindow) {
      infowindow.close();
    } else {
      infowindow = new google.maps.InfoWindow();
      infowindow.setZIndex(100);
    }

    var content = "<h4 style='font-size:15px; margin-bottom: 10px;'>" + e.row['contractType'].value + ' ' + e.row['contractNo'].value + "</h4>"
    + "<b>Sale Date: </b>" + e.row['saleDate'].value + "<br>"
    + "<b>Contract Type: </b>" + e.row['contractType'].value + "<br>"
    + "<b>Contract/Parcel No.: </b>" + e.row['contractNo'].value + "<br>"
    + "<b>Size: </b>" + e.row['hectares'].value + " hectares<br>"
    + "<b>Tract No.: </b>" + e.row['tractNo'].value + "<br>"
    + "<b>Legal Coordinates: </b>" + e.row['uwi'].value + "<br>"
    + "<b>Rights: </b>" + e.row['topZone'].value + " " + e.row['baseZone'].value + "<br>";

    infoWindowContent = infowindow.setContent(content);
    infowindow.setPosition(e.latLng);
    infowindow.open(map);   
  });

  google.maps.event.addListener($rootScope.previousLandSaleLayer, 'click', function(e) 
  {
    if (infowindow) {
      infowindow.close();
    } else {
      infowindow = new google.maps.InfoWindow();
      infowindow.setZIndex(100);
    }

    var content = "<h4 style='font-size:15px; margin-bottom: 10px;'>" + e.row['status'].value  + ": " + e.row['contractType'].value + ' ' + e.row['contractNo'].value + "</h4>"
    + "<b>Sale Date: </b>" + e.row['saleDate'].value + "<br>";
    if (e.row['status'].value == 'Accepted') {
      content += "<b>Sale Bonus: </b>" + e.row['bonus'].value + "<br>"
      + "<b>Price Per Hectare: </b>" + e.row['dollarPerHectare'].value + " / hectare" + "<br>"
      + "<b>Buyers: </b>" + e.row['ClientDescription'].value + "<br>";
    }
    content += "<b>Contract Type: </b>" + e.row['contractType'].value + "<br>"
    + "<b>Contract/Parcel No.: </b>" + e.row['contractNo'].value + "<br>"
    + "<b>Size: </b>" + e.row['hectares'].value + " hectares<br>"
    + "<b>Tract No.: </b>" + e.row['tractNo'].value + "<br>"
    + "<b>Legal Coordinates: </b>" + e.row['uwi'].value + "<br>"
    + "<b>Rights: </b>" + e.row['topZone'].value + " " + e.row['baseZone'].value + "<br>";

    infoWindowContent = infowindow.setContent(content);

    infowindow.setPosition(e.latLng);
    infowindow.open(map);   
  });

  google.maps.event.addListener(map, "click", function(event) {
    infowindow.close();
  });

  $scope.disclaimer = $sce.trustAsHtml(disclaimer);
  $scope.copyrightRange = COPYRIGHT_RANGE;
  $scope.dashboardOpen = false;

  $rootScope.showPrevious = false;
  $rootScope.showUpcoming = true;

  $scope.showLegend = false;

  document.getElementById("closeAd").onclick = function() {
    document.getElementById("adModal").style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == infoModal) {
      infoModal.style.display = "none";
    } else if (event.target == document.getElementById("adModal")) {
      document.getElementById("adModal").style.display = "none";
    }
  };

  $('#data-panel').scroll(function(){
    var elementPosition = $('#province-header').offset();
    if ($('#charts').offset().top > 105) {
      $('#province-header').css('position','relative').css('top','0px')
        .css('width','100%');
      $('#province-header-filler').css('height','0px');
    } else if (elementPosition.top <= 55) {
      $('#province-header').css('position','fixed').css('top','55px')
        .css('width',$('#charts').width());
      $('#province-header-filler').css('height','50px');
    }   
  });

  google.maps.event.addListener(map, 'bounds_changed', function() {
    localStorage.neLat = map.getBounds().getNorthEast().lat();
    localStorage.neLng = map.getBounds().getNorthEast().lng();
    localStorage.swLat = map.getBounds().getSouthWest().lat();
    localStorage.swLng = map.getBounds().getSouthWest().lng();
  });

  google.maps.event.addListener(map, 'idle', function() {
    $rootScope.neLat = map.getBounds().getNorthEast().lat();
    $rootScope.neLng = map.getBounds().getNorthEast().lng();
    $rootScope.swLat = map.getBounds().getSouthWest().lat();
    $rootScope.swLng = map.getBounds().getSouthWest().lng();

    if ($rootScope.dashboardWindow) {
      if (!$rootScope.dashboardWindow.closed) {
        localStorage.neLat = $rootScope.neLat;
        localStorage.neLng = $rootScope.neLng;
        localStorage.swLat = $rootScope.swLat;
        localStorage.swLng = $rootScope.swLng;
      }
    }
  });

  $scope.onSelectDrilling = function() {
    $location.search('view', 'drilling');
    $rootScope.viewType = 'Drilling';
    localStorage.viewType = 'Drilling';

    $scope.legend = $sce.trustAsHtml(WELL_LEGEND);
    $scope.dataRangeTable = $sce.trustAsHtml(drillingDateRangeTable);
    $scope.dataAttributions = $sce.trustAsHtml(wellAttributions);

    $rootScope.licencingLayer.setMap(null);
    $rootScope.upComingLandSaleLayer.setMap(null);
    $rootScope.previousLandSaleLayer.setMap(null);
    $rootScope.drillingLayer.setMap(map);
  };

  $scope.onSelectLicencing = function() {
    $location.search('view', 'licences');
    $rootScope.viewType = 'Licences';
    localStorage.viewType = 'Licences';

    $scope.legend = $sce.trustAsHtml(WELL_LEGEND);
    $scope.dataRangeTable = $sce.trustAsHtml(licensingDateRangeTable);
    $scope.dataAttributions = $sce.trustAsHtml(wellAttributions);

    $rootScope.drillingLayer.setMap(null);
    $rootScope.upComingLandSaleLayer.setMap(null);
    $rootScope.previousLandSaleLayer.setMap(null);
    $rootScope.licencingLayer.setMap(map);
  };

  $scope.onSelectLandSales = function() {
    $location.search('view', 'landsales');
    $rootScope.viewType = 'Land Sales';
    localStorage.viewType = 'Land Sales';

    $scope.legend = $sce.trustAsHtml(LAND_SALE_LEGEND);
    $scope.dataRangeTable = $sce.trustAsHtml(landSaleDateRangeTable);
    $scope.dataAttributions = $sce.trustAsHtml(landSaleAttributions);

    $rootScope.drillingLayer.setMap(null);
    $rootScope.licencingLayer.setMap(null);

    if ($rootScope.showUpcoming) {
      $rootScope.upComingLandSaleLayer.setMap(map);
    } else {
      $rootScope.upComingLandSaleLayer.setMap(null);
    }

    if ($rootScope.showPrevious) {
      $rootScope.previousLandSaleLayer.setMap(map);
    } else {
      $rootScope.previousLandSaleLayer.setMap(null);
    }
  };

  handleURLParameters = function() {
    if ($location.search().view == 'drilling') {
      $scope.onSelectDrilling();
    } else if ($location.search().view == 'licences') {
      $scope.onSelectLicencing();
    } else if ($location.search().view == 'landsales') {
      $scope.onSelectLandSales();
    } else {
      $scope.onSelectDrilling();
    }
  };
  handleURLParameters();

  $scope.openDashboard = function() {
    var dashboardHeight = screen.height - 100;

    $rootScope.dashboardWindow = window.open('dashboard.html', 'newwindow', 'width=1140, height=' + dashboardHeight.toString() + ', scrollbars=yes, resizable=yes');
    $scope.dashboardOpen = true;

    var timer = setInterval(checkDashboard, 1500);

    function checkDashboard() {
      if ($rootScope.dashboardWindow.closed) {
        $scope.$apply(function() {
          $scope.dashboardOpen = false;
        });
        clearInterval(timer);
      }
    }
  };

  $scope.toggleFullScreen = function() {
    var elem = document.getElementById("body");
    if (document.requestFullscreen) {
      if (elem.fullScreenElement) {
        document.cancelFullScreen();
      } else {
        elem.requestFullscreen();
      }
    } else if (elem.msRequestFullscreen) {
      if (document.msFullscreenElement) {
        document.msExitFullscreen();
      } else {
        elem.msRequestFullscreen();
      }
    } else if (elem.mozRequestFullScreen) {
      if (document.mozFullScreenElement) {
        document.mozCancelFullScreen();
      } else {
        elem.mozRequestFullScreen();
      }
    } else if (elem.webkitRequestFullscreen) {
      if (document.webkitFullscreenElement) {
        document.webkitCancelFullScreen();
      } else {
        elem.webkitRequestFullscreen();
      }
    }
  }

  $scope.toggleLegend = function() {
    $scope.showLegend = !$scope.showLegend;
  }

}]);

google.charts.load("current", {
  packages:['table','corechart'],
  callback: function() {
    angular.bootstrap(document, ['mapApp']);
  }
});
