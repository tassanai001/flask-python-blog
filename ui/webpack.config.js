module.exports = {
  // This is the "main" file which should include all other modules
  context: __dirname,
  entry: __dirname + "/src/main.js",
  // Where should the compiled file go?
  output: {
    // To the `dist` folder
    path: __dirname + "/dist",
    publicPath: "dist/",
    // With the filename `build.js` so it's dist/build.js
    filename: "build.js"
  },
  module: {
    // Special compilation rules
    rules: [
      {
        // I tried this option as well, it didn't help
        // test: /\.vue$/,
        // loader: 'vue-loader',
        // options: {
        //   loaders: {
        //     // {{#sass}}
        //     // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
        //     // the "scss" and "sass" values for the lang attribute to the right configs here.
        //     // other preprocessors should work out of the box, no loader config like this necessary.
        //     'scss': 'vue-style-loader!css-loader!sass-loader',
        //     'sass': 'vue-style-loader!css-loader!sass-loader?indentedSyntax'
        //     // {{/sass}}
        //   }
        //   // other vue-loader options go here
        // }
        test: /\.vue$/,
        loader: "vue-loader",
        options: {
          loaders: {
            // Customize to your liking
            js: "babel-loader",
            scss: ["style-loader", "css-loader", "sass-loader"]
          }
        }
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: "file-loader",
        options: {
          name: "[name].[ext]?[hash]"
        }
      }
    ]
  },
  resolve: {
    alias: { vue$: "vue/dist/vue.esm.js" }
  }
};
