
//TODO: implement local storage to reduce the number of
//AJAX requests to Flickr.
//var store = localStorage.getItem('flickrRequest') || "";
//store.setItem('flickrRequest', value)

var Place = function(name, range) {
    'use strict';
    this.name = name;
    this.range = ko.observable(range);
};

//observable array for each photo
//to construct the flickr uri, see:
//https://www.flickr.com/services/api/misc.urls.html
var Photo = function(photo, location) {
    'use strict';
    this.farmId = photo.farm;
    this.svrId = photo.server;
    this.photoId = photo.id;
    this.owner = photo.owner;
    this.scrt = photo.secret;
    this.photoLoc = location; //object with keys: lat, lon
    this.locId = photo.place_id;
    this.size = 't'; //t is for thumb
    this.thumbUrl = 'https://farm' + this.farmId + '.staticflickr.com/' + this.svrId;
    this.thumbUrl += '/' + this.photoId + '_' + this.scrt + '_' + this.size + '.jpg';
    this.extUrl = 'https://farm' + this.farmId + '.staticflickr.com/' + this.svrId;
    this.extUrl += '/' + this.photoId + '_' + this.scrt +'.jpg';
    this.fullTitle = photo.title;
    //this.tags = photo.tags;
    //don't let long titles mess with the page
    if (this.fullTitle.length > 20) {
        this.title = this.fullTitle.substring(0, 19)+'...';
    } else if (this.fullTitle==="") {
        this.title = "(untitled)";
    } else {
        this.title = this.fullTitle;
    }
    //keep track of clicks and/or likes/dislikes
    this.giveLove = ko.observable(0);

    //keep track of the toggle variable for each item
    //to show or hide the 'like' and 'close' buttons
    this.showSelector = ko.observable(false);

    //toggle visibility for filtering functions
    this.visible = ko.observable(true);
};

var User = function(person, allImageObjects) {
    //self = this;
    this.alias = person.path_alias;
    this.userId = person.id;

    //make an observable array out of photo objects
    //for keeping track of all photos from distinct users

    this.images = ko.observableArray(allImageObjects);

    //variable for toggling display of user data
    this.display = ko.observable(true);
    var baseUrl = 'https://www.flickr.com/photos/';
    this.userUrl = baseUrl + this.userId;
};

