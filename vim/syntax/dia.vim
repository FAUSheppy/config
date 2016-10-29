echom "WAT IS THIS CRAP"

syntax match nodeID "/\vN.*:"
syntax match leaveID '/\v[A-MO-Z].*:'

syntax match annotation "[%@].*"

syntax match regie "\*.*\*"

hi def link nodeID Structure
hi def link leaveID Tag
hi def link annotation Function
hi def link regie String

let b:current_syntax = 'dia'
