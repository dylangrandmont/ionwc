var landGridInitialized = false;

var sectionLabels = [],
    townshipLabels = [],
    nts250kLabels = [],
    nts50kLabels = [],
    ntsBlockLabels = [],
    ntsUnitLabels = [];

var w5w6SectionLayer,
    w4w5SectionLayer,
    w3w4SectionLayer,
    w2w3SectionLayer,
    w1w2SectionLayer,
    e1w1SectionLayer,
    townshipLayer,
    nts50kLayer,
    nts250kLayer,
    ntsBlockLayer,
    w112NTSLayer,
    w122NTSLayer;

var w5w6TableID = '1SsV04Zh5sacl-VyRrbFnGOKD1YvYFgI15j94yDzw',
    w4w5TableID = '184zFumB3NJ4Bc87EYdOLRt0UL7IyOPmmaq02M5gs',
    w3w4TableID = '1KUyHDvtzQPZ1ImQQNYxZRaiCnq9XjOpzWfZfetig',
    w2w3TableID = '1td3bi62ZGm3WuAl3q5F9RFPUHYVOiZ8rZ_Oa2_K2',
    w1w2TableID = '1x3gyCk37KvkwXQAooEikllenn_MAfzNw04j0kWbo',
    e1w1TableID = '1HbFQHpGXvjjjb_FXGkXisowpRfFF5lePJkLj36gU',
    townshipTableID = '1oAMu9KLywpYq0huxKsXXZv4LzJp5eWzC8bs-ZxHw',
    ntsBlockTableID = '1X6Jwg177ivCsbvm5PlF-IEglQQlSG9iaR3KQO6wb',
    w112NTSTableID = '10wMZQLhGZSx5GlFjLk2ug3TZVvD4TdGaY1M3g1mq',
    w122NTSTableID = '1-uSMpARw1ZGDbcrBxxpB1vvw6d70wiq6_Uz0trq9',
    closestSectionTableID,
    closestNTSUnitTableID;

var w5w6LabelTableID = '18qUVQeJlqOZLiO6N8E44o4r_VXfqyk4HkehljNuY',
    w4w5LabelTableID = '1izV4_zLaS90KI2srS5VZPIZhw-MLWZ5ADve_4cOA',
    w3w4LabelTableID = '1Lf45NBxf8Tkyu2CnNWk06U4miV4NZ8RlKaO5W3sB',
    w2w3LabelTableID = '1d9zBaS1rZXFwSgdE05JIiq1i5XdzXi41FeSsubyR',
    w1w2LabelTableID = '1fKicnwFNeWAj-UgCcQt6BeO0HCdKCc26TN62gJ_Z',
    e1w1LabelTableID = '1PUPVXGCDpU3OpVOYRUQMpsZRhkF3oN6KbclRtuS8',
    ntsBlockLabelTableID = '1waGyZUHxHxFXd_BBaF5IzBm3hyLxk84trf_bpX4E';
    w112NTSLabelTableID = '1b9xfUP-btu5EvYaUjSFgOBjGxyBfNi1setmjSUmU',
    w122NTSLabelTableID = '14AHEqJvI--MRdLLTfAwh319gTTfq2fKNgTUYK-vI';

var meridianLngs = [-97.45, -102.0, -106.0, -110.0, -114.0, -118.0];

function initializeLandGrid() {
  landGridInitialized = true;

  w5w6SectionLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: w5w6TableID
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  });

  w4w5SectionLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: w4w5TableID
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  w3w4SectionLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: w3w4TableID
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  w2w3SectionLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: w2w3TableID,
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  });  

  w1w2SectionLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: w1w2TableID,
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  e1w1SectionLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: e1w1TableID,
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  townshipLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: townshipTableID,
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  nts50kLayer = new google.maps.KmlLayer('http://ionwc.com/data/kml/NTS_50k_polygon.kml', {
    suppressInfoWindows: true,
    preserveViewport: true
  });

  nts250kLayer = new google.maps.KmlLayer('http://ionwc.com/data/kml/NTS_250k_polygon.kml', {
    suppressInfoWindows: true,
    preserveViewport: true
  });

  ntsBlockLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: ntsBlockTableID,
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  w112NTSLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: w112NTSTableID,
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  w122NTSLayer = new google.maps.FusionTablesLayer({
    query: {
      select: '\'Geocodable address\'',
      from: w122NTSTableID,
    },
    suppressInfoWindows: true,
    options: {
      styleId: 2,
      templateId: 2
    }
  }); 

  landGridOn = false;

  google.maps.event.addListener(map, "bounds_changed", onBoundsChanged);
  google.maps.event.addListener(map, "zoom_changed", onZoomChanged);
}

