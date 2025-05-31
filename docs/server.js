// docs/server.js
const express = require('express')
const path = require('path')
const app = express()

const port = process.env.PORT || 4000

// Раздаём статические файлы из той же папки, где лежит этот server.js
app.use(express.static(__dirname))

// Для любых других роутов возвращаем index.html из этой же папки
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'))
})

app.listen(port, () => {
    console.log(`🟢 App listening on port ${port}`)
})
