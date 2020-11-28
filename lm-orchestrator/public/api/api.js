var all_mamas; // returned DB of mamas
var all_garfields; // returned DB of garfields
var selected_mamas;
var selected_garfields;

async function loadMamas() {
  try {
    const url = "/users/mama/all";

    const response = await superagent.get(url);
    all_mamas = response.body;
    return all_mamas;
  } catch (error) {
    console.log(error.response.body);
  }
}

async function loadGarfields() {
  try {
    const url = "/users/garfield/all";

    const response = await superagent.get(url);
    all_garfields = response.body;
    return all_garfields;
  } catch (error) {
    console.log(error.response.body);
  }
}

async function sendSelections() {
  try {
    var mama_ids = [];
    selected_mamas.forEach((mama) => {
      mama_ids.push(mama._id);
    });

    var garf_ids = [];
    selected_garfields.forEach((garfs) => {
      garf_ids.push(garfs._id);
    });

    const url = "/optimize/request";
    const response = await superagent.post(url).send({
      garfields: garf_ids,
      mamas: mama_ids,
    });
    // console.log(response);
    return response.text;
  } catch (error) {
    console.log(error);
  }
}

async function getOptResults(id) {
  try {
    const url = "/optimize/results/" + id;

    const response = await superagent.get(url);
    // console.log(response);
    return response;
  } catch (error) {
    console.log(error);
  }
}

async function file_load() {
  try {
    const url = "/upload";

    var frm = new FormData(document.getElementById("myForm"));
    const response = await superagent
      .post(url)
      .attach("xlfile", frm.get("xlfile"));
  } catch (error) {
    console.log(error);
  }
}

async function getPastRuns() {
  try {
    const url = "/optimize/list";

    const response = await superagent.get(url);
    // console.log(response);
    return response;
  } catch (error) {
    console.log(error);
  }
}

function exported() {
  table = document.getElementById("results_table");
  var $results_table = $("#results_table");
  $($results_table).table2excel({
    exclude: ".noExl",
    name: "Excel Document Name",
    filename:
      "BBBootstrap" +
      new Date().toISOString().replace(/[\-\:\.]/g, "") +
      ".xls",
    fileext: ".xls",
    exclude_img: true,
    exclude_links: true,
    exclude_inputs: true,
    preserveColors: false,
  });
}