function onBoundsChanged() {
  var zoom = map.getZoom();

  if (landGridOn) {
    if (zoom >= 6) {
      clearNTS250kLabels();
      clearNTS50kLabels();
      update250kLabels();

      if (zoom >= 8) {
        clearNTSBlockLabels();
        update50kLabels();

        if (zoom >= 9) {
          clearTownshipLabels();
          clearSectionLabels();
          updateTownships();
          updateNTSBlockLabels();

          if (zoom >= 11){
            clearNTSUnitLabels();
            enableNTSUnitsInView();

            if (zoom >= 12) {
              updateSections();
              updateNTSUnitLabels();
            }
          }
        }
      }
    }
  }
}

function onZoomChanged() {
  var zoom = map.getZoom();

  if (landGridOn && zoom >= 5) {
    townshipLayer.setMap(null);
    clearNTS250kLabels();
    if (zoom >= 6) {
      nts50kLayer.setMap(null);
      townshipLayer.setMap(map);
      nts250kLayer.setMap(map);
      updateLayerOrders();
      if (zoom >= 7) {
        ntsBlockLayer.setMap(null);
        nts50kLayer.setMap(map);
        updateLayerOrders();
        clearNTS50kLabels();
        if (zoom >= 8) {
          ntsBlockLayer.setMap(map);
          updateLayerOrders();
          clearNTS50kLabels();
          clearTownshipLabels();
          if (zoom >= 10) {
            w112NTSLayer.setMap(null);
            w122NTSLayer.setMap(null);
            if (zoom >= 11) {
              clearSectionLayers();
              if (zoom < 12) {
                clearSectionLabels();
                clearNTSUnitLabels();
              }
            }
          }
        }
      }
    }
  } else {
    townshipLayer.setMap(null);
    nts250kLayer.setMap(null);
    nts50kLayer.setMap(null);
    ntsBlockLayer.setMap(null);
    w112NTSLayer.setMap(null);
    w122NTSLayer.setMap(null);
    clearSectionLayers();
    clearSectionLabels();
    clearTownshipLabels();
    clearNTS250kLabels();
    clearNTS50kLabels();
    clearNTSBlockLabels();
    clearNTSUnitLabels();
  }
}

function updateLayerOrders() {
  if (licencingLayer.getMap() != null) {
    licencingLayer.setMap(licencingLayer.getMap());
  }

  if (drillingLayer.getMap() != null) {
    drillingLayer.setMap(drillingLayer.getMap());
  }

  if (upComingLandSaleLayer.getMap() != null) {
    upComingLandSaleLayer.setMap(upComingLandSaleLayer.getMap());
  }

  if (previousLandSaleLayer.getMap() != null) {
    previousLandSaleLayer.setMap(previousLandSaleLayer.getMap());
  }

  if (typeof adLayers !== 'undefined') {
    for (var i = 0; i < adLayers.length; i++) {
      if (previousLayer.getMap() != null) {
        adLayers[i].setMap(adLayers[i].getMap());
      }
    }
  }
}

function clearSectionLayers() {
  w5w6SectionLayer.setMap(null);
  w4w5SectionLayer.setMap(null);
  w3w4SectionLayer.setMap(null);
  w2w3SectionLayer.setMap(null);
  w1w2SectionLayer.setMap(null);
  e1w1SectionLayer.setMap(null);
}

function clearSectionLabels() {
  for (var i=0; i<sectionLabels.length; i++) {
    sectionLabels[i].setMap(null);
  }
  sectionLabels = [];
}

function clearTownshipLabels() {
  for (var i=0; i<townshipLabels.length; i++) {
    townshipLabels[i].setMap(null);
  }
  townshipLabels = [];
}

function clearNTS250kLabels() {
  for (var i=0; i<nts250kLabels.length; i++) {
    nts250kLabels[i].setMap(null);
  }
  nts250kLabels = [];
}

function clearNTS50kLabels() {
  for (var i=0; i<nts50kLabels.length; i++) {
    nts50kLabels[i].setMap(null);
  }
  nts50kLabels = [];
}

function clearNTSBlockLabels() {
  for (var i=0; i<ntsBlockLabels.length; i++) {
    ntsBlockLabels[i].setMap(null);
  }
  ntsBlockLabels = [];
}


