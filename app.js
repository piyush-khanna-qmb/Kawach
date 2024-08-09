const express= require("express")
const bodyParser= require('body-parser')
const app= express()
const port =  process.env.PORT|| 3000;
app.use(bodyParser.urlencoded({extended: true}))

app.get("/", function(req, res) {
    console.log("New home request by:", req.hostname);
    console.log(req.body);
    res.send("Ok :)")
})

var listener = app.listen(port, function(){
    console.log('Listening on port ' + JSON.stringify(listener.address()));
});