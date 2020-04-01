var array = txt.innerHTML.replace(new RegExp("'", 'g'), "").replace("[","").replace("]","").split(",");				
text = "<ul class='list-group list-group-flush' >";
for (i = 0; i < array.length; i++) {
text += "<li class='list-group-item list-group-item-primary' style='position:static;width:200px;'>" + array[i] + "</li>";
}
text += "</ul>";				
document.getElementById("facilities").innerHTML=text;