function clearNTSUnitLabels() {
  for (var i=0; i<ntsUnitLabels.length; i++) {
    ntsUnitLabels[i].setMap(null);
  }
  ntsUnitLabels = [];
}

function updateSections() {
  closestSectionTableID = getNearestSectionTableID(map.getCenter().lng());
  closestSectionLabelTableID = getLabelTableID(closestSectionTableID);
  enableClosestSectionMap(closestSectionTableID);

  var queryStr = "SELECT 'geometry', 'SC' FROM "+ closestSectionLabelTableID + " WHERE ST_INTERSECTS(geometry, RECTANGLE(LATLNG"+map.getBounds().getSouthWest()+",LATLNG"+map.getBounds().getNorthEast()+"))";  ;   
  var queryText = encodeURIComponent(queryStr);
  var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq='  + queryText);

  query.send(updateSectionsText);
}

function getNearestSectionTableID(lng) {
  var closestMeridian,
  minDistance = 100.0;
  for (i = 0; i < meridianLngs.length; i++) {
    if (Math.abs(lng - meridianLngs[i]) < minDistance) {
      minDistance = Math.abs(lng - meridianLngs[i]);
      closestMeridian = i+1;
    }
  }
  switch(closestMeridian) {
    case 1:
    return e1w1TableID;
    case 2:
    return w1w2TableID;
    case 3:
    return w2w3TableID;
    case 4:
    return w3w4TableID;
    case 5:
    return w4w5TableID;
    default:
    return w5w6TableID;
  }
}

function getLabelTableID(tableid) {
  switch(tableid) {
    case w5w6TableID:
    return w5w6LabelTableID;
    case w4w5TableID:
    return w4w5LabelTableID;
    case w3w4TableID:
    return w3w4LabelTableID;
    case w2w3TableID:
    return w2w3LabelTableID;
    case w1w2TableID:
    return w1w2LabelTableID;
    case e1w1TableID:
    return e1w1LabelTableID;
  }
}

function updateSectionsText(response) {
  var responseTable = response.getDataTable();

  if (responseTable !== null) {
    numRows = responseTable.getNumberOfRows();

    for(i = 0; i < numRows; i++) {
      var latlng = response.getDataTable().getValue(i, 0).toString().replace('<Point><coordinates>', '').replace('</coordinates></Point>', '')
      var lng = latlng.split(',')[0];
      var lat = latlng.split(',')[1];
      var sectionString = response.getDataTable().getValue(i, 1).toString();
      var point = new google.maps.LatLng(
        parseFloat(lat),
        parseFloat(lng)
      );

      sectionLabels.push(new InfoBox({
        content: sectionString,
        boxStyle: {
          border: "0px solid black",
          textAlign: "center",
          fontSize: "9pt",
          width: "50px"
        },
        disableAutoPan: true,
        pixelOffset: new google.maps.Size(-25, 0),
        position: point,
        closeBoxURL: "",
        isHidden: false,
        enableEventPropagation: true
      }));

      sectionLabels[sectionLabels.length-1].open(map);
    }
  }
}

function enableClosestSectionMap(tableID) {
  if (map.getZoom() > 12) {
    switch(tableID) {
      case w5w6TableID:
      clearSectionLayers();
      w5w6SectionLayer.setMap(map);
      break;
      case w4w5TableID:
      clearSectionLayers();
      w4w5SectionLayer.setMap(map);
      break;
      case w3w4TableID:
      clearSectionLayers();
      w3w4SectionLayer.setMap(map);
      break;
      case w2w3TableID:
      clearSectionLayers();
      w2w3SectionLayer.setMap(map);
      break;
      case w1w2TableID:
      clearSectionLayers();
      w1w2SectionLayer.setMap(map);
      break;
      case e1w1TableID:
      clearSectionLayers();
      e1w1SectionLayer.setMap(map);
      break;
    }

    updateLayerOrders();
  }
}

function enableNTSUnitsInView() {
  if (map.getCenter().lng() > -122.0 &&
    map.getCenter().lng() < -120.0) {
    w112NTSLayer.setMap(map);
    w122NTSLayer.setMap(null);
    closestNTSUnitTableID = w112NTSLabelTableID;
  } else if (map.getCenter().lng() > -124.0 &&
    map.getCenter().lng() < -122.0) {
    w112NTSLayer.setMap(null);
    w122NTSLayer.setMap(map);
    closestNTSUnitTableID = w122NTSLabelTableID;
  } else {
    w112NTSLayer.setMap(null);
    w122NTSLayer.setMap(null);
  }
}

