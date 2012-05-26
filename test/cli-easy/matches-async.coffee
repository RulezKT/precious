exec     = require('child_process').exec
parallel = require('async').parallel

man = (page, cb) ->
  exec "man #{page}", (err, stdout, stderr) ->
    if err?
      cb err, stderr.toString()
    else
      cb null, "\n#{stdout}\n"

parallel {
  man: (cb) ->
    parallel {
      precious1: (cb) -> man 'precious', cb
      json7: (cb) -> man 'precious-json', cb
    }, (err, pages) ->
      cb null, pages
  # there could be other stuff to load in parallel to man-pages
}, (err, matches) ->
  # console.log matches
  module.exports = matches

