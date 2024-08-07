const express= require('express')
const bodyParser= require('body-parser')
const app= express()
const port =  process.env.PORT|| 3000;
app.use(bodyParser.urlencoded({extended: true}))

app.get("/", function(req, res) {
    console.log("New home request by:", req.hostname);
    res.send("Ok :)")
    console.log(req.body);
})

app.listen(port, ()=> {
    console.log("Server started at port:", port);
})