function updateTownships() {
  var queryStr = "SELECT 'geometry', 'DLS_ID' FROM 1BDEHLkR0cR_UEOB0IvIfTu5pP5GDYI0CCQ1ioweU WHERE ST_INTERSECTS(geometry, RECTANGLE(LATLNG"+map.getBounds().getSouthWest()+",LATLNG"+map.getBounds().getNorthEast()+"))";  ;   
  var queryText = encodeURIComponent(queryStr);
  var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq='  + queryText);
  query.send(updateTownshipsText);
}

function updateTownshipsText(response) {
  var responseTable = response.getDataTable();

  if (responseTable !== null) {
    numRows = responseTable.getNumberOfRows();
    var labelSize = "12pt",
        labelWidth = "75px",
        labelOffset = -37;

    if (map.getZoom() == 10) {
      labelSize = "9pt";
      labelWidth = "56px";
      labelOffset = -28;
    } else if (map.getZoom() == 9) {
      labelSize = "8pt";
      labelWidth = "50px";
      labelOffset = -25;
    }

    for(i = 0; i < numRows; i++) {
      var latlng = response.getDataTable().getValue(i, 0).toString().replace('<Point><coordinates>', '').replace('</coordinates></Point>', '')
      var lng = latlng.split(',')[0];
      var lat = latlng.split(',')[1];
      var sectionString = response.getDataTable().getValue(i, 1).toString();
      var point = new google.maps.LatLng(
        parseFloat(lat),
        parseFloat(lng));
      townshipLabels.push(new InfoBox({
        content: sectionString,
        boxStyle: {
          border: "0px solid black",
          textAlign: "center",
          fontSize: labelSize,
          width: labelWidth
        },
        disableAutoPan: true,
        pixelOffset: new google.maps.Size(labelOffset, -5),
        position: point,
        closeBoxURL: "",
        isHidden: false,
        enableEventPropagation: true
      }));

      townshipLabels[townshipLabels.length-1].open(map);
    }
  }
}


function update250kLabels() {
  var queryStr = "SELECT 'geometry', 'NTS_ID' FROM 1w4ZpQgXgzKsX2OswFGn70XpyltsYJnVaP1i7zQ9I WHERE ST_INTERSECTS(geometry, RECTANGLE(LATLNG"+map.getBounds().getSouthWest()+",LATLNG"+map.getBounds().getNorthEast()+"))";  ;   
  var queryText = encodeURIComponent(queryStr);
  var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq='  + queryText);
  query.send(update250kLabelsText);
}

function update250kLabelsText(response) {
  var responseTable = response.getDataTable();

  if (responseTable !== null) {
    numRows = responseTable.getNumberOfRows();

    for(i = 0; i < numRows; i++) {
      var latlng = response.getDataTable().getValue(i, 0).toString().replace('<Point><coordinates>', '').replace('</coordinates></Point>', '')
      var lng = latlng.split(',')[0];
      var lat = latlng.split(',')[1];
      var sectionString = response.getDataTable().getValue(i, 1).toString();
      var point = new google.maps.LatLng(
        parseFloat(lat),
        parseFloat(lng));
      nts250kLabels.push(new InfoBox({
        content: sectionString
        ,boxStyle: {
          border: "0px solid black",
          textAlign: "center",
          color: "black",
          fontSize: "12pt",
          width: "75px"
        }
        ,disableAutoPan: true
        ,pixelOffset: new google.maps.Size(-37, -11)
        ,position: point
        ,closeBoxURL: ""
        ,isHidden: false
        ,enableEventPropagation: true
      }));
      nts250kLabels[nts250kLabels.length-1].open(map);
    }
  }
}

function update50kLabels() {
  var queryStr = "SELECT 'geometry', 'NTS_50K' FROM 1Izlxp4e1TBVSKCI-volXITIKVv0W2KZEV-OfWM3j WHERE ST_INTERSECTS(geometry, RECTANGLE(LATLNG"+map.getBounds().getSouthWest()+",LATLNG"+map.getBounds().getNorthEast()+"))";  ;   
  var queryText = encodeURIComponent(queryStr);
  var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq='  + queryText);
  query.send(update50kLabelsText);
}

