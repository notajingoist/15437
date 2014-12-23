// Include gulp
var gulp = require('gulp'); 

// Include Our Plugins
var jshint = require('gulp-jshint');
var less = require('gulp-less');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');

// Lint Task
gulp.task('lint', function() {
    return gulp.src('grumblr_app/static/js/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// Compile Our Less
gulp.task('less', function() {
    return gulp.src('grumblr_app/static/css/*.less')
        .pipe(less())
        .pipe(gulp.dest('grumblr_app/static/css'));
});

// Concatenate & Minify JS
gulp.task('scripts', function() {
    return gulp.src('grumblr_app/static/js/*.js')
        .pipe(concat('all.js'))
        .pipe(gulp.dest('dist'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('grumblr_app/static/js/*.js', ['lint', 'scripts']);
    gulp.watch('grumblr_app/static/css/*.less', ['less']);
});

// Default Task
gulp.task('default', ['lint', 'less', 'scripts', 'watch']);