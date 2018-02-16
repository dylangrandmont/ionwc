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

const chmod = require('gulp-chmod');
gulp.task('chmod', () =>
    gulp.src('src/app.js')
        .pipe(chmod({
            owner: {
                read: true,
                write: true,
                execute: true
            },
            group: {
            	read: true,
                execute: true
            },
            others: {
            	read: true,
                execute: true
            }
        }))
        .pipe(gulp.dest('dist'))
);

const zip = require('gulp-zip');
gulp.task('zip', () =>
    gulp.src('app/**')
        .pipe(zip('map.zip'))
        .pipe(gulp.dest('dist'))
);

gulp.task('build', ['chmod', 'zip'], function (){
});
