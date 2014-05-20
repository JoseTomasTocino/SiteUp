module.exports = function (grunt) {

    grunt.initConfig({
        clean: {
            sass: [".sass-cache", "siteup_frontend/static/css/style.css"],
            js: ["siteup_frontend/static/js/main.js"]
        },
        compass: {
            build: {
                options: {
                    config: 'config.rb'
                }
            }
        },
        watch: {
            sass: {
                files: ['theme/scss/**/*.scss', '*.html'],
                tasks: ['compass'],
                options: {
                    livereload: true,
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // grunt.registerTask('default', ['clean:sass', 'clean:js', 'compass', 'autoprefixer']);
    grunt.registerTask('default', ['clean:sass', 'clean:js', 'compass', 'autoprefixer', 'concat' /*, 'uglify'*/]);
}