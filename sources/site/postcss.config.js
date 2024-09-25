const enableBuild = process.env.mode === 'build'

export default ({ ctx }) => ({
	map: enableBuild ? false : 'inline',
	plugins: {
		'@csstools/postcss-global-data':{
		  files: ['./node_modules/@viur/ignite/foundation/mediaqueries.css']
		},
    'postcss-import': {},
		'postcss-discard-comments': enableBuild ? {} : false,
		'@csstools/postcss-bundler': {},
		'postcss-preset-env': {
			stage: 3,
			minimumVendorImplementations: 2,
			autoprefixer: {},
			debug: true,
			features: {
    			'color-mix': true,
				'nesting-rules': true,
				'oklab-function': true,
                //'cascade-layers': true,
                'custom-media-queries': true,
  			}
		},
		'postcss-focus': {},
		'postcss-sort-media-queries': {},
		'cssnano': enableBuild ? {} : false,
	}
})
