// setup server
const express = require("express");
const app = express();
const process = require("process");
const superagent = require("superagent");
const geolib = require("geolib");
const cors = require("cors");
const XLSX = require("xlsx");
const multer = require("multer");
const upload = multer({ dest: "uploads/" });

// switch for local debugging
var localMode = true;
var optimizerPath = "";

// data parser - used to parse post data
var bodyParser = require("body-parser");
var jsonParser = bodyParser.json();
app.use(bodyParser.urlencoded({ extended: true }));

// allow cross-origin resource sharing (CORS)
app.use(cors());

// setup directory used to serve static files
app.use(express.static("public"));

// MongoDB connection parameters
const MongoClient = require("mongodb").MongoClient;
var ObjectId = require("mongodb").ObjectId;
const db_url =
  "mongodb+srv://[secret]@lasagna-class-project-d.ljwaj.mongodb.net/endless-pastabilities?retryWrites=true&w=majority";
const dbClient = new MongoClient(db_url, {
  useUnifiedTopology: true,
  useNewUrlParser: true,
});

const getGarfields = function (db, res, id = null, cohort = null) {
  const collection = db.collection("garfield");

  const findFilter = {};

  if (id != null) findFilter["_id"] = ObjectId(id);

  if (cohort != null) findFilter["cohort"] = cohort;

  collection.find(findFilter).toArray(function (err, docs) {
    console.log("Find Garfields. Returning " + docs.length + " values.");
    res.send(docs);
  });
};

const createGarfield = function (db, userData, res) {
  const collection = db.collection("garfield");
  collection.insertOne(userData, function (err, result) {
    res.send(result.insertedId);
  });
};

const getMamas = function (db, res, id = null, cohort = null) {
  const collection = db.collection("mama");

  const findFilter = {};

  if (id != null) findFilter["_id"] = ObjectId(id);

  if (cohort != null) findFilter["cohort"] = cohort;

  collection.find(findFilter).toArray(function (err, docs) {
    console.log("Find Mamas. Returning " + docs.length + " values.");
    res.send(docs);
  });
};

const tryByCohort = function(db, res){
  const collection = db.collection("mama");
  collection.aggregate([
    {$lookup: 
      {
        from: 'regions',
        localField: 'zip_code',
        foreignField: '_id',
        as: 'something'
      }
    }]).toArray((err, r) => {
      res.send(r);
    });
};

const createMama = function (db, userData, res) {
  const collection = db.collection("mama");
  collection.insertOne(userData, function (err, result) {
    res.send(result.insertedId);
  });
};

const buildDistanceMatrix = function (db, res) {
  const dMatrix = db.collection("distance-matrix");
  const garfield = db.collection("garfield");
  const mama = db.collection("mama");

  mama.find({}).toArray(function (err_mama, mamas) {
    garfield.find({}).toArray(function (err_garfield, garfields) {
      mamas.forEach((element_mama) => {
        if (element_mama.lat != null && element_mama.long != null) {
          var jsonPush = {};
          jsonPush["mama"] = element_mama._id.toString();
          garfields.forEach((element_garfield) => {
            if (element_garfield.lat != null && element_garfield.long != null) {
              const new_distance =
                geolib.getDistance(
                  { latitude: element_mama.lat, longitude: element_mama.long },
                  {
                    latitude: element_garfield.lat,
                    longitude: element_garfield.long,
                  }
                ) / 1609.34;
              jsonPush[element_garfield._id.toString()] = new_distance;
            }
          });
          console.log(jsonPush);
          dMatrix.insertOne(jsonPush);
        }
      });
      res.send("done.");
    });
  });
};

const addOptimizeRequest = function (db, mamas, garfields, res) {
  const garfield = db.collection("garfield");
  const mama = db.collection("mama");
  const requestTable = db.collection("optimize-requests");
  const controlTable = db.collection("optimize-control");

  const d = new Date().toISOString();

  requestTable.insertOne(
    { _id: d, garfields: garfields, mamas: mamas },
    (err, insertRes) => {

      controlTable.insertOne({ _id: d, status: "pending" }, (e2, i2) => {

        if (insertRes["insertedCount"] > 0 && i2["insertedCount"] > 0)
        {
          const p = optimizerPath + '/optimize/' + d;
          console.log("optimizer request url: " + p);
          superagent.get(p).end();
          res.send(d);
        }
        else res.send(null);
      });
    }
  );
};

const getOptimizeStatus = function (db, id, res) {
  const controlTable = db.collection("optimize-control");
  controlTable.findOne({ _id: id }, (err, docs) => {
    res.send(docs);
  });
};

const getOptimizeResult = function (db, id, res) {
  const resultTable = db.collection("optimize-results");
  resultTable.find({ _id: id }).toArray((err, result) => {
    res.send(result);
  });
};

const getRunIDs = function(db, res, options = {}){
  const controlTable = db.collection("optimize-control");
  controlTable.find({}, options).toArray((err,result) => {
    res.send(result);
  });
};

const getRegionList = function(db, res) {
  const regionTable = db.collection("regions");
  regionTable.distinct('Region', (err, result) => {
    res.send(result);
  });
};

const getRegionalLeaderList = function(db, res) {
  const regionTable = db.collection("regions");
  regionTable.distinct('Regional Leader', (err, result) => {
    res.send(result);
  });
};

const cleanExit = function (db) {
  db.close(() => {
    console.log("MongoDB connection closed.");
    process.exit(0);
  });
};