var ViewModel = function() {
    'use strict';

    var self = this;

    set_bg_image();

    //initialize a photos object
    this.photoList = ko.observableArray();
    this.currentPlace = ko.observable();
    this.currentListItem = ko.observable();

    //array for photo markers
    this.photoMarkerList = ko.observableArray();
    //object for location marker
    this.locationMarkerList = ko.observableArray();
    //object for info windows
    this.infoWindowList = ko.observableArray();
    //keep track of users by alias and their photos
    this.users = ko.observableArray();

    //initialize the map with a global scope for access at different levels
    var mapOptions = {
        disableDefaultUI: true,
        disableDoubleClickZoom: true,
        rotateControl: true,
        scaleControl: true,
        zoomControl: true,
        zoom: 16
    };

    var map = new google.maps.Map(document.getElementById("map"), mapOptions);

    // upon request, get a user's current location
    var freegeoip = "http://freegeoip.net/json/";

    this.getInitialGeoLocation = function() {
        var thisLoc = $.getJSON(freegeoip, {})
            .done(function(data) {
                console.log(data.latitude, data.longitude);
                var initialLoc = { lat: data.latitude, lng: data.longitude};
                self.initializeMap(initialLoc);
            })
            .fail(function() {
                alert("The geolocation request has failed.");
                self.initializeMap("Error Flag");
            });
    };
    var initialLoc = ko.observable();

    // this.getCurrentLocation();

    this.initializeMap = function(initialLocation) {

        var locations;
        var errorFlag;
        //set default locations for no no geolocation capability.
        var picklecrowON = {lat: 51.5022729, lng: -90.0588331};
        var dauphinMB = {lat: 51.1494, lng: -100.0494};
        var browserSupportFlag = Boolean();

        if (initialLocation == "Error Flag") {
            errorFlag = true;
            alert("Geolocation service failed.  Go directly to Pickle Crow, ON and tell us what's it like.");
            initialLocation = picklecrowON;
            map.setCenter(initialLocation);
        } else {
            map.setCenter(initialLocation);
            //self.currentPlace(initialLocation);
            self.createPlaceMarker(initialLocation);
        }

        google.maps.event.addListenerOnce(map, 'tilesloaded', self.initializeLocation);

    };

    this.initializeLocation = function() {
        self.setPlace();
    };

    this.placeMarkerAndPanTo = function(latLng, map) {
        //not sure I want a marker in this instance
        var marker = new google.maps.Marker({
            position: latLng,
            animation: google.maps.Animation.DROP,
            icon: 'static/images/icons/locMarker.svg',
            map: map,
            zoom: 10
        });

        map.panTo(latLng);
        //add new marker to locationMarkerList
        self.locationMarkerList.push(marker);
        self.setPlace();
    };

    /*
    createPlaceMarker(placeData) reads Google Places search results to create map pins.
    placeData is the object returned from search results containing information
    about a single location.
    */
    this.createPlaceMarker = function(locLiteral) {
        //var place = new google.maps.PlacesService();
        var name = "You might be here.";
        //var map = self.map;

        //get the boungs of the current view
        var bounds = map.getBounds();

        // marker is an object with additional data about the pin for a single location
        var marker = new google.maps.Marker({
            map: self.map,
            // free open source svg graphics from http://uxrepo.com/
            icon: 'static/images/icons/locMarker.svg',
            position: locLiteral,
            animation: google.maps.Animation.DROP,
            title: name
        });

        self.locationMarkerList.push(marker);

        // fit the map to the new marker
        map.fitBounds(bounds);
        // center the map
        map.setCenter(bounds.getCenter());
    };

    this.getWindowContent = function(photo) {

        var fullWindowTitle = photo.fullTitle;
        var windowTitle = "";
        //don't let long titles mess with the infoWindow
        if (fullWindowTitle.length > 15) {
            windowTitle = fullWindowTitle.substring(0, 14)+'...';
        } else if (fullWindowTitle==="") {
            windowTitle = "(untitled)";
        } else {
            windowTitle = fullWindowTitle;
        }

        var imgBaseUrl = 'https://farm' + photo.farmId + '.staticflickr.com/' + photo.svrId;
        imgBaseUrl += '/' + photo.photoId + '_' + photo.scrt;
        var imgUrl = imgBaseUrl + '.jpg';
        var imgThumbUrl = imgBaseUrl + '_' + 't' + '.jpg';

        var infoWindowContent = "<div class='customInfoWindow'><h5>";
        infoWindowContent += windowTitle + "</h5><a href='" + imgUrl + "'>";
        infoWindowContent += "<img src='" + imgThumbUrl + "'>" + "</a></div>";

        return [windowTitle, infoWindowContent];
    };

    this.openInfoWindow = function(marker, photo) {

        //close any open info windows before opening new one
        //but first check if any have been added to the observable array

        if (self.infoWindowList().length===0) {

            var windowTitle = self.getWindowContent(photo)[0];
            var infoWindowContent = self.getWindowContent(photo)[1];

            // infoWindows are the little helper windows that open when you click
            // or hover over a pin on a map. They usually contain more information
            // about a location.
            var newWindow = new google.maps.InfoWindow({
                title: windowTitle,
                content: infoWindowContent
            });

            newWindow.open(map, marker);
            self.infoWindowList().push(newWindow);
        } else {
            //close and delete the existing infoWindow, thenloop back
            //into this same function to trigger first condition and
            //open a new window
            self.closeInfoWindow();
            this.openInfoWindow(marker, photo);
        }
    };

    this.closeInfoWindow = function() {
        //close any info windows currently open
        //and remove them from the infowindow observable array
        var numOldWindows = self.infoWindowList().length;

        for (var i = 0; i < numOldWindows; i++) {
            self.infoWindowList()[i].close();
            self.infoWindowList.removeAll();
        }
    };


    this.createPhotoMarker = function(photoObj) {

        var photo = self.getPhotoObjectById(photoObj.id);

        var windowTitle = self.getWindowContent(photo)[0];
        //var infoWindowContent = self.getWindowContent(photo)[1];
        // marker is an object with additional data about the pin for a single location
        // var marker = new google.maps.Marker({
        //     map: map,
        //     // free open source svg graphics from http://uxrepo.com/
        //     icon: '/images/icons/cameraMarker.svg',
        //     position: new google.maps.LatLng(photoObj.latitude, photoObj.longitude),
        //     title: windowTitle,
        //     photoId: photoObj.id,
        //     scaledSize: new google.maps.Size(36, 26)
        // });

        var icon = {
            url: 'static/images/icons/cameraMarker.svg',
            scaledSize: new google.maps.Size(44, 33),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0),
        };

        var positn = new google.maps.LatLng(photoObj.latitude, photoObj.longitude);
        var marker = new google.maps.Marker({
            position: positn,
            title: windowTitle,
            photoId: photoObj.id,
            map: map,
            icon: icon
        });

        //add the marker to the photoMarkerList observable array
        self.photoMarkerList.push(marker);

        //listen for click, and animate marker and toggle info window
        google.maps.event.addListener(marker, 'click', function() {
            self.animateMarker(marker);
            self.openInfoWindow(marker, photo);

            //bring back the image in list view if it was removed
            var visibility = photo.visible();
            if (visibility === 'undefined' || visibility === false) {
                photo.visible(true);
            }
            var element = document.getElementById(marker.photoId);
        });

        self.createUserList(photoObj);
    };

    //keep track of individual users whose
    //photos are displayed
    this.userList = {};

    this.getAllUserPhotos = function(userId) {
        var allImageIds = self.userList[userId];
        var allImageObjects = [];
        allImageIds.forEach(function(imageId) {
            var photoObject = self.getPhotoObjectById(imageId);
            allImageObjects.push(photoObject);
        });
        return allImageObjects;
    };

    this.createUserList = function(photoObj) {
        // populate a list of users whose images are displayed
        var owner = photoObj.owner;
        var owners = self.userList;
        if (owners === "null" || "undefined") {
            owners = [];
        } else {
            owners = Object.keys(owners);
        }

        var photoId = photoObj.id;

        //create an object of 'owner_id': [array of photo_id]
        //avoid duplicate entries of photos or owners
        if (owners.indexOf(owner) !== -1) {
            //new entry for array of photos
            var photoArray = self.userList[owner];
            //retrieve actual username for this new owner entry
            var userName = self.getUserName(owner);

            if (photoArray.indexOf(photoId) === -1) {
                self.userList[userName].push(photoId);
            }
        } else {
            self.userList[owner] = [photoId];
        }
    };

    //mapping function for autocomplete to wait for
    //asynchronous request:
    //http://stackoverflow.com/questions/5627284/pass-in-an-array-of-deferreds-to-when

    //utility function for ajax request resolution for createUserObject, below
    this.whenAll = function(array) {
        return $.when.apply($, array);
    };

    //store all 'alias' or screen names in an array for
    //use with autocomplete function in 'user name' filter
    var allUserNames = [];

    this.filterUsers = function(){

        $("#userFilter").autocomplete({
            source: allUserNames
        });
    };

    //filter by username will display only the map pins and
    //list items corresponding to the selected user
    //additional help with combining jquery ui with knockout,
    //specifically with adding 'blur' to trigger update to
    //the selectedUser observable:
    //http://blogs.msmvps.com/theproblemsolver/2013/11/18/using-the-jquery-io-autocomplete-widget-with-knockout/
    this.selectedUser = ko.observable();

    this.filterByUser = function() {

        var allUsers = self.users();

        var allUserIds= Object.keys(self.userList);

        var allPhotos = self.photoList();

        var availableTags = Object.keys(allUsers);

        var selectedUser = self.selectedUser();

        //by default, show all images
        var userImages = allPhotos;

        // return the array of all user images currently displayed
        // 'some' function breaks when match is discovered
        // when value is reset to default 'filter by user'
        // show all images
        allUsers.some(function(user) {
            if (selectedUser === user.alias) {
                userImages = user.images();
            } else if (selectedUser==='Filter by Username') {
                //avoid opening multiple infowindows
                //when using filter feature
                self.closeInfoWindow();
                self.selectedUser("User not found.");
            }
        });

        // filter function for the 'filter by user' feature.
        // hide all photos and pins not belonging to the
        // selected user, but refresh to show all others when
        // refreshed.
        // toggleListItem takes in (image object, google map set variable,
        // list item visibility)
        // null/false = off (hide); map/true = on (visible)

        allPhotos.forEach(function(photo) {
            if (userImages.indexOf(photo) === -1) {
                self.toggleListItem(photo, null, false);
            } else {
                self.toggleListItem(photo, map, true);
            }
        });

    };


    this.animateMarker = function(marker) {
        //toggle marker bounce
        marker.setAnimation(google.maps.Animation.BOUNCE);

        //make bouncing effect stop after a bounce or two
        setTimeout(function() {
            marker.setAnimation(null);
        }, 700);
    };

    /* Callback(results, status) makes sure the search returned results for a location.
    If so, it creates a new map marker for that location.*/
    this.callback = function(results, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            self.createPlaceMarker(results[0]);
        }
    };


    /*  pinPoster(locations) takes in the array of locations created by locationFinder()
    and fires off Google place searches for each location  */
    this.pinPoster = function(locations) {

        // creates a Google place search service object. PlacesService does the work of
        // actually searching for location data.
        var service = new google.maps.places.PlacesService(map);

        // Iterates through the array of locations, creates a search object for each location
        for (var place in locations) {
            // the search request object
            var request = {
                location: place,
                query: place
            };

            // Actually searches the Google Maps API for location data and runs the callback
            // function with the search results after each search.
            service.textSearch(request, self.callback);
        }
    };

    this.createUserObject = function() {
        var apiKey = self.get_flickr_api_key();
    };

    this.make_flickr_user_request = function (apiKey) {
        // Requests User objects from flicker API based on Username
        // associated with a photo
        var requestUrl = 'https://api.flickr.com/services/rest/?method=flickr.people.getInfo';

        //how many names are we looking for?
        var numberOfUsers = Object.keys(self.userList).length;

        var allUsers = Object.keys(self.userList);

        //go through all of the usernames in allUsers and make an ajax
        //request for the nickname.  The 'then' portion of script
        //will be executed after all the requests have resolved (or on error)
        self.whenAll($.map(allUsers, function(k, v) {
            return $.getJSON(requestUrl, {
                api_key: apiKey,
                user_id: k,
                format: "json",
                nojsoncallback: 1
                })

                .done(function(data) {
                    var allImageObjects = self.getAllUserPhotos(k);
                    self.users.push( new User(data.person, allImageObjects) );
                })

                .fail(function() {
                    alert("The Flickr request has kicked the bucket.  What'd you do??");
                });
        })).then(function() {
            self.users().forEach(function(user) {
                if (user==='null') {
                    allUserNames.push('anonymous');
                } else {
                    allUserNames.push(user.alias);
                }
            });
            //only run filterUsers once all ajax requests are complete
            self.filterUsers();
        });
    };

    this.make_flickr_photo_request = function(flickr_key, bounds) {
        // the flickr request string filters for photos with geoTag, by the
        // location stored in place.name, and by the keywords listed in the
        // tags array, default to "or"(any) of the tags instead of "and" (all)

        // search for images only in the current map view
        // required bounding box format is [min_lon, min_lat, max_lon, max_lat]
        var searchBounds = bounds.b.b + ',' + bounds.f.f + ',' + bounds.b.f + ',' + bounds.f.b;
        var searchTags = "graffiti";
        var flickr_base_uri = 'https://api.flickr.com/services/rest/?method=flickr.photos.search';
        $.getJSON(flickr_base_uri, {
            api_key: flickr_key,
            bbox: searchBounds,
            extras: "geo",
            has_geo: "1",
            per_page: 25,
            tags: searchTags,
            tagmode: "all",
            format: "json",
            nojsoncallback: 1
        })
        .done(function(data) {
            var allPhotos = data.photos.photo;
            //max is 250 photos, but only put
            //georeferenced photos into the allPhotos array
            allPhotos.forEach(function(photo){
                if (photo.latitude) {
                    if (photo.latitude !== 0) {
                        //create a location object
                        var location = {lat: photo.latitude, lon: photo.longitude};
                        //measure distance to currentlocation
                        //and only push if it's inside the current setdistance
                        self.photoList.push( new Photo(photo, location) );
                        //create a map marker pin
                        self.createPhotoMarker(photo);
                    }
                }
            });
        })
        .fail(function() {
            alert("The Flickr request has kicked the bucket.  What'd you do??");
        });
    };

    this.get_flickr_api_key = function(bounds) {
        $.getJSON('/api_key_query', {
        })
        .done(function(data) {
            // Send the api_key to the flickr api request function
            // to avoid problems with asynchronous ajax requests
            self.make_flickr_photo_request(data.result, bounds);
            self.make_flickr_user_request(data.result);
        })
        .fail(function() {
            alert("Failed to retrieve Flickr API Key.  What'd you do??");
        });
    };

    this.flickrData = function(bounds) {
        // Retrieve the flickr api key from secure folder, then because
        // of asynchronous Ajax request, on successful retrieval, trigger
        // a second ajax request to the actual flickr API.
        var flickr_key = self.get_flickr_api_key(bounds);
    };

    //setPlace gets called from page load and from a change in the
    //search range selector, and captures the current map viewport
    //for image searching purposes
    this.setPlace = function() {
        var bounds = map.getBounds();
        self.currentPlace(bounds);
        self.flickrData(bounds);
    };

    //hightlight list item and set as current on click
    //and toggle 'like' and 'close' buttons on select
    this.highlightedRowIndex = ko.observable();

    this.setCurrentListItem = function(e) {

        //highlights current list item
        self.currentListItem(e);
        //highlight corresponding map marker
        var matchId = e.photoId;
        var currentMarkerIndex = self.getMapMarker(matchId);
        var currentMarker = self.photoMarkerList()[currentMarkerIndex];

        //animate selected marker and open infoWindow
        self.animateMarker(currentMarker);

        //toggle the 'like' and 'close' buttons when
        //the thumb is selected

        switch (e.showSelector()) {
            case false:
                e.showSelector(true);
                break;
            case true:
                e.showSelector(false);
        }

        self.openInfoWindow(currentMarker, e);
    };

    //toggle the "information" section
    this.showInfo = ko.observable(false);

    this.toggleInfo = function(data) {
        switch (self.showInfo()) {
            case false:
                self.showInfo(true);
                break;
            case true:
                self.showInfo(false);
        }
    };

    //toggle the filter window
    this.showFilters = ko.observable(false);
    this.userObjectInitialized = ko.observable(false);

    this.toggleFilterWindow = function(data) {
        switch (self.showFilters()) {
            case false:
                self.showFilters(true);
                //only have one filter open at a time
                self.showDistance(false);

                if (self.userObjectInitialized()===false) {
                    self.createUserObject();
                    self.userObjectInitialized(true);
                }
                break;
            case true:
                self.showFilters(false);
        }
    };
    //separate the functions for distance search
    //and user search to minimize space taken up
    //by displaying filters.
    this.showDistance = ko.observable(false);

    this.toggleDistanceWindow = function(data) {
        switch (self.showDistance()) {
            case false:
                self.showDistance(true);
                //only have one filter open at a time
                self.showFilters(false);
                break;
            case true:
                self.showDistance(false);
        }

        //delay the AJAX request associated with populating
        //the "by user" filter until the filter menu is selected
        if (self.userObjectInitialized()===false){
            self.createUserObject();
            self.userObjectInitialized(true);
        }
    };

    //toggles the giveLove property between 1 and 0
    //to toggle a red heart on click.
    this.giveLove = function(data) {
        return data.giveLove();
    };

    this.toggleLove = function(data) {
        switch (data.giveLove()) {
            case 1:
                data.giveLove(0);
                return data.giveLove();
            case 0:
                data.giveLove(1);
                return data.giveLove();
        }

    };


    //this gets fired when the User filter is triggered,
    //and also when the list item close button is clicked
    this.toggleListItem = function(photo, mapBool, visible) {

        //hide or show map marker depending on values passed in
        //for map and visible
        var currentMarkerIndex = self.getMapMarker(photo.photoId);
        if (typeof currentMarkerIndex==='number') {
            self.photoMarkerList()[currentMarkerIndex].setMap(mapBool);
            //toggle visibility of the corresponding list item
            photo.visible(visible);
        }
    };
    //hide the list item when it's called from clicking on the
    //'close' button on the selected list item.
    this.hideListItem = function(photo) {
        self.toggleListItem(photo, null, false);
    };

    this.getMapMarker = function (matchId) {
        //remove corresponding  map marker
        var listLen = self.photoMarkerList().length;
        for (var i = 0; i < listLen; i++) {
            if (matchId === self.photoMarkerList()[i].photoId) {
                return i;
                //note that this may only function if the request
                //remains static.  before implementing dynamic ajax
                //requests, check to see if the item must first
                //be removed from markerList so that the indices of
                //markers in mapMarker remain in correspondence with
                //the correct photo.
                //self.mapMarkerList().remove(self.mapMarkerList()[i]);
            }
        }
    };

    //return a photo object based on an id.
    //basically a reverse search of getMapMarker
    this.getPhotoObjectById = function(photoId) {
        var listLen = self.photoList().length;
        for (var i = 0; i < listLen; i++) {
            if (photoId === self.photoList()[i].photoId) {
                return self.photoList()[i];
            }
        }
    };

    //filter photos by radius from the marker
    //Search distance options
    this.availableRange = ko.observableArray([
        { distLabel: "100 m", distance: 0.1 },
        { distLabel: "500 m", distance: 0.5 },
        { distLabel: "1 km", distance: 1.0 },
        { distLabel: "5 km", distance: 5.0 }
    ]);

    //help on implementation of distance measurement between lat-lng points:
    //http://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    this.filterByDistance = function(maxDistance) {

        var bounds = map.getBounds();
        var cLoc = bounds.getCenter();
        var lat1 = cLoc.lat();
        var lon1 = cLoc.lng();

        var listLen = self.photoMarkerList().length;

        for (var i = 0; i < listLen; i++) {

            var marker = self.photoMarkerList()[i];

            var lat2 = marker.position.lat();
            var lon2 = marker.position.lng();

            if (this.getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) > maxDistance) {
                self.removePhotoPin(marker);
            } else {
                var photo = self.getPhotoObjectById(marker.photoId);
                self.toggleListItem(photo, map, true);
            }
        }
    };

    this.removePhotoPin = function(marker) {
        var photo = self.getPhotoObjectById(marker.photoId);
        //hide item from list
        self.toggleListItem(photo, null, false);
        //setVisible is a google maps function for
        //setting visibility of a pin
        //marker.setVisible(false);
    };

    this.getDistanceFromLatLonInKm = function(lat1,lon1,lat2,lon2) {
            var R = 6371; // Radius of the earth in km
            var dLat = this.deg2rad(lat2-lat1);  // deg2rad below
            var dLon = this.deg2rad(lon2-lon1);
            var a = Math.sin(dLat/2) * Math.sin(dLat/2);
            a += Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) * Math.sin(dLon/2) * Math.sin(dLon/2);
            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            var d = R * c; // Distance in km
            return d;
    };

    this.deg2rad = function(deg) {
        return deg * (Math.PI/180);
    };


    this.setSearchDist = function(selected) {

        var searchDist;
        switch (selected) {
            case "100 m":
                searchDist = 0.1;
                break;
            case "500 m":
                searchDist = 0.5;
                break;
            case "1 km":
                searchDist = 1.0;
                break;
            case "5 km":
                searchDist = 5.0;
                break;
            case "Set Search Radius":
                //default search distance is 500m
                searchDist = 1.0;
                break;
            default:
                alert("Go ahead, set a search radius \n don't be scared.");
                //searchDist = 0.5;
        }
        return searchDist;
    };

    //trigger the listener after the page has loaded to avoid
    //returning undefined map
    //
    this.selectedRadius = ko.observable("500 m");

    //this.updateStatus = function() {

    this.distanceFilter = function(){

            var selected = $('#distSelect option:selected');
            var selectedValue = selected.text();

            var maxDistance = self.setSearchDist(selectedValue);
            self.selectedRadius(maxDistance);

            self.filterByDistance(maxDistance);
    };

    //when no image results are returned, it's either
    //because geolocation isn't enabled and user is
    //taken to Pickle Crow, Ontario, or no photos
    //exist in the current bounds.  Create a function
    //to allow for entering a new location altogether.
    //
    this.newPlace = ko.observable();

    this.changePlace = function() {

        // Create the search box and link it to the UI element.
        var geocoder = new google.maps.Geocoder();

        geocoder.geocode({'address': self.newPlace()}, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                self.setPlace();
                // var marker = new google.maps.Marker({
                //     map: map,
                //     position: results[0].geometry.location
                //     });
            } else {
            alert('Geolocate was not successful for the following reason: ' + status);
            }
        });
    };

    //create a deferred object to defer triggering a function
    this.deferred = $.Deferred();

    //listen for map interactions and update currentPlace
    map.addListener('dblclick', function(e) {

        //first remove the existing location pin
        var currentMarker = self.locationMarkerList()[0];

        if (currentMarker) {
            currentMarker.setMap(null);
            self.locationMarkerList.remove(currentMarker);
        }

        //clear all existing places and photo markers
        //from their respective tracking arrays
        var allPhotoMarkers = self.photoMarkerList();
        //reset all photo markers on map
        allPhotoMarkers.forEach(function(marker) {
            marker.setMap(null);
        });

        //reset all variables
        self.photoMarkerList.removeAll();
        self.locationMarkerList.removeAll();
        self.users.removeAll();
        self.userList = [];
        self.photoList.removeAll();
        this.currentPlace = ko.observable();
        this.currentListItem = ko.observable();
        self.userObjectInitialized(false);

        //then set a new pin and update currentPlace
        self.placeMarkerAndPanTo(e.latLng, map);

        //and reapply the distance filter
        // var maxDistance = self.setSearchDist(self.selectedRadius());
        // self.selectedRadius(maxDistance);
        // self.filterByDistance(maxDistance);

        //when place changes, close all infoWindows
        self.closeInfoWindow();

    });

    // this.initializeMap();

};

