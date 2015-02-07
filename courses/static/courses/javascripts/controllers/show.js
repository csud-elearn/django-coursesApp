var app = angular.module('controllers');

app.controller('ShowCourseController', ['$scope', '$routeParams', '$location', 'Page', 'Comment', function($scope, $routeParams, $location, Page, Comment) {
  $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
    $scope.course = page.course
    
    $scope.firstPage = function() {
      return $scope.page.order === 1;
    };
    $scope.lastPage = function() {
      return $scope.page.order === $scope.page.total_pages;
    };

  });

  $scope.nextPage = function() {
    $location.path($scope.course.id + "/view/" + ($scope.page.order + 1));
  };
  $scope.previousPage = function() {
    $location.path($scope.course.id + "/view/" + ($scope.page.order - 1));
  };

  $scope.comments = Comment.query({courseId: $routeParams.courseId});

  var newComment = new Comment({"placeholder":"Ton commentaire", "user":"Keran", course_id: $routeParams.courseId});
  $scope.comment = Object.create(newComment);

  $scope.saveComment = function() {
    $scope.comment.$save(function(comment) {
      $scope.comments.push(comment);
      $scope.comment = Object.create(newComment);
    });
  };
}]);