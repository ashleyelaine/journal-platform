'use strict';

const configs = require('./.gulp.config');
const gulp = require('gulp');

// Errors Handler for tasks
const gutil = require('gulp-util');
const notify = require('gulp-notify');
const reportErrors = (error) => {
  const lineNumber = (error.lineNumber) ? 'LINE ' + error.lineNumber + ' -- ' : '';
  notify({
    title: 'Task Error: [' + error.plugin + ']',
    message: lineNumber + 'See console.',
    sound: 'Sosumi',
  }).write(error);

  gutil.beep();

  var report = '';
  var chalk = gutil.colors.white.bgRed;

  report += chalk('TASK:') + ' [' + error.plugin + ']\n';
  report += chalk('CULPRIT:') + ' ' + error.message + '\n';
  if (error.lineNumber) {
    report += chalk('LINE:') + ' ' + error.lineNumber + '\n';
  }
  if (error.fileName) {
    report += chalk('FILE:') + ' ' + error.fileName + '\n';
  }
  if (error.cause) {
    report += chalk('CAUSE:') + ' ' + error.cause + '\n';
  }
  console.error(report);
};


/* ----- BEGINS GULP TASKS ----- */
// Tasks are in alphabetical orders.


const argv = require('yargs').argv;
const autoprefixer = require('autoprefixer');
const browserSync = require('browser-sync').create();
const changed = require('gulp-changed');
const concat = require('gulp-concat');
const cssmin = require('gulp-cssmin');
const del = require('del');
const eslint = require('gulp-eslint');
const gulpif = require('gulp-if');
const imagemin = require('gulp-imagemin');
const lazypipe = require('lazypipe');
const newer = require('gulp-newer');
const plumber = require('gulp-plumber');
const postcss = require('gulp-postcss');
const sass = require('gulp-sass');
const sasslint = require('gulp-sass-lint');
const soften = require('gulp-soften');
const sourcemaps = require('gulp-sourcemaps');
const stripCssComments = require('gulp-strip-css-comments');
const uglify = require('gulp-uglify');
const using = require('gulp-using');


/* ----- build ----- */

gulp.task('build', ['scripts', 'sass', 'fonts', 'images'], function(done) {
  done();
});


/* ----- clean ----- */

gulp.task('clean', (cb) => {
  del(['static/**/*']);
  cb();
});

gulp.task('clean:css', () => {
  return del(['static/css']);
});

gulp.task('clean:fonts', () => {
  return del(['static/fonts']);
});

gulp.task('clean:images', () => {
  return del(['static/images']);
});

gulp.task('clean:js', () => {
  return del(['static/js']);
});


/* ----- detab ----- */

const detab = lazypipe()
  .pipe(function() {
      return soften(0);
  });


/* ----- fonts ----- */

gulp.task('fonts', () =>{
  return gulp.src(configs.paths.fonts_vendor.concat(configs.paths.fonts_src))
    .pipe(newer(configs.paths.fonts_dest))
    .pipe(gulp.dest(configs.paths.fonts_dest))
    .pipe(browserSync.reload({stream: true}));
});


/* ----- images ----- */

gulp.task('images', () => {
  return gulp.src(configs.paths.images_src)
    .pipe(using(configs.using_opts))
    .pipe(newer(configs.paths.images_dest))
    .pipe(gulpif(argv.production, imagemin()))
    .pipe(gulp.dest(configs.paths.images_dest))
    .pipe(browserSync.reload({stream: true}));
});


/* ----- lint ----- */

gulp.task('lint', ['lint:js', 'lint:sass']);

gulp.task('lint:js', () => {
  return gulp.src(configs.paths.scripts_src.concat([
    'gulpfile.js', '.gulp.config.js',
  ]))
    .pipe(detab())
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError())
  ;
});

gulp.task('lint:sass', () => {
  return gulp.src(configs.paths.scss_src)
    .pipe(detab())
    .pipe(sasslint())
    .pipe(sasslint.format())
    .pipe(sasslint.failOnError())
  ;
});


/* ----- sass ----- */

const compileSassTask = lazypipe()
  .pipe(function() {
    return sourcemaps.init();
  })
  .pipe(function() {
    return sass().on('error', reportErrors);
  })
  .pipe(function() {
    return postcss([autoprefixer({browsers: ['last 15 versions', '> 1%']})]);
  })
  .pipe(function() {
    return gulpif(argv.production, cssmin());
  })
  .pipe(function() {
    return sourcemaps.write('.');
  })
  .pipe(stripCssComments);

gulp.task('sass', ['lint:sass'], () => {
  return gulp.src(configs.paths.scss_vendor.concat(configs.paths.scss_src))
    .pipe(changed(configs.paths.scss_dest))
    .pipe(using(configs.using_opts))
    .pipe(plumber({
      errorHandler: reportErrors,
    }))
    .pipe(compileSassTask())
    .pipe(concat(configs.paths.scss_out))
    .pipe(gulp.dest(configs.paths.scss_dest))
    .pipe(browserSync.stream({match: '**/*.css'}));
});


/* ----- scripts ----- */

gulp.task('scripts', ['lint:js'], () => {
  return gulp.src(configs.paths.scripts_vendor.concat(configs.paths.scripts_src))
    .pipe(using(configs.using_opts))
    .pipe(concat(configs.paths.scripts_out))
    .pipe(gulpif(argv.production, uglify().on('error', reportErrors)))
    .pipe(gulp.dest(configs.paths.scripts_dest))
    .pipe(browserSync.stream({match: '**/*.js'}));
});


/* ----- watch ----- */

gulp.task('watch', ['build'], function() {
  browserSync.init({
      proxy: configs.bs_proxy,
      xip: configs.bs_use_xip,
  });

  gulp.watch(configs.paths.scss_watch, ['sass']);
  gulp.watch(configs.paths.images_watch, ['images']);
  gulp.watch(configs.paths.scripts_watch, ['scripts']);
  gulp.watch(configs.paths.fonts_watch, ['fonts']);
  gulp.watch(configs.paths.html_watch).on('change', browserSync.reload);
});

gulp.task('default', [argv.production ? 'build' : 'watch']);
