var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: {
        'index': './src/index.js',
        'activity_view': './src/activities/preview.js',
        'activities_view': './src/activities/viewactivities.js',
        'activity_attendees': './src/activities/attendees.js',
        'create_activity': './src/activities/create.js',
    },
    output: {
        path: path.resolve('./static/bundles/'),
        publicPath: '/static/bundles/',
        filename: '[name]-[hash].js'
    },
    plugins: [
        new BundleTracker(
            {
                filename: './webpack-stats.json'
            }
        )
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            }
        ]
    },
    resolve: {
        extensions: [
            '*',
            '.js',
            '.jsx'
        ]
    }
};