async function generateTables() {
  document.getElementById("content-background").innerHTML = ui.loading;

  try {
    all_mamas = await loadMamas();
    all_garfields = await loadGarfields();
  } finally {
    mama_html = `
  <div class = "row">
  <div class = "col-md-12">
  <div class = "card bootstrap-table">

  <div class = "card-header">
  <h4 class = "card-title">Mamas</h4>
  <p class = "card-category">Select which mamas to include in this week's run:</p>
  </div>

  <div class = "card-body">
  <div class = "bootstrap-table">
  <div class = "fixed-table-toolbar">
  <div class = "fixed-table-body">
  <table id="mama_table" data-search="true" data-click-to-select="true" data-pagination="true" data-show-columns="true" class = "table table-striped">
  <thead>
  <tr>
  <th  data-field="selected" data-checkbox="true" data-sortable="true" data-switchable="false"></th>
  <th class = "d-none" data-field="_id" data-sortable="true" data-switchable="false">Select</th>
  <th data-field="name" data-sortable="true" data-switchable="false">Mama Name</th>
  <th data-field="address" data-sortable="true">Address</th>
  <th data-field="quantity" data-sortable="true" data-halign="center" data-align="center">Quantity</th>
  <th data-field="frequency" data-sortable="true" data-halign="center" data-align="center">Frequency</th>
  <th data-field="miles" data-sortable="true" data-halign="center" data-align="center">Miles</th>
  <th data-field="cohort" data-sortable="true" data-halign="center" data-align="center">Cohort</th>
  <th data-field="state" data-sortable="true" data-halign="center" data-align="center">State</th>
  </tr>
</thead>
</table>
  </div>
  </div>
  </div>
  </div>
  </div>
  </div>
  </div>
`;
    garfield_html = `

  <div class = "row">
  <div class = "col-md-12">
  <div class = "card bootstrap-table">

  <div class = "card-header">
  <h4 class = "card-title">Garfields</h4>
  <p class = "card-category">Select which garfields to include in this week's run:</p>
  </div>

  <div class = "card-body">
  <div class = "bootstrap-table">
  <div class = "fixed-table-toolbar">
  <div class = "fixed-table-body">
  <table id="garfield_table" data-content-type="application/json" data-data-type = "json" data-search="true" data-click-to-select="true" data-pagination="true" data-show-columns="true" class = "table table-striped">
  <thead>
  <tr>
  <th data-field="selected" data-checkbox="true" data-sortable="true" data-switchable="false">Select</th>
  <th class = "d-none" data-field="_id" data-sortable="true" data-switchable="false">Select</th>
  <th data-field="name" data-sortable="true" data-switchable="false">Garfield Name</th>
  <th data-field="address" data-sortable="true">Address</th>
  <th data-field="quantity" data-sortable="true" data-halign="center" data-align="center">Quantity</th>
  <th data-field="cohort" data-sortable="true" data-halign="center" data-align="center">Cohort</th>
  <th data-field="state" data-sortable="true" data-halign="center" data-align="center">State</th>
  </tr>
</thead>
</table>
  </div>
  </div>
  </div>
  </div>
  </div>
  </div>
  </div>

<button class = "btn btn-outline btn-round btn-wd" id="reviewSelections" type="submit" onclick = "reviewModule();">Review Selections</button>`;

    document.getElementById("target").innerHTML =
      ui.loadMamasGarfields + mama_html + garfield_html + "</div></div>";
  }

  var $mama_table = $("#mama_table");
  var $garfield_table = $("#garfield_table");
  $mama_table.bootstrapTable("checkAll");
  $garfield_table.bootstrapTable("checkAll");

  $(function () {
    $mama_table.bootstrapTable({ data: all_mamas });
    $garfield_table.bootstrapTable({ data: all_garfields });
  });

  var $button = $("#reviewSelections");

  $(function () {
    $button.click(function () {
      selected_mamas = [];
      $mama_table.bootstrapTable("getSelections").forEach((mama) => {
        // selected_mamas.push(mama._id);

        selected_mamas.push({
          _id: mama._id,
          quantity: mama.quantity,
          special_dairy: mama.special_dairy,
          special_gluten: mama.special_gluten,
          special_veg: mama.special_veg,
          special_vgn: mama.special_vgn,
        });
      });

      selected_garfields = [];
      $garfield_table.bootstrapTable("getSelections").forEach((garf) => {
        // selected_garfields.push(garf._id);

        selected_garfields.push({
          _id: garf._id,
          quantity: garf.quantity,
          special_dairy: garf.special_dairy,
          special_gluten: garf.special_gluten,
          special_veg: garf.special_veg,
          special_vgn: garf.special_vgn,
        });
      });
      revSelections();
    });
  });
}

