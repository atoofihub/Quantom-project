const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const { dirname } = require('path');
const fs = require('fs');
const { parse } = require("csv-parse");

const app = express();

const resolve = require('path').resolve;
const absolutePath = resolve('./');

app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
app.use(express.static(absolutePath + '/'));
app.use('/assets', express.static(__dirname + '/assets'));
app.set("view engine", "ejs");
app.set("views", __dirname);

app.get('/static', (req, res) => {
    res.render('show_result.ejs');
});
app.get('/dynamic', (req, res) => {
    res.render('index.ejs');
});
app.post('/run', (req, res) => {
    let data = JSON.parse( JSON.stringify(req.body) ) ;
    let LValue = data.LValue.toString();
    let final_data = [];
    console.log('hello');
  const pythonProcess = spawn('python3', [ __dirname + '/main.py' ,  '-l '+LValue]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
    setTimeout(function (){
        if(fs.existsSync(__dirname+'/eigenvalues_L'+LValue+'.csv')){

            fs.createReadStream(__dirname+'/eigenvalues_L'+LValue+'.csv')
            .pipe(parse({ delimiter: ",", from_line: 2 }))
            .on("data", function (row) {
                final_data.push([ row[1],row[2],row[4],row[5],row[6]+","+row[7]+","+row[8]+","+row[9]+","+row[10]+","+row[11]+","+row[12]+","+row[13] ]);
                // console.log(row);
            })
            .on("error", function (error) {
                console.log(error.message);
            })
            .on("end", function () {
                console.log(final_data[0]);
                res.json({
                    'status' : 200,
                    'data' : final_data
                });
                console.log("finished");
            }); 

        }
    },500);
  });
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});