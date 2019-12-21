function autobot(clicked_id){
  var id2 = clicked_id.substr(clicked_id);
  var id = id2.replace(/\D/g, "");
  var title = 'title';
  var description = 'description';
  var price = 'price';
  var titleid = title + id;
  var descriptionid = description + id;
  var priceid = price + id;
  hide = 'hide';
  hideid = hide + id;
  var popup = document.getElementById('popup');
  var popupproductname = document.getElementById('popupproductname');
  var popupproductdescription = document.getElementById('popupproductdescription');
  var overlay = document.getElementById("overlay");
  var itemprice = document.getElementById("itemprice");
  popup.style.display = "block";
  overlay.style.display = "block";
  popupproductname.innerHTML = document.getElementById(titleid).innerHTML;
  popupproductdescription.innerHTML = document.getElementById(descriptionid).innerHTML;
  pricename = document.getElementById(priceid).innerHTML.substr(1);
  itemprice.innerHTML = pricename;
  query_id = document.getElementById("hide").innerHTML;
  hide_id = document.getElementById(hideid).innerHTML;
  document.getElementById('query_id').value = query_id;
  document.getElementById('query_product_id').value = hide_id;
  document.getElementById("query_product_quantity").value = document.getElementById('jiggy').innerHTML;
};
function buymore(){
  increase = document.getElementById("pft");
  multiples = document.getElementById("jiggy");
  itemprice = document.getElementById("itemprice");
  jiggy = document.getElementById("jiggy").innerHTML;
  actualprice = itemprice.innerHTML;
  intjiggy = jiggy * 1
  var newmultiple = intjiggy + 1;
  multiples.innerHTML = newmultiple;
  intactualprice = actualprice * 1
  var newprice = newmultiple * pricename;
  itemprice.innerHTML = newprice;
  document.getElementById("query_product_quantity").value = newmultiple;

}
function buyless(){
  testing = document.getElementById('jiggy').innerHTML;
  if (testing > 1){
        increase = document.getElementById("pft");
        multiples = document.getElementById("jiggy");
        itemprice = document.getElementById("itemprice");
        actualprice = itemprice.innerHTML;
        jiggy = document.getElementById("jiggy").innerHTML;
        intjiggy = jiggy * 1
        var newmultiple = intjiggy - 1;
        multiples.innerHTML = newmultiple;
        intactualprice = actualprice * 1
        var newprice = itemprice.innerHTML - pricename;
        itemprice.innerHTML = newprice;
        document.getElementById("query_product_quantity").value = newmultiple;
  }else{
    console.log("must buy one item")
  }

}
function closepopup(){
  var popupproductname = document.getElementById('popupproductname');
  var popupproductdescription = document.getElementById('popupproductdescription');
  var itemprice = document.getElementById('itemprice');
  var quantity = document.getElementById('jiggy');
  popup.style.display = "none";
  overlay.style.display = "none";
  popupproductname.innerHTML = "";
  popupproductdescription.innerHTML = "";
  itemprice.innerHTML = "";
  quantity.innerHTML = "1";
  document.getElementById("query_id").value = "";
  document.getElementById("query_product_id").value = "";
  document.getElementById("query_product_quantity").value = "";
}
function submitform(){
  submitbutton = document.getElementById("hiddensubmitbutton");
  submitbutton.click()

}
