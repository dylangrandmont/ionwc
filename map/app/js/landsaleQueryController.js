app.controller('landsaleQueryController', ['$scope', '$rootScope', '$location', function($scope, $rootScope, $location) {

  var today = new Date();

  $rootScope.showPrevious = false;
  $rootScope.showUpcoming = true;

  handleURLParameters = function() {
    //Format as 2017-01-01
    if ($location.search().fromDate) {
      $scope.fromDate = new Date($location.search().fromDate);
      $scope.previousFromDate = new Date($location.search().fromDate);

      $scope.fromDate.setHours($scope.fromDate.getHours() + 12);
      $scope.previousFromDate.setHours($scope.previousFromDate.getHours() + 12);

      if ($scope.fromDate.getTime() < today.getTime()) {
        $scope.fromDate = new Date();

        $rootScope.showPrevious = true;
      }

      if ($scope.previousFromDate.getTime() > today.getTime()) {
        $scope.previousFromDate = new Date();
        $scope.previousFromDate.setDate(today.getDate() - 365);

        $rootScope.showPrevious = false;
        $rootScope.showUpcoming = true;
      }

    } else {
      $scope.fromDate = new Date();

      $scope.previousFromDate = new Date();
      $scope.previousFromDate.setDate(today.getDate() - 365);
    }

    if ($location.search().toDate) {
      $scope.toDate = new Date($location.search().toDate);
      $scope.previousToDate = new Date($location.search().toDate);

      $scope.toDate.setHours($scope.toDate.getHours() + 12);
      $scope.previousToDate.setHours($scope.previousToDate.getHours() + 12);

      if ($scope.toDate.getTime() < today.getTime()) {
        $scope.toDate = new Date();
        $scope.toDate.setDate(today.getDate() + 365);

        $rootScope.showPrevious = true;
        $rootScope.showUpcoming = false;
      }

      if ($scope.previousToDate.getTime() > today.getTime()) {
        $scope.previousToDate = new Date();

        $rootScope.showUpcoming = true;
      }

    } else {
      $scope.toDate = new Date();
      $scope.toDate.setDate(today.getDate() + 365);

      $scope.previousToDate = new Date();
    }
  };
  handleURLParameters();

  if ($rootScope.viewType == 'Land Sales') { 
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
  }

  $scope.filterProvince = 'AB';
  $scope.format = 'dd-MMM-yyyy';

  $scope.age = "";
  $scope.showLicences = true;
  $scope.showLeases = true;

  $scope.showZoneFilter = false;

  $scope.zones = zones;

  $scope.setFormation = function(age) {
      $scope.age = age;
      $scope.onLandSaleQueryChange();
  }

  $scope.fromDateOptions = {
    maxDate: new Date(2020, 0, 0),
    minDate: new Date(2016, 0, 0),
    showWeeks: false
  };

  $scope.toDateOptions = {
    minDate: new Date(2016, 0, 0),
    maxDate: new Date(2020, 0, 0),
    showWeeks: false
  };

  $scope.openFromDate = function() {
    $scope.fromDatePopup.opened = true;
  };

  $scope.openToDate = function() {
    $scope.toDatePopup.opened = true;
  };

  $scope.$watch('previousFromDate', function() {
    $scope.onLandSaleQueryChange()
  });

  $scope.$watch('previousToDate', function() {
    $scope.onLandSaleQueryChange()
  });

  $scope.fromDatePopup = {
    opened: false
  };

  $scope.toDatePopup = {
    opened: false
  };

  google.maps.event.addListener(map, 'idle', function() {
    $scope.updateVizualizations();
  });

  $rootScope.$on('updateProvince', function(event, province) {
    $scope.filterProvince = province;
    $scope.updateVizualizations();
  });

    var querySales = "SELECT 'saleDate' AS 'Select Sale Date', count(contractNo) AS 'Contracts', SUM(hectares) AS 'Hectares' FROM " +
    "1HUapBmqcSP_Dkz1OA_L1LAv7flecCkVeK8gQrJnV" + " WHERE 'saleDate' >= '" + $rootScope.dateService.getReformatedDate(new Date()) + 
    "' GROUP BY 'saleDate' ORDER BY 'saleDate' ASC";

    var queryTextSales = encodeURIComponent(querySales);
    var gvizQuerySales = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryTextSales);

    gvizQuerySales.send(function(response) 
    {
      var salesList = new google.visualization.Table(document.getElementById('sales-dates-list'));
      var data = response.getDataTable();

      var formatter = new google.visualization.NumberFormat(
        {fractionDigits: '2'}
        );
      formatter.format(data, 2);

      var view = new google.visualization.DataView(data);

      salesList.draw(view, {
        width: 320
      });

      var selectCurrentPostings = function() {
        var selectedItem = salesList.getSelection()[0];
        $scope.fromDate = data.getValue(selectedItem.row, 0);
        $scope.toDate = $scope.fromDate;
        $scope.onLandSaleQueryChange();
      };

      google.visualization.events.addListener(salesList, 'select', selectCurrentPostings);
    });


    var queryPrevSales = "SELECT 'saleDate' AS 'Select Result Date', count(saleDate) AS 'Contracts', sum(bonus) AS 'Bonuses' FROM " +
    "1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn" + " GROUP BY 'saleDate' ORDER BY 'saleDate' DESC";
    var queryPrevTextSales = encodeURIComponent(queryPrevSales);
    var gvizQueryPrevSales = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryPrevTextSales);

    gvizQueryPrevSales.send(function(response) 
    {
      var prevSalesList = new google.visualization.Table(document.getElementById('prev-sales-dates-list'));
      var data = response.getDataTable();
      var view = new google.visualization.DataView(data);

      prevSalesList.draw(view, {
        width: 320,
        height:300
      });

      var selectHandlerPrevDates = function() {
        var selectedItem = prevSalesList.getSelection()[0];
        var value = data.getValue(selectedItem.row, 0);
        $scope.previousFromDate = value;
        $scope.previousToDate = $scope.previousFromDate;
        $scope.onLandSaleQueryChange();
      };

      google.visualization.events.addListener(prevSalesList, 'select', selectHandlerPrevDates);
    });

  $scope.updateVizualizations = function() {
    var provinceFilterString,
        saleDateString = '';

    if ($scope.filterProvince == 'map') {
      provinceFilterString = "'centerLatitude' <= '" + $rootScope.neLat + "' AND 'centerLatitude' >= '" + $rootScope.swLat
      + "' AND 'centerLongitude' <= '" + $rootScope.neLng + "' AND 'centerLongitude' >= '" + $rootScope.swLng + "'";
    } else {
      provinceFilterString = "'province'='" + $scope.filterProvince + "'";
    }

    var queryString = "SELECT 'saleDate' AS 'Select Result Date', sum(bonus) AS 'Bonuses', sum(hectares) AS 'Hectares' FROM " + "1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn" + " WHERE " + saleDateString + provinceFilterString + " AND 'status'='Accepted' GROUP BY 'saleDate' ORDER BY 'saleDate' DESC";
    var queryText = encodeURIComponent(queryString);
    var gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);

    gvizQuery.send(function(response) 
    {
      var data = response.getDataTable();

      var formatter = new google.visualization.NumberFormat(
        { prefix: '$'}
        );
      formatter.format(data, 1);

      var view = new google.visualization.DataView(data);

      view.setColumns([0,1]);
      prevSalesList = new google.visualization.ColumnChart(document.getElementById('stats-bonus-chart'));
      chartOptions.title = 'Total Sales Bonuses';
      prevSalesList.draw(view, chartOptions);

      view.setColumns([0,2]);
      hectaresList = new google.visualization.ColumnChart(document.getElementById('stats-hectares-chart'));
      chartOptions.title = 'Total Hectares Purchased';
      hectaresList.draw(view, chartOptions);
    });

    queryString = "SELECT 'ClientDescription' AS 'Buyer / WI', sum(bonus) AS 'Total Bonuses' FROM " + "1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn" + " WHERE " + provinceFilterString + " AND 'status'='Accepted' GROUP BY 'ClientDescription' ORDER BY sum(bonus) DESC LIMIT 15";
    queryText = encodeURIComponent(queryString);
    gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);
    gvizQuery.send(function(response) 
    {
      var data = response.getDataTable();
      var formatter = new google.visualization.NumberFormat(
        { prefix: '$'}
        );
      formatter.format(data, 1);
      var view = new google.visualization.DataView(data);
      var clientList = new google.visualization.ColumnChart(document.getElementById('stats-client-bonus-chart'));
      stubChartOptions.title = 'Top Buyers by Bonuses';
      clientList.draw(view, stubChartOptions);

      var clientTable = new google.visualization.Table(document.getElementById('stats-client-bonus-table'));
      clientTable.draw(view, tableOptions);      
    });

    queryString = "SELECT 'ClientDescription' AS 'Buyer / WI', sum(hectares) AS 'Purchased Hectares' FROM " + "1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn" + " WHERE " + provinceFilterString + " AND 'status'='Accepted' GROUP BY 'ClientDescription' ORDER BY sum(hectares) DESC LIMIT 15";
    queryText = encodeURIComponent(queryString);
    gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);
    gvizQuery.send(function(response) 
    {
      var data = response.getDataTable();
      var formatter = new google.visualization.NumberFormat(
        { suffix: ' ha'}
        );
      formatter.format(data, 1);
      var view = new google.visualization.DataView(data);

      clientList = new google.visualization.ColumnChart(document.getElementById('stats-client-hectares-chart'));
      stubChartOptions.title = 'Top Buyers by Hectares';
      clientList.draw(view, stubChartOptions);

      var clientTable = new google.visualization.Table(document.getElementById('stats-client-hectares-table'));
      clientTable.draw(view, tableOptions);   
    });

    queryString = "SELECT 'contractType', count(contractType) FROM " + "1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn" + " WHERE " + provinceFilterString + " GROUP BY 'contractType' ORDER BY 'contractType' DESC";
    queryText = encodeURIComponent(queryString);
    gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);
    gvizQuery.send(function(response) 
    {
      var data = response.getDataTable();
      var view = new google.visualization.DataView(data);

      contractTypeList = new google.visualization.PieChart(document.getElementById('stats-contract-chart'));
      pieChartOptions.title = 'Contract Type';
      contractTypeList.draw(view, pieChartOptions);
    });

    queryString = "SELECT 'status', count(status) FROM " + "1n_vrhZ_gRfyv_Zg-lNBdeRfmQq62CNUgG8crWdGn" + " WHERE " + provinceFilterString + " GROUP BY 'status' ORDER BY 'status' DESC";
    queryText = encodeURIComponent(queryString);
    gvizQuery = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq=' + queryText);
    gvizQuery.send(function(response) 
    {
      var data = response.getDataTable();
      var view = new google.visualization.DataView(data);

      statusList = new google.visualization.PieChart(document.getElementById('stats-status-chart'));
      pieChartOptions.title = 'Sale Status';
      statusList.draw(view, pieChartOptions);
    });
  };

  $scope.toggleShowPrevious = function() {
    $rootScope.showPrevious = !$rootScope.showPrevious;
    if ($rootScope.showPrevious) {
      $rootScope.previousLandSaleLayer.setMap(map);
    } else {
      $rootScope.previousLandSaleLayer.setMap(null);
    }
  };

  $scope.toggleShowUpcoming = function () {
    $rootScope.showUpcoming = !$rootScope.showUpcoming;
    if ($rootScope.showUpcoming) {
      $rootScope.upComingLandSaleLayer.setMap(map);
    } else {
      $rootScope.upComingLandSaleLayer.setMap(null);
    }
  };

  $scope.showAllUpcoming = function() {

    $scope.fromDate = new Date();
    $scope.toDate = new Date();
    $scope.toDate.setDate($scope.toDate.getDate() + 365);

    $scope.onLandSaleQueryChange();
  };

  $scope.showAllPrevious = function() {
    $scope.previousFromDate = new Date(2016, 0, 0);
    $scope.previousToDate = new Date();

    $scope.onLandSaleQueryChange();
  };

  $scope.onLandSaleQueryChange = function() {

    var queryStrings = getQueryStrings();
    $rootScope.upComingLandSaleLayer.setOptions({
      query: {
        select: 'address',
        from: tableIDs.upComingLandSale,
        where: queryStrings.upComingQuery
      }
    });
    $rootScope.previousLandSaleLayer.setOptions({
      query: {
        select: 'address',
        from: tableIDs.previousLandSale,
        where: queryStrings.previousQuery
      }
    });
  };

  getQueryStrings = function() {
    var queryString = "";

    if ($scope.showZoneFilter) {
      if ($scope.age == '0') {
        queryString += "'topAge' <= " + $scope.age + " AND 'baseAge' >= " + $scope.age + " AND ";
      } else if ($scope.age == '-1') {
        queryString += "'topAge'='0' AND 'baseAge'='9999' AND ";
      } else if ($scope.age != ''){
        queryString += "'topAge' < " + $scope.age + " AND 'baseAge' >= " + $scope.age + " AND ";
      }
    }

    if ($scope.showContractFilter) {
      if ($scope.showLicences && $scope.showLeases) {
        queryString += "'contractType' IN ('Licence','Lease') AND ";
      } else if ($scope.showLicences) {
        queryString += "'contractType'='Licence' AND ";
      } else if ($scope.showLeases) {
        queryString += "'contractType'='Lease' AND ";
      } else {
        queryString += "'contractType'='DoesNotExist' AND ";
      }
    }

    upComingQuery = queryString + "'saleDate' >= '" + $rootScope.dateService.getReformatedDate($scope.fromDate) + "' AND 'saleDate' <= '" + $rootScope.dateService.getReformatedDate($scope.toDate) + "'";
    previousQuery = queryString + "'saleDate' >= '" + $rootScope.dateService.getReformatedDate($scope.previousFromDate) + "' AND 'saleDate' <= '" + $rootScope.dateService.getReformatedDate($scope.previousToDate) + "'";
    queryStrings = {
      'upComingQuery': upComingQuery,
      'previousQuery': previousQuery
    }

    return queryStrings;
  }
}]);
