from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets


# Create an application
app = QtWidgets.QApplication([])

# And a window5
win = QtWidgets.QWidget()
win.setWindowTitle('Select Your Area')
win.resize(900,600)

# And give it a layout
layout = QtWidgets.QVBoxLayout()
win.setLayout(layout)

# Create and fill a QWebView
view = QtWebEngineWidgets.QWebEngineView()
view.setHtml('''
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Places Searchbox</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #description {
        font-family: Roboto;
        font-size: 15px;
        font-weight: 300;
      }

      #infowindow-content .title {
        font-weight: bold;
      }

      #infowindow-content {
        display: none;
      }

      #map #infowindow-content {
        display: inline;
      }

      .pac-card {
        margin: 10px 10px 0 0;
        border-radius: 2px 0 0 2px;
        box-sizing: border-box;
        -moz-box-sizing: border-box;
        outline: none;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        background-color: #fff;
        font-family: Roboto;
      }

      #pac-container {
        padding-bottom: 12px;
        margin-right: 12px;
      }

      .pac-controls {
        display: inline-block;
        padding: 5px 11px;
      }

      .pac-controls label {
        font-family: Roboto;
        font-size: 13px;
        font-weight: 300;
      }

      #pac-input {
        background-color: #fff;
        font-family: Roboto;
        font-size: 15px;
        font-weight: 300;
        margin-left: 12px;
        padding: 0 11px 0 13px;
        text-overflow: ellipsis;
        width: 400px;
      }

      #pac-input:focus {
        border-color: #4d90fe;
      }

      #title {
        color: #fff;
        background-color: #4d90fe;
        font-size: 25px;
        font-weight: 500;
        padding: 6px 12px;
      }
      #target {
        width: 345px;
      }
    </style>
  </head>
  <body onload="onload();">
    <input id="pac-input" class="controls" type="text" placeholder="Search Box">
    <input type="text" name="enter" class="enter" value="" id="lat"/>
    <input id ="lng">
    <div id="map"></div>
    
    <script>
      // This example adds a search box to a map, using the Google Place Autocomplete
      // feature. People can enter geographical searches. The search box will return a
      // pick list containing a mix of places and predicted search terms.

      // This example requires the Places library. Include the libraries=places
      // parameter when you first load the API. For example:
      // <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">


function initialize() {
  var markers = [];
  var map = new google.maps.Map(document.getElementById('map'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  var defaultBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(-33.8902, 151.1759),
      new google.maps.LatLng(-33.8474, 151.2631));
  map.fitBounds(defaultBounds);
  var input = /** @type {HTMLInputElement} */(
    document.getElementById('pac-input')
  );
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();
    if (places.length == 0) {
      return;
    }
    for (var i = 0, marker; marker = markers[i]; i++) {
      marker.setMap(null);
    }
    markers = [];
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0, place; place = places[i]; i++) {
      var image = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };
      var marker = new google.maps.Marker({
        draggable: true,
        map: map,
        icon: image,
        title: place.name,
        position: place.geometry.location
      });
      // drag response
      google.maps.event.addListener(marker, 'dragend', function(e) {
        displayPosition(this.getPosition());
      });
      // click response
      google.maps.event.addListener(marker, 'click', function(e) {
        displayPosition(this.getPosition());
      });
      markers.push(marker);
      bounds.extend(place.geometry.location);
    }
    map.fitBounds(bounds);
  });
  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
  });
  // displays a position on two <input> elements
  function displayPosition(pos) {
    document.getElementById('lat').value = pos.lat();
    document.getElementById('lng').value = pos.lng();
  }
}  
google.maps.event.addDomListener(window, 'load', initialize);
</script>

<script type="text/javascript">
    var lotitude;
    var longitude;
    function onload() { 
        latitude = document.getElementById('lat').value;
        longitude = document.getElementById('lng').value;
        return [latitude,longitude];
    }
</script>
    <script src="https://maps.googleapis.com/maps/api/js?&libraries=places&callback=initialize"
         async defer></script>
  </body>
</html>
''')


# A button to call our JavaScript
button = QtWidgets.QPushButton('Okay')

# Interact with the HTML page.
def js_callback(result):
    print(result)

def complete_name():
    view.page().runJavaScript("onload();", js_callback)
# Connect 'complete_name' to the button's 'clicked' signal
button.clicked.connect(complete_name)

# Add the QWebView and button to the layout
layout.addWidget(view)
layout.addWidget(button)

# Show the window and run the app
win.show()
app.exec_()
