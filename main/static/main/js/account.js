function opensearbardiv(){
  searchbardiv = document.getElementById("searchbardiv");
  searchbutton = document.getElementById("searchbutton");
  closebarleft = document.getElementById("closebarleft");
  closebarright = document.getElementById("closebarright");
  searchquery = document.getElementById("searchquery");
  searchbardiv.style.visibility = "visible";
  searchbardiv.style.width = "70%";
  closebarleft.style.height = "2px";
  closebarright.style.height = "2px";
}
function closesearchbardiv(){
  searchbardiv = document.getElementById("searchbardiv");
  searchbutton = document.getElementById("searchbutton");
  closebarleft = document.getElementById("closebarleft");
  closebarright = document.getElementById("closebarright");
  searchquery = document.getElementById("searchquery");
  searchbardiv.style.visibility = "hidden";
  searchbardiv.style.width = "0%";
  closebarleft.style.height = "0px";
  closebarright.style.height = "0px";
  searchquery.value = "";
}
