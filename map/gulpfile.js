const gulp = require('gulp');

var browserSync = require('browser-sync').create();

gulp.task('browserSync', function() {
  browserSync.init({
    server: {
      baseDir: 'app'
    },
  })
})

gulp.task('watch', ['browserSync'], function (){
});

const zip = require('gulp-zip');
 
gulp.task('build', () =>
    gulp.src('app/**')
        .pipe(zip('map.zip'))
        .pipe(gulp.dest('dist'))
);