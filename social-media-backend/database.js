var sqlite3 = require('sqlite3').verbose()
var md5 = require('md5')

const DBSOURCE = "../social-media-training/twitter.db" 


let db = new sqlite3.Database(DBSOURCE, (err) => {
    if (err) {
      // Cannot open database
      console.error(err.message)
      throw err
    }else{
        console.log('Connected to the SQlite database.')
    }
})


module.exports = db

