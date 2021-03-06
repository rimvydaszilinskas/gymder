var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: {
        'index': './src/index.js',
        'activity_tag_filtering': './src/activities/tagSearch.js',
        'activity_view': './src/activities/preview.js',
        'activities_view': './src/activities/viewactivities.js',
        'activity_attendees': './src/activities/attendees.js',
        'activities_search': './src/activities/search.js',
        'create_activity': './src/activities/create.js',
        'user_groups': './src/groups/user_groups.js',
        'group_create': './src/groups/create.js',
        'group_view': './src/groups/preview.js',
        'group_members': './src/groups/members.js',
        'group_activities': './src/groups/activities.js',
        'profile': './src/users/profile.js',
        'profile_settings': './src/users/settings.js',
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
