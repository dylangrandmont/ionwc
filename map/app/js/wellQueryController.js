app.controller('wellQueryController', ['$scope', '$rootScope', '$location', function($scope, $rootScope, $location) {

  $scope.licensee = '';
  $scope.zone = '';
  $scope.fluid = '';
  $scope.format = 'dd-MMM-yyyy';
  $scope.toDate = new Date();
  $scope.fromDate = $rootScope.dateService.getDefaultWellStartDate();

  localStorage.licensee = $scope.licensee;
  localStorage.zone = $scope.zone;
  localStorage.fluid = $scope.fluid;
  localStorage.fromDate = $rootScope.dateService.getReformatedDate($scope.fromDate);
  localStorage.toDate = $rootScope.dateService.getReformatedDate($scope.toDate);

  $scope.fromDateOptions = {
    maxDate: new Date(2020, 0, 0),
    minDate: new Date(2010, 0, 0),
    showWeeks: false
  };

  $scope.toDateOptions = {
    minDate: new Date(2010, 0, 0),
    maxDate: new Date(2020, 0, 0),
    showWeeks: false
  };

  $scope.openFromDate = function() {
    $scope.fromDatePopup.opened = true;
  };

  $scope.openToDate = function() {
    $scope.toDatePopup.opened = true;
  };

  $scope.$watch('fromDate', function() {
    $scope.onWellQueryChange(true)
  });

  $scope.$watch('toDate', function() {
    $scope.onWellQueryChange(true)
  });

  $rootScope.$watch('viewType', function() {
    $scope.onWellQueryChange(true)
  });

  $scope.fromDatePopup = {
    opened: false
  };

  $scope.toDatePopup = {
    opened: false
  };

  var stubChartOptionsOp = JSON.parse(JSON.stringify(stubChartOptions));
  var stubChartOptionsZn = JSON.parse(JSON.stringify(stubChartOptions));

  stubChartOptionsOp.title = "Most Active Operators";
  stubChartOptionsZn.title = "Most Active Zones";

  google.maps.event.addListener(map, 'idle', function() {
    updateVizualizations();
  });

  window.addEventListener("storage", function () {
    if ($rootScope.dashboardWindow) {
      if (!$rootScope.dashboardWindow.closed) {
        $scope.$apply(function(){
          $scope.licensee = localStorage.licensee;
          $scope.zone = localStorage.zone;
          $scope.fluid = localStorage.fluid;
        });

        $scope.onWellQueryChange(false);
      }
    }
  }, false);

  var getPrevNextDate = function(date, increment)
  {
    var newDate = new Date(date.getTime() + increment);
    return newDate;
  };

  var canAccessGoogleVisualization = function() 
  {
    if ((typeof google === 'undefined') || (typeof google.visualization === 'undefined')) {
      return false;
    } else {
      return true;
    }
  };

  var updateVizualizations = function() {
    var tableID = ($rootScope.viewType === 'Drilling') ? tableIDs.drilling : tableIDs.licensing;
    var dateString = ($rootScope.viewType === 'Drilling') ? 'DrillDate' : 'Date';
    var statsTableTotalLabel = ($rootScope.viewType === 'Drilling') ? 'Total Displayed Spuds' : 'Total Displayed Licences';
    var chartDataType = ($rootScope.viewType === 'Drilling') ? 'Spuds' : 'Licences';
    chartOptions.title = "Well " + chartDataType + " with Time";

    if(canAccessGoogleVisualization()) {

    google.visualization.drawChart({
      "containerId": "well-count",
      "dataSourceUrl": "//www.google.com/fusiontables/gvizdata?tq=", 
      "query": "SELECT count(Licensee) AS '" + statsTableTotalLabel + "' FROM " + tableID + 
        " WHERE 'Licensee' CONTAINS IGNORING CASE '" + $scope.licensee + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + 
        $scope.zone + "' AND 'Substance' CONTAINS IGNORING CASE '" + $scope.fluid + "' AND  '" + 
        dateString + "' >= '" + $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND '" + dateString + "' <= '" + 
        $rootScope.dateService.getReformatedDate($scope.toDate) + "' AND 'latitude' >= '" + $rootScope.swLat + "' AND 'latitude' <= '" + 
        $rootScope.neLat + "' AND 'longitude' <= '" + $rootScope.neLng + "' AND 'longitude' >= '" + 
        $rootScope.swLng + "'",
      "chartType": "Table",
      "options": {width: 320}
    });

    google.visualization.drawChart({
      "containerId": "operators-table",
      "dataSourceUrl": "//www.google.com/fusiontables/gvizdata?tq=", 
      "query":"SELECT 'Licensee' AS 'Top Operators', count(Licensee) AS Count FROM " + tableID + 
        " WHERE 'Licensee' CONTAINS IGNORING CASE '" + $scope.licensee + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + 
        $scope.zone + "' AND 'Substance' CONTAINS IGNORING CASE '" + $scope.fluid + "' AND  '" + 
        dateString + "' >= '" + $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND '" + dateString + "' <= '" + 
        $rootScope.dateService.getReformatedDate($scope.toDate) + "' AND 'latitude' >= '" + $rootScope.swLat + "' AND 'latitude' <= '" + 
        $rootScope.neLat + "' AND 'longitude' <= '" + $rootScope.neLng + "' AND 'longitude' >= '" + 
        $rootScope.swLng + "' GROUP BY 'Licensee' ORDER BY count(Licensee) desc LIMIT 15 ",
       "chartType": "Table",
       "options": {width: 320}
    });

    google.visualization.drawChart({
      "containerId": "zones-table",
      "dataSourceUrl": "//www.google.com/fusiontables/gvizdata?tq=", 
      "query":"SELECT 'TerminatingZone' AS 'Top Terminating Zones', count(TerminatingZone) AS Count FROM " + tableID + 
        " WHERE 'Licensee' CONTAINS IGNORING CASE '" + $scope.licensee + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + 
        $scope.zone + "' AND 'Substance' CONTAINS IGNORING CASE '" + $scope.fluid + "' AND  '" + 
        dateString + "' >= '" + $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND '" + dateString + "' <= '" + 
        $rootScope.dateService.getReformatedDate($scope.toDate) + "' AND 'latitude' >= '" + $rootScope.swLat + "' AND 'latitude' <= '" + 
        $rootScope.neLat + "' AND 'longitude' <= '" + $rootScope.neLng + "' AND 'longitude' >= '" + 
        $rootScope.swLng + "' GROUP BY 'TerminatingZone' ORDER BY count(TerminatingZone) desc LIMIT 15 ",
      "chartType": "Table",
      "options": {width: 320}
    });

    google.visualization.drawChart({
      "containerId": "operators-chart",
      "dataSourceUrl": "//www.google.com/fusiontables/gvizdata?tq=", 
      "query":"SELECT 'Licensee', count(Licensee) AS '' FROM " + tableID + " WHERE 'Licensee' CONTAINS IGNORING CASE '" + 
        $scope.licensee + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + $scope.zone + 
        "' AND 'Substance' CONTAINS IGNORING CASE '" + $scope.fluid  + "' AND  '" + dateString + 
        "' >= '" + $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND '" + dateString + "' <= '" + $rootScope.dateService.getReformatedDate($scope.toDate) + 
        "' AND 'latitude' >= '" + $rootScope.swLat + "' AND 'latitude' <= '" + 
          $rootScope.neLat + "' AND 'longitude' <= '" + $rootScope.neLng + "' AND 'longitude' >= '" + 
          $rootScope.swLng + "' GROUP BY 'Licensee' ORDER BY count(Licensee) desc LIMIT 15 ",
      "chartType": "ColumnChart",
      "options": stubChartOptionsOp
    });
    
    google.visualization.drawChart({
      "containerId": "zones-chart",
      "dataSourceUrl": "//www.google.com/fusiontables/gvizdata?tq=", 
      "query":"SELECT 'TerminatingZone' AS 'Terminating Zone', count(TerminatingZone) AS '' FROM " + tableID + 
        " WHERE 'Licensee' CONTAINS IGNORING CASE '" + $scope.licensee + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + 
        $scope.zone + "' AND 'Substance' CONTAINS IGNORING CASE '" + $scope.fluid + "' AND  '" + dateString + "' >= '" + 
        $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND '" + dateString + "' <= '" + $rootScope.dateService.getReformatedDate($scope.toDate) + 
        "' AND 'latitude' >= '" + $rootScope.swLat + "' AND 'latitude' <= '" + 
        $rootScope.neLat + "' AND 'longitude' <= '" + $rootScope.neLng + "' AND 'longitude' >= '" + 
        $rootScope.swLng + "' GROUP BY 'TerminatingZone' ORDER BY count(TerminatingZone) desc LIMIT 15 ",
      "chartType": "ColumnChart",
      "options": stubChartOptionsZn
    });
    
    var query = "SELECT '" + dateString + "', count(" + dateString + ") AS " + chartDataType + " FROM " + tableID + 
      " WHERE 'Licensee' CONTAINS IGNORING CASE '" + $scope.licensee + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + 
      $scope.zone + "' AND 'Substance' CONTAINS IGNORING CASE '" + $scope.fluid + "' AND '" + dateString + "' >= '" + 
      $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND '" + dateString + "' <= '" + $rootScope.dateService.getReformatedDate($scope.toDate) + 
      "' AND 'latitude' >= '" + $rootScope.swLat + "' AND 'latitude' <= '" + 
      $rootScope.neLat + "' AND 'longitude' <= '" + $rootScope.neLng + "' AND 'longitude' >= '" + 
      $rootScope.swLng + "' GROUP BY '" + dateString + "' ORDER BY '" + dateString + "'";
    var queryText = encodeURIComponent(query);
    var gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);

    gvizQuery.send(function(response) 
    {
      var dates = new google.visualization.ColumnChart(document.getElementById('variation-time'));
      var data = response.getDataTable();
      var view = new google.visualization.DataView(data);
      dates.draw(view, chartOptions);
    });
    
    query = "SELECT 'Substance', count(Substance) FROM " + tableID + " WHERE 'Licensee' CONTAINS IGNORING CASE '" + 
      $scope.licensee + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + $scope.zone + 
      "' AND 'Substance' CONTAINS IGNORING CASE '" + $scope.fluid + "' AND  '" + dateString + "' >= '" + 
      $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND '" + dateString + "' <= '" + $rootScope.dateService.getReformatedDate($scope.toDate) + 
      "' AND 'latitude' >= '" + $rootScope.swLat + "' AND 'latitude' <= '" + 
      $rootScope.neLat + "' AND 'longitude' <= '" + $rootScope.neLng + "' AND 'longitude' >= '" + 
      $rootScope.swLng + "' GROUP BY 'Substance'";           

    var queryText = encodeURIComponent(query);
    var gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);

    gvizQuery.send(function(response) {
      topFluids = new google.visualization.PieChart(document.getElementById('variation-fluid'));

      var data = response.getDataTable();

      var slicesColor = {};

      for (var i=0; i < data.getNumberOfRows(); i++){
        if (data.getValue(i, 0) == 'Crude Bitumen')
        { slicesColor[i] = {color: 'rgb(194, 134, 73)' }; }
        else if (data.getValue(i, 0) =='Crude Oil')
        { slicesColor[i] = {color: 'rgb(111, 255, 111)' }; }
        else if (data.getValue(i, 0) == 'Gas')
        { slicesColor[i] = {color: 'rgb(255, 66, 66)' }; }
        else if (data.getValue(i, 0) == 'Water')
        { slicesColor[i] = {color: 'rgb(106, 106, 255)' }; }
      }

      var view = new google.visualization.DataView(data);

      pieChartOptions.title = "Licensed Substance";
      pieChartOptions.slices = slicesColor;
      topFluids.draw(view, pieChartOptions);
    });
  }
  };

  $scope.goNext = function() {
    var diff = Math.round(Math.abs(($scope.toDate.getTime() - $scope.fromDate.getTime())));
    $scope.fromDate = getPrevNextDate($scope.fromDate, diff);
    $scope.toDate = getPrevNextDate($scope.toDate, diff);
  };

  $scope.goPrev = function() {
    var diff = -1 * Math.round(Math.abs(($scope.toDate.getTime() - $scope.fromDate.getTime())));
    $scope.fromDate = getPrevNextDate($scope.fromDate, diff);
    $scope.toDate = getPrevNextDate($scope.toDate, diff);
  };

  $scope.onWellQueryChange = function(updateLocalStorage) {
    $rootScope.drillingLayer.setOptions({
      query: {
        select: 'address',
        from: tableIDs.drilling,
        where: "'Licensee' CONTAINS IGNORING CASE '" + $scope.licensee + "' AND 'Substance' CONTAINS IGNORING CASE '" + 
        $scope.fluid + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + $scope.zone + "' AND  'DrillDate' >= '" + 
        $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND 'DrillDate' <= '" + $rootScope.dateService.getReformatedDate($scope.toDate) + "'" 
      },
      styles: markerColors 
    });

    $rootScope.licencingLayer.setOptions({
      query: {
        select: 'address',
        from: tableIDs.licensing,
        where: "'Licensee' CONTAINS IGNORING CASE '" + $scope.licensee + "' AND 'Substance' CONTAINS IGNORING CASE '" + 
        $scope.fluid + "' AND 'TerminatingZone' CONTAINS IGNORING CASE '" + $scope.zone + "' AND  'Date' >= '" + 
        $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND 'Date' <= '" + $rootScope.dateService.getReformatedDate($scope.toDate) + "'" 
      },
      styles: markerColors 
    });

    updateVizualizations();

    if ($rootScope.dashboardWindow && updateLocalStorage) {
      if (!$rootScope.dashboardWindow.closed) {
        localStorage.licensee = $scope.licensee;
        localStorage.zone = $scope.zone;
        localStorage.fluid = $scope.fluid;
        localStorage.fromDate = $rootScope.dateService.getReformatedDate($scope.fromDate);
        localStorage.toDate = $rootScope.dateService.getReformatedDate($scope.toDate);
      }
    }
  };
}]);