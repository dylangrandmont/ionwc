app.controller('provinceSelectController', ['$scope', '$rootScope', function($scope, $rootScope) {
  $scope.changeProvince = function(province) {
    document.getElementById("label-map").style.backgroundColor = 'white';
    document.getElementById("label-bc").style.backgroundColor = 'white';
    document.getElementById("label-ab").style.backgroundColor = 'white';
    document.getElementById("label-sk").style.backgroundColor = 'white';
    document.getElementById("label-mb").style.backgroundColor = 'white';

    document.getElementById("label-map").style.color = "black"; 
    document.getElementById("label-bc").style.color = "black"; 
    document.getElementById("label-ab").style.color = "black"; 
    document.getElementById("label-sk").style.color = "black"; 
    document.getElementById("label-mb").style.color = "black"; 

    if (province == 'BC') {
      document.getElementById("label-bc").style.backgroundColor = "#f4511e";
      document.getElementById("label-bc").style.color = 'white';
    } else if (province == 'AB') {
      document.getElementById("label-ab").style.backgroundColor = "#f4511e";
      document.getElementById("label-ab").style.color = 'white';
    } else if (province == 'SK') {
      document.getElementById("label-sk").style.backgroundColor = "#f4511e";
      document.getElementById("label-sk").style.color = 'white';
    } else if (province == 'MB') {
      document.getElementById("label-mb").style.backgroundColor = "#f4511e";
      document.getElementById("label-mb").style.color = 'white';
    } else if (province == 'map') {
      document.getElementById("label-map").style.backgroundColor = "#f4511e";
      document.getElementById("label-map").style.color = 'white';
    }

    $rootScope.$emit('updateProvince', province);
  };
}]);
