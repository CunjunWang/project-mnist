// const path = require("path");
// const HtmlWebpackPlugin = require('html-webpack-plugin');
//
// module.exports = {
//     entry: ["babel-polyfill", "./js/Drawer.js"],
//     output: {
//         path: path.resolve(__dirname, "dist"),
//         filename: "js/bundle.js"
//     },
//     devServer: {
//         contentBase: "./dist"
//     },
//     plugins: [
//         new HtmlWebpackPlugin({
//             filename: 'index.html',
//             template: '../templates/index.html'
//         })
//     ],
//     module: {
//         rules: [
//             {
//                 test: /\.js$/,
//                 exclude: /node_modules/,
//                 use: {
//                     loader: 'babel-loader'
//                 }
//             }
//         ]
//     },
//     resolve: {
//         alias: {
//             joi: 'joi-browser'
//         }
//     }
// };