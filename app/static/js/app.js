var myApp = angular.module('wishlistApp', []);

    myApp.controller('defaultController', function($scope, $location, $localStorage, $http) {
        $scope.appClickEvent = function(clickEvent) {
            var element = clickEvent.target;
            var img_url = element.src;
            console.log(img_url);
            // change to $location.path() when you switch to angular routes
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
        };
        
       
});
    myApp.controller('emailController', function($scope, $location, $http) {
        $scope.isPopupVisible = false;
        $scope.isComposePopupVisible = false;
        $scope.composeEmail = {};
        
        $scope.showPopup = function(email) {
        $scope.selectedEmail = email;
        $scope.isPopupVisible = true;
    };
        $scope.closePopup = function() {
            $scope.isPopupVisible = false;
    };
         $scope.emailSent = false;
         // change to $location.path() when you switch to angular routes
         var addressBarUrl = location.pathname;
            console.log(addressBarUrl);
            var addressBarUrlParts = addressBarUrl.split("/");
            console.log(addressBarUrlParts);
        
        $scope.sendEmail = function() {
            $http.post("/api/user/" + addressBarUrlParts[3] + "/wishlists/share", {email: $scope.email})
            .then(function (response) {
                $scope.emailSent =true;
                console.log (response.data);
                jQuery('#myModal').modal('hide');
                
                }, function() {
                    $scope.emailSent = false;
                });
        };
        
        $scope.showComposePopup = function() {
            $scope.composeEmail = {};
            $scope.isComposePopupVisible = true;
        };
 
});