async function revSelections() {
  var mamas_tot = Object.keys(selected_mamas).length;
  var garfield_tot = Object.keys(selected_garfields).length;

  var mama_cap = 0;
  var mama_special_dairy = 0;
  var mama_special_gluten = 0;
  var mama_special_veg = 0;
  var mama_special_vgn = 0;

  selected_mamas.forEach((mama) => {
    mama_cap += mama.quantity;
    if (mama.special_dairy) {
      mama_special_dairy += mama.quantity;
    }
    if (mama_special_gluten) {
      mama_special_gluten += mama.quantity;
    }
    if (mama_special_veg) {
      mama_special_veg += mama.quantity;
    }
    if (mama_special_vgn) {
      mama_special_vgn += mama.quantity;
    }
  });

  var garf_cap = 0;
  var garf_special_dairy = 0;
  var garf_special_gluten = 0;
  var garf_special_veg = 0;
  var garf_special_vgn = 0;

  selected_garfields.forEach((garf) => {
    garf_cap += garf.quantity;
    if (garf.special_dairy) {
      garf_special_dairy += garf.quantity;
    }
    if (garf_special_gluten) {
      garf_special_gluten += garf.quantity;
    }
    if (garf_special_veg) {
      garf_special_veg += garf.quantity;
    }
    if (garf_special_vgn) {
      garf_special_vgn += garf.quantity;
    }
  });

  var review_data = [
    {
      type: "Mamas",
      selected_tot: mamas_tot,
      capacity: mama_cap,
      special_dairy: mama_special_dairy,
      special_gluten: mama_special_gluten,
      special_veg: mama_special_veg,
      special_vgn: mama_special_vgn,
    },

    {
      type: "Garfields",
      selected_tot: garfield_tot,
      capacity: garf_cap,
      special_dairy: garf_special_dairy,
      special_gluten: garf_special_gluten,
      special_veg: garf_special_veg,
      special_vgn: garf_special_vgn,
    },
  ];

  review_table_html = `
  <div class = "row">
  <div class = "col-md-12">
  <div class = "card bootstrap-table">

  <div class = "card-header">
  <h4 class = "card-title">Selections Review</h4>
  <p class = "card-category">Review your chosen mamas and garfields:</p>
  </div>

  <div class = "card-body">
  <div class = "bootstrap-table">
  <div class = "fixed-table-toolbar">
  <div class = "fixed-table-body">
  <table id="review_table" data-click-to-select="true" data-pagination="true" data-show-columns="true" class = "table table-striped">
  <thead>
  <tr>
  <th data-field="type" data-sortable="true" data-switchable="false">User Type</th>
  <th data-field="selected_tot" data-sortable="true" data-switchable="false">Total Selected</th>
  <th data-field="capacity" data-sortable="true" data-switchable="false">Capacity</th>
  <th data-field="special_dairy" data-sortable="true" data-switchable="false">Dairy</th>
  <th data-field="special_gluten" data-sortable="true" data-switchable="false">Gluten</th>
  <th data-field="special_veg" data-sortable="true" data-switchable="false">Vegetarian</th>
  <th data-field="special_vgn" data-sortable="true" data-switchable="false">Vegan</th>
  </tr>
</thead>
</table>
  </div>
  </div>
  </div>
  </div>
  </div>
  </div>
  </div>

  <button class = "btn btn-outline btn-round btn-wd" id="submitOpt" type="submit" onclick = "optModule(); submitOptimizationReq();">Optimize!</button>
  `;

  document.getElementById("target").innerHTML =
    ui.review + review_table_html + "</div></div>";

  var $review_table = $("#review_table");

  $(function () {
    $review_table.bootstrapTable({ data: review_data });
  });
}

async function submitOptimizationReq() {
  run_id = await sendSelections();

  run_id_html = `
  <div class="align-items-center justify-content-center" style = "color: grey"><p>Your Run ID is: ${run_id}</p></div>
  `;

  document.getElementById("content-background").innerHTML =
    ui.optimize_loading + run_id_html + "</div></div></div></div>";
  var count = 0;

  (async function checkStatus() {
    try {
      const url = "/optimize/status/" + run_id;

      const response = await superagent.get(url);

      if (
        count <= 30 &&
        response.body.status != "success" &&
        response.body.status.substring(0, 7) != "Failed"
      ) {
        count++;
        setTimeout(checkStatus, 5000);
      } else if (response.body.status == "success") {
        loadResults(run_id);
      } else {
        results_table_html = `

  <div class = "row">
  <div class = "col-md-12">
  <div class = "card bootstrap-table">

  <div class = "card-header">
  <h4 class = "card-title">We encountered a problem!</h4>
  <p class = "card-category"><strong>The optimization couldn't produce a result with the mamas and garfields you selected. Please try again.<strong></p>
  <br>
  </div>
  </div>
  </div>
  </div>
<button class = "btn btn-outline btn-round btn-wd" onclick = "loadMamasGarfields()">Try Again</button>
<button class = "btn btn-outline btn-round btn-wd" onclick = "selectPriorRun()">View Past Runs</button>`;

        document.getElementById("target").innerHTML =
          ui.optimize + results_table_html;
      }
    } catch (error) {
      console.log(error);
      results_table_html = `

      <div class = "row">
      <div class = "col-md-12">
      <div class = "card bootstrap-table">
    
      <div class = "card-header">
      <h4 class = "card-title">We encountered a problem!</h4>
      <p class = "card-category"><strong>The optimization couldn't produce a result with the mamas and garfields you selected. Please try again.<strong></p>
      <br>
      </div>
      </div>
      </div>
      </div>
    <button class = "btn btn-outline btn-round btn-wd" onclick = "loadMamasGarfields()">Try Again</button>
    <button class = "btn btn-outline btn-round btn-wd" onclick = "selectPriorRun()">View Past Runs</button>`;

      document.getElementById("target").innerHTML =
        ui.optimize + results_table_html;
    }
  })();
}

