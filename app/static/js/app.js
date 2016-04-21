var myApp = angular.module('wishlistApp', []);

    myApp.controller('defaultController', function($scope, $http) {
        $scope.appClickEvent = function(clickEvent) {
            var element = clickEvent.target;
            var img_url = element.src;
            console.log(img_url);
            
            var address_url = location.pathname;
            console.log(address_url);
            
            var address_urlparts = address_url.split("/");
            console.log(address_urlparts);
            
            $http.post('/api/imageurl/addimage' ,{
                image_url : img_url,
                item_id : address_urlparts[4]
            }).then(function(response){
                window.location = '/api/user/' + localStorage.getItem('userid');
            });
        }
        
       
});
    myApp.controller('emailCtrl', function($scope, $http) {
        $scope.isPopupVisible = false;
        $scope.isComposePopupVisible = false;
        $scope.composeEmail = {};
        
        $scope.sendEmail = function() {
            $scope.isComposePopupVisible = false;
            alert($scope.composeEmail.to
                + " " + $scope.composeEmail.subject
                + " " + $scope.composeEmail.body);
    };
        $scope.showComposePopup = function() {
        $scope.composeEmail = {};
        $scope.isComposePopupVisible = true;
    };

         $scope.closeComposePopup = function() {
        $scope.isComposePopupVisible = false;
    };
        $scope.showPopup = function(email) {
        $scope.isPopupVisible = true;
    };
        $scope.closePopup = function() {
        $scope.isPopupVisible = false;
    };
        
        $scope.showComposePopup = function() {
            $scope.composeEmail = {};
            $scope.isComposePopupVisible = true;
    };
 
});