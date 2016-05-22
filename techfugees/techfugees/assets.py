from django_assets import Bundle, register

# JavaScript
common_js = Bundle(
    'js/project.js',
)
js_all = Bundle(
    common_js,
    filters="jsmin",
    output='generated/packed.js'
)
register('js_all', js_all)

#CSS and SASS
sass = Bundle('sass/main.scss',
              filters='scss',
              output='generated/sass.css',
              depends='sass/_*.scss')
css_all = Bundle('css/*.css',
                 output='generated/css_all.css')

register('sass', sass)
register('css_all', css_all)