async function loadResults(run_id) {
  results = await getOptResults(run_id);

  if (results.body[0].matched_mamas.length == 0) {
    results_table_html = `

      <div class = "row">
      <div class = "col-md-12">
      <div class = "card bootstrap-table">
    
      <div class = "card-header">
      <h4 class = "card-title">We encountered a problem!</h4>
      <p class = "card-category"><strong>The optimization couldn't produce a result with the mamas and garfields you selected. Please try again.<strong></p>
      <br>
      </div>
      </div>
      </div>
      </div>
    <button class = "btn btn-outline btn-round btn-wd" onclick = "loadMamasGarfields()">Try Again</button>
    <button class = "btn btn-outline btn-round btn-wd" onclick = "selectPriorRun()">View Past Runs</button>`;

    document.getElementById("target").innerHTML =
      ui.optimize + results_table_html;
  } else {
    results_table_html = `

    <div class = "row">
    <div class = "col-md-12">
    <div class = "card bootstrap-table">
  
    <div class = "card-header">
    <h4 class = "card-title">Optimization Results</h4>
    <p class = "card-category">Review the optimization results and export:</p>
    </div>
  
    <div class = "card-body">
    <div class = "bootstrap-table">
    <div class = "fixed-table-toolbar">
    <div class = "fixed-table-body">
    <table
    id="results_table"
    data-toggle="table"
    data-detail-view="true"
    data-detail-formatter="mydetailFormatter"
    data-show-export="true"  
    data-toolbar="#toolbar"
    class = "table table-striped">
    <thead>
      <tr>
        <th data-field="Name" data-sortable="true">Mama Name</th>
        <th data-field="Capacity Usage" data-sortable="true">Capacity Usage</th>
        <th data-field="Distance Limit" data-sortable="true">Distance Limit</th>
        <th data-field="Furthest Garfield" data-sortable="true">Furthest Garfield</th>
        <th data-field="Cluster Distance" data-sortable="true">Max Cluster Distance</th>
        <th class = "d-none" data-field="str_gars" data-sortable="true"></th>
      </tr>
    </thead>
   </table>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
  
  <button class = "btn btn-outline btn-round btn-wd" id="exportable" onclick = "exported()">Export</button>
  <button class = "btn btn-outline btn-round btn-wd" onclick = "selectPriorRun()">View Past Runs</button>`;

    document.getElementById("target").innerHTML =
      ui.optimize + results_table_html;

    var $results_table = $("#results_table");

    function mydetailFormatter(index, row) {
      var html = [];
      $.each(row.Garfields, function (key, value) {
        html.push(
          "<p><b>" +
            value.Name +
            ":</b></p> " +
            "<ul>" +
            "<li> Quantity: " +
            value.Quantity +
            "</li>" +
            "<li> Distance: " +
            value.Distance +
            " miles" +
            "</li>" +
            "<li> Special Requests: " +
            value.Special_Requests +
            "</li>" +
            "</ul>"
        );
      });

      return html.join("");
    }

    $(function () {
      results.body[0].matched_mamas.forEach((mama) => {
        mama["str_gars"] = JSON.stringify(mama.Garfields);
      });

      $results_table.bootstrapTable({
        data: results.body[0].matched_mamas,
        detailFormatter: mydetailFormatter,
      });
    });
  }
}

