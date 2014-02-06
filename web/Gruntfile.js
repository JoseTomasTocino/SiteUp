module.exports = function (grunt) {

    grunt.initConfig({
        clean: {
            sass: [".sass-cache", "siteup_frontend/static/css/style.css"],
            js: ["siteup_frontend/static/js/main.js"]
        },
        compass: {
            build: {
                options: {
                    sassDir: 'siteup_frontend/static_src/scss',
                    cssDir: 'siteup_frontend/static/css',
                    environment: 'production'
                }
            }
        },
        autoprefixer: {
            options: {
                browsers: ['last 2 version']
            },
            build: {
                src: 'siteup_frontend/static/css/style.css'
            },
        },
        concat: {
            options: {
                separator: ';',
            },
            build: {
                src: ['src/js/**/*.js'],
                dest: 'src/js/main.js'
            }
        },
        uglify: {
            build: {
                src: 'src/js/main.js',
                dest: 'assets/js/main.min.js'
            }
        },
        watch: {
            sass: {
                files: ['siteup_frontend/static_src/scss/**/*.scss', 'siteup_frontend/templates/*'],
                tasks: ['clean:sass', 'compass', 'autoprefixer'],
                options: {
                    livereload: true,
                }
            },
            js: {
                files: 'src/js/**/*.js',
                tasks: ['clean:js', 'concat', 'uglify'],
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['clean:sass', 'clean:js', 'compass', 'autoprefixer']);
//    grunt.registerTask('default', ['clean:sass', 'clean:js', 'compass', 'autoprefixer', 'concat', 'uglify']);
}