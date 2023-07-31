const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const { dirname } = require('path');
const multer = require('multer');
const fs = require('fs');
const { parse } = require("csv-parse");
const readline = require('readline');
const upload = multer({ dest: __dirname+'/uploads/' });

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
app.get('/static_phi_matrixes', (req, res) => {
    res.render('static_phi_matrixes.ejs');
});
app.post('/static_phi_matrixes_result',upload.single('csvFile'), (req, res) => {
    if (!req.file) {
      return res.status(400).send('No file uploaded');
    }


  const rl = readline.createInterface({
    input: fs.createReadStream(req.file.path),
    crlfDelay: Infinity
  });

  let lineNumber = 0;
  let final_array = {},new_line,betaArray = [],SheetArray = [];
  rl.on('line', (line) => {
    lineNumber++;

    if (lineNumber === 1) {
      // Skip the first line of the file
      return;
    }
    new_line = line.split(",");
    if (!betaArray.includes(new_line[2])) {
      betaArray.push(new_line[2]);
    }
    if (!SheetArray.includes(new_line[4])) {
      SheetArray.push(new_line[4]);
    }
    
    if(typeof final_array[new_line[2]] === "undefined"){
      final_array[new_line[2]] = {};
    }
    final_array[new_line[2]][new_line[4]] = new_line.splice(6);

    lineNumber++;
  });

  rl.on('close', () => {
    // Delete the uploaded file
    fs.unlinkSync(req.file.path);
    
    // Send a response to the client
    res.render('static_phi_matrixes_result.ejs',{final_array : final_array,betaArray:betaArray,SheetArray:SheetArray});
  });
    
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