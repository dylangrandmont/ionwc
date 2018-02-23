var dashboardApp = angular.module('dashboardApp', [])
.controller('dashboardController', ['$scope', function($scope) {

  var topOperatorsData,
      topZonesData,
      topFluidsData;

  var topOperators = new google.visualization.ColumnChart(document.getElementById('licenseeChart')),
      topOperatorsTable = new google.visualization.Table(document.getElementById('licenseeTable')),
      topZones = new  google.visualization.ColumnChart(document.getElementById('zoneChart')),
      topZonesTable = new  google.visualization.Table(document.getElementById('zoneTable')),
      topFluids = new google.visualization.PieChart(document.getElementById('fluidChart'));

  selectHandlerOperators = function() {
    selectHandler(topOperators, topOperatorsData, 'operator');
  };

  selectHandlerZones = function() {
    selectHandler(topZones, topZonesData, 'zone');
  };

  selectHandlerOperatorsTable = function() {
    selectHandler(topOperatorsTable, topOperatorsData, 'operator');
  };

  selectHandlerZonesTable = function() {
    selectHandler(topZonesTable, topZonesData, 'zone');
  };

  selectHandlerFluids = function() {
    selectHandler(topFluids, topFluidsData, 'fluid');
  };

  selectHandler = function(vizualization, dataTable, type) {
    var selectedItem = vizualization.getSelection()[0];

    if (type === 'operator') {
      localStorage.licensee = dataTable.getValue(selectedItem.row, 0);
    } else if (type == 'zone') {
      localStorage.zone = dataTable.getValue(selectedItem.row, 0);
    } else if (type === 'fluid') {
      localStorage.fluid = dataTable.getValue(selectedItem.row, 0);
    }

    updateCharts();
  };

  google.visualization.events.addListener(topOperators, 'select', selectHandlerOperators);
  google.visualization.events.addListener(topOperatorsTable, 'select', selectHandlerOperatorsTable);
  google.visualization.events.addListener(topZones, 'select', selectHandlerZones);
  google.visualization.events.addListener(topZonesTable, 'select', selectHandlerZonesTable);
  google.visualization.events.addListener(topFluids, 'select', selectHandlerFluids);

  $scope.viewType = localStorage.viewType;
  $scope.copyrightRange = COPYRIGHT_RANGE;

  window.addEventListener('storage', function() {
    updateCurrentView();
  }, false);

  $scope.resetLicensee = function() {
    localStorage.licensee = '';

    updateCharts();
  }

  $scope.resetZone = function() {
    localStorage.zone = '';

    updateCharts();
  }

  $scope.resetFluid = function() {
    localStorage.fluid = '';

    updateCharts();
  }

  $scope.resetAll = function() {
    localStorage.licensee = '';
    localStorage.zone = '';
    localStorage.fluid = '';

    updateCharts();
  }

  var updateCurrentView = function() {
    $scope.viewType = localStorage.viewType;

    if (localStorage.viewType === 'Drilling') {
      onDrillingSelected();
    } else if (localStorage.viewType === 'Licences') {
      onLicencesSelected();
    }

    updateCharts();
  };

  onDrillingSelected = function() {
    $scope.infoWindowDate = "Spud Date:"; 
    $scope.tableID = '1lc9vWq_M45gnsL5VLLNsLKBPlPQ2LgCOWxt_kUHI';
    $scope.statsTableTotalLabel = 'Total Displayed Spuds';
    $scope.chartDataType = "Spuds"; 
    $scope.chartTitle = "Wells Spudded";
    $scope.dataDate = "DrillDate";
    $scope.data = {title:"Well Activity"};
  }

  onLicencesSelected = function() {
    $scope.infoWindowDate = "License Date:"; 
    $scope.tableID = '1c5dt503OlbDr5-nRRP-xsotq3cTuJeBx3p5K_Ri7';
    $scope.statsTableTotalLabel = 'Total Displayed Licences';
    $scope.chartDataType = "Licences"; 
    $scope.chartTitle = "Issued Licences"; 
    $scope.dataDate = "Date";
    $scope.data = {title:"Well Licences"};
  }

  updateCharts = function() {
      updateOperatorsChart();
      updateZonesChart();
      updateFluidsChart();
      updateTimeChart();
  }

  var updateOperatorsChart = function() {
    var queryOperators = "SELECT 'Licensee', count(Licensee) AS " + $scope.chartDataType + " FROM " + 
      $scope.tableID + " WHERE 'Licensee' CONTAINS IGNORING CASE '" + localStorage.licensee + 
      "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + localStorage.zone + "' AND 'Substance' CONTAINS IGNORING CASE '" + 
      localStorage.fluid + "' AND '" + $scope.dataDate + "' >= '" +  localStorage.fromDate + "' AND '" + $scope.dataDate + "' <= '" 
      + localStorage.toDate + "' AND 'latitude' >= '" + localStorage.swLat + "' AND 'latitude' <= '" + localStorage.neLat 
      + "' AND 'longitude' <= '" + localStorage.neLng + "' AND 'longitude' >= '" + localStorage.swLng 
      + "' GROUP BY 'Licensee' ORDER BY count(Licensee) desc LIMIT 15 ";           

    var gvizQueryOperators = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + encodeURIComponent(queryOperators));

    gvizQueryOperators.send(function(response) {
      if (response !== null && response !== undefined) {

        topOperatorsData = response.getDataTable();

          var view = new google.visualization.DataView(topOperatorsData);

          topOperators.draw(view, {
            colors: ['#f4511e'], 
            title: 'Most Active Licensees',
            titleTextStyle: {fontName: 'Arial', fontSize: 16,  bold: true},       
            legend: 'none', 
            width: 329,
            height: 200,
            hAxis: {textPosition: 'none', count: -1},
            vAxis: {format: 'short', minValue:0, maxValue :4},
            chartArea: {left: '14%', width:'89%', top:'20%', height:'80%'}
          });

          topOperatorsTable.draw(topOperatorsData, {width: 328, height: 338});
      }
    });
  };

  var updateZonesChart = function() {
    var queryZones = "SELECT 'TerminatingZone' AS 'Terminating Zone', count(TerminatingZone) AS " + $scope.chartDataType + 
      " FROM " + $scope.tableID + " WHERE 'Licensee' CONTAINS IGNORING CASE '" + localStorage.licensee + 
      "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + localStorage.zone + 
      "' AND 'Substance' CONTAINS IGNORING CASE '" + localStorage.fluid + "' AND '" + $scope.dataDate + "' >= '" + 
      localStorage.fromDate + "' AND '" + $scope.dataDate + "' <= '" + localStorage.toDate + 
      "' AND 'latitude' >= '" + localStorage.swLat + "' AND 'latitude' <= '" + localStorage.neLat + 
      "' AND 'longitude' <= '" + localStorage.neLng + "' AND 'longitude' >= '" + localStorage.swLng + 
      "' GROUP BY 'TerminatingZone' ORDER BY count(TerminatingZone) desc LIMIT 15 ";       

    var gvizQueryZones = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + encodeURIComponent(queryZones));

    gvizQueryZones.send(function(response) {
      if (response !== null && response !== undefined) {

        topZonesData = response.getDataTable();

          var view = new google.visualization.DataView(topZonesData);

          topZones.draw(view, {
            colors: ['#f4511e'], 
            title: 'Most Active Formations',
            titleTextStyle: {fontName: 'Arial', fontSize: 16,  bold: true},       
            legend: 'none', 
            width: 329,
            height: 200,
            hAxis: {textPosition: 'none', count: -1},
            vAxis: {format: 'short', minValue:0, maxValue :4},
            chartArea: {left: '14%', width:'89%', top:'20%', height:'80%'}
          });

          topZonesTable.draw(topZonesData, {width: 329, height: 338});
      }
    });
  };

  var updateFluidsChart = function() {
    var queryFluids = "SELECT 'Substance', count(Substance) FROM " + $scope.tableID + 
    " WHERE 'Licensee' CONTAINS IGNORING CASE '" + localStorage.licensee + 
    "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + localStorage.zone + 
    "' AND 'Substance' CONTAINS IGNORING CASE '" + localStorage.fluid + "' AND '" + $scope.dataDate + "' >= '" + 
    localStorage.fromDate + "' AND '" + $scope.dataDate + "' <= '" + localStorage.toDate + "' AND 'latitude' >= '" + localStorage.swLat + "' AND 'latitude' <= '" + localStorage.neLat + 
    "' AND 'longitude' <= '" + localStorage.neLng + "' AND 'longitude' >= '" + localStorage.swLng + 
    "' GROUP BY 'Substance'";           

    var gvizQueryFluids = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + encodeURIComponent(queryFluids));

    gvizQueryFluids.send(function(response) {
      if (response !== null && response !== undefined) {

        topFluidsData = response.getDataTable();

        var slicesColor = {};

        for (var i = 0; i < topFluidsData.getNumberOfRows(); i++){
          if (topFluidsData.getValue(i, 0) == 'Crude Bitumen'){ 
            slicesColor[i] = {color: 'rgb(194, 134, 73)' };
          } else if (topFluidsData.getValue(i, 0) =='Crude Oil') {
            slicesColor[i] = {color: 'rgb(111, 255, 111)' };
          } else if (topFluidsData.getValue(i, 0) == 'Gas') {
            slicesColor[i] = {color: 'rgb(255, 66, 66)' };
          } else if (topFluidsData.getValue(i, 0) == 'Water'){
            slicesColor[i] = {color: 'rgb(106, 106, 255)' };
          }
        }

        var view = new google.visualization.DataView(topFluidsData);

        topFluids.draw(view, { 
          titleTextStyle: {fontName: 'Arial', fontSize: 16,  bold: true},
          title: $scope.chartDataType + ' by Licensed Substance',
          width: 443, 
          height: 300,  
          is3D: true,
          chartArea: {width:'100%'},
          slices : slicesColor,
          sliceVisibilityThreshold: 0.01,   
          pieSliceTextStyle: {color: 'black', fontSize: 12},
          legend: {position: 'labeled'},
        });
      }
    });
  };

  var updateTimeChart = function() {
    var query = "SELECT '" + $scope.dataDate + "', count(" + $scope.dataDate + ") AS " + $scope.chartDataType + " FROM " + 
    $scope.tableID + " WHERE 'Licensee' CONTAINS IGNORING CASE '" + localStorage.licensee + 
    "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + localStorage.zone + 
    "' AND 'Substance' CONTAINS IGNORING CASE '" + localStorage.fluid + "' AND '" + $scope.dataDate + 
    "' >= '" +  localStorage.fromDate + "' AND '" + $scope.dataDate + "' <= '" + localStorage.toDate + "' AND 'latitude' >= '" + localStorage.swLat + "' AND 'latitude' <= '" + 
    localStorage.neLat + "' AND 'longitude' <= '" + localStorage.neLng + "' AND 'longitude' >= '" + localStorage.swLng + 
    "' GROUP BY '" + $scope.dataDate + "' ORDER BY '" + $scope.dataDate + "'";

    var gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + encodeURIComponent(query));

    gvizQuery.send(function(response) {
      if (response !== null && response !== undefined) {
        var dates = new google.visualization.ColumnChart(document.getElementById('timeChart'));
        var data = response.getDataTable();
        var view = new google.visualization.DataView(data);
        dates.draw(view, { 
          colors: ['#f4511e'],
          title: 'Daily Well ' + $scope.chartDataType + ' over Time',
          legend: 'none', 
          height: '350', 
          vAxis: {format: "#", minValue: 0, maxValue: 4},
          bar: {groupWidth: "95%"},
          hAxis: {},
          chartArea: {left: '6%', width:'92%'}
        });
      }
    });
  };

  updateCurrentView();
}]);


google.charts.load("current", {packages:['table','corechart']});
google.charts.setOnLoadCallback(function() {
    angular.bootstrap(document, ['dashboardApp']);
});