async function fileLoad() {
  //TODO: Add success field

  excel_html = `
  <form action="/upload" method="post" id = "myForm" enctype="multipart/form-data">
<input type="file" name="xlfile" id="xlf" onchange = "file_load();"/> 
</form>`;
  document.getElementById("target").innerHTML =
    ui.files + excel_html + "</div></div>";

  $("#myForm").change(function (e) {
    submitted_success = `
      <div class = "row">
      <div class = "col-md-12">
      <div class = "card bootstrap-table">
    
      <div class = "card-header">
      <h4 class = "card-title">Success!</h4>
      <p class = "card-category"><strong>We are processing your file. Please check back later to see the updated entries in the database.<strong></p>
      <br>
      </div>
      </div>
      </div>
      </div>
      `;
    document.getElementById("target").innerHTML = ui.files + submitted_success;
  });
}

async function selectPriorRun() {
  run_list = await getPastRuns();

  run_select_html = `
  <label for="sel1">Select run ID:</label>
  <select id="sel1" onchange = "loadResults(value)">
  </select>
  `;
  document.getElementById("target").innerHTML = ui.prior + run_select_html;

  var $sel1 = $("#sel1");
  $sel1.append("<option selected>" + "</option>");

  $(function () {
    $.each(run_list.body.slice().reverse(), function (key, value) {
      $sel1.append(
        '<option value = "' + value._id + '">' + value._id + "</option>"
      );
    });
  });
}

async function getHomePageDetails() {
  document.getElementById("content-background").innerHTML = ui.loading;

  try {
    run_list = await getPastRuns();

    const url = "/optimize/status/" + run_list.body.pop()._id;

    const response = await superagent.get(url);

    var date = Date(run_list.body._id);

    home_page_cards = `
    <div class="container-fluid">
    <div class="row">
      <div class="col-lg-4 col-sm-5">
        <div class="card card-stats">
          <div class="card-body">
            <div class="row">
              <div class="col-5">
                <div class="icon-big text-center icon-warning">
                  <i class="material-icons nc-icon nc-chart text-warning"
                    >local_dining</i
                  >
                </div>
              </div>
              <div class="col-7">
                <div class="numbers">
                  <p class="card-category">Lasagna Supply</p>
                  <h4 class="card-title">${
                    response.body.kpi[0].kpi_total_lasagna_supply
                  }</h4>
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <hr>
            <div class="stats">
              <i class="material-icons fa">update</i>
              As of ${date.substring(0, 28)}
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-sm-5">
        <div class="card card-stats">
          <div class="card-body">
            <div class="row">
              <div class="col-5">
                <div class="icon-big text-center icon-warning">
                  <i class="material-icons nc-icon nc-chart text-warning"
                    >family_restroom</i
                  >
                </div>
              </div>
              <div class="col-7">
                <div class="numbers">
                  <p class="card-category">Lasagna Demand</p>
                  <h4 class="card-title">${
                    response.body.kpi[0].kpi_total_lasagna_demand
                  }</h4>
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <hr />
            <div class="stats">
              <i class="material-icons fa">update</i>
              As of ${date.substring(0, 28)}
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-4 col-sm-5">
        <div class="card card-stats">
          <div class="card-body">
            <div class="row">
              <div class="col-5">
                <div class="icon-big text-center icon-warning">
                  <i class="material-icons nc-icon nc-chart text-warning"
                    >done_all</i
                  >
                </div>
              </div>
              <div class="col-7">
                <div class="numbers">
                  <p class="card-category">Requests Fulfilled</p>
                  <h4 class="card-title">${
                    response.body.kpi[0].kpi_num_lasagnas_delivered
                  }</h4>
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <hr>
            <div class="stats">
              <i class="material-icons fa">update</i>
              As of ${date.substring(0, 28)}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  `;
    document.getElementById("target").innerHTML =
      ui.default + home_page_cards + "</div>";
  } catch (error) {}
}
