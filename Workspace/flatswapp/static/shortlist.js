function addToShortlist() {
		  var xhttp = new XMLHttpRequest();
		  xhttp.onreadystatechange = function() {
		  if (this.status == 200) {
				document.getElementById('add').innerHTML="Remove from Shortlist";
				document.getElementById('add').setAttribute('onclick','removeFromShortlist();');
				document.getElementById('add').setAttribute('id','remove')
			}
		};
		  xhttp.open("GET", "http://localhost:8000/flatswapp/property/{{ property.slug }}/add_shortlist", true);

		  
		  xhttp.send();
		}
		
		function removeFromShortlist() {
		  var xhttp = new XMLHttpRequest();
		  xhttp.onreadystatechange = function() {
		  if (this.status == 200) {
				document.getElementById('remove').innerHTML="Add to Shortlist";
				document.getElementById('remove').setAttribute('onclick','addToShortlist();');
				document.getElementById('remove').setAttribute('id','add')
			}
		};
		  xhttp.open("GET", "http://localhost:8000/flatswapp/property/{{ property.slug }}/remove_shortlist", true);
		  
		  xhttp.send();
		}