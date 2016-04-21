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
        
        //console.log($scope.userid);
        
        // $scope.storeUserId = function(userid) {
        //     console.log('test');
        //     localStorage.setItem('userid', userid);
        // }
});
 
