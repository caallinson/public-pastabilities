var ui = {};

ui.default = `
<nav class="navbar navbar-expand-lg">
  <div class="container-fluid">
    <div class="navbar-wrapper">
      <div class="navbar-minimize">
        <button
          id="minimizeSidebar"
          class="btn btn-warning btn-fill btn-round btn-icon d-none d-lg-block"
        >
          <i class="material-icons visible-on-sidebar-regular">more_vert</i>
          <i class="material-icons visible-on-sidebar-mini">menu_open</i>
        </button>
      </div>
      <a class="navbar-brand" href="#">Home</a>
    </div>
    <button
      class="navbar-toggler navbar-toggler-right"
      type="button"
      data-toggle="collapse"
      aria-control="navigation-index"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-bar burger-lines"></span>
    </button>
  </div>
</nav>

<div class="content" id="content-background">
`;

ui.loadMamasGarfields = `

<nav class = "navbar navbar-expand-lg">
<div class = "container-fluid">

<div class = "navbar-wrapper">
<div class = "navbar-minimize">
<button id="minimizeSidebar" class = "btn btn-warning btn-fill btn-round btn-icon d-none d-lg-block">
<i class = "material-icons visible-on-sidebar-regular">more_vert</i>
<i class = "material-icons visible-on-sidebar-mini">menu_open</i>
</button>
</div>
<a class = "navbar-brand" href="#">Optimize Mamas and Garfields</a>
</div>
<button class="navbar-toggler navbar-toggler-right" type = "button" data-toggle="collapse" aria-control="navigation-index" aria-expanded="false" aria-label="Toggle navigation">
<span class = "navbar-toggler-bar burger-lines"></span>

</button>

</div>
</nav>

<div class = "content" id = "content-background">
<div class = "container-fluid" >

`;

ui.review = `
<nav class = "navbar navbar-expand-lg">
<div class = "container-fluid">

<div class = "navbar-wrapper">
<div class = "navbar-minimize">
<button id="minimizeSidebar" class = "btn btn-warning btn-fill btn-round btn-icon d-none d-lg-block">
<i class = "material-icons visible-on-sidebar-regular">more_vert</i>
<i class = "material-icons visible-on-sidebar-mini">menu_open</i>
</button>
</div>
<a class = "navbar-brand" href="#">Review Selections</a>
</div>
<button class="navbar-toggler navbar-toggler-right" type = "button" data-toggle="collapse" aria-control="navigation-index" aria-expanded="false" aria-label="Toggle navigation">
<span class = "navbar-toggler-bar burger-lines"></span>

</button>

</div>
</nav>

<div class = "content">
<div class = "container-fluid">
`;

ui.optimize = `
<nav class = "navbar navbar-expand-lg">
<div class = "container-fluid">

<div class = "navbar-wrapper">
<div class = "navbar-minimize">
<button id="minimizeSidebar" class = "btn btn-warning btn-fill btn-round btn-icon d-none d-lg-block">
<i class = "material-icons visible-on-sidebar-regular">more_vert</i>
<i class = "material-icons visible-on-sidebar-mini">menu_open</i>
</button>
</div>
<a class = "navbar-brand" href="#">Optimization Results</a>
</div>
<button class="navbar-toggler navbar-toggler-right" type = "button" data-toggle="collapse" aria-control="navigation-index" aria-expanded="false" aria-label="Toggle navigation">
<span class = "navbar-toggler-bar burger-lines"></span>

</button>

</div>
</nav>

<div class = "content" id = "content-background">
<div class = "container-fluid">
`;

ui.files = `
<nav class = "navbar navbar-expand-lg">
<div class = "container-fluid">

<div class = "navbar-wrapper">
<div class = "navbar-minimize">
<button id="minimizeSidebar" class = "btn btn-warning btn-fill btn-round btn-icon d-none d-lg-block">
<i class = "material-icons visible-on-sidebar-regular">more_vert</i>
<i class = "material-icons visible-on-sidebar-mini">menu_open</i>
</button>
</div>
<a class = "navbar-brand" href="#">Upload New Mamas and Garfields</a>
</div>
<button class="navbar-toggler navbar-toggler-right" type = "button" data-toggle="collapse" aria-control="navigation-index" aria-expanded="false" aria-label="Toggle navigation">
<span class = "navbar-toggler-bar burger-lines"></span>

</button>

</div>
</nav>

<div class = "content" id = "content-background">
<div class = "container-fluid">

<div data-notify="container" id = "warning" class = "col-11 col-sm-4 alert alert-warning alert-with-icon alert-dismissible" role = "alert" data-notify-position = "top-right" style = "display: inline-block; margin: 0px auto; position: fixed; transition: all 0.5 ease-in-out 0s; z-index: 1031; top: 20px; right: 20px;">
<button type = "button" aria-label = "Close" class = "close"  data-dismiss = "alert" style = "position: absolute; right: 10px; top: 50%; margin-top: -13px; z-index: 1033;">
<span aria-hidden = "true"><i class = "material-icons" style = "font-size: 20px">close</i></span>
</button>
<span data-notify="icon" class = "nc-icon nc-app"><i class="material-icons" style = "font-size: 30px">construction</i></span>
<span data-notify="title"><b>Heads Up!</b></span>
<span data-notify="message">This feature is currently a placeholder for future functionality for users to upload real changes to supply and demand data.</span>
</div>
`;

ui.prior = `
<nav class = "navbar navbar-expand-lg">
<div class = "container-fluid">

<div class = "navbar-wrapper">
<div class = "navbar-minimize">
<button id="minimizeSidebar" class = "btn btn-warning btn-fill btn-round btn-icon d-none d-lg-block">
<i class = "material-icons visible-on-sidebar-regular">more_vert</i>
<i class = "material-icons visible-on-sidebar-mini">menu_open</i>
</button>
</div>
<a class = "navbar-brand" href="#">Past Optimization Runs</a>
</div>
<button class="navbar-toggler navbar-toggler-right" type = "button" data-toggle="collapse" aria-control="navigation-index" aria-expanded="false" aria-label="Toggle navigation">
<span class = "navbar-toggler-bar burger-lines"></span>

</button>

</div>
</nav>

<div class = "content" id = "content-background">
<div class = "container-fluid">

`;

ui.loading = `

<div class = "content">
<div class = "container-fluid">
<div class = "row align-items-center justify-content-center">
<div class = "col-md-12 align-items-center justify-content-center">
<div class="loader align-items-center justify-content-center"></div>
</div>
</div>
</div>
</div>
`;

ui.optimize_loading = `

<div class = "content">
<div class = "container-fluid">
<div class = "row align-items-center justify-content-center">
<div class = "col-md-12 align-items-center justify-content-center">
<div class="loader align-items-center justify-content-center"></div>
<hr>
<div><h2 style = "color: grey">Optimization in progress! This may take a few minutes.</h2></div>

`;

var target = document.getElementById("target");

var defaultModule = function () {
  target.innerHTML = ui.default;
  getHomePageDetails();
};

var loadMamasGarfields = function () {
  target.innerHTML = ui.loadMamasGarfields;
  generateTables();
};

var reviewModule = function () {
  target.innerHTML = ui.review;
};

var optModule = function () {
  target.innerHTML = ui.optimize;
};

var loadFile = function () {
  target.innerHTML = ui.files;
  fileLoad();
};

var viewPrior = function () {
  target.innerHTML = ui.prior;
  selectPriorRun();
};

defaultModule();

$(".alert").alert();