// Connect to MongoDB and advertise endpoints
dbClient.connect(function (err) {
  console.log("Connecting to MongoDB");
  const db = dbClient.db("endless-pastabilities");

  // Get All Garfields
  app.get("/users/garfield/all", function (req, res) {
    getGarfields(db, res);
  });

  // Get Garfield by ID
  app.get("/users/garfield/id/:id", function (req, res) {
    getGarfields(db, res, (id = req.params.id));
  });

  // Get Garfield by cohort
  app.get("/users/garfield/cohort/:cohort", function (req, res) {
    getGarfields(db, res, null, (cohort = req.params.cohort));
  });

  // Create new Garfield
  app.post("/users/garfield/create", jsonParser, function (req, res) {
    const userData = {};
    userData["name"] = req.body.name;
    userData["address"] = req.body.address;
    userData["city"] = req.body.city;
    userData["state"] = req.body.state;
    userData["zip_code"] = req.body.zip_code;
    userData["special_veg"] = req.body.special_veg;
    userData["special_vgn"] = req.body.special_vgn;
    userData["special_dairy"] = req.body.special_dairy;
    userData["special_gluten"] = req.body.special_gluten;
    userData["lat"] = req.body.lat;
    userData["long"] = req.body.long;
    if (req.body.quantity === undefined) userData["quantity"] = 0;
    else userData["quantity"] = parseInt(req.body.quantity);
    if (req.body.cohort === undefined) userData["cohort"] = "zzz";
    else userData["cohort"] = req.body.cohort;
    userData["active"] = false;
    createGarfield(db, userData, res);
  });

  // Get All Mamas
  app.get("/users/mama/all", function (req, res) {
    getMamas(db, res);
  });

  // Get Mamas by ID
  app.get("/users/mama/id/:id", function (req, res) {
    getMamas(db, res, (id = req.params.id), null);
  });

  // Get Mamas by cohort
  app.get("/users/mama/cohort/:cohort", function (req, res) {
    getMamas(db, res, null, (cohort = req.params.cohort));
  });

  // Create new Mama
  app.post("/users/mama/create", jsonParser, function (req, res) {
    const userData = {};
    userData["name"] = req.body.name;
    userData["address"] = req.body.address;
    userData["city"] = req.body.city;
    userData["state"] = req.body.state;
    userData["zip_code"] = req.body.zip_code;
    userData["special_veg"] = req.body.special_veg;
    userData["special_vgn"] = req.body.special_vgn;
    userData["special_dairy"] = req.body.special_dairy;
    userData["special_gluten"] = req.body.special_gluten;
    userData["lat"] = req.body.lat;
    userData["long"] = req.body.long;
    if (req.body.quantity === undefined) userData["quantity"] = 0;
    else userData["quantity"] = parseInt(req.body.quantity);
    if (req.body.miles === undefined) userData["miles"] = 0;
    else userData["miles"] = parseInt(req.body.miles);
    if (req.body.cohort === undefined) userData["cohort"] = "zzz";
    else userData["cohort"] = req.body.cohort;
    userData["active"] = false;
    createMama(db, userData, res);
  });

  // Rebuild the distance table
  app.get("/working/rebuildmatrix", function (req, res) {
    buildDistanceMatrix(db, res);
  });

  // Add new Optimizer request
  app.post("/optimize/request", jsonParser, function (req, res) {
    const garfields = req.body.garfields;
    const mamas = req.body.mamas;
    addOptimizeRequest(db, mamas, garfields, res);
  });

  // Get run status
  app.get("/optimize/status/:id", function (req, res) {
    getOptimizeStatus(db, req.params.id, res);
  });

  // Get control table entries
  app.get("/optimize/list", function (req, res){
    getRunIDs(db, res);
  });

  // Get control table IDs
  app.get("/optimize/list/idonly", function (req, res){
    getRunIDs(db, res, {projection:{'_id':1}});
  });

  // Get run results
  app.get("/optimize/results/:id", function (req, res) {
    getOptimizeResult(db, req.params.id, res);
  });

  // Get Region list
  app.get("/info/regions", function (req, res) {
    getRegionList(db, res);
  });

  // Get Regional Leader list
  app.get("/info/regionalleaders", function (req, res) {
    getRegionalLeaderList(db, res);
  });

  // Test
  app.get("/test/cohort", function (req, res) {
    tryByCohort(db, res);
  });

  app.post("/upload", upload.array("xlfile"), function (req, res) {
    var XLSX = require("xlsx");
    var workbook = XLSX.readFile(req.files[0].path);
    // console.log(workbook);

    var sheet_name_list = workbook.SheetNames;
    sheet_name_list.forEach(function (y) {
      var worksheet = workbook.Sheets[y];
      for (z in worksheet) {
        if (z[0] === "!") continue;
      }
    });
  });
});

// start server
// -----------------------
app.listen(process.env.PORT || 3000, function () {
  console.log("Starting LM Orchestrator");
  console.log("Trying " + process.env.PORT);
  console.log("Fallback to 3000");
  if(process.env.PORT === undefined)
  {
    localMode = true;
    optimizerPath = "https://lm-optimizer.azurewebsites.net";
    console.log("Local Mode");
  }  
  else
  {
    localMode = false;
    optimizerPath = "https://lm-optimizer.azurewebsites.net";
    console.log("Production Mode");
  }
  
});

process.on("SIGINT", (code) => {
  console.log("Dying with " + code);
  cleanExit(dbClient);
});

process.on("SIGTERM", (code) => {
  console.log("Dying with " + code);
  cleanExit(dbClient);
});