function update50kLabelsText(response) {
  var responseTable = response.getDataTable();

  if (responseTable !== null) {
    numRows = responseTable.getNumberOfRows();

    for(i = 0; i < numRows; i++) {
      var latlng = response.getDataTable().getValue(i, 0).toString().replace('<Point><coordinates>', '').replace('</coordinates></Point>', '')
      var lng = latlng.split(',')[0];
      var lat = latlng.split(',')[1];
      var sectionString = response.getDataTable().getValue(i, 1).toString();
      var point = new google.maps.LatLng(
        parseFloat(lat),
        parseFloat(lng));
      nts50kLabels.push(new InfoBox({
        content: sectionString
        ,boxStyle: {
          border: "0px solid black"
          ,textAlign: "center"
          ,fontSize: "11pt"
          ,width: "40px"
        }
        ,disableAutoPan: true
        ,pixelOffset: new google.maps.Size(-20, -5)
        ,position: point
        ,closeBoxURL: ""
        ,isHidden: false
        ,enableEventPropagation: true
      }));
      nts50kLabels[nts50kLabels.length-1].open(map);
    }
  }
}

function updateNTSBlockLabels() {
  var queryStr = "SELECT 'geometry', 'BC_BLOCK' FROM " + ntsBlockLabelTableID + " WHERE ST_INTERSECTS(geometry, RECTANGLE(LATLNG"+map.getBounds().getSouthWest()+",LATLNG"+map.getBounds().getNorthEast()+"))";  ;   
  var queryText = encodeURIComponent(queryStr);
  var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq='  + queryText);
  query.send(updateNTSBlockLabelsText);
}

function updateNTSBlockLabelsText(response) {
  var responseTable = response.getDataTable();

  if (responseTable !== null) {
    numRows = responseTable.getNumberOfRows();

    for(i = 0; i < numRows; i++) {
      var latlng = response.getDataTable().getValue(i, 0).toString().replace('<Point><coordinates>', '').replace('</coordinates></Point>', '')
      var lng = latlng.split(',')[0];
      var lat = latlng.split(',')[1];
      var sectionString = response.getDataTable().getValue(i, 1).toString();
      var point = new google.maps.LatLng(
        parseFloat(lat),
        parseFloat(lng));
      ntsBlockLabels.push(new InfoBox({
        content: sectionString
        ,boxStyle: {
          border: "0px solid black"
          ,textAlign: "center"
          ,fontSize: "9pt"
          ,width: "40px"
        }
        ,disableAutoPan: true
        ,pixelOffset: new google.maps.Size(-20, -5)
        ,position: point
        ,closeBoxURL: ""
        ,isHidden: false
        ,enableEventPropagation: true
      }));
      ntsBlockLabels[ntsBlockLabels.length-1].open(map);
    }
  }
}

function updateNTSUnitLabels() {
  var queryStr = "SELECT 'geometry', 'BC_UNIT' FROM " + closestNTSUnitTableID + " WHERE ST_INTERSECTS(geometry, RECTANGLE(LATLNG"+map.getBounds().getSouthWest()+",LATLNG"+map.getBounds().getNorthEast()+"))";  ;   
  var queryText = encodeURIComponent(queryStr);
  var query = new google.visualization.Query('http://www.google.com/fusiontables/gvizdata?tq='  + queryText);
  query.send(updateNTSUnitLabelsText);
}

function updateNTSUnitLabelsText(response) {
  var responseTable = response.getDataTable();

  if (responseTable !== null) {
    numRows = responseTable.getNumberOfRows();

    for(i = 0; i < numRows; i++) {
      var latlng = response.getDataTable().getValue(i, 0).toString().replace('<Point><coordinates>', '').replace('</coordinates></Point>', '')
      var lng = latlng.split(',')[0];
      var lat = latlng.split(',')[1];
      var sectionString = response.getDataTable().getValue(i, 1).toString();
      var point = new google.maps.LatLng(
        parseFloat(lat),
        parseFloat(lng));
      ntsUnitLabels.push(new InfoBox({
        content: sectionString
        ,boxStyle: {
          border: "0px solid black"
          ,textAlign: "center"
          ,fontSize: "8pt"
          ,width: "40px"
        }
        ,disableAutoPan: true
        ,pixelOffset: new google.maps.Size(-20, -5)
        ,position: point
        ,closeBoxURL: ""
        ,isHidden: false
        ,enableEventPropagation: true
      }));
      ntsUnitLabels[ntsUnitLabels.length-1].open(map);
    }
  }
}

function toggleLandGrid() {
  if (document.getElementById('layer_00').checked) {
    if (!landGridInitialized) {
      initializeLandGrid();
    }

    if (map.getZoom() < 6) {
      map.setZoom(6);
    }

    landGridOn = true;
    onZoomChanged();
    onBoundsChanged();
  } else {
    landGridOn = false;
    onZoomChanged();
    onBoundsChanged();
  }
}