//don't load the UI until maps has loaded.
//this will prevent a request happening before
//the page can accept it.

var LOC = '';

$(window).load(function() {

    //LOC = https://freegeoip.net/json/
    ko.applyBindings(new ViewModel());

    // START HELPER FUNCTiONS

    // toggle the loader to slide up to hidden
    //  position when geolocation button is clicked
    $(".useMyLocation").click(function() {
        $(".loader").delay( 800 ).slideUp( { duration: 1500, easing: "easeInOutQuart" }, function() {
            //let the information preload and then draw up
            //the curtains for show time!
            });
    });
    // toggle the loader to slide up to hidden
    // position when set location is clicked
    $("#setLocationBtn").click(function() {
        $(".loader").delay( 800 ).slideUp( { duration: 1500, easing: "easeInOutQuart" }, function() {
            //let the information preload and then draw up
            //the curtains for show time!
            });
    });

    $(".Button").on("click",function(e){
        $(this).parent().toggleClass("is-Open");
    });

});

var set_bg_image = function() {
    var self = this;
    var s = new Snap("#splashLogo");
    var g = s.group();

    var logo = Snap.load('/static/images/artchivelogo_frontpage.svg', function(f) {
        g.append(f);
        var logo_svg = g.select("#logo_text");
        var logo_dims = logo_svg.getBBox();
        var canvas_width = $(document).width();
        var canvas_height = $(document).height();
        console.log(logo_dims.height, canvas_height);
        //g.transform('s2');
        var init_x = ( (canvas_width - logo_dims.width) / 2.5 ).toString();
        //canvas height gets divided by 4 because svg height is 50vh
        var init_y = ( (canvas_height / 4 - logo_dims.height) / 2 ).toString();
        // set initial placement in middle of canvas
        t_string = 's1.1 t' + init_x.toString() + ' ' + init_y.toString();
        g.transform(t_string);
        //g.transform('S1.2 ' + t_string);
        // var sf = (canvas_width -40) / logo_dims.width;
        // var transform_str = 's' + sf.toString();
        // console.log(init_x, init_y);
        // init_x = (0.8*parseInt(init_x) / sf).toString();
        // init_y = (0.5*parseInt(init_y) / sf).toString();
        // transform_str += ' t' + init_x + ' ' + init_y;
        // g.animate({
        //     transform: transform_str
        // }, 1000, mina.elastic);
    });
};


// var googleFailure = function() {
//     alert('Google Maps failed to load.');
// };

