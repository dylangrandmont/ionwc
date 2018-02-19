const gulp = require('gulp');
const browserSync = require('browser-sync').create();
const jasmine = require('gulp-jasmine');
const zip = require('gulp-zip');

gulp.task('watch', ()=>
  browserSync.init({
    server: {
      baseDir: 'app'
    },
  })
);
 
gulp.task('test', () =>
  gulp.src('test/*.js')
    // gulp-jasmine works on filepaths so you can't have any plugins before it
    .pipe(jasmine())
);

gulp.task('zip', () =>
  gulp.src('app/**')
    .pipe(zip('map.zip'))
    .pipe(gulp.dest('dist'))
);

gulp.task('build', ['test', 'zip'], function